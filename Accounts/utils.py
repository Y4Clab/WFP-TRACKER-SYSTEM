import uuid

class UserUtils:
    @staticmethod
    def get_unique_token():
        token = str(uuid.uuid4())
        return token
