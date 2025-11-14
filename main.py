from libprobe.probe import Probe
from lib.check.system import CheckSystem
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckSystem,
    )

    probe = Probe("hpprocurve", version, checks)

    probe.start()
