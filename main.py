from libprobe.probe import Probe
from lib.check.controller import check_controller
from lib.check.eventlog import check_eventlog
from lib.check.storage import check_storage
from lib.check.system import check_system
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'controller': check_controller,
        'eventlog': check_eventlog,
        'storage': check_storage,
        'system': check_system,
    }

    probe = Probe("hpprocurve", version, checks)

    probe.start()
