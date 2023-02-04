from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from ..utils import get_data

QUERIES = (
    MIB_INDEX['HP-ICF-CHASSIS']['hpicfSensorEntry'],
    MIB_INDEX['NETSWITCH-MIB']['hpLocalMemEntry'],
    MIB_INDEX['STATISTICS-MIB']['hpSwitchMiscStat'],
)


async def check_system(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    state = await get_data(asset, asset_config, check_config, QUERIES)
    for item in state.get('hpLocalMemEntry', []):
        total = item.get('hpLocalMemTotalBytes')
        used = item.get('hpLocalMemAllocBytes')
        try:
            item['hpLocalMemPercentUsed'] = used / total * 100
        except Exception:
            pass

    return state
