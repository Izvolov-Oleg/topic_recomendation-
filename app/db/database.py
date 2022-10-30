import pickle

from app.core.settings import settings

with open(settings.database_path, "rb") as f:
    database = pickle.load(f)
