import ipih

from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

NAME: str = "PolibasePersonNotificationAutomation"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "0.15"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Polibase person notification automation service",
    host=HOST.NAME,
    use_standalone=True,
    version=VERSION,
    standalone_name="plb_ntfc_auto",
)
