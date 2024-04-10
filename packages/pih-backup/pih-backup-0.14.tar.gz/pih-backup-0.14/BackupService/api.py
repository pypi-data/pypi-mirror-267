import ipih

from pih import A, PIHThread
from pih.tools import while_not_do, j, nns, lw, nnd
from BackupService.const import ROBOCOPY as RBK, PATH
from pih.collections import RobocopyJobDescription, RobocopyJobItem, RobocopyJobStatus

from typing import Callable
from subprocess import CompletedProcess


class BackupApi:
    def start_robocopy_job(self, value: RobocopyJobItem, force: bool = False) -> bool:
        def internal_start_robocopy_job(
            job_item: RobocopyJobItem, force: bool = False
        ) -> bool:
            def run_robocopy_job(job_item: RobocopyJobItem) -> None:
                job_name: Callable[[], str] = lambda: self.get_job_name(
                    name, source, destination
                )
                source: str = nns(job_item.source)
                destination: str = nns(job_item.destination)
                name: str = nns(job_item.name)
                job_path: str = self.get_job_path(name, source, destination)
                job_status: RobocopyJobStatus | None = None
                if not job_item.live:
                    job_status = self.get_job_status(name, source, destination)
                    job_status.active = True
                    self.save_job_status(job_status)
                    A.E.backup_robocopy_job_was_started(job_name(), job_status)
                process: CompletedProcess = A.EXC.execute(
                    A.EXC.create_command_for_psexec(
                        (RBK.NAME, RBK.JOB_PARAMETER_NAME + job_path),
                        job_item.host,
                        interactive=not job_item.live,
                        run_from_system_account=job_item.run_from_system_account,
                        run_with_elevetion=job_item.run_with_elevetion,
                    ),
                    show_output=True,
                    capture_output=False,
                )
                last_status: int = -1
                if job_item.live:
                    pid: int = process.returncode
                    job_status = self.get_job_status(name, source, destination)
                    job_status.live = True
                    job_status.active = True
                    job_status.pid = pid
                    self.save_job_status(job_status)
                    A.E.backup_robocopy_job_was_started(job_name(), job_status)
                    while_not_do(
                        lambda: not A.EXC.process_is_exists(pid, job_item.host),
                        sleep_time=5,
                    )
                else:
                    last_status = process.returncode
                job_status = self.get_job_status(name, source, destination)
                job_status.active = False
                job_status.pid = -1
                job_status.last_created = A.D.now_to_string(A.CT.ISO_DATETIME_FORMAT)
                job_status.last_status = last_status
                self.save_job_status(job_status)
                A.E.backup_robocopy_job_was_completed(job_name(), job_status)

            #
            job_status: RobocopyJobStatus = self.get_job_status(
                nns(job_item.name), nns(job_item.source), nns(job_item.destination)
            )
            if not job_status.active or force:
                job_status.active = True
                self.save_job_status(job_status)
                PIHThread(run_robocopy_job, args=(job_item,))
                return True
            return False

        return internal_start_robocopy_job(value, force)

    @staticmethod
    def get_job_list() -> list[RobocopyJobItem]:
        rjm: dict[str, dict[str, list[RobocopyJobDescription]]] = nnd(RBK.JOB_MAP)
        result: list[RobocopyJobItem] = []
        for source in rjm:
            for destination in rjm[source]:
                for job_description in rjm[source][destination]:
                    job_item: RobocopyJobItem = A.D.fill_data_from_source(
                        RobocopyJobItem(), job_description
                    )
                    job_item.source = source
                    job_item.destination = destination
                    job_item.name = lw(job_item.name)
                    result.append(job_item)
        return result

    @staticmethod
    def get_job_name(name: str, source: str, destination: str) -> str:
        result: str = ""
        if not A.D.is_empty(name):
            result += name
            if not A.D.is_empty(source):
                result += j((":", source))
                if not A.D.is_empty(destination):
                    result += j((A.CT_V.ARROW, destination))
        return result

    @staticmethod
    def get_job_status(name: str, source: str, destination: str) -> RobocopyJobStatus:
        return A.R_DS.value(
            A.D_F.BACKUP.job_status_name(name, source, destination), RobocopyJobStatus
        ).data or RobocopyJobStatus(name, source, destination)

    @staticmethod
    def save_job_status(value: RobocopyJobStatus) -> bool:
        return A.A_DS.value(
            value,
            A.D_F.BACKUP.job_status_name(
                nns(value.name), nns(value.source), nns(value.destination)
            ),
        )

    @staticmethod
    def get_job_path(name: str, source: str, destination: str) -> str:
        return A.PTH.join(
            PATH.JOB_CONFIG.DIRECTORY, j((source, destination), "-"), name
        )