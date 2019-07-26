from dotenv import load_dotenv
import os
import logging.config


load_dotenv()


API_KEYS = list(filter(lambda x: x, os.getenv("API_KEYS", "").replace(' ', '').split(';')))
ROTATE_SHADOWSOCKS_KEYS_EACH_X_SECONDS = int(os.getenv("ROTATE_SHADOWSOCKS_KEYS_EACH_X_SECONDS", 3600))
SHADOWSOCKS_KEYS_LIMIT = int(os.getenv("SHADOWSOCKS_KEYS_LIMIT", 3000))
SS_KEY_PORT = int(os.getenv("SS_KEY_PORT", 9000))
CIPHER = str(os.getenv("CIPHER", "chacha20-ietf-poly1305"))

LOG_LVL = str(os.getenv("LOG_LVL", "INFO")).upper()
DEBUG = bool(int(os.getenv("DEBUG", 0)))
DISABLE_API_KEY_AUTH = bool(int(os.getenv("DISABLE_API_KEY_AUTH", 0)))

SERVICE_ID = str(os.getenv("SERVICE_ID", "4d1a90b6-df1e-4ba3-b592-86109a42c531"))
VERSION = str(os.getenv("VERSION", ""))
RELEASE_ID = str(os.getenv("RELEASE_ID", "RELEASE_ID"))
DESCRIPTION = str(os.getenv("DESCRIPTION", "DESCRIPTION"))


LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "advanced": {
            "format":
            "%(asctime)s | %(filename)10s:%(lineno)4s | %(levelname)8s | %(message)s "
        }
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "advanced",
            "stream": "ext://sys.stdout"
        },
    },
    "loggers": {
        '' : {
            'handlers': ['stdout'],
            'level': LOG_LVL,
        },
    }
}

logging.config.dictConfig(LOG_CONFIG)

