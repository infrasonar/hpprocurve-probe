from asyncsnmplib.mib.mib_index import MIB_INDEX
from libprobe.asset import Asset
from ..utils import get_data

QUERIES = (
    MIB_INDEX['CPQHLTH-MIB']['cpqHeFltTolFanEntry'],
    MIB_INDEX['CPQHLTH-MIB']['cpqHeFltTolPowerSupplyEntry'],
    MIB_INDEX['CPQHLTH-MIB']['cpqHeResMem2ModuleEntry'],
    MIB_INDEX['CPQHLTH-MIB']['cpqHeResMemModuleEntry'],
    MIB_INDEX['CPQHLTH-MIB']['cpqHeResilientMemory'],
    MIB_INDEX['CPQHLTH-MIB']['cpqHeTemperatureEntry'],
    MIB_INDEX['CPQHOST-MIB']['cpqHoFileSysEntry'],
    MIB_INDEX['CPQSTDEQ-MIB']['cpqSeCpuEntry'],
)


def on_powersupplyentry(item: dict):
    total = item.get('cpqHeFltTolPowerSupplyCapacityMaximum')
    used = item.get('cpqHeFltTolPowerSupplyCapacityUsed')
    try:
        item['cpqHeFltTolPowerSupplyCapacityUsedPercent'] = 100 * used / total
    except Exception:
        pass


def on_hofilesysentry(item: dict):
    # when no such information available -1 value is returned (CPQHOST-MIB)
    total = item.pop('cpqHoFileSysSpaceTotal', -1)
    if total > 0:
        item['cpqHoFileSysSpaceTotal'] = total * 1024 * 1024
    used = item.pop('cpqHoFileSysSpaceUsed', -1)
    if used > 0:
        item['cpqHoFileSysSpaceUsed'] = used * 1024 * 1024
    percentused = item.pop('cpqHoFileSysPercentSpaceUsed', -1)
    if percentused >= 0:
        item['cpqHoFileSysPercentSpaceUsed'] = percentused
    return item


async def check_system(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    state = await get_data(asset, asset_config, check_config, QUERIES)
    for item in state.get('cpqHeFltTolPowerSupplyEntry', []):
        on_powersupplyentry(item)
    for item in state.get('cpqHoFileSysEntry', []):
        on_hofilesysentry(item)
    return state
