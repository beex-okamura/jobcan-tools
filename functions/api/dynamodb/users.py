from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute, ListAttribute

from lib.dynamodb import DynamoDBMeta
from lib.environment import get_environment

env = get_environment()


class UserModel(Model):
    class Meta(DynamoDBMeta):
        table_name = f"jobcan-{env.stage}-user-attributes"

    user_id = UnicodeAttribute(hash_key=True)
    jobcan_user_id = UnicodeAttribute()
    jobcan_password = UnicodeAttribute()
    slack_acess_token = UnicodeAttribute()
    send_punch_channel = ListAttribute(of=UnicodeAttribute)
    updated_dt = UTCDateTimeAttribute(default=datetime.now, null=False)
