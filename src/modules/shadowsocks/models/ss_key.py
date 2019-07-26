from datetime import datetime
import uuid
from .ss_cipher import SSCipher


class SSKey(object):
    """Shadowsocks key (for end user connection)"""

    @classmethod
    def create(
            cls,
            port: int = 9000,
            cipher: str = SSCipher.chacha20_ietf_poly1305,
            is_enabled: bool = True
    ) -> 'SSKey':
        """Create new key"""
        return cls(
            key_id=str(uuid.uuid4()),
            port=port,
            user_id=str(uuid.uuid4()),
            cipher=SSCipher(cipher).cipher,
            secret=str(uuid.uuid4()),
            created_ts=datetime.utcnow().timestamp(),
            is_enabled=is_enabled
        )

    def __init__(
            self,
            key_id: str = None,
            user_id: str = None,
            port: int = None,
            cipher: str = None,
            secret: str = None,
            created_ts: float = None,
            is_enabled: bool = None
    ):
        self.key_id = key_id
        self.user_id = user_id
        self.secret = secret
        self.cipher = cipher
        self.port = port
        self.created_ts = created_ts
        self.is_enabled = is_enabled

    def serialize(self) -> dict:
        return {
            'key_id': self.key_id,
            'user_id': self.user_id,
            'port': self.port,
            'cipher': self.cipher,
            'secret': self.secret,
            'created_ts': self.created_ts,
            'is_enabled': self.is_enabled
        }
