from fenix.symphony import symphony


class vpc(symphony):
    """
    VPC fenix Broker Class

    Returns:
        fenix.vpc: fenix VPC Broker Object
    """

    # Market Data Dictonaries

    id = "vpc"

    # Base URLs

    base_urls = {
        "api_documentation_url": "http://122.160.19.15:3000/doc/interactive",
        "market_data_url": "http://122.160.19.15:3000/apimarketdata/instruments/master",
        "base_url": "http://122.160.19.15:3000/interactive",
        "access_token": "http://122.160.19.15:3000/interactive/user/session",
    }
