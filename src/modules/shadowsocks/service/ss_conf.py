from typing import List
from os import path
import os
from datetime import datetime, timedelta, timezone
import json
import portalocker
import logging
import yaml
import random
from ..models import SSKey
from ..models import SSCipher


LOGGER = logging.getLogger(__file__)


class SSConf(object):
    """
    WARNING:
        Method SSConf().__load() could create an dummy config file if it does not exist or config content is empty.
        Unfortunately it could raise race condition situation when two process tries create config file.
        To avoid race condition - just create instance of SSConf (it creates config file as well) before any
        async-operations of any kind.
    """

    @classmethod
    def get_instance(cls) -> 'SSConf':
        """Tiny method to get SSConf instance with similar configuration everywhere"""
        from settings import settings
        return SSConf(
            rotate_shadowsocks_keys_each_x_seconds=settings.ROTATE_SHADOWSOCKS_KEYS_EACH_X_SECONDS,
            shadowsocks_keys_limit=settings.SHADOWSOCKS_KEYS_LIMIT,
            ss_keys_port=settings.SS_KEY_PORT,
            cipher=settings.CIPHER
        )

    def __init__(
            self,
            rotate_shadowsocks_keys_each_x_seconds: int = 3600,
            shadowsocks_keys_limit: int = 1000,
            ss_keys_port: int = 9000,
            cipher: str = SSCipher.chacha20_ietf_poly1305,
            config_fp: str = None,
            lock_config_timeout: int = 3,
            *args, **kwargs
    ):
        self.rotate_dt_delta = timedelta(seconds=rotate_shadowsocks_keys_each_x_seconds)
        self.cipher = SSCipher(cipher).cipher
        self.lock_config_timeout = lock_config_timeout
        self.ss_keys_port = ss_keys_port
        self.shadowsocks_keys_limit = shadowsocks_keys_limit
        self.config_fp = path.abspath(
            config_fp or path.join(path.dirname(__file__), 'ss_users_config.json')
        )

        # variables below loads from config file
        self.updated_at = None
        self.__ss_keys = []
        self.__config_data = None
        self.__load()
        self.rotate()

    @property
    def is_config_exists(self) -> bool:
        return path.isfile(self.config_fp)

    @property
    def ss_keys(self) -> List[SSKey]:
        self.rotate()
        return self.__ss_keys

    @ss_keys.setter
    def ss_keys(self, value: SSKey):
        self.__ss_keys = value

    @property
    def ss_outline_yml_users_config(self) -> str:
        self.rotate()
        data = {
            'keys': [
                {
                    'id': x.user_id,
                    'port': x.port,
                    'cipher': x.cipher,
                    'secret': x.secret
                }
                for x in self.ss_keys
            ]
        }
        data = str(yaml.dump(data, default_flow_style=False))
        return data

    def get_random_keys(self, count: int = 1) -> List[SSKey]:
        return [random.choice(self.ss_keys) for x in range(count)]

    def __load(self, **kwargs) -> None:
        """
        Load data from config file to current SSConf instance
        """
        if not self.is_config_exists:
            self.__create_dummy_config()
        config_data = self.__read_config_data()
        config_data_size = len(str(config_data).encode())
        if config_data_size == 0:
            # Race condition
            logging.warning("Config is empty: {}".format(self.config_fp))
            raise Exception('Config is empty')

        self.__config_data = json.loads(config_data)
        self.updated_at = datetime.fromtimestamp(float(self.__config_data['updated_at']), timezone.utc)

        if any([
                self.shadowsocks_keys_limit != self.__config_data['shadowsocks_keys_limit'],
                self.rotate_dt_delta.total_seconds() != self.__config_data['rotate_dt_delta']
            ]):
            LOGGER.info('Configuration was changed. Reloading config...')
            self.rotate(True)

        ss_keys = []
        for key in self.__config_data['keys']:
            ss_keys.append(SSKey(**key))
        self.ss_keys = ss_keys

    @classmethod
    def build_ss_config(
            cls,
            updated_at: datetime,
            keys: List[SSKey] = None,
            rotate_dt_delta: timedelta = timedelta(hours=1),
            shadowsocks_keys_limit: int = 100
    ) -> str:
        """Generates config content"""
        return json.dumps({
            'updated_at': updated_at.timestamp(),
            'updated_at_human_readable': str(updated_at),
            'rotate_dt_delta': rotate_dt_delta.total_seconds(),
            'shadowsocks_keys_limit': shadowsocks_keys_limit,
            'keys': [key.serialize() for key in keys or []]
            },
            ensure_ascii=False
        )

    def rotate(self, force: bool = False) -> 'SSConf':
        """Recreate all ss keys in config"""
        now = datetime.now(timezone.utc)
        if (now - self.updated_at).total_seconds() >= self.rotate_dt_delta.total_seconds() or force:
            ss_keys = []
            for i in range(self.shadowsocks_keys_limit):
                ss_keys.append(SSKey.create(port=self.ss_keys_port, cipher=self.cipher))
            config = self.build_ss_config(now, ss_keys, self.rotate_dt_delta, self.shadowsocks_keys_limit)
            self.__write_config_data(config)
            self.__load()
        return self

    def __read_config_data(self, **kwargs) -> str:
        rec_num = int(kwargs.get('__rec_num', 0))
        if rec_num >= 2:
            raise RecursionError()
        if self.is_config_exists:
            config_data = {}

            with portalocker.Lock(self.config_fp, 'rb+', timeout=self.lock_config_timeout) as fh:
                f = None
                try:
                    f = open(self.config_fp, 'r')
                    config_data = f.read()
                except Exception as e:
                    LOGGER.error('Unable to write config: {}'.format(str(e)))
                finally:
                    if f and not f.closed:
                        f.close()
                fh.flush()
                os.fsync(fh.fileno())
            return config_data
        else:
            self.__create_dummy_config()
            return self.__read_config_data(__rec_num=rec_num + 1)

    def __write_config_data(self, data: str) -> None:
        if not self.is_config_exists:
            with open(self.config_fp, 'w') as f:
                f.write('')
        with portalocker.Lock(self.config_fp, 'rb+', timeout=self.lock_config_timeout) as fh:
            f = None
            try:
                f = open(self.config_fp, 'w')
                f.write(data)
            except Exception as e:
                LOGGER.error('Unable to write config: {}'.format(str(e)))
            finally:
                if f and not f.closed:
                    f.close()
            fh.flush()
            os.fsync(fh.fileno())

    def __create_dummy_config(self, force: bool = False) -> None:
        """Methods creates dummy config with expired updated_ts"""
        if not self.is_config_exists or force:
            expired_dt = datetime.now(timezone.utc) - timedelta(days=10 * 365)
            self.__write_config_data(self.build_ss_config(expired_dt))
