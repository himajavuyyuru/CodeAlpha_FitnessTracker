import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Central place for app settings.

    Reading from environment variables (with a fallback default) means
    the same code can run on your laptop and on a deployed server without
    editing this file — you just set real values as environment variables
    in production.
    """
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-this")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "instance", "fitness.db"),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
