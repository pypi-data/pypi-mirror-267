import ipih

from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

NAME: str = "PolibasePersonNotificationAnswer"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "0.13"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Polibase Person Notification Answer service",
    host=HOST.NAME,
    use_standalone=True,
    version=VERSION,
    standalone_name="plb_ntf_answ",
)
