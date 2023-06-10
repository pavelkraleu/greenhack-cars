import os

GS_BUCKET_NAME = os.getenv("GCP_BUCKET_STATIC")

STORAGES = {
    "staticfiles": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"},
    "default": {"BACKEND": "storages.backends.gcloud.GoogleCloudStorage"},
}
GS_DEFAULT_ACL = "publicRead"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.getenv("GCP_CLOUD_SQL_NAME"),
        "USER": os.getenv("GCP_CLOUD_SQL_USER"),
        "PASSWORD": os.getenv("GCP_CLOUD_SQL_PASS"),
        "HOST": os.getenv("GCP_CLOUD_SQL_HOST"),
        "PORT": os.getenv("GCP_CLOUD_SQL_PORT", 5432),
    }
}
