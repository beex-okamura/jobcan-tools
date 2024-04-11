from dynamodb.users import UserModel
from schemas.users import UserInfo


class Users():
    @staticmethod
    def get_user(user_id: str) -> UserInfo:
        user = UserModel.get(user_id).attribute_values
        return UserInfo(**user)
