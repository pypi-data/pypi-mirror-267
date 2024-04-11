import numpy as np
import pandas as pd
import pyotp, pickle, codecs
from py5paisa import FivePaisaClient
from retrying import retry
from upstox_client.rest import ApiException

from quantplay.broker.generics.broker import Broker
from quantplay.exception.exceptions import (
    RetryableException,
    TokenException,
    retry_exception,
)
from quantplay.utils.constant import Constants, timeit


class FivePaisa(Broker):
    @timeit(MetricName="Upstox:__init__")
    def __init__(
        self,
        app_source=None,
        app_user_id=None,
        app_password=None,
        user_key=None,
        encryption_key=None,
        client_id=None,
        totp_key=None,
        pin=None,
        client=None,
        load_instrument=True,
    ):
        try:
            if client:
                self.set_client(client)
            else:

                client = FivePaisaClient(
                    cred={
                        "APP_SOURCE": app_source,
                        "APP_NAME": f"5P{client_id}",
                        "USER_ID": app_user_id,
                        "USER_KEY": user_key,
                        "PASSWORD": app_password,
                        "ENCRYPTION_KEY": encryption_key,
                    }
                )
                self.user_key = user_key
                self.client = client
                self.client.get_totp_session(client_id, pyotp.TOTP(totp_key).now(), pin)
        except Exception as e:
            raise e

        self.set_user_id()

        if load_instrument:
            self.load_instrument()
        super(FivePaisa, self).__init__()

    def set_client(self, serialized_client):
        self.client = pickle.loads(codecs.decode(serialized_client.encode(), "base64"))

    def set_user_id(self):
        self.user_id = self.client.client_code

    def get_client(self):
        return codecs.encode(pickle.dumps(self.client), "base64").decode()

    def load_instrument(self):
        super().load_instrument("5paisa_instruments")

    def handle_exception(self, e):
        if "Unauthorized" in e.reason:
            raise TokenException("Token Expired")
        raise RetryableException(e.reason)

    def token_url(self):
        url = f"https://dev-openapi.5paisa.com/WebVendorLogin/VLogin/Index?VendorKey={self.user_key}&ResponseURL=http://127.0.0.1"

    def holdings(self):
        data = self.client.holdings()
        return pd.DataFrame(data)

    def set_access_token(self, access_token):
        self.access_token = access_token

    def get_product(self, product):
        if product == "NRML":
            return "D"
        elif product == "CNC":
            return "D"
        elif product == "MIS":
            return "I"
        return product

    def get_lot_size(self, exchange, tradingsymbol):
        return int(
            self.symbol_data["{}:{}".format(exchange, tradingsymbol)]["lot_size"]
        )

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="5Paisa:get_ltp")
    def get_ltp(self, exchange=None, tradingsymbol=None):
        # create an instance of the API class
        api_instance = upstox_client.MarketQuoteApi(
            upstox_client.ApiClient(self.configuration)
        )
        api_version = "2.0"  # str | API Version Header

        try:
            symbol_info = self.symbol_data[f"{exchange}:{tradingsymbol}"]
            # Market quotes and instruments - LTP quotes.
            api_response = api_instance.ltp(symbol_info["instrument_key"], api_version)

            return api_response.data[
                f"{self.get_exchange(symbol_info['exchange'])}:{tradingsymbol}"
            ].last_price
        except ApiException as e:
            Constants.logger.error(
                "Exception when calling MarketQuoteApi->ltp: %s\n" % e
            )
            self.handle_exception(e)

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="5Paisa:profile")
    def profile(self):
        response = {"user_id": self.client.client_code}

        return response

    def add_exchange(self, data):
        exchange_condition = [
            (data["Exch"] == "N") & (data["ExchType"] == "D"),
            (data["Exch"] == "N") & (data["ExchType"] == "C"),
            (data["Exch"] == "B") & (data["ExchType"] == "D"),
            (data["Exch"] == "B") & (data["ExchType"] == "C"),
        ]

        exchange_name = ["NFO", "NSE", "BFO", "BSE"]

        data.loc[:, "exchange"] = np.select(
            exchange_condition, exchange_name, default=0
        )

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="Upstox:positions")
    def positions(self, drop_cnc=True):
        # create an instance of the API class
        positions = self.client.positions()

        if len(positions) == 0:
            return pd.DataFrame(columns=self.positions_column_list)
        positions = pd.DataFrame(positions)
        positions.rename(
            columns={
                "ScripName": "tradingsymbol",
                "SellQty": "sell_quantity",
                "BuyQty": "buy_quantity",
                "SellValue": "sell_value",
                "BuyValue": "buy_value",
                "LTP": "ltp",
                "ScripCode": "token",
                "NetQty": "quantity",
            },
            inplace=True,
        )

        positions["pnl"] = positions.sell_value - positions.buy_value
        positions["pnl"] += (positions.quantity) * positions.ltp
        self.add_exchange(positions)

        positions.loc[:, "option_type"] = np.where(
            positions.exchange.isin(["NFO", "BFO"]),
            positions.tradingsymbol.str.split(" ").str[-2],
            np.nan,
        )

        positions["product"] = positions["OrderFor"].replace(
            ["I", "D"], ["MIS", "NRML"]
        )
        positions["product"] = np.where(
            (
                (positions["exchange"].isin(["NSE", "BSE"]))
                & (positions["product"] == "NRML")
            ),
            "CNC",
            positions["product"],
        )

        if drop_cnc:
            positions = positions[positions["product"] != "CNC"]
        existing_columns = list(positions.columns)
        columns_to_keep = list(
            set(self.positions_column_list).intersection(set(existing_columns))
        )
        return positions[columns_to_keep]

    @retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="Upstox:orders")
    def orders(self, tag=None, add_ltp=True):
        orders = self.client.order_book()
        if len(orders) == 0:
            return pd.DataFrame(columns=self.orders_column_list)
        orders = pd.DataFrame(orders)
        self.add_exchange(orders)

        orders.rename(
            columns={
                "BrokerOrderId": "order_id",
                "ScripName": "tradingsymbol",
                "BuySell": "transaction_type",
                "AveragePrice": "average_price",
                "OrderStatus": "status",
                "ScripCode": "token",
                "Qty": "quantity",
                "TradedQty": "filled_quantity",
                "PendingQty": "pending_quantity",
                "BrokerOrderTime": "order_timestamp",
            },
            inplace=True,
        )

        positions = self.positions()
        positions = positions.sort_values("product").groupby(["tradingsymbol"]).head(1)
        orders = pd.merge(
            orders,
            positions[["tradingsymbol", "ltp"]],
            how="left",
            left_on=["tradingsymbol"],
            right_on=["tradingsymbol"],
        )

        orders.loc[:, "pnl"] = (
            orders.ltp * orders.filled_quantity
            - orders.average_price * orders.filled_quantity
        )
        orders.loc[:, "pnl"] = np.where(
            orders.transaction_type == "SELL", -orders.pnl, orders.pnl
        )
        orders.transaction_type = orders.transaction_type.replace(
            ["S", "B"], ["SELL", "BUY"]
        )

        if tag:
            orders = orders[orders.tag == tag]

        orders["tradingsymbol"] = np.where(
            orders.exchange == "NSE",
            orders.tradingsymbol.str.replace("-EQ", ""),
            orders.tradingsymbol,
        )

        orders["update_timestamp"] = orders.order_timestamp
        orders.status = orders.status.replace(
            ["Fully Executed"],
            ["COMPLETE"],
        )
        orders["product"] = orders["DelvIntra"].replace(["D", "I"], ["CNC", "MIS"])
        orders["product"] = np.where(
            ((orders["product"] == "CNC") & (orders["exchange"].isin(["NFO", "BFO"]))),
            "NRML",
            orders["product"],
        )

        existing_columns = list(orders.columns)
        columns_to_keep = list(
            set(self.orders_column_list).intersection(set(existing_columns))
        )
        orders = orders[columns_to_keep]
        return orders

    @retry(
        wait_exponential_multiplier=3000,
        wait_exponential_max=10000,
        stop_max_attempt_number=3,
        retry_on_exception=retry_exception,
    )
    @timeit(MetricName="Upstox:margins")
    def margins(self):
        margins = self.client.margin()[0]

        margins = {
            "margin_used": margins["MarginUtilized"],
            "margin_available": margins["NetAvailableMargin"],
        }
        return margins

    @timeit(MetricName="5Paisa:account_summary")
    def account_summary(self):
        margins = self.margins()
        response = {
            "margin_used": margins["margin_used"],
            "margin_available": margins["margin_available"],
            "pnl": float(self.positions().pnl.sum()),
        }
        return response

    def get_quantplay_product(self, exchange, product):
        product_map = {"D": "CNC", "I": "MIS"}
        if product in product_map:
            product = product_map[product]
        if product == "CNC" and exchange in ["NFO", "BFO"]:
            product = "NRML"

        return product
