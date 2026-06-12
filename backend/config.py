"""Application configuration."""

import os
import secrets

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))
DATABASE_PATH = os.environ.get("DATABASE_PATH", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mono_repo.db"))
