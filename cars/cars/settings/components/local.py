DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "cars",
        "USER": "carssuper",
        "PASSWORD": "",
        "HOST": "localhost",
        "PORT": "",
    }
}

# GDAL_LIBRARY_PATH = "/opt/homebrew/Cellar/gdal/3.6.4_4/lib/libgdal.dylib"
# GEOS_LIBRARY_PATH = "/opt/homebrew/Cellar/geos/3.11.2/lib/libgeos_c.dylib"

DEBUG = True

SQL_LOGGING_ENABLED = False

if SQL_LOGGING_ENABLED:
    LOGGING = {
        "version": 1,
        "filters": {
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            }
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "filters": ["require_debug_true"],
                "class": "logging.StreamHandler",
            }
        },
        "loggers": {
            "django.db.backends": {
                "level": "DEBUG",
                "handlers": ["console"],
            }
        },
    }
