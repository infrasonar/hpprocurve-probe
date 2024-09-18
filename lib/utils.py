import logging
from asyncsnmplib.utils import InvalidConfigException, snmp_queries
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from typing import Tuple
from . import DOCS_URL


async def get_data(
        asset: Asset,
        asset_config: dict,
        check_config: dict,
        queries: Tuple[Tuple[int], ...]) -> dict:
    address = check_config.get('address')
    if address is None:
        address = asset.name

    try:
        state = await snmp_queries(address, asset_config, queries)
    except InvalidConfigException as e:
        msg = str(e) or type(e).__name__
        logging.error(f'Invalid config. Exception: {msg}')
        raise CheckException(
            'Invalid config. Please refer to the following documentation'
            f' for detailed instructions: <{DOCS_URL}>')
    return state
