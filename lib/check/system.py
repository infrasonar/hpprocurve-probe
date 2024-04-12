from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
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
    icf_sensor = state.get('hpicfSensorEntry', [])
    local_mem = state.get('hpLocalMemEntry', [])
    misc_stat = state.get('hpSwitchMiscStat', [])
    if not icf_sensor and not local_mem and not misc_stat:
        raise CheckException('SNMP data retrieval failed; '
                             'This could indicate an incorrect switch type')

    for item in local_mem:
        total = item.get('hpLocalMemTotalBytes')
        used = item.get('hpLocalMemAllocBytes')
        try:
            item['hpLocalMemPercentUsed'] = used / total * 100
        except Exception:
            pass

    return state
