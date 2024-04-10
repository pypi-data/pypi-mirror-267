import ipih

from pih.collections.service import ServiceDescription
from pih.consts.hosts import Hosts
from pih.consts import CONST

NAME: str = "PolibaseApp"

VERSION: str = "0.11"

HOST = Hosts.POLIBASE

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Polibase Application service",
    host=HOST.NAME,
    python_executable_path=CONST.UNKNOWN,
    run_from_system_account=True,
    standalone_name="plb_app",
    use_standalone=True,
    version=VERSION,
)
