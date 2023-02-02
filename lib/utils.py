from asyncsnmplib.exceptions import SnmpNoConnection, SnmpNoAuthParams
from asyncsnmplib.utils import InvalidConfigException, snmp_queries
from libprobe.asset import Asset
from libprobe.exceptions import CheckException, IgnoreResultException


async def get_data(
        asset: Asset,
        asset_config: dict,
        check_config: dict,
        queries: dict) -> dict:
    address = check_config.get('address')
    if address is None:
        address = asset.name
    try:
        state = await snmp_queries(address, asset_config, queries)
    except SnmpNoConnection:
        raise CheckException('unable to connect')
    except (InvalidConfigException, SnmpNoAuthParams):
        raise IgnoreResultException
    except Exception:
        raise
    else:
        return state
