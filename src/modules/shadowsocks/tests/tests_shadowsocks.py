import unittest
from os import path, remove
from multiprocessing import Pool
from modules.shadowsocks.service import SSConf
import time


conf_fp = path.abspath(path.join(path.dirname(__file__), 'test_ss_conf.json'))


def worker(*args, **kwargs):
    ss_conf = SSConf(10, 10, config_fp=conf_fp)
    user_id = ss_conf.ss_keys[0].user_id
    ss_conf.rotate(True)
    assert user_id not in [ x.user_id for x in ss_conf.ss_keys]


class TestShadowsocks(unittest.TestCase):

    def test_io_lock(self):

        if path.isfile(conf_fp):
            remove(conf_fp)
        SSConf(10, 10, config_fp=conf_fp)

        pool = Pool(processes=10)
        pool.map(worker, [x for x in range(100)])

        if path.isfile(conf_fp):
            remove(conf_fp)

    def test_rotation(self):

        if path.isfile(conf_fp):
            remove(conf_fp)

        user_limit = 3
        ss_conf = SSConf(2, user_limit, config_fp=conf_fp)
        user_id = ss_conf.ss_keys[0].user_id
        assert user_id in [x.user_id for x in ss_conf.ss_keys]
        time.sleep(4)
        assert user_id not in [x.user_id for x in ss_conf.ss_keys]
        assert len(ss_conf.ss_keys) == user_limit

        if path.isfile(conf_fp):
            remove(conf_fp)


if __name__ == '__main__':
    unittest.main()