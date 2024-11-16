import os


class SecretSettings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM_DECODE = os.getenv("ALGORITHM_DECODE")


SECRET_KEY = SecretSettings().SECRET_KEY
ALGORITHM = SecretSettings().ALGORITHM_DECODE
