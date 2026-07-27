import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

# instance folder না থাকলে তৈরি করবে
os.makedirs(INSTANCE_DIR, exist_ok=True)

class Config:
    SECRET_KEY = "student-management-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        INSTANCE_DIR,
        "student.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False