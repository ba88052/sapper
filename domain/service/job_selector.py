from domain.service.job.customize_select_job import CustomizeSelect
from domain.service.job.flatten_json_job import FlattenJson


class JobSelectorDomainService:
    def select(self, job_name, mission_id, mission_name, domain_infra_respository):
        if job_name == "flatten_json":
            return FlattenJson(
                mission_id=mission_id,
                mission_name=mission_name,
                domain_infra_respository=domain_infra_respository,
            )
        elif job_name == "customize_select":
            return CustomizeSelect(
                mission_id=mission_id,
                mission_name=mission_name,
                domain_infra_respository=domain_infra_respository,
            )
        else:
            raise ValueError(f"Mission is not defind.")
