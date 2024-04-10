import ipih


from pih.consts import CONST
from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

NAME: str = "PolibaseDatabase"

HOST = Hosts.POLIBASE

VERSION: str = "0.15"


SD: ServiceDescription = ServiceDescription(
    name=NAME,
    host=HOST.NAME,
    description="Polibase database api",
    commands=("create_polibase_database_backup",),
    version=VERSION,
    use_standalone=True,
    standalone_name="plb_db",
    run_from_system_account=True,
    python_executable_path=CONST.UNKNOWN,
)
