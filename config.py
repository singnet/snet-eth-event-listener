AWS_REGION = "us-east-1"
ETHEREUM_ENVIRONMENT = "ropsten"
EVENT_FETCH_LIMIT = 50
EVENT_PUBLISH_LIMIT = 50
EVENT_LISTENER_ARN = ""

class EthereumNetwork:
    name = ETHEREUM_ENVIRONMENT
    id = 3
    default_provider = "HttpProvider"


class HttpProvider:
    type = "HTTP_PROVIDER"
    connection_url = f"https://{ETHEREUM_ENVIRONMENT}.infura.io/v3/"
    web3_class = "HTTPProvider"


class WebSocketProvider:
    type = "WS_PROVIDER"
    connection_url = f"wss://{ETHEREUM_ENVIRONMENT}.infura.io/ws/v3/"
    web3_class = "providers.WebsocketProvider"


class AlternateEthereumNetwork:
    name = ETHEREUM_ENVIRONMENT
    id = 3


DB_DETAILS = {
    "driver": "mysql+pymysql",
    "host": "localhost",
    "user": "unittest_root",
    "password": "unittest_pwd",
    "name": "ethereum_events_unittest_db",
    "port": 3306
}

