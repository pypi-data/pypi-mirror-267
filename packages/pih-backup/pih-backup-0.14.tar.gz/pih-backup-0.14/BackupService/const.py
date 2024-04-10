import ipih

from pih import A
from pih.collections import RobocopyJobDescription
from pih.collections.service import ServiceDescription

NAME: str = "Backup"

VERSION: str = "0.14"


JOB_CONFIG_ALIAS: str = "job_config"


class ROBOCOPY:

    NAME: str = "robocopy"
    JOB_PARAMETER_NAME: str = "/job:"

    JOB_MAP: dict[str, dict[str, list[RobocopyJobDescription]]] | None = None

    class JOB_NAMES:

        MOVE_1C_BACKUPS: str = "move_1c_backups"
        POLIBASE_DATA: str = "polibase_data"
        POLIBASE_DATA_LIVE: str = "polibase_data_live"
        POLIBASE_FILES: str = "polibase_files"
        OMS: str = "oms"
        SCAN: str = "scan"
        HOMES: str = "homes"
        SHARES: str = "shares"
        FACADE: str = "facade"
        USER_DESKTOP: str = "user_desktop"
        VALENTA: str = A.CT.VALENTA.NAME
        DM: str = "DM"


HOST = A.CT_H.BACKUP_WORKER


class PATH:

    class JOB_CONFIG:

        FILE_NAME: str = A.PTH.add_extension(JOB_CONFIG_ALIAS, A.CT_F_E.JSON)
        DIRECTORY_NAME: str = "robocopy_config"
        DIRECTORY: str = A.PTH.join(
            A.PTH.FACADE.SERVICE(NAME),
            DIRECTORY_NAME,
        )

        VALUE: str = A.PTH.join(A.PTH.FACADE.SERVICE(NAME), FILE_NAME)


SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Backup service",
    host=HOST.NAME,
    commands=("robocopy_start_job", "robocopy_get_job_status_list"),
    version=VERSION,
    standalone_name="backup",
    use_standalone=True,
    parameters={JOB_CONFIG_ALIAS: PATH.JOB_CONFIG.VALUE},
)
