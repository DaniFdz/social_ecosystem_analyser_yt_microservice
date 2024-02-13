LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "filters": [],
        },
    },
    "loggers": {
        logger_name: {
            "level": log_level,
            "propagate": True,
        }
        for logger_name, log_level in zip(("src"), ("WARNING", "ERROR"))
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console"],
    },
}
