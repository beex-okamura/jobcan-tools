from datetime import datetime

from pynamodb.attributes import ListAttribute, UnicodeAttribute, UTCDateTimeAttribute
from pynamodb.models import Model

from lib.dynamodb import DynamoDBMeta
from lib.environment import get_environment

env = get_environment()


class UserModel(Model):
    class Meta(DynamoDBMeta):
        table_name = f"jobcan-{env.stage}-user-attributes"

    user_id = UnicodeAttribute(hash_key=True)
    jobcan_user_id = UnicodeAttribute()
    jobcan_password = UnicodeAttribute()
    slack_access_token = UnicodeAttribute()
    send_punch_channels = ListAttribute(of=UnicodeAttribute)
    updated_dt = UTCDateTimeAttribute(default=datetime.now, null=False)
