import ipih

from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

NAME: str = "PolibasePersonAnswerAutomation"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "0.14"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Polibase person answer automation service",
    host=HOST.NAME,
    use_standalone=True,
    version=VERSION,
    standalone_name="plb_answ_auto",
)
