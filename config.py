ETHEREUM_ENVIRONMENT = "ropsten"


class EthereumNetwork:
    name = ETHEREUM_ENVIRONMENT
    id = 3
    default_provider = "HttpProvider"


class HttpProvider:
    type = "HTTP_PROVIDER"
    connection_url = f"https://{ETHEREUM_ENVIRONMENT}.infura.io/v3/1d336f192201401e8fd22a0db17bc85a"
    web3_class = "HTTPProvider"


class WebSocketProvider:
    type = "WS_PROVIDER"
    connection_url = f"wss://{ETHEREUM_ENVIRONMENT}.infura.io/ws/v3/1d336f192201401e8fd22a0db17bc85a"
    web3_class = "providers.WebsocketProvider"


class AlternateEthereumNetwork:
    name = ETHEREUM_ENVIRONMENT
    id = 3


DB_DETAILS = {
    "driver": "mysql+pymysql",
    "host": "localhost",
    "user": "unittest_root",
    "password": "unittest_pwd",
    "name": "event_pub_sub_unittest_db",
    "port": 3306
}

EVENT_FETCH_LIMIT = 50
