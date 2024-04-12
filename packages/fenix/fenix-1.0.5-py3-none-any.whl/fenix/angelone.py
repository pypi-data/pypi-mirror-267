from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Any

from fenix.base.broker import Broker

from fenix.base.constants import Side
from fenix.base.constants import OrderType
from fenix.base.constants import ExchangeCode
from fenix.base.constants import Product
from fenix.base.constants import Validity
from fenix.base.constants import Variety
from fenix.base.constants import Status
from fenix.base.constants import Order
from fenix.base.constants import Position
from fenix.base.constants import Profile
from fenix.base.constants import Root
from fenix.base.constants import WeeklyExpiry
from fenix.base.constants import UniqueID


from fenix.base.errors import InputError
from fenix.base.errors import ResponseError
from fenix.base.errors import TokenDownloadError

if TYPE_CHECKING:
    from requests.models import Response


class angelone(Broker):
    """
    AngelOne fenix Broker Class.

    Returns:
        fenix.angeloner: fenix AngelOne Broker Object.
    """

    indices = {}
    eq_tokens = {}
    fno_tokens = {}
    token_params = [
        "user_id",
        "pin",
        "totpstr",
        "api_key",
    ]
    id = "angelone"
    _session = Broker._create_session()

    # Base URLs

    base_urls = {
        "api_doc": "https://smartapi.angelbroking.com/docs",
        "access_token": "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword",
        "base": "https://apiconnect.angelbroking.com/rest/secure/angelbroking",
        "market_data": "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json",
    }

    # Order Placing URLs

    urls = {
        "place_order": f"{base_urls['base']}/order/v1/placeOrder",
        "modify_order": f"{base_urls['base']}/order/v1/modifyOrder",
        "cancel_order": f"{base_urls['base']}/order/v1/cancelOrder",
        "orderbook": f"{base_urls['base']}/order/v1/getOrderBook",
        "tradebook": f"{base_urls['base']}/order/v1/getTradeBook",
        "positions": f"{base_urls['base']}/order/v1/getPosition",
        "holdings": f"{base_urls['base']}/portfolio/v1/getAllHolding",
        "rms_limits": f"{base_urls['base']}/user/v1/getRMS",
        "profile": f"{base_urls['base']}/user/v1/getProfile",
    }

    # Request Parameters Dictionaries

    req_exchange = {
        ExchangeCode.NSE: "NSE",
        ExchangeCode.BSE: "BSE",
        ExchangeCode.NFO: "NFO",
        ExchangeCode.MCX: "MCX",
    }

    req_side = {
        Side.BUY: "BUY",
        Side.SELL: "SELL",
    }

    req_product = {
        Product.MIS: "INTRADAY",
        Product.NRML: "CARRYFORWARD",
        Product.CNC: "DELIVERY",
        Product.MARGIN: "MARGIN",
        Product.BO: "BO",
    }

    req_order_type = {
        OrderType.MARKET: "MARKET",
        OrderType.LIMIT: "LIMIT",
        OrderType.SL: "STOPLOSS_LIMIT",
        OrderType.SLM: "STOPLOSS_MARKET",
    }

    req_variety = {
        Variety.REGULAR: "NORMAL",
        Variety.STOPLOSS: "STOPLOSS",
        Variety.AMO: "AMO",
        Variety.BO: "ROBO",
    }

    req_validity = {
        Validity.DAY: "DAY",
        Validity.IOC: "IOC",
    }

    # Response Parameters Dictionaries

    resp_status = {
        "open pending": Status.PENDING,
        "not modified": Status.PENDING,
        "not cancelled": Status.PENDING,
        "modify pending": Status.PENDING,
        "trigger pending": Status.PENDING,
        "cancel pending": Status.PENDING,
        "validation pending": Status.PENDING,
        "put order req received": Status.PENDING,
        "modify validation pending": Status.PENDING,
        "after market order req received": Status.PENDING,
        "modify after market order req received": Status.PENDING,
        "cancelled": Status.CANCELLED,
        "cancelled after market order": Status.CANCELLED,
        "open": Status.OPEN,
        "complete": Status.FILLED,
        "rejected": Status.REJECTED,
        "modified": Status.MODIFIED,
    }

    resp_order_type = {
        "MARKET": OrderType.MARKET,
        "LIMIT": OrderType.LIMIT,
        "STOPLOSS_LIMIT": OrderType.SL,
        "STOPLOSS_MARKET": OrderType.SLM,
    }

    resp_product = {
        "DELIVERY": Product.CNC,
        "CARRYFORWARD": Product.NRML,
        "MARGIN": Product.MARGIN,
        "INTRADAY": Product.MIS,
        "BO": Product.BO,
    }

    resp_variety = {
        "NORMAL": Variety.REGULAR,
        "STOPLOSS": Variety.STOPLOSS,
        "AMO": Variety.AMO,
        "ROBO": Variety.BO,
    }

    # NFO Script Fetch

    @classmethod
    def create_eq_tokens(cls) -> dict:
        """
        Downlaods NSE & BSE Equity Info for F&O Segment.
        Stores them in the angelone.indices Dictionary.

        Returns:
            dict: Unified fenix indices format.
        """
        df = cls.data_reader(cls.base_urls["market_data"], filetype="json")

        df["tick_size"] = df["tick_size"].astype(int) / 100

        df_bse = df[df["exch_seg"] == ExchangeCode.BSE][
            ["symbol", "token", "tick_size", "lotsize", "exch_seg"]
        ]
        df_bse.rename(
            {
                "symbol": "Symbol",
                "token": "Token",
                "tick_size": "TickSize",
                "lotsize": "LotSize",
                "exch_seg": "Exchange",
            },
            axis=1,
            inplace=True,
        )

        df_bse["Token"] = df_bse["Token"].astype(int)
        df_bse.set_index(df_bse["Symbol"], inplace=True)
        df_bse.drop_duplicates(subset=["Symbol"], keep="first", inplace=True)

        df_nse = df[df["symbol"].str.endswith("-EQ")][
            ["name", "symbol", "token", "tick_size", "lotsize", "exch_seg"]
        ]
        df_nse.rename(
            {
                "name": "Index",
                "symbol": "Symbol",
                "token": "Token",
                "tick_size": "TickSize",
                "lotsize": "LotSize",
                "exch_seg": "Exchange",
            },
            axis=1,
            inplace=True,
        )

        df_nse["Token"] = df_nse["Token"].astype(int)
        df_nse.set_index(df_nse["Index"], inplace=True)
        df_nse.drop(columns="Index", inplace=True)

        cls.eq_tokens[ExchangeCode.NSE] = df_nse.to_dict(orient="index")
        cls.eq_tokens[ExchangeCode.BSE] = df_bse.to_dict(orient="index")

        return cls.eq_tokens

    @classmethod
    def create_indices(cls) -> dict:
        """
        Downloads all the Broker Indices Token data.
        Stores them in the angelone.indices Dictionary.

        Returns:
            dict: Unified fenix indices format.
        """
        df = cls.data_reader(cls.base_urls["market_data"], filetype="json")
        df = df[df["instrumenttype"] == "AMXIDX"][["symbol", "token", "exch_seg"]]

        df.rename(
            {"symbol": "Symbol", "token": "Token", "exch_seg": "Exchange"},
            axis=1,
            inplace=True,
        )
        df.index = df["Symbol"]
        df["Token"] = df["Token"].astype(int)

        indices = df.to_dict(orient="index")

        indices[Root.BNF] = indices["Nifty Bank"]
        indices[Root.NF] = indices["Nifty 50"]
        indices[Root.FNF] = indices["Nifty Fin Service"]
        indices[Root.MIDCPNF] = indices["NIFTY MID SELECT"]

        cls.indices = indices

        return indices

    @classmethod
    def create_fno_tokens(cls) -> dict:
        """
        Downloades Token Data for the FNO Segment for the 3 latest Weekly Expiries.
        Stores them in the angelone.fno_tokens Dictionary.

        Raises:
            TokenDownloadError: Any Error Occured is raised through this Error Type.
        """
        try:
            df = cls.data_reader(cls.base_urls["market_data"], filetype="json")

            df.rename(
                {
                    "token": "Token",
                    "name": "Root",
                    "expiry": "Expiry",
                    "symbol": "Symbol",
                    "tick_size": "TickSize",
                    "lotsize": "LotSize",
                    "strike": "StrikePrice",
                    "exch_seg": "Exchange",
                },
                axis=1,
                inplace=True,
            )

            df_nfo = df[
                (
                    (df["Root"] == "BANKNIFTY")
                    | (df["Root"] == "NIFTY")
                    | (df["Root"] == "FINNIFTY")
                    | (df["Root"] == "MIDCPNIFTY")
                )
                & (df["Exchange"] == ExchangeCode.NFO)
                & (df["instrumenttype"] == "OPTIDX")
            ]

            df_bfo = df[
                ((df["Root"] == "SENSEX") | (df["Root"] == "BANKEX"))
                & (df["Exchange"] == ExchangeCode.BFO)
                & (df["instrumenttype"] == "OPTIDX")
            ]

            df = cls.concat_df([df_nfo, df_bfo])

            df["Option"] = df["Symbol"].str.extract(r"(CE|PE)")
            df["StrikePrice"] = (df["StrikePrice"] // 100).astype(str)
            df["TickSize"] = df["TickSize"] / 100
            df["Token"] = df["Token"].astype(int)

            df = df[
                [
                    "Token",
                    "Symbol",
                    "Expiry",
                    "Option",
                    "StrikePrice",
                    "LotSize",
                    "Root",
                    "TickSize",
                    "Exchange",
                ]
            ]

            df["Expiry"] = cls.pd_datetime(df["Expiry"]).dt.date.astype(str)

            expiry_data = cls.jsonify_expiry(data_frame=df)

            cls.fno_tokens = expiry_data

            return expiry_data

        except Exception as exc:
            raise TokenDownloadError({"Error": exc.args}) from exc

    # Headers & Json Parsers

    @classmethod
    def create_headers(
        cls,
        params: dict,
    ) -> dict[str, str]:
        """
        Generate Headers used to access Endpoints in AngelOne.

        Parameters:
            params (dict) : A dictionary which should consist the following keys:
                user_id (str): User ID of the Account.
                pin (str): pin of the Account Holder.
                totpstr (str): String of characters used to generate TOTP.
                api_key (str): API Key of the Account.

        Returns:
            dict[str, str]: AngelOne Headers.
        """
        for key in cls.token_params:
            if key not in params:
                raise KeyError(f"Please provide {key}")

        totp = cls.totp_creator(params["totpstr"])

        headers = {
            "Content-type": "application/json",
            "X-ClientLocalIP": "127.0.0.1",
            "X-ClientPublicIP": "106.193.147.98",
            "X-MACAddress": "00:00:00:00:00:00",
            "Accept": "application/json",
            "X-PrivateKey": params["api_key"],
            "X-UserType": "USER",
            "X-SourceID": "WEB",
        }

        json_data = {
            "clientcode": params["user_id"],
            "password": params["pin"],
            "totp": totp,
        }

        response = cls.fetch(
            method="POST",
            url=cls.base_urls["access_token"],
            json=json_data,
            headers=headers,
        )
        response = cls._json_parser(response)

        headers = {
            "headers": {
                "Content-type": "application/json",
                "X-ClientLocalIP": "127.0.0.1",
                "X-ClientPublicIP": "106.193.147.98",
                "X-MACAddress": "00:00:00:00:00:00",
                "Accept": "application/json",
                "X-PrivateKey": params["api_key"],
                "X-UserType": "USER",
                "X-SourceID": "WEB",
                "Authorization": f"Bearer {response['data']['jwtToken']}",
                "x-api-key": "nBmFCnuK",
                "x-client-code": params["user_id"],
                "x-feed-token": response["data"]["feedToken"],
            }
        }

        cls._session = cls._create_session()

        return headers

    @classmethod
    def _json_parser(
        cls,
        response: Response,
    ) -> dict[Any, Any] | list[dict[Any, Any]]:
        """
        Parses the Json Repsonse Obtained from Broker.

        Parameters:
            response (Response): Json Response Obtained from Broker.

        Raises:
            ResponseError: Raised if any error received from broker.

        Returns:
            dict: json response obtained from exchange.
        """
        json_response = cls.on_json_response(response)
        # print(json_response)
        if json_response["status"]:
            return json_response

        raise ResponseError(cls.id + " " + json_response["message"])

    @classmethod
    def _orderbook_json_parser(
        cls,
        order: dict,
    ) -> dict[Any, Any]:
        """
        Parse Orderbook Order Json Response.

        Parameters:
            order (dict): Orderbook Order Json Response from Broker.

        Returns:
            dict: Unified fenix Order Response.
        """
        parsed_order = {
            Order.ID: order["orderid"],
            Order.USERID: order["ordertag"],
            Order.TIMESTAMP: cls.datetime_strp(
                order["updatetime"], "%d-%b-%Y %H:%M:%S"
            ),
            Order.SYMBOL: order["tradingsymbol"],
            Order.TOKEN: int(order["symboltoken"]),
            Order.SIDE: cls.req_side.get(
                order["transactiontype"], order["transactiontype"]
            ),
            Order.TYPE: cls.resp_order_type.get(order["ordertype"], order["ordertype"]),
            Order.AVGPRICE: order["averageprice"],
            Order.PRICE: order["price"],
            Order.TRIGGERPRICE: order["triggerprice"],
            Order.TARGETPRICE: order["squareoff"],
            Order.STOPLOSSPRICE: order["stoploss"],
            Order.TRAILINGSTOPLOSS: order["trailingstoploss"],
            Order.QUANTITY: int(order["quantity"]),
            Order.FILLEDQTY: int(order["filledshares"]),
            Order.REMAININGQTY: int(order["unfilledshares"]),
            Order.CANCELLEDQTY: int(order["cancelsize"]),
            Order.STATUS: cls.resp_status.get(order["status"], order["status"]),
            Order.REJECTREASON: order["text"],
            Order.DISCLOSEDQUANTITY: int(order["disclosedquantity"]),
            Order.PRODUCT: cls.resp_product.get(
                order["producttype"], order["producttype"]
            ),
            Order.EXCHANGE: cls.req_exchange.get(order["exchange"], order["exchange"]),
            Order.SEGMENT: cls.req_exchange.get(order["exchange"], order["exchange"]),
            Order.VALIDITY: cls.req_validity.get(order["duration"], order["duration"]),
            Order.VARIETY: cls.resp_variety.get(order["variety"], order["variety"]),
            Order.INFO: order,
        }

        return parsed_order

    @classmethod
    def _tradebook_json_parser(
        cls,
        order: dict,
    ) -> dict[Any, Any]:
        """
        Parse Tradebook Order Json Response.

        Parameters:
            order (dict): Tradebook Order Json Response from Broker.

        Returns:
            dict: Unified fenix Order Response.
        """
        parsed_order = {
            Order.ID: order["orderid"],
            Order.USERID: "",
            Order.TIMESTAMP: cls.datetime_strp(
                order["updatetime"], "%d-%b-%Y %H:%M:%S"
            ),
            Order.SYMBOL: order["tradingsymbol"],
            Order.TOKEN: int(order["symboltoken"]),
            Order.SIDE: cls.req_side.get(
                order["transactiontype"], order["transactiontype"]
            ),
            Order.TYPE: cls.resp_order_type.get(order["ordertype"], order["ordertype"]),
            Order.AVGPRICE: order["averageprice"],
            Order.PRICE: order["price"],
            Order.TRIGGERPRICE: order["triggerprice"],
            Order.TARGETPRICE: order["squareoff"],
            Order.STOPLOSSPRICE: order["stoploss"],
            Order.TRAILINGSTOPLOSS: order["trailingstoploss"],
            Order.QUANTITY: int(order["quantity"]),
            Order.FILLEDQTY: int(order["filledshares"]),
            Order.REMAININGQTY: int(order["unfilledshares"]),
            Order.CANCELLEDQTY: int(order["cancelsize"]),
            Order.STATUS: cls.resp_status.get(order["status"], order["status"]),
            Order.REJECTREASON: order["text"],
            Order.DISCLOSEDQUANTITY: int(order["disclosedquantity"]),
            Order.PRODUCT: cls.resp_product.get(
                order["producttype"], order["producttype"]
            ),
            Order.EXCHANGE: cls.req_exchange.get(order["exchange"], order["exchange"]),
            Order.SEGMENT: cls.req_exchange.get(order["exchange"], order["exchange"]),
            Order.VALIDITY: cls.req_validity.get(order["duration"], order["duration"]),
            Order.VARIETY: cls.resp_variety.get(order["variety"], order["variety"]),
            Order.INFO: order,
        }

        return parsed_order

    @classmethod
    def _position_json_parser(
        cls,
        position: dict,
    ) -> dict[Any, Any]:
        """
        Parse Acoount Position Json Response.

        Parameters:
            order (dict): Acoount Position Json Response from Broker.

        Returns:
            dict: Unified fenix Position Response.
        """
        parsed_position = {
            Position.SYMBOL: position["tradingsymbol"],
            Position.TOKEN: int(position["symboltoken"]),
            Position.NETQTY: int(position["netqty"]),
            Position.AVGPRICE: float(position["netprice"]),
            Position.MTM: None,
            Position.PNL: None,
            Position.BUYQTY: int(position["buyqty"]),
            Position.BUYPRICE: float(position["totalbuyavgprice"]),
            Position.SELLQTY: int(position["sellqty"]),
            Position.SELLPRICE: float(position["totalsellavgprice"]),
            Position.LTP: None,
            Position.PRODUCT: cls.resp_product.get(
                position["producttype"], position["producttype"]
            ),
            Position.EXCHANGE: cls.req_exchange.get(
                position["exchange"], position["exchange"]
            ),
            Position.INFO: position,
        }

        return parsed_position

    @classmethod
    def _profile_json_parser(
        cls,
        profile: dict,
    ) -> dict[Any, Any]:
        """
        Parse User Profile Json Response.

        Parameters:
            profile (dict): User Profile Json Response from Broker.

        Returns:
            dict: Unified fenix Profile Response.
        """
        parsed_profile = {
            Profile.CLIENTID: profile["clientcode"],
            Profile.NAME: profile["name"],
            Profile.EMAILID: profile["email"],
            Profile.MOBILENO: profile["mobileno"],
            Profile.PAN: "",
            Profile.ADDRESS: "",
            Profile.BANKNAME: "",
            Profile.BANKBRANCHNAME: None,
            Profile.BANKACCNO: "",
            Profile.EXHCNAGESENABLED: profile["exchanges"],
            Profile.ENABLED: True,
            Profile.INFO: profile,
        }

        return parsed_profile

    @classmethod
    def _create_order_parser(
        cls,
        response: Response,
        headers: dict,
    ) -> dict[Any, Any]:
        """
        Parse Json Response Obtained from Broker After Placing Order to get order_id
        and fetching the json repsone for the said order_id.

        Parameters:
            response (Response): Json Repsonse Obtained from broker after Placing an Order.
            headers (dict): headers to send order request with.

        Returns:
            dict: Unified fenix Order Response.
        """
        info = cls._json_parser(response)

        order_id = info["data"]["orderid"]
        order = cls.fetch_order(order_id=order_id, headers=headers)

        return order

    # Order Functions

    @classmethod
    def create_order(
        cls,
        token_dict: dict,
        quantity: int,
        side: str,
        product: str,
        validity: str,
        variety: str,
        unique_id: str,
        headers: dict,
        price: float = 0,
        trigger: float = 0,
        target: float = 0,
        stoploss: float = 0,
        trailing_sl: float = 0,
    ) -> dict[Any, Any]:
        """
        Place an Order.

        Parameters:
            token_dict (dict): a dictionary with details of the Ticker. Obtianed from eq_tokens or fno_tokens.
            quantity (int): Order quantity.
            side (str): Order Side: BUY, SELL.
            product (str, optional): Order product.
            validity (str, optional): Order validity.
            variety (str, optional): Order variety.
            unique_id (str): Unique user order_id.
            headers (dict): headers to send order request with.
            price (float): Order price
            trigger (float): order trigger price
            target (float, optional): Order Target price. Defaults to 0.
            stoploss (float, optional): Order Stoploss price. Defaults to 0.
            trailing_sl (float, optional): Order Trailing Stoploss percent. Defaults to 0.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not price and trigger:
            order_type = OrderType.SLM
            variety = (
                cls.req_variety[Variety.STOPLOSS]
                if variety == cls.req_variety[Variety.REGULAR]
                else variety
            )
        elif not price:
            order_type = OrderType.MARKET
        elif not trigger:
            order_type = OrderType.LIMIT
        else:
            order_type = OrderType.SL
            variety = (
                cls.req_variety[Variety.STOPLOSS]
                if variety == cls.req_variety[Variety.REGULAR]
                else variety
            )

        if not target:
            json_data = {
                "symboltoken": token_dict["Token"],
                "exchange": cls._key_mapper(
                    cls.req_exchange, token_dict["Exchange"], "exchange"
                ),
                "tradingsymbol": token_dict["Symbol"],
                "price": price,
                "triggerprice": trigger,
                "quantity": quantity,
                "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
                "ordertype": cls.req_order_type[order_type],
                "producttype": cls._key_mapper(cls.req_product, product, "product"),
                "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
                "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
                "ordertag": unique_id,
                "disclosedquantity": "0",
            }

        else:
            json_data = {
                "symboltoken": token_dict["Token"],
                "exchange": cls._key_mapper(
                    cls.req_exchange, token_dict["Exchange"], "exchange"
                ),
                "tradingsymbol": token_dict["Symbol"],
                "price": price,
                "triggerprice": trigger,
                "squareoff": target,
                "stoploss": stoploss,
                "trailingStopLoss": trailing_sl,
                "quantity": quantity,
                "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
                "ordertype": cls.req_order_type[order_type],
                "producttype": cls._key_mapper(cls.req_product, product, "product"),
                "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
                "variety": cls.req_variety[Variety.BO],
                "ordertag": unique_id,
                "disclosedquantity": "0",
            }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def market_order(
        cls,
        token_dict: dict,
        quantity: int,
        side: str,
        unique_id: str,
        headers: dict,
        target: float = 0.0,
        stoploss: float = 0.0,
        trailing_sl: float = 0.0,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.REGULAR,
    ) -> dict[Any, Any]:
        """
        Place Market Order.

        Parameters:
            token_dict (dict): a dictionary with details of the Ticker. Obtianed from eq_tokens or fno_tokens.
            quantity (int): Order quantity.
            side (str): Order Side: BUY, SELL.
            unique_id (str): Unique user order_id.
            headers (dict): headers to send order request with.
            target (float, optional): Order Target price. Defaults to 0.
            stoploss (float, optional): Order Stoploss price. Defaults to 0.
            trailing_sl (float, optional): Order Trailing Stoploss percent. Defaults to 0.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity. Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.REGULAR.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not target:
            json_data = {
                "symboltoken": token_dict["Token"],
                "exchange": cls._key_mapper(
                    cls.req_exchange, token_dict["Exchange"], "exchange"
                ),
                "tradingsymbol": token_dict["Symbol"],
                "price": "0",
                "triggerprice": "0",
                "quantity": quantity,
                "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
                "ordertype": cls.req_order_type[OrderType.MARKET],
                "producttype": cls._key_mapper(cls.req_product, product, "product"),
                "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
                "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
                "ordertag": unique_id,
                "disclosedquantity": "0",
            }
        else:
            json_data = {
                "symboltoken": token_dict["Token"],
                "exchange": cls._key_mapper(
                    cls.req_exchange, token_dict["Exchange"], "exchange"
                ),
                "tradingsymbol": token_dict["Symbol"],
                "price": "0",
                "triggerprice": "0",
                "squareoff": target,
                "stoploss": stoploss,
                "trailingStopLoss": trailing_sl,
                "quantity": quantity,
                "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
                "ordertype": cls.req_order_type[OrderType.MARKET],
                "producttype": cls._key_mapper(cls.req_product, product, "product"),
                "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
                "variety": cls.req_variety[Variety.BO],
                "ordertag": unique_id,
                "disclosedquantity": "0",
            }
        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def limit_order(
        cls,
        token_dict: dict,
        price: float,
        quantity: int,
        side: str,
        unique_id: str,
        headers: dict,
        target: float = 0.0,
        stoploss: float = 0.0,
        trailing_sl: float = 0.0,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.REGULAR,
    ) -> dict[Any, Any]:
        """
        Place Limit Order.

        Parameters:
            token_dict (dict): a dictionary with details of the Ticker. Obtianed from eq_tokens or fno_tokens.
            price (float): Order price.
            quantity (int): Order quantity.
            side (str): Order Side: BUY, SELL.
            unique_id (str): Unique user order_id.
            headers (dict): headers to send order request with.
            target (float, optional): Order Target price. Defaults to 0.
            stoploss (float, optional): Order Stoploss price. Defaults to 0.
            trailing_sl (float, optional): Order Trailing Stoploss percent. Defaults to 0.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity. Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.REGULAR.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not target:
            json_data = {
                "symboltoken": token_dict["Token"],
                "exchange": cls._key_mapper(
                    cls.req_exchange, token_dict["Exchange"], "exchange"
                ),
                "tradingsymbol": token_dict["Symbol"],
                "price": price,
                "triggerprice": "0",
                "quantity": quantity,
                "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
                "ordertype": cls.req_order_type[OrderType.LIMIT],
                "producttype": cls._key_mapper(cls.req_product, product, "product"),
                "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
                "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
                "ordertag": unique_id,
                "disclosedquantity": "0",
            }

        else:
            json_data = {
                "symboltoken": token_dict["Token"],
                "exchange": cls._key_mapper(
                    cls.req_exchange, token_dict["Exchange"], "exchange"
                ),
                "tradingsymbol": token_dict["Symbol"],
                "price": price,
                "triggerprice": "0",
                "squareoff": target,
                "stoploss": stoploss,
                "trailingStopLoss": trailing_sl,
                "quantity": quantity,
                "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
                "ordertype": cls.req_order_type[OrderType.LIMIT],
                "producttype": cls._key_mapper(cls.req_product, product, "product"),
                "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
                "variety": cls.req_variety[Variety.BO],
                "ordertag": unique_id,
                "disclosedquantity": "0",
            }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def sl_order(
        cls,
        token_dict: dict,
        price: float,
        trigger: float,
        quantity: int,
        side: str,
        unique_id: str,
        headers: dict,
        target: float = 0.0,
        stoploss: float = 0.0,
        trailing_sl: float = 0.0,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.STOPLOSS,
    ) -> dict[Any, Any]:
        """
        Place Stoploss Order.

        Parameters:
            token_dict (dict): a dictionary with details of the Ticker. Obtianed from eq_tokens or fno_tokens.
            price (float): Order price.
            trigger (float): order trigger price.
            quantity (int): Order quantity.
            side (str): Order Side: BUY, SELL.
            unique_id (str): Unique user order_id.
            headers (dict): headers to send order request with.
            target (float, optional): Order Target price. Defaults to 0.
            stoploss (float, optional): Order Stoploss price. Defaults to 0.
            trailing_sl (float, optional): Order Trailing Stoploss percent. Defaults to 0.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity. Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.REGULAR.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not target:
            json_data = {
                "symboltoken": token_dict["Token"],
                "exchange": cls._key_mapper(
                    cls.req_exchange, token_dict["Exchange"], "exchange"
                ),
                "tradingsymbol": token_dict["Symbol"],
                "price": price,
                "triggerprice": trigger,
                "quantity": quantity,
                "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
                "ordertype": cls.req_order_type[OrderType.SL],
                "producttype": cls._key_mapper(cls.req_product, product, "product"),
                "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
                "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
                "ordertag": unique_id,
                "disclosedquantity": "0",
            }

        else:
            json_data = {
                "symboltoken": token_dict["Token"],
                "exchange": cls._key_mapper(
                    cls.req_exchange, token_dict["Exchange"], "exchange"
                ),
                "tradingsymbol": token_dict["Symbol"],
                "price": price,
                "triggerprice": trigger,
                "squareoff": target,
                "stoploss": stoploss,
                "trailingStopLoss": trailing_sl,
                "quantity": quantity,
                "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
                "ordertype": cls.req_order_type[OrderType.SL],
                "producttype": cls._key_mapper(cls.req_product, product, "product"),
                "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
                "variety": cls.req_variety[Variety.BO],
                "ordertag": unique_id,
                "disclosedquantity": "0",
            }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def slm_order(
        cls,
        token_dict: dict,
        trigger: float,
        quantity: int,
        side: str,
        unique_id: str,
        headers: dict,
        target: float = 0.0,
        stoploss: float = 0.0,
        trailing_sl: float = 0.0,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.STOPLOSS,
    ) -> dict[Any, Any]:
        """
        Place Stoploss-Market Order.

        Parameters:
            token_dict (dict): a dictionary with details of the Ticker. Obtianed from eq_tokens or fno_tokens.
            trigger (float): order trigger price.
            quantity (int): Order quantity.
            side (str): Order Side: BUY, SELL.
            unique_id (str): Unique user order_id.
            headers (dict): headers to send order request with.
            target (float, optional): Order Target price. Defaults to 0.
            stoploss (float, optional): Order Stoploss price. Defaults to 0.
            trailing_sl (float, optional): Order Trailing Stoploss percent. Defaults to 0.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity. Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.REGULAR.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not target:
            json_data = {
                "symboltoken": token_dict["Token"],
                "exchange": cls._key_mapper(
                    cls.req_exchange, token_dict["Exchange"], "exchange"
                ),
                "tradingsymbol": token_dict["Symbol"],
                "price": "0",
                "triggerprice": trigger,
                "quantity": quantity,
                "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
                "ordertype": cls.req_order_type[OrderType.SLM],
                "producttype": cls._key_mapper(cls.req_product, product, "product"),
                "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
                "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
                "ordertag": unique_id,
                "disclosedquantity": "0",
            }

        else:
            json_data = {
                "symboltoken": token_dict["Token"],
                "exchange": cls._key_mapper(
                    cls.req_exchange, token_dict["Exchange"], "exchange"
                ),
                "tradingsymbol": token_dict["Symbol"],
                "price": "0",
                "triggerprice": trigger,
                "squareoff": target,
                "stoploss": stoploss,
                "trailingStopLoss": trailing_sl,
                "quantity": quantity,
                "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
                "ordertype": cls.req_order_type[OrderType.SLM],
                "producttype": cls._key_mapper(cls.req_product, product, "product"),
                "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
                "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
                "ordertag": unique_id,
                "disclosedquantity": "0",
            }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    # Equity Order Functions

    @classmethod
    def create_order_eq(
        cls,
        exchange: str,
        symbol: str,
        quantity: int,
        side: str,
        product: str,
        validity: str,
        variety: str,
        unique_id: str,
        headers: dict,
        price: float = 0,
        trigger: float = 0,
    ) -> dict[Any, Any]:
        """
        Place an Order in NSE/BSE Equity Segment.

        Parameters:
            exchange (str): Exchange to place the order in. Possible Values: NSE, BSE.
            symbol (str): Trading symbol, the same one you use on TradingView. Ex: "RELIANCE", "BHEL"
            quantity (int): Order quantity.
            side (str): Order Side: BUY, SELL.
            product (str, optional): Order product.
            validity (str, optional): Order validity.
            variety (str, optional): Order variety.
            unique_id (str): Unique user order_id.
            headers (dict): headers to send order request with.
            price (float): Order price
            trigger (float): order trigger price

        Returns:
            dict: fenix Unified Order Response.
        """
        if not cls.eq_tokens:
            cls.create_eq_tokens()

        exchange = cls._key_mapper(cls.req_exchange, exchange, "exchange")
        detail = cls._eq_mapper(cls.eq_tokens[exchange], symbol)
        token = detail["Token"]
        symbol = detail["Symbol"]

        if not price and trigger:
            order_type = OrderType.SLM
            variety = (
                cls.req_variety[Variety.STOPLOSS]
                if variety == cls.req_variety[Variety.REGULAR]
                else variety
            )
        elif not price:
            order_type = OrderType.MARKET
        elif not trigger:
            order_type = OrderType.LIMIT
        else:
            order_type = OrderType.SL
            variety = (
                cls.req_variety[Variety.STOPLOSS]
                if variety == cls.req_variety[Variety.REGULAR]
                else variety
            )

        json_data = {
            "symboltoken": token,
            "exchange": exchange,
            "tradingsymbol": symbol,
            "price": price,
            "triggerprice": trigger,
            "quantity": quantity,
            "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
            "ordertype": cls.req_order_type[order_type],
            "producttype": cls._key_mapper(cls.req_product, product, "product"),
            "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
            "variety": cls.req_variety[Variety.BO],
            "ordertag": unique_id,
            "disclosedquantity": "0",
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def market_order_eq(
        cls,
        exchange: str,
        symbol: str,
        quantity: int,
        side: str,
        unique_id: str,
        headers: dict,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.REGULAR,
    ) -> dict[Any, Any]:
        """
        Place Market Order in NSE/BSE Equity Segment.

        Parameters:
            exchange (str): Exchange to place the order in. Possible Values: NSE, BSE.
            symbol (str): Trading symbol, the same one you use on TradingView. Ex: "RELIANCE", "BHEL"
            quantity (int): Order quantity.
            side (str): Order Side: BUY, SELL.
            unique_id (str): Unique user order_id.
            headers (dict): headers to send order request with.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity. Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.REGULAR.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not cls.eq_tokens:
            cls.create_eq_tokens()

        exchange = cls._key_mapper(cls.req_exchange, exchange, "exchange")
        detail = cls._eq_mapper(cls.eq_tokens[exchange], symbol)
        token = detail["Token"]
        symbol = detail["Symbol"]

        json_data = {
            "symboltoken": token,
            "exchange": exchange,
            "tradingsymbol": symbol,
            "price": "0",
            "triggerprice": "0",
            "quantity": quantity,
            "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
            "ordertype": cls.req_order_type[OrderType.MARKET],
            "producttype": cls._key_mapper(cls.req_product, product, "product"),
            "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
            "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
            "ordertag": unique_id,
            "disclosedquantity": "0",
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def limit_order_eq(
        cls,
        exchange: str,
        symbol: str,
        price: float,
        quantity: int,
        side: str,
        unique_id: str,
        headers: dict,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.REGULAR,
    ) -> dict[Any, Any]:
        """
        Place Limit Order in NSE/BSE Equity Segment.

        Parameters:
            exchange (str): Exchange to place the order in. Possible Values: NSE, BSE.
            symbol (str): Trading symbol, the same one you use on TradingView. Ex: "RELIANCE", "BHEL"
            price (float): Order price.
            quantity (int): Order quantity.
            side (str): Order Side: BUY, SELL.
            unique_id (str): Unique user order_id.
            headers (dict): headers to send order request with.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity. Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.REGULAR.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not cls.eq_tokens:
            cls.create_eq_tokens()

        exchange = cls._key_mapper(cls.req_exchange, exchange, "exchange")
        detail = cls._eq_mapper(cls.eq_tokens[exchange], symbol)
        token = detail["Token"]
        symbol = detail["Symbol"]

        json_data = {
            "symboltoken": token,
            "exchange": exchange,
            "tradingsymbol": symbol,
            "price": price,
            "triggerprice": "0",
            "quantity": quantity,
            "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
            "ordertype": cls.req_order_type[OrderType.LIMIT],
            "producttype": cls._key_mapper(cls.req_product, product, "product"),
            "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
            "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
            "ordertag": unique_id,
            "disclosedquantity": "0",
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def sl_order_eq(
        cls,
        exchange: str,
        symbol: str,
        price: float,
        trigger: float,
        quantity: int,
        side: str,
        unique_id: str,
        headers: dict,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.STOPLOSS,
    ) -> dict[Any, Any]:
        """
        Place Stoploss Order in NSE/BSE Equity Segment.

        Parameters:
            exchange (str): Exchange to place the order in. Possible Values: NSE, BSE.
            symbol (str): Trading symbol, the same one you use on TradingView. Ex: "RELIANCE", "BHEL"
            price (float): Order price.
            trigger (float): order trigger price.
            quantity (int): Order quantity.
            side (str): Order Side: BUY, SELL.
            unique_id (str): Unique user order_id.
            headers (dict): headers to send order request with.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity. Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.REGULAR.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not cls.eq_tokens:
            cls.create_eq_tokens()

        exchange = cls._key_mapper(cls.req_exchange, exchange, "exchange")
        detail = cls._eq_mapper(cls.eq_tokens[exchange], symbol)
        token = detail["Token"]
        symbol = detail["Symbol"]

        json_data = {
            "symboltoken": token,
            "exchange": exchange,
            "tradingsymbol": symbol,
            "price": price,
            "triggerprice": trigger,
            "quantity": quantity,
            "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
            "ordertype": cls.req_order_type[OrderType.SL],
            "producttype": cls._key_mapper(cls.req_product, product, "product"),
            "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
            "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
            "ordertag": unique_id,
            "disclosedquantity": "0",
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def slm_order_eq(
        cls,
        exchange: str,
        symbol: str,
        trigger: float,
        quantity: int,
        side: str,
        unique_id: str,
        headers: dict,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.STOPLOSS,
    ) -> dict[Any, Any]:
        """
        Place Stoploss-Market Order in NSE/BSE Equity Segment.

        Parameters:
            exchange (str): Exchange to place the order in. Possible Values: NSE, BSE.
            symbol (str): Trading symbol, the same one you use on TradingView. Ex: "RELIANCE", "BHEL"
            trigger (float): order trigger price.
            quantity (int): Order quantity.
            side (str): Order Side: BUY, SELL.
            unique_id (str): Unique user order_id.
            headers (dict): headers to send order request with.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity. Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.REGULAR.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not cls.eq_tokens:
            cls.create_eq_tokens()

        exchange = cls._key_mapper(cls.req_exchange, exchange, "exchange")
        detail = cls._eq_mapper(cls.eq_tokens[exchange], symbol)
        token = detail["Token"]
        symbol = detail["Symbol"]

        json_data = {
            "symboltoken": token,
            "exchange": exchange,
            "tradingsymbol": symbol,
            "price": "0",
            "triggerprice": trigger,
            "quantity": quantity,
            "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
            "ordertype": cls.req_order_type[OrderType.SLM],
            "producttype": cls._key_mapper(cls.req_product, product, "product"),
            "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
            "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
            "ordertag": unique_id,
            "disclosedquantity": "0",
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    # NFO Order Functions

    @classmethod
    def create_order_fno(
        cls,
        exchange: str,
        root: str,
        expiry: str,
        option: str,
        strike_price: str,
        quantity: int,
        side: str,
        product: str,
        validity: str,
        variety: str,
        unique_id: str,
        headers: dict,
        price: float = 0.0,
        trigger: float = 0.0,
    ) -> dict[Any, Any]:
        """
        Place an Order in F&O Segment.

        Parameters:
            exchange (str):  Exchange to place the order in.
            root (str): Derivative: BANKNIFTY, NIFTY.
            expiry (str): Expiry of the Option: 'CURRENT', 'NEXT', 'FAR'.
            option (str): Option Type: 'CE', 'PE'.
            strike_price (str): Strike Price of the Option.
            quantity (int): Order quantity.
            side (str): Order Side: 'BUY', 'SELL'.
            product (str): Order product.
            validity (str): Order validity.
            variety (str): Order variety.
            unique_id (str): Unique user orderid.
            headers (dict): headers to send order request with.
            price (float): price of the order.
            trigger (float): trigger price of the order.

        Raises:
            KeyError: If Strike Price Does not Exist.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not cls.fno_tokens:
            cls.create_fno_tokens()

        detail = cls.fno_tokens[expiry][root][option]
        detail = detail.get(strike_price, None)

        if not detail:
            raise KeyError(f"StrikePrice: {strike_price} Does not Exist")

        token = detail["Token"]
        symbol = detail["Symbol"]

        if not price and trigger:
            order_type = OrderType.SLM
            variety = (
                cls.req_variety[Variety.STOPLOSS]
                if variety == cls.req_variety[Variety.REGULAR]
                else variety
            )
        elif not price:
            order_type = OrderType.MARKET
        elif not trigger:
            order_type = OrderType.LIMIT
        else:
            order_type = OrderType.SL
            variety = (
                cls.req_variety[Variety.STOPLOSS]
                if variety == cls.req_variety[Variety.REGULAR]
                else variety
            )

        json_data = {
            "symboltoken": token,
            "exchange": cls._key_mapper(cls.req_exchange, exchange, "exchange"),
            "tradingsymbol": symbol,
            "price": price,
            "triggerprice": trigger,
            "quantity": quantity,
            "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
            "ordertype": cls.req_order_type[order_type],
            "producttype": cls._key_mapper(cls.req_product, product, "product"),
            "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
            "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
            "ordertag": unique_id,
            "disclosedquantity": "0",
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def market_order_fno(
        cls,
        option: str,
        strike_price: str,
        quantity: int,
        side: str,
        headers: dict,
        root: str = Root.BNF,
        expiry: str = WeeklyExpiry.CURRENT,
        exchange: str = ExchangeCode.NFO,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.REGULAR,
        unique_id: str = UniqueID.MARKETORDER,
    ) -> dict[Any, Any]:
        """
        Place Market Order in F&O Segment.

        Parameters:
            option (str): Option Type: 'CE', 'PE'.
            strike_price (str): Strike Price of the Option.
            quantity (int): Order quantity.
            side (str): Order Side: 'BUY', 'SELL'.
            headers (dict): headers to send order request with.
            root (str): Derivative: BANKNIFTY, NIFTY.
            expiry (str, optional): Expiry of the Option: 'CURRENT', 'NEXT', 'FAR'. Defaults to WeeklyExpiry.CURRENT.
            exchange (str, optional):  Exchange to place the order in. Defaults to ExchangeCode.NFO.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.DAY.
            unique_id (str, optional): Unique user orderid. Defaults to UniqueID.MARKETORDER.

        Raises:
            KeyError: If Strike Price Does not Exist.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not cls.fno_tokens:
            cls.create_fno_tokens()

        detail = cls.fno_tokens[expiry][root][option]
        detail = detail.get(strike_price, None)

        if not detail:
            raise KeyError(f"StrikePrice: {strike_price} Does not Exist")

        symbol = detail["Symbol"]
        token = detail["Token"]

        json_data = {
            "symboltoken": token,
            "exchange": cls._key_mapper(cls.req_exchange, exchange, "exchange"),
            "tradingsymbol": symbol,
            "price": "0",
            "triggerprice": "0",
            "quantity": quantity,
            "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
            "ordertype": cls.req_order_type[OrderType.MARKET],
            "producttype": cls._key_mapper(cls.req_product, product, "product"),
            "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
            "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
            "ordertag": unique_id,
            "disclosedquantity": "0",
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def limit_order_fno(
        cls,
        option: str,
        strike_price: str,
        price: float,
        quantity: int,
        side: str,
        headers: dict,
        root: str = Root.BNF,
        expiry: str = WeeklyExpiry.CURRENT,
        exchange: str = ExchangeCode.NFO,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.REGULAR,
        unique_id: str = UniqueID.LIMITORDER,
    ) -> dict[Any, Any]:
        """
        Place Limit Order in F&O Segment.

        Parameters:
            option (str): Option Type: 'CE', 'PE'.
            strike_price (str): Strike Price of the Option.
            price (float): price of the order.
            quantity (int): Order quantity.
            side (str): Order Side: 'BUY', 'SELL'.
            headers (dict): headers to send order request with.
            root (str): Derivative: BANKNIFTY, NIFTY.
            expiry (str, optional): Expiry of the Option: 'CURRENT', 'NEXT', 'FAR'. Defaults to WeeklyExpiry.CURRENT.
            exchange (str, optional):  Exchange to place the order in. Defaults to ExchangeCode.NFO.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.DAY.
            unique_id (str, optional): Unique user orderid. Defaults to UniqueID.MARKETORDER.

        Raises:
            KeyError: If Strike Price Does not Exist.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not cls.fno_tokens:
            cls.fno_tokens()

        detail = cls.fno_tokens[expiry][root][option]
        detail = detail.get(strike_price, None)

        if not detail:
            raise KeyError(f"StrikePrice: {strike_price} Does not Exist")

        symbol = detail["Symbol"]
        token = detail["Token"]

        json_data = {
            "symboltoken": token,
            "exchange": cls._key_mapper(cls.req_exchange, exchange, "exchange"),
            "tradingsymbol": symbol,
            "price": price,
            "triggerprice": "0",
            "quantity": quantity,
            "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
            "ordertype": cls.req_order_type[OrderType.LIMIT],
            "producttype": cls._key_mapper(cls.req_product, product, "product"),
            "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
            "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
            "ordertag": unique_id,
            "disclosedquantity": "0",
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def sl_order_fno(
        cls,
        option: str,
        strike_price: str,
        price: float,
        trigger: float,
        quantity: int,
        side: str,
        headers: dict,
        root: str = Root.BNF,
        expiry: str = WeeklyExpiry.CURRENT,
        exchange: str = ExchangeCode.NFO,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.STOPLOSS,
        unique_id: str = UniqueID.SLORDER,
    ) -> dict[Any, Any]:
        """
        Place Stoploss Order in F&O Segment.

        Parameters:
            option (str): Option Type: 'CE', 'PE'.
            strike_price (str): Strike Price of the Option.
            price (float): price of the order.
            trigger (float): trigger price of the order.
            quantity (int): Order quantity.
            side (str): Order Side: 'BUY', 'SELL'.
            headers (dict): headers to send order request with.
            root (str): Derivative: BANKNIFTY, NIFTY.
            expiry (str, optional): Expiry of the Option: 'CURRENT', 'NEXT', 'FAR'. Defaults to WeeklyExpiry.CURRENT.
            exchange (str, optional):  Exchange to place the order in. Defaults to ExchangeCode.NFO.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.DAY.
            unique_id (str, optional): Unique user orderid. Defaults to UniqueID.MARKETORDER.

        Raises:
            KeyError: If Strike Price Does not Exist.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not cls.fno_tokens:
            cls.create_fno_tokens()

        detail = cls.fno_tokens[expiry][root][option]
        detail = detail.get(strike_price, None)

        if not detail:
            raise KeyError(f"StrikePrice: {strike_price} Does not Exist")

        symbol = detail["Symbol"]
        token = detail["Token"]

        json_data = {
            "symboltoken": token,
            "exchange": cls._key_mapper(cls.req_exchange, exchange, "exchange"),
            "tradingsymbol": symbol,
            "price": price,
            "triggerprice": trigger,
            "quantity": quantity,
            "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
            "ordertype": cls.req_order_type[OrderType.SL],
            "producttype": cls._key_mapper(cls.req_product, product, "product"),
            "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
            "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
            "ordertag": unique_id,
            "disclosedquantity": "0",
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def slm_order_fno(
        cls,
        option: str,
        strike_price: str,
        trigger: float,
        quantity: int,
        side: str,
        headers: dict,
        root: str = Root.BNF,
        expiry: str = WeeklyExpiry.CURRENT,
        exchange: str = ExchangeCode.NFO,
        product: str = Product.MIS,
        validity: str = Validity.DAY,
        variety: str = Variety.STOPLOSS,
        unique_id: str = UniqueID.SLORDER,
    ) -> dict[Any, Any]:
        """
        Place Stoploss-Market Order in F&O Segment.

        Parameters:
            option (str): Option Type: 'CE', 'PE'.
            strike_price (str): Strike Price of the Option.
            trigger (float): trigger price of the order.
            quantity (int): Order quantity.
            side (str): Order Side: 'BUY', 'SELL'.
            headers (dict): headers to send order request with.
            root (str): Derivative: BANKNIFTY, NIFTY.
            expiry (str, optional): Expiry of the Option: 'CURRENT', 'NEXT', 'FAR'. Defaults to WeeklyExpiry.CURRENT.
            exchange (str, optional):  Exchange to place the order in. Defaults to ExchangeCode.NFO.
            product (str, optional): Order product. Defaults to Product.MIS.
            validity (str, optional): Order validity Defaults to Validity.DAY.
            variety (str, optional): Order variety Defaults to Variety.DAY.
            unique_id (str, optional): Unique user orderid. Defaults to UniqueID.MARKETORDER.

        Raises:
            KeyError: If Strike Price Does not Exist.

        Returns:
            dict: fenix Unified Order Response.
        """
        if not cls.fno_tokens:
            cls.create_fno_tokens()

        detail = cls.fno_tokens[expiry][root][option]
        detail = detail.get(strike_price, None)

        if not detail:
            raise KeyError(f"StrikePrice: {strike_price} Does not Exist")

        symbol = detail["Symbol"]
        token = detail["Token"]

        json_data = {
            "symboltoken": token,
            "exchange": cls._key_mapper(cls.req_exchange, exchange, "exchange"),
            "tradingsymbol": symbol,
            "price": "0",
            "triggerprice": trigger,
            "quantity": quantity,
            "transactiontype": cls._key_mapper(cls.req_side, side, "side"),
            "ordertype": cls.req_order_type[OrderType.SLM],
            "producttype": cls._key_mapper(cls.req_product, product, "product"),
            "duration": cls._key_mapper(cls.req_validity, validity, "validity"),
            "variety": cls._key_mapper(cls.req_variety, variety, "variety"),
            "ordertag": unique_id,
            "disclosedquantity": "0",
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    # Order Details, OrderBook & TradeBook

    @classmethod
    def fetch_raw_orderbook(
        cls,
        headers: dict,
    ) -> list[dict]:
        """
        Fetch Raw Orderbook Details, without any Standardaization.

        Parameters:
            headers (dict): headers to send fetch_orders request with.

        Returns:
            list[dict]:Raw Broker Orderbook Response.
        """
        response = cls.fetch(
            method="GET",
            url=cls.urls["orderbook"],
            headers=headers["headers"],
        )
        info = cls._json_parser(response)
        return info["data"]

    @classmethod
    def fetch_orderbook(
        cls,
        headers: dict,
    ) -> list[dict]:
        """
        Fetch Orderbook Details.

        Parameters:
            headers (dict): headers to send fetch_orders request with.

        Returns:
            list[dict]: List of dicitonaries of orders using fenix Unified Order Response.
        """
        info = cls.fetch_raw_orderbook(headers=headers)
        orders = []

        if info:
            for order in info:
                detail = cls._orderbook_json_parser(order)
                orders.append(detail)

        return orders

    @classmethod
    def fetch_tradebook(
        cls,
        headers: dict,
    ) -> list[dict]:
        """
        Fetch Tradebook Details.

        Parameters:
            headers (dict): headers to send fetch_orders request with.

        Returns:
            list[dict]: List of dicitonaries of orders using fenix Unified Order Response.
        """
        response = cls.fetch(
            method="GET",
            url=cls.urls["tradebook"],
            headers=headers["headers"],
        )
        info = cls._json_parser(response)

        orders = []
        if info["data"]:
            for order in info["data"]:
                detail = cls._tradebook_json_parser(order)
                orders.append(detail)

        return orders

    @classmethod
    def fetch_orders(
        cls,
        headers: dict,
    ) -> list[dict]:
        """
        Fetch OrderBook Details which is unified across all brokers.
        Use This if you want Avg price, etc. values which sometimes unavailable
        thorugh fetch_orderbook.

        Paramters:
            order_id (str): id of the order.

        Raises:
            InputError: If order does not exist.

        Returns:
            dict: fenix Unified Order Response.
        """
        return cls.fetch_orderbook(headers=headers)

    @classmethod
    def fetch_order(
        cls,
        order_id: str,
        headers: dict,
    ) -> dict[Any, Any]:
        """
        Fetch Order Details.

        Paramters:
            order_id (str): id of the order.

        Raises:
            InputError: If order does not exist.

        Returns:
            dict: fenix Unified Order Response.
        """
        info = cls.fetch_raw_orderbook(headers=headers)

        if info:
            for order in info:
                if order["orderid"] == order_id:
                    detail = cls._orderbook_json_parser(order)
                    return detail

        raise InputError({"This orderid does not exist."})

    # Order Modification

    @classmethod
    def modify_order(
        cls,
        order_id: str,
        headers: dict,
        price: float | None = None,
        trigger: float | None = None,
        quantity: int | None = None,
        order_type: str | None = None,
        validity: str | None = None,
    ) -> dict[Any, Any]:
        """
        Modify an open order.

        Parameters:
            order_id (str): id of the order to modify.
            headers (dict): headers to send modify_order request with.
            price (float | None, optional): price of t.he order. Defaults to None.
            trigger (float | None, optional): trigger price of the order. Defaults to None.
            quantity (int | None, optional): order quantity. Defaults to None.
            order_type (str | None, optional): Type of Order. defaults to None
            validity (str | None, optional): Order validity Defaults to None.

        Returns:
            dict: fenix Unified Order Response.
        """
        order_info = cls.fetch_order(order_id=order_id, headers=headers)

        json_data = {
            "orderid": order_id,
            "symboltoken": order_info[Order.TOKEN],
            "exchange": order_info[Order.EXCHANGE],
            "tradingsymbol": order_info[Order.SYMBOL],
            "price": price or order_info[Order.PRICE],
            "quantity": quantity or order_info[Order.QUANTITY],
            "ordertype": (
                cls._key_mapper(cls.req_order_type, order_type, "order_type")
                if order_type
                else cls.req_order_type[order_info[Order.TYPE]]
            ),
            "producttype": cls.req_product.get(
                order_info[Order.PRODUCT], order_info[Order.PRODUCT]
            ),
            "duration": (
                cls._key_mapper(cls.req_validity, validity, "validity")
                if validity
                else cls.req[order_info[Order.VALIDITY]]
            ),
            "variety": cls.req_variety.get(
                order_info[Order.VARIETY], order_info[Order.VARIETY]
            ),
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["modify_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(response=response, headers=headers)

    @classmethod
    def cancel_order(
        cls,
        order_id: str,
        headers: dict,
    ) -> dict[Any, Any]:
        """
        Cancel an open order.

        Parameters:
            order_id (str): id of the order.
            headers (dict): headers to send cancel_order request with.

        Returns:
            dict: fenix Unified Order Response.
        """
        curr_order = cls.fetch_order(order_id=order_id, headers=headers)

        json_data = {
            "orderid": order_id,
            "variety": cls.req_variety.get(
                curr_order[Order.VARIETY], curr_order[Order.VARIETY]
            ),
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["cancel_order"],
            json=json_data,
            headers=headers["headers"],
        )

        info = cls._json_parser(response)
        return cls.fetch_order(order_id=info["data"]["orderid"], headers=headers)

    # Positions, Account Limits & Profile

    @classmethod
    def fetch_day_positions(
        cls,
        headers: dict,
    ) -> dict[Any, Any]:
        """
        Fetch the Day's Account Positions.

        Args:
            headers (dict): headers to send rms_limits request with.

        Returns:
            dict[Any, Any]: fenix Unified Position Response.
        """
        response = cls.fetch(
            method="GET",
            url=cls.urls["positions"],
            headers=headers["headers"],
        )
        info = cls._json_parser(response)

        positions = []
        if info["data"]:
            for position in info["data"]:
                detail = cls._position_json_parser(position)
                positions.append(detail)

        return positions

    @classmethod
    def fetch_net_positions(
        cls,
        headers: dict,
    ) -> dict[Any, Any]:
        """
        Fetch Total Account Positions.

        Args:
            headers (dict): headers to send rms_limits request with.

        Returns:
            dict[Any, Any]: fenix Unified Position Response.
        """
        return cls.fetch_day_positions(headers=headers)

    @classmethod
    def fetch_positions(
        cls,
        headers: dict,
    ) -> dict[Any, Any]:
        """
        Fetch Day & Net Account Positions.

        Args:
            headers (dict): headers to send rms_limits request with.

        Returns:
            dict[Any, Any]: fenix Unified Position Response.
        """
        return cls.fetch_day_positions(headers=headers)

    @classmethod
    def fetch_holdings(
        cls,
        headers: dict,
    ) -> dict[Any, Any]:
        """
        Fetch Account Holdings.

        Args:
            headers (dict): headers to send rms_limits request with.

        Returns:
            dict[Any, Any]: fenix Unified Positions Response.
        """
        response = cls.fetch(
            method="GET",
            url=cls.urls["holdings"],
            headers=headers["headers"],
        )
        return cls._json_parser(response)["data"]

    @classmethod
    def rms_limits(
        cls,
        headers: dict,
    ) -> dict[Any, Any]:
        """
        Fetch Risk Management System Limits.

        Parameters:
            headers (dict): headers to send rms_limits request with.

        Returns:
            dict: fenix Unified RMS Limits Response.
        """
        response = cls.fetch(
            method="GET",
            url=cls.urls["rms_limits"],
            headers=headers["headers"],
        )
        return cls._json_parser(response)["data"]

    @classmethod
    def profile(
        cls,
        headers: dict,
    ) -> dict[Any, Any]:
        """
        Fetch Profile Limits of the User.

        Parameters:
            headers (dict): headers to send profile request with.

        Returns:
            dict: fenix Unified Profile Response.
        """
        response = cls.fetch(
            method="GET",
            url=cls.urls["profile"],
            headers=headers["headers"],
        )
        info = cls._json_parser(response)
        profile = cls._profile_json_parser(info["data"])

        return profile
