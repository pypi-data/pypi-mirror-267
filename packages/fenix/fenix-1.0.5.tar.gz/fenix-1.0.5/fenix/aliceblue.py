from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Any

import base64
import hashlib
from os import urandom

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import modes

from fenix.base.broker import Broker

from fenix.base.constants import Side
from fenix.base.constants import OrderType
from fenix.base.constants import ExchangeCode
from fenix.base.constants import Product
from fenix.base.constants import Validity
from fenix.base.constants import Variety
from fenix.base.constants import Status
from fenix.base.constants import Order
from fenix.base.constants import Profile
from fenix.base.constants import Root
from fenix.base.constants import WeeklyExpiry
from fenix.base.constants import UniqueID


from fenix.base.errors import InputError
from fenix.base.errors import ResponseError
from fenix.base.errors import TokenDownloadError

if TYPE_CHECKING:
    from requests.models import Response


class CryptoJsAES:
    @staticmethod
    def __pad(data):
        BLOCK_SIZE = 16
        length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
        return data + (chr(length) * length).encode()

    @staticmethod
    def __unpad(data):
        return data[: -(data[-1] if isinstance(data[-1], int) else ord(data[-1]))]

    @staticmethod
    def __bytes_to_key(data, salt, output=48):
        assert len(salt) == 8, len(salt)
        data += salt
        key = hashlib.md5(data).digest()
        final_key = key
        while len(final_key) < output:
            key = hashlib.md5(key + data).digest()
            final_key += key
        return final_key[:output]

    @staticmethod
    def encrypt(message, passphrase):
        salt = urandom(8)
        key_iv = CryptoJsAES.__bytes_to_key(passphrase, salt, 32 + 16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = Cipher(algorithms.AES(key), modes.CBC(iv))
        return base64.b64encode(
            b"Salted__"
            + salt
            + aes.encryptor().update(CryptoJsAES.__pad(message))
            + aes.encryptor().finalize()
        )

    @staticmethod
    def decrypt(encrypted, passphrase):
        encrypted = base64.b64decode(encrypted)
        assert encrypted[0:8] == b"Salted__"
        salt = encrypted[8:16]
        key_iv = CryptoJsAES.__bytes_to_key(passphrase, salt, 32 + 16)
        key = key_iv[:32]
        iv = key_iv[32:]
        aes = Cipher(algorithms.AES(key), modes.CBC(iv))
        return CryptoJsAES.__unpad(
            aes.decryptor.update(encrypted[16:]) + aes.decryptor().finalize()
        )


class aliceblue(Broker):
    """
    AliceBlue fenix Broker Class.

    Returns:
        fenix.aliceblue: fenix AliceBlue Broker Object.
    """

    # Market Data Dictonaries

    indices = {}
    eq_tokens = {}
    fno_tokens = {}
    token_params = [
        "user_id",
        "password",
        "birth_year",
        "totpstr",
        "api_key",
    ]
    id = "aliceblue"
    _session = Broker._create_session()

    # Base URLs

    base_urls = {
        "api_doc": "https://v2api.aliceblueonline.com/introduction",
        "token_01": "https://ant.aliceblueonline.com/rest/AliceBlueAPIService",
        "token_02": "https://ant.aliceblueonline.com/",
        "base": "https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api",
        "market_data": "https://v2api.aliceblueonline.com/restpy/contract_master",
    }

    # Access Token Generation URLs

    token_urls = {
        "get_enc_key": f"{base_urls['base']}/customer/getAPIEncpkey",
        "session_id": f"{base_urls['base']}/customer/getUserSID",
        "get_encryption_key": f"{base_urls['token_01']}/customer/getEncryptionKey",
        "enc_key": f"{base_urls['token_02']}/omk/auth/access/client/enckey",
        "login": f"{base_urls['token_02']}/omk/auth/access/v1/pwd/validate",
        "verify_totp": f"{base_urls['token_02']}/omk/auth/access/topt/verify",
    }

    # Order Placing URLs

    urls = {
        "place_order": f"{base_urls['base']}/placeOrder/executePlaceOrder",
        "modify_order": f"{base_urls['base']}/placeOrder/modifyOrder",
        "cancel_order": f"{base_urls['base']}/placeOrder/cancelOrder",
        "exit_bracket_order": f"{base_urls['base']}/placeOrder/exitBracketOrder",
        "orderbook": f"{base_urls['base']}/placeOrder/fetchOrderBook",
        "tradebook": f"{base_urls['base']}/placeOrder/fetchTradeBook",
        "order_history": f"{base_urls['base']}/placeOrder/orderHistory",
        "positions": f"{base_urls['base']}/positionAndHoldings/positionBook",
        "holdings": f"{base_urls['base']}/positionAndHoldings/holdings",
        "sqoff_position": f"{base_urls['base']}/positionAndHoldings/sqrOofPosition",
        "rms_limits": f"{base_urls['base']}/limits/getRmsLimits",
        "profile": f"{base_urls['base']}/customer/accountDetails",
    }

    # Request Parameters Dictionaries

    req_exchange = {
        ExchangeCode.NSE: "NSE",
        ExchangeCode.NFO: "NFO",
        ExchangeCode.BSE: "BSE",
        ExchangeCode.BFO: "BFO",
        ExchangeCode.BCD: "BCD",
        ExchangeCode.MCX: "MCX",
        ExchangeCode.CDS: "CDS",
    }

    req_order_type = {
        OrderType.MARKET: "MKT",
        OrderType.LIMIT: "L",
        OrderType.SL: "SL",
        OrderType.SLM: "SL-M",
    }

    req_product = {
        Product.MIS: "MIS",
        Product.NRML: "NRML",
        Product.CNC: "CNC",
        Product.CO: "CO",
        Product.BO: "BO",
    }

    req_side = {
        Side.BUY: "BUY",
        Side.SELL: "SELL",
    }

    req_validity = {
        Validity.DAY: "DAY",
        Validity.IOC: "IOC",
    }

    req_variety = {
        Variety.REGULAR: "REGULAR",
        Variety.STOPLOSS: "REGULAR",
        Variety.BO: "BO",
        Variety.AMO: "AMO",
    }

    # Response Parameters Dictionaries

    resp_order_type = {
        "MKT": OrderType.MARKET,
        "L": OrderType.LIMIT,
        "SL": OrderType.SL,
        "SL-M": OrderType.SLM,
    }

    resp_segment = {
        "nse_cm": ExchangeCode.NSE,
        "bse_cm": ExchangeCode.BSE,
        "nse_fo": ExchangeCode.NFO,
        "bse_fo": ExchangeCode.BFO,
        "mcx_fo": ExchangeCode.MCX,
        "cde_fo": ExchangeCode.CDS,
        "mcx_sx": ExchangeCode.BFO,
        "bcs_fo": ExchangeCode.BCD,
        "nse_com": ExchangeCode.NCO,
        "bse_com": ExchangeCode.BCO,
    }

    resp_side = {
        "B": Side.BUY,
        "S": Side.SELL,
    }

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

    # NFO Script Fetch

    @classmethod
    def create_eq_tokens(cls) -> dict:
        """
        Downlaods NSE & BSE Equity Info for F&O Segment.
        Stores them in the aliceblue.indices Dictionary.

        Returns:
            dict: Unified fenix indices format.
        """
        params = {"exch": ExchangeCode.BSE}
        response = cls.fetch(
            method="GET",
            url=cls.base_urls["market_data"],
            params=params,
        )
        data = cls._json_parser(response)[ExchangeCode.BSE]

        df_bse = cls.data_frame(data)

        df_bse = df_bse[(df_bse["instrument_type"] == "E")]
        df_bse = df_bse[["trading_symbol", "token", "lot_size", "tick_size", "exch"]]
        df_bse.rename(
            {
                "trading_symbol": "Symbol",
                "tick_size": "TickSize",
                "lot_size": "LotSize",
                "exch": "Exchange",
                "token": "Token",
            },
            axis=1,
            inplace=True,
        )

        df_bse.set_index(df_bse["Symbol"], inplace=True)

        df_bse["TickSize"] = df_bse["TickSize"].astype(float)
        df_bse["LotSize"] = df_bse["LotSize"].astype(int)
        df_bse["Token"] = df_bse["Token"].astype(int)

        params = {"exch": ExchangeCode.NSE}
        response = cls.fetch(
            method="GET",
            url=cls.base_urls["market_data"],
            params=params,
        )
        data = cls._json_parser(response)[ExchangeCode.NSE]

        df_nse = cls.data_frame(data)

        df_nse = df_nse[(df_nse["group_name"] == "EQ")]
        df_nse = df_nse[
            ["symbol", "trading_symbol", "token", "lot_size", "tick_size", "exch"]
        ]
        df_nse.rename(
            {
                "symbol": "Index",
                "trading_symbol": "Symbol",
                "tick_size": "TickSize",
                "lot_size": "LotSize",
                "exch": "Exchange",
                "token": "Token",
            },
            axis=1,
            inplace=True,
        )

        df_nse.set_index(df_nse["Index"], inplace=True)
        df_nse.drop(columns="Index", inplace=True)

        df_nse["TickSize"] = df_nse["TickSize"].astype(float)
        df_nse["LotSize"] = df_nse["LotSize"].astype(int)
        df_nse["Token"] = df_nse["Token"].astype(int)

        cls.eq_tokens[ExchangeCode.NSE] = df_nse.to_dict(orient="index")
        cls.eq_tokens[ExchangeCode.BSE] = df_bse.to_dict(orient="index")

        return cls.eq_tokens

    @classmethod
    def create_indices(cls) -> dict:
        """
        Downloads all the Broker Indices Token data.
        Stores them in the aliceblue.indices Dictionary.

        Returns:
            dict: Unified fenix indices format.
        """

        params = {"exch": "INDICES"}
        response = cls.fetch(
            method="GET",
            url=cls.base_urls["market_data"],
            params=params,
        )
        data = cls._json_parser(response)

        indices = {}

        for exch in [ExchangeCode.NSE, ExchangeCode.BSE, ExchangeCode.MCX]:
            for token_data in data[exch]:
                indices[token_data["symbol"]] = {
                    "Symbol": token_data["symbol"],
                    "Token": token_data["token"],
                    "Exchange": exch,
                }

        indices[Root.BNF] = indices["NIFTY BANK"]
        indices[Root.NF] = indices["NIFTY 50"]
        indices[Root.FNF] = indices["NIFTY FIN SERVICE"]
        indices[Root.MIDCPNF] = indices["NIFTY MIDCAP SELECT"]

        cls.indices = indices

        return indices

    @classmethod
    def create_fno_tokens(cls) -> dict:
        """
        Downloades Token Data for the FNO Segment for the 3 latest Weekly Expiries.
        Stores them in the aliceblue.fno_tokens Dictionary.

        Raises:
            TokenDownloadError: Any Error Occured is raised through this Error Type.
        """
        try:
            params = {"exch": ExchangeCode.NFO}
            response = cls.fetch(
                method="GET",
                url=cls.base_urls["market_data"],
                params=params,
            )
            data = cls._json_parser(response)[ExchangeCode.NFO]

            df_nfo = cls.data_frame(data)

            df_nfo = df_nfo[
                (
                    (df_nfo["symbol"] == "BANKNIFTY")
                    | (df_nfo["symbol"] == "NIFTY")
                    | (df_nfo["symbol"] == "FINNIFTY")
                    | (df_nfo["symbol"] == "MIDCPNIFTY")
                )
                & ((df_nfo["instrument_type"] == "OPTIDX"))
            ]

            params = {"exch": ExchangeCode.BFO}
            response = cls.fetch(
                method="GET",
                url=cls.base_urls["market_data"],
                params=params,
            )
            data = cls._json_parser(response)[ExchangeCode.BFO]

            df_bfo = cls.data_frame(data)

            df_bfo = df_bfo[
                ((df_bfo["symbol"] == "SENSEX") | (df_bfo["symbol"] == "BANKEX"))
                & ((df_bfo["instrument_type"] == "IO"))
            ]

            df = cls.concat_df([df_nfo, df_bfo])

            df.rename(
                {
                    "option_type": "Option",
                    "symbol": "Root",
                    "exch": "Exchange",
                    "expiry_date": "Expiry",
                    "trading_symbol": "Symbol",
                    "tick_size": "TickSize",
                    "lot_size": "LotSize",
                    "strike_price": "StrikePrice",
                    "token": "Token",
                },
                axis=1,
                inplace=True,
            )
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

            df["StrikePrice"] = df["StrikePrice"].astype(int).astype(str)
            df["Expiry"] = cls.pd_datetime(df["Expiry"], unit="ms").dt.date.astype(str)
            df["Token"] = df["Token"].astype(int)
            df["TickSize"] = df["TickSize"].astype(float)
            df["LotSize"] = df["LotSize"].astype(float)

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
        Generate Headers used to access Endpoints in AliceBlue.

        Parameters:
            Params (dict) : A dictionary which should consist the following keys:
                user_id (str): User ID of the Account.
                password (str): Password of the Account.
                birth_year (str): Birth Year of the Account Holder.
                totpstr (str): String of characters used to generate TOTP.
                api_key (str): API Key of the Account.

        Returns:
            dict[str, str]: AliceBlue Headers.
        """
        for key in cls.token_params:
            if key not in params:
                raise KeyError(f"Please provide {key}")

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }

        json_data = {"userId": params["user_id"]}
        response = cls.fetch(
            method="POST",
            url=cls.token_urls["get_enc_key"],
            json=json_data,
            headers=headers,
        )
        response = cls._json_parser(response)

        if response["login"]:

            encryption_key = response["encKey"]

            hash_code = hashlib.sha256(
                (params["user_id"] + params["api_key"] + encryption_key).encode()
            ).hexdigest()
            json_data = {"userId": params["user_id"], "userData": hash_code}
            response = cls.fetch(
                method="POST",
                url=cls.token_urls["session_id"],
                json=json_data,
            )
            response = cls._json_parser(response)

            access_token = response["sessionID"]

            sha256_encryption1 = hashlib.sha256(
                access_token.encode("utf-8")
            ).hexdigest()
            susertoken = hashlib.sha256(sha256_encryption1.encode("utf-8")).hexdigest()

            headers = {
                "headers": {
                    "ID": params["user_id"],
                    "AccessToken": access_token,
                    "Authorization": f'Bearer {params["user_id"]} {access_token}',
                    "X-SAS-Version": "2.0",
                    "User-Agent": "AliceBlue_V21.0.1",
                    "Content-Type": "application/json",
                    "susertoken": susertoken,
                }
            }

            cls._session = cls._create_session()
            return headers

        else:

            json_data = {"userId": params["user_id"]}
            response = cls.fetch(
                method="POST",
                url=cls.token_urls["enc_key"],
                json=json_data,
            )
            response = cls._json_parser(response)

            encryption_key = response["result"][0]["encKey"]
            checksum = CryptoJsAES.encrypt(
                params["password"].encode(), encryption_key.encode()
            )
            checksum = checksum.decode("utf-8")
            json_data = {
                "userId": params["user_id"],
                "userData": checksum,
                "source": "WEB",
            }

            login_req = cls.fetch(
                method="POST",
                url=cls.token_urls["login"],
                json=json_data,
            )
            login_resp = cls._json_parser(login_req)
            login_token = login_resp["result"][0]["token"]

            totp = cls.totp_creator(params["totpstr"])
            headers = {"authorization": f'Bearer {params["user_id"]} WEB {login_token}'}
            json_data = {
                "totp": totp,
                "userId": params["user_id"],
                "source": "WEB",
                "deviceId": "4f8fc3f597d72e79d66a798d6f82bf62",
            }
            _ = cls.fetch(
                method="POST",
                url=cls.token_urls["verify_totp"],
                json=json_data,
                headers=headers,
            )  # totp_req

            json_data = {"userId": params["user_id"]}
            response = cls.fetch(
                method="POST",
                url=cls.token_urls["get_enc_key"],
                json=json_data,
            )
            response = cls._json_parser(response)

            encryption_key = response["encKey"]

            hash_code = hashlib.sha256(
                (params["user_id"] + params["api_key"] + encryption_key).encode()
            ).hexdigest()
            json_data = {"userId": params["user_id"], "userData": hash_code}
            response = cls.fetch(
                method="POST",
                url=cls.token_urls["session_id"],
                json=json_data,
            )
            response = cls._json_parser(response)

            access_token = response["sessionID"]
            sha256_encryption1 = hashlib.sha256(
                access_token.encode("utf-8")
            ).hexdigest()
            susertoken = hashlib.sha256(sha256_encryption1.encode("utf-8")).hexdigest()

            headers = {
                "ID": params["user_id"],
                "AccessToken": access_token,
                "Authorization": f'Bearer {params["user_id"]} {access_token}',
                "X-SAS-Version": "2.0",
                "User-Agent": "AliceBlue_V21.0.1",
                "Content-Type": "application/json",
                "susertoken": susertoken,
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
        if isinstance(json_response, dict):
            stat = json_response.get("stat", None)

            if stat == "Ok" or not stat:
                return json_response

            error = json_response.get("emsg", None)
            error = error if error else json_response.get("Emsg", None)
            raise ResponseError(cls.id + " " + error)

        if isinstance(json_response, list):
            stat = json_response[0].get(
                "stat",
            )

            if stat == "Ok" or not stat:
                return json_response

            error = json_response[0].get("emsg", None)
            error = error if error else json_response[0].get("Emsg", str(json_response))
            raise ResponseError(cls.id + " " + error)

    @classmethod
    def _orderhistory_json_parser(
        cls,
        order: dict,
    ) -> dict[Any, Any]:
        """
        Parses Order History Json Response to a fenix Unified Order Response.

        Parameters:
            order (dict): Order History Json Response from Broker.

        Returns:
            dict: Unified fenix Order Response.
        """
        parsed_order = {
            Order.ID: order["nestordernumber"],
            Order.USERID: "",
            Order.TIMESTAMP: (
                cls.datetime_strp(order["ExchTimeStamp"], "%d/%m/%Y %H:%M:%S")
                if order["ExchTimeStamp"]
                else order["ExchTimeStamp"]
            ),
            Order.SYMBOL: order["Trsym"],
            Order.TOKEN: "",
            Order.SIDE: cls.resp_side.get(order["Action"], order["Action"]),
            Order.TYPE: cls.resp_order_type.get(order["Ordtype"], order["Ordtype"]),
            Order.AVGPRICE: float(order.get("averageprice") or 0.0),
            Order.PRICE: float(order.get("Prc") or 0.0),
            Order.TRIGGERPRICE: float(order.get("triggerprice") or 0.0),
            Order.TARGETPRICE: 0.0,
            Order.STOPLOSSPRICE: 0.0,
            Order.TRAILINGSTOPLOSS: 0.0,
            Order.QUANTITY: int(order["Qty"]),
            Order.FILLEDQTY: int(order.get("filledShares") or 0),
            Order.REMAININGQTY: int(order["Qty"]) - int(order.get("filledShares") or 0),
            Order.CANCELLEDQTY: 0,
            Order.STATUS: cls.resp_status.get(order["Status"], order["Status"]),
            Order.REJECTREASON: order["rejectionreason"],
            Order.DISCLOSEDQUANTITY: int(order["disclosedqty"]),
            Order.PRODUCT: cls.req_product.get(
                order["productcode"], order["productcode"]
            ),
            Order.EXCHANGE: cls.req_exchange.get(order["exchange"], order["exchange"]),
            Order.SEGMENT: cls.req_exchange.get(order["exchange"], order["exchange"]),
            Order.VALIDITY: cls.req_validity.get(order["duration"], order["duration"]),
            Order.VARIETY: "",
            Order.INFO: order,
        }

        return parsed_order

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
            Order.ID: order["Nstordno"],
            Order.USERID: order["remarks"],
            Order.TIMESTAMP: (
                cls.datetime_strp(order["ExchConfrmtime"], "%d-%b-%Y %H:%M:%S")
                if order["ExchConfrmtime"] != "--"
                else cls.datetime_strp(order["OrderedTime"], "%d/%m/%Y %H:%M:%S")
            ),
            Order.SYMBOL: order["Trsym"],
            Order.TOKEN: int(order["token"]),
            Order.SIDE: cls.resp_side.get(order["Trantype"], order["Trantype"]),
            Order.TYPE: cls.resp_order_type.get(order["Prctype"], order["Prctype"]),
            Order.AVGPRICE: float(order["Avgprc"]),
            Order.PRICE: float(order["Prc"]),
            Order.TRIGGERPRICE: float(order["Trgprc"]),
            Order.TARGETPRICE: 0.0,
            Order.STOPLOSSPRICE: 0.0,
            Order.TRAILINGSTOPLOSS: 0.0,
            Order.QUANTITY: order["Qty"],
            Order.FILLEDQTY: order["Fillshares"],
            Order.REMAININGQTY: order["Unfilledsize"],
            Order.CANCELLEDQTY: order["Cancelqty"],
            Order.STATUS: cls.resp_status.get(order["Status"], order["Status"]),
            Order.REJECTREASON: order["RejReason"],
            Order.DISCLOSEDQUANTITY: order["Dscqty"],
            Order.PRODUCT: cls.req_product.get(order["Pcode"], order["Pcode"]),
            Order.EXCHANGE: cls.req_exchange.get(order["Exchange"], order["Exchange"]),
            Order.SEGMENT: cls.resp_segment.get(order["Exseg"], order["Exseg"]),
            Order.VALIDITY: cls.req_validity.get(order["Validity"], order["Validity"]),
            Order.VARIETY: "",
            Order.INFO: order,
        }

        return parsed_order

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
        exchanges_enabled = [
            cls.resp_segment.get(i, None)
            for i in profile["exchEnabled"].split("|")
            if i
        ]

        parsed_profile = {
            Profile.CLIENTID: profile["accountId"],
            Profile.NAME: profile["accountName"],
            Profile.EMAILID: profile["emailAddr"],
            Profile.MOBILENO: profile["cellAddr"],
            Profile.PAN: "",
            Profile.ADDRESS: "",
            Profile.BANKNAME: "",
            Profile.BANKBRANCHNAME: None,
            Profile.BANKACCNO: "",
            Profile.EXHCNAGESENABLED: exchanges_enabled,
            Profile.ENABLED: profile["accountStatus"] == "Activated",
            Profile.INFO: profile,
        }

        return parsed_profile

    @classmethod
    def _create_order_parser(
        cls, response: Response, key_to_check: str, headers: dict
    ) -> dict[Any, Any]:
        """
        Parse Json Response Obtained from Broker After Placing Order to get order_id
        and fetching the json repsone for the said order_id.

        Parameters:
            response (Response): Json Repsonse Obtained from broker after Placing an Order.
            key_to_check(str): Defines the key to check for order_id in the json respsone obtained after placing an order.
            headers (dict): headers to send order request with.

        Returns:
            dict: Unified fenix Order Response.
        """
        info = cls._json_parser(response)

        order_id = info[0].get(key_to_check)
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
        price: float = 0.0,
        trigger: float = 0.0,
        target: float = 0.0,
        stoploss: float = 0.0,
        trailing_sl: float = 0.0,
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
        elif not price:
            order_type = OrderType.MARKET
        elif not trigger:
            order_type = OrderType.LIMIT
        else:
            order_type = OrderType.SL

        if not target:
            json_data = [
                {
                    "symbol_id": token_dict["Token"],
                    "exch": cls._key_mapper(
                        cls.req_exchange, token_dict["Exchange"], "exchange"
                    ),
                    "trading_symbol": token_dict["Symbol"],
                    "price": price,
                    "trigPrice": trigger,
                    "qty": quantity,
                    "transtype": cls._key_mapper(cls.req_side, side, "side"),
                    "prctyp": cls.req_order_type[order_type],
                    "pCode": cls._key_mapper(cls.req_product, product, "product"),
                    "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                    "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                    "orderTag": unique_id,
                    "discqty": 0,
                }
            ]

        else:
            json_data = [
                {
                    "symbol_id": token_dict["Token"],
                    "exch": cls._key_mapper(
                        cls.req_exchange, token_dict["Exchange"], "exchange"
                    ),
                    "trading_symbol": token_dict["Symbol"],
                    "price": price,
                    "trigPrice": trigger,
                    "target": target,
                    "stopLoss": stoploss,
                    "trailing_stop_loss": trailing_sl,
                    "qty": quantity,
                    "transtype": cls._key_mapper(cls.req_side, side, "side"),
                    "prctyp": cls._key_mapper(
                        cls.req_order_type, order_type, "order_type"
                    ),
                    "pCode": cls._key_mapper(cls.req_product, product, "product"),
                    "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                    "complexty": cls.req_variety[Variety.BO],
                    "orderTag": unique_id,
                    "discqty": 0,
                }
            ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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
            json_data = [
                {
                    "symbol_id": token_dict["Token"],
                    "exch": cls._key_mapper(
                        cls.req_exchange, token_dict["Exchange"], "exchange"
                    ),
                    "trading_symbol": token_dict["Symbol"],
                    "price": 0,
                    "trigPrice": 0,
                    "qty": quantity,
                    "transtype": cls._key_mapper(cls.req_side, side, "side"),
                    "prctyp": cls.req_order_type[OrderType.MARKET],
                    "pCode": cls._key_mapper(cls.req_product, product, "product"),
                    "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                    "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                    "orderTag": unique_id,
                    "discqty": 0,
                }
            ]

        else:
            json_data = [
                {
                    "symbol_id": token_dict["Token"],
                    "exch": cls._key_mapper(
                        cls.req_exchange, token_dict["Exchange"], "exchange"
                    ),
                    "trading_symbol": token_dict["Symbol"],
                    "price": 0,
                    "trigPrice": 0,
                    "target": target,
                    "stopLoss": stoploss,
                    "trailing_stop_loss": trailing_sl,
                    "qty": quantity,
                    "transtype": cls._key_mapper(cls.req_side, side, "side"),
                    "prctyp": cls.req_order_type[OrderType.MARKET],
                    "pCode": cls._key_mapper(cls.req_product, product, "product"),
                    "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                    "complexty": cls.req_variety[Variety.BO],
                    "orderTag": unique_id,
                    "discqty": 0,
                }
            ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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
            json_data = [
                {
                    "symbol_id": token_dict["Token"],
                    "exch": cls._key_mapper(
                        cls.req_exchange, token_dict["Exchange"], "exchange"
                    ),
                    "trading_symbol": token_dict["Symbol"],
                    "price": price,
                    "trigPrice": 0,
                    "qty": quantity,
                    "transtype": cls._key_mapper(cls.req_side, side, "side"),
                    "prctyp": cls.req_order_type[OrderType.LIMIT],
                    "pCode": cls._key_mapper(cls.req_product, product, "product"),
                    "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                    "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                    "orderTag": unique_id,
                    "discqty": 0,
                }
            ]

        else:
            json_data = [
                {
                    "symbol_id": token_dict["Token"],
                    "exch": cls._key_mapper(
                        cls.req_exchange, token_dict["Exchange"], "exchange"
                    ),
                    "trading_symbol": token_dict["Symbol"],
                    "price": price,
                    "trigPrice": 0,
                    "target": target,
                    "stopLoss": stoploss,
                    "trailing_stop_loss": trailing_sl,
                    "qty": quantity,
                    "transtype": cls._key_mapper(cls.req_side, side, "side"),
                    "prctyp": cls.req_order_type[OrderType.LIMIT],
                    "pCode": cls._key_mapper(cls.req_product, product, "product"),
                    "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                    "complexty": cls.req_variety[Variety.BO],
                    "orderTag": unique_id,
                    "discqty": 0,
                }
            ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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
            json_data = [
                {
                    "symbol_id": token_dict["Token"],
                    "exch": cls._key_mapper(
                        cls.req_exchange, token_dict["Exchange"], "exchange"
                    ),
                    "trading_symbol": token_dict["Symbol"],
                    "price": price,
                    "trigPrice": trigger,
                    "qty": quantity,
                    "transtype": cls._key_mapper(cls.req_side, side, "side"),
                    "prctyp": cls.req_order_type[OrderType.SL],
                    "pCode": cls._key_mapper(cls.req_product, product, "product"),
                    "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                    "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                    "orderTag": unique_id,
                    "discqty": 0,
                }
            ]
        else:
            json_data = [
                {
                    "symbol_id": token_dict["Token"],
                    "exch": cls._key_mapper(
                        cls.req_exchange, token_dict["Exchange"], "exchange"
                    ),
                    "trading_symbol": token_dict["Symbol"],
                    "price": price,
                    "trigPrice": trigger,
                    "target": target,
                    "stopLoss": stoploss,
                    "trailing_stop_loss": trailing_sl,
                    "qty": quantity,
                    "transtype": cls._key_mapper(cls.req_side, side, "side"),
                    "prctyp": cls.req_order_type[OrderType.SL],
                    "pCode": cls._key_mapper(cls.req_product, product, "product"),
                    "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                    "complexty": cls.req_variety[Variety.BO],
                    "orderTag": unique_id,
                    "discqty": 0,
                }
            ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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
            json_data = [
                {
                    "symbol_id": token_dict["Token"],
                    "exch": cls._key_mapper(
                        cls.req_exchange, token_dict["Exchange"], "exchange"
                    ),
                    "trading_symbol": token_dict["Symbol"],
                    "price": 0,
                    "trigPrice": trigger,
                    "qty": quantity,
                    "transtype": cls._key_mapper(cls.req_side, side, "side"),
                    "prctyp": cls.req_order_type[OrderType.SLM],
                    "pCode": cls._key_mapper(cls.req_product, product, "product"),
                    "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                    "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                    "orderTag": unique_id,
                    "discqty": 0,
                }
            ]
        else:
            json_data = [
                {
                    "symbol_id": token_dict["Token"],
                    "exch": cls._key_mapper(
                        cls.req_exchange, token_dict["Exchange"], "exchange"
                    ),
                    "trading_symbol": token_dict["Symbol"],
                    "price": 0,
                    "trigPrice": trigger,
                    "target": target,
                    "stopLoss": stoploss,
                    "trailing_stop_loss": trailing_sl,
                    "qty": quantity,
                    "transtype": cls._key_mapper(cls.req_side, side, "side"),
                    "prctyp": cls.req_order_type[OrderType.SLM],
                    "pCode": cls._key_mapper(cls.req_product, product, "product"),
                    "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                    "complexty": cls.req_variety[Variety.BO],
                    "orderTag": unique_id,
                    "discqty": 0,
                }
            ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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
        price: float = 0.0,
        trigger: float = 0.0,
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
        elif not price:
            order_type = OrderType.MARKET
        elif not trigger:
            order_type = OrderType.LIMIT
        else:
            order_type = OrderType.SL

        json_data = [
            {
                "symbol_id": token,
                "exch": exchange,
                "trading_symbol": symbol,
                "price": price,
                "trigPrice": trigger,
                "qty": quantity,
                "transtype": cls._key_mapper(cls.req_side, side, "side"),
                "prctyp": cls.req_order_type[order_type],
                "pCode": cls._key_mapper(cls.req_product, product, "product"),
                "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                "orderTag": unique_id,
                "discqty": 0,
            }
        ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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

        json_data = [
            {
                "symbol_id": token,
                "exch": exchange,
                "trading_symbol": symbol,
                "price": 0,
                "trigPrice": 0,
                "qty": quantity,
                "transtype": cls._key_mapper(cls.req_side, side, "side"),
                "prctyp": cls.req_order_type[OrderType.MARKET],
                "pCode": cls._key_mapper(cls.req_product, product, "product"),
                "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                "orderTag": unique_id,
                "discqty": 0,
            }
        ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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

        json_data = [
            {
                "symbol_id": token,
                "exch": exchange,
                "trading_symbol": symbol,
                "price": price,
                "trigPrice": 0,
                "qty": quantity,
                "transtype": cls._key_mapper(cls.req_side, side, "side"),
                "prctyp": cls.req_order_type[OrderType.LIMIT],
                "pCode": cls._key_mapper(cls.req_product, product, "product"),
                "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                "orderTag": unique_id,
                "discqty": 0,
            }
        ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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

        json_data = [
            {
                "symbol_id": token,
                "exch": exchange,
                "trading_symbol": symbol,
                "price": price,
                "trigPrice": trigger,
                "qty": quantity,
                "transtype": cls._key_mapper(cls.req_side, side, "side"),
                "prctyp": cls.req_order_type[OrderType.SL],
                "pCode": cls._key_mapper(cls.req_product, product, "product"),
                "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                "orderTag": unique_id,
                "discqty": 0,
            }
        ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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

        json_data = [
            {
                "symbol_id": token,
                "exch": exchange,
                "trading_symbol": symbol,
                "price": 0,
                "trigPrice": trigger,
                "qty": quantity,
                "transtype": cls._key_mapper(cls.req_side, side, "side"),
                "prctyp": cls.req_order_type[OrderType.SLM],
                "pCode": cls._key_mapper(cls.req_product, product, "product"),
                "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                "orderTag": unique_id,
                "discqty": 0,
            }
        ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

    # FNO Order Functions

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
        elif not price:
            order_type = OrderType.MARKET
        elif not trigger:
            order_type = OrderType.LIMIT
        else:
            order_type = OrderType.SL

        json_data = [
            {
                "symbol_id": token,
                "exch": cls._key_mapper(cls.req_exchange, exchange, "exchange"),
                "trading_symbol": symbol,
                "price": price,
                "trigPrice": trigger,
                "qty": quantity,
                "transtype": cls._key_mapper(cls.req_side, side, "side"),
                "prctyp": cls.req_order_type[order_type],
                "pCode": cls._key_mapper(cls.req_product, product, "product"),
                "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                "orderTag": unique_id,
                "discqty": 0,
            }
        ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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

        json_data = [
            {
                "symbol_id": token,
                "exch": cls._key_mapper(cls.req_exchange, exchange, "exchange"),
                "trading_symbol": symbol,
                "price": 0,
                "trigPrice": 0,
                "qty": quantity,
                "transtype": cls._key_mapper(cls.req_side, side, "side"),
                "prctyp": cls.req_order_type[OrderType.MARKET],
                "pCode": cls._key_mapper(cls.req_product, product, "product"),
                "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                "orderTag": unique_id,
                "discqty": 0,
            }
        ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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
            cls.create_fno_tokens()

        detail = cls.fno_tokens[expiry][root][option]
        detail = detail.get(strike_price, None)

        if not detail:
            raise KeyError(f"StrikePrice: {strike_price} Does not Exist")

        symbol = detail["Symbol"]
        token = detail["Token"]

        json_data = [
            {
                "symbol_id": token,
                "exch": cls._key_mapper(cls.req_exchange, exchange, "exchange"),
                "trading_symbol": symbol,
                "price": price,
                "trigPrice": 0,
                "qty": quantity,
                "transtype": cls._key_mapper(cls.req_side, side, "side"),
                "prctyp": cls.req_order_type[OrderType.LIMIT],
                "pCode": cls._key_mapper(cls.req_product, product, "product"),
                "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                "orderTag": unique_id,
                "discqty": 0,
            }
        ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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

        json_data = [
            {
                "symbol_id": token,
                "exch": cls._key_mapper(cls.req_exchange, exchange, "exchange"),
                "trading_symbol": symbol,
                "price": price,
                "trigPrice": trigger,
                "qty": quantity,
                "transtype": cls._key_mapper(cls.req_side, side, "side"),
                "prctyp": cls.req_order_type[OrderType.SL],
                "pCode": cls._key_mapper(cls.req_product, product, "product"),
                "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                "orderTag": unique_id,
                "discqty": 0,
            }
        ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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

        json_data = [
            {
                "symbol_id": token,
                "exch": cls._key_mapper(cls.req_exchange, exchange, "exchange"),
                "trading_symbol": symbol,
                "price": 0,
                "trigPrice": trigger,
                "qty": quantity,
                "transtype": cls._key_mapper(cls.req_side, side, "side"),
                "prctyp": cls.req_order_type[OrderType.SLM],
                "pCode": cls._key_mapper(cls.req_product, product, "product"),
                "ret": cls._key_mapper(cls.req_validity, validity, "validity"),
                "complexty": cls._key_mapper(cls.req_variety, variety, "variety"),
                "orderTag": unique_id,
                "discqty": 0,
            }
        ]

        response = cls.fetch(
            method="POST",
            url=cls.urls["place_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="NOrdNo", headers=headers
        )

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
            list[dict]: Raw Broker Orderbook Response.
        """
        response = cls.fetch(
            method="GET",
            url=cls.urls["orderbook"],
            headers=headers["headers"],
        )
        try:
            return cls._json_parser(response)

        except ResponseError:
            return []

    @classmethod
    def fetch_raw_orderhistory(
        cls,
        order_id: str,
        headers: dict,
    ) -> list[dict]:
        """
        Fetch Raw History of an order.

        Paramters:
            order_id (str): id of the order.
            headers (dict): headers to send orderhistory request with.

        Returns:
            list[dict]: Raw Broker Order History Response.
        """
        json_data = {"nestOrderNumber": order_id}
        response = cls.fetch(
            method="POST",
            url=cls.urls["order_history"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._json_parser(response)

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

        try:
            info = cls._json_parser(response)
        except ResponseError:
            return []

        orders = []
        for order in info:
            detail = cls._orderbook_json_parser(order)
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
        order_id = str(order_id)
        for order in info:
            if order["Nstordno"] == order_id:
                detail = cls._orderbook_json_parser(order)
                return detail

        raise InputError({"This order_id does not exist."})

    @classmethod
    def fetch_orderhistory(
        cls,
        order_id: str,
        headers: dict,
    ) -> list[dict]:
        """
        Fetch History of an order.

        Paramters:
            order_id (str): id of the order.
            headers (dict): headers to send orderhistory request with.

        Returns:
            list: A list of dicitonaries containing order history using fenix Unified Order Response.
        """
        info = cls.fetch_raw_orderhistory(order_id=order_id, headers=headers)

        order_history = []
        for order in info:
            history = cls._orderhistory_json_parser(order)
            order_history.append(history)

        return order_history

    # Order Modification & Sq Off

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
            order_type (str | None, optional): Type of Order. defaults to None.
            validity (str | None, optional): Order validity Defaults to None.

        Returns:
            dict: fenix Unified Order Response.
        """
        order_history = cls.fetch_raw_orderhistory(order_id=order_id, headers=headers)
        order_info = order_history[0]

        json_data = {
            "nestOrderNumber": order_info["nestordernumber"],
            "exch": order_info["exchange"],
            "trading_symbol": order_info["Trsym"],
            "price": price or order_info["Prc"],
            "qty": quantity or order_info["Qty"],
            "trigPrice": trigger or order_info["trigger"],
            "transtype": order_info["Action"],
            "prctyp": (
                cls._key_mapper(cls.req_order_type, order_type, "order_type")
                if order_type
                else order_info["Ordtype"]
            ),
            "pCode": order_info["productcode"],
            "filledQuantity": order_info["filledShares"],
            "discqty": "0",
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["modify_order"],
            json=json_data,
            headers=headers["headers"],
        )
        _ = cls._json_parser(response)

        return cls.fetch_order(order_id=order_id, headers=headers)

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
        order = cls.fetch_order(order_id=order_id, headers=headers["headers"])

        json_data = {
            "exch": cls.req_exchange[order["exchange"]],
            "nestOrderNumber": order["id"],
            "trading_symbol": order["symbol"],
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["cancel_order"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="nestOrderNumber", headers=headers
        )

    @classmethod
    def sq_off_position(
        cls,
        symbol: str,
        token: int,
        exchange: str,
        quantity: int,
        headers: dict,
        product: str = Product.MIS,
    ) -> dict[Any, Any]:
        """
        Sqaure-Off Position.

        Args:
            symbol (str): Trading Symbol.
            token (int): Exchange Token.
            exchange (str): Exchange to place the order in.
            quantity (int): Order Quantity.
            headers (dict): headers to send order request with.
            product (str, optional): Order Product. Defaults to Product.MIS.

        Returns:
            dict[Any, Any]: fenix Unified Order Response.
        """
        json_data = {
            "exchSeg": cls.req_exchange[exchange],
            "pCode": cls.req_product[product],
            "netQty": quantity,
            "tockenNo": token,
            "symbol": symbol,
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["sqoff_position"],
            json=json_data,
            headers=headers["headers"],
        )

        return cls._create_order_parser(
            response=response, key_to_check="nestOrderNumber", headers=headers
        )

    @classmethod
    def exit_bo(
        cls,
        order_id: str,
        headers: dict,
    ) -> dict[Any, Any]:
        """
        Exit Bracket Order.

        Parameters:
            order_id (str): id of the order.
            headers (dict): headers to send order request with.

        Returns:
            dict[Any, Any]: fenix Unified Order Response.
        """
        json_data = {"nestOrderNumber": order_id}

        response = cls.fetch(
            method="POST",
            url=cls.urls["order_history"],
            json=json_data,
            headers=headers["headers"],
        )
        order_history = cls._json_parser(response)

        order = order_history[0]

        json_data = {
            "nestOrderNumber": order["nestordernumber"],
            "symbolOrderId": order["Trsym"],
            "status": order["Status"],
        }

        response = cls.fetch(
            method="POST",
            url=cls.urls["exit_bracket_order"],
            json=json_data,
            headers=headers["headers"],
        )
        response = cls._json_parser(response)

        return cls.fetch_order(order_id=order_id, headers=headers["headers"])

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
        json_data = {"ret": Validity.DAY}
        response = cls.fetch(
            method="POST",
            url=cls.urls["positions"],
            json=json_data,
            headers=headers["headers"],
        )

        try:
            return cls._json_parser(response)
        except ResponseError as e:
            if "no data" in str(e):
                return []

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
        json_data = {"ret": "NET"}
        response = cls.fetch(
            method="POST",
            url=cls.urls["positions"],
            json=json_data,
            headers=headers["headers"],
        )

        try:
            return cls._json_parser(response)
        except ResponseError as e:
            if "no data" in str(e):
                return []

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
        day_positions = cls.fetch_day_positions(headers=headers)
        net_positions = cls.fetch_net_positions(headers=headers)

        return day_positions + net_positions

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
        try:
            return cls._json_parser(response)
        except ResponseError as e:
            if "no data" in str(e):
                return []

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
        return cls._json_parser(response)

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
        response = cls._json_parser(response)

        profile = cls._profile_json_parser(response)
        return profile
