import os
import logging.config
from dotenv import load_dotenv
load_dotenv()

_logging_json = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "default": {
      "format": "%(asctime)s - %(levelname)s - %(message)s",
      "datefmt": "%Y-%m-%d %H:%M:%S"
    }
  },
  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "formatter": "default"
    },
    "rotating": {
      "class": "logging.handlers.TimedRotatingFileHandler",
      "formatter": "default",
      "filename": os.getenv("LOG_PATH", default="procmon.log"),
      "when": "midnight",
      "backupCount": 3
    }
  },
  "loggers": {
    "": {
      "handlers": ["console"],
      "level": "CRITICAL",
      "propagate": True
    },
    "pve": {
      "handlers": ["rotating"],
      "level": "DEBUG"
    }
  }
}
logging.config.dictConfig(_logging_json)
logger = logging.getLogger('pve.process')
