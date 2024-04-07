from lib.environment import get_environment

env = get_environment()

class DynamoDBMeta:
    host = env.endpoint_url
