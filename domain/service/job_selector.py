from domain.service.job.customize_select_job import CustomizeSelect
from domain.service.job.flatten_json_job import FlattenJson
from domain.service.job.fuzzy_comparison_job import FuzzyComparison
from domain.service.job.update_checklist_table_for_anonymization_job import UpdateCheckListTableJob


class JobSelectorDomainService:
    def select(self, job_name, mission_id, mission_name, domain_infra_repository):
        if job_name == "flatten_json":
            return FlattenJson(
                mission_id=mission_id,
                mission_name=mission_name,
                domain_infra_repository=domain_infra_repository,
            )
        elif job_name == "customize_select":
            return CustomizeSelect(
                mission_id=mission_id,
                mission_name=mission_name,
                domain_infra_repository=domain_infra_repository,
            )
        elif job_name == "fuzzy_comparison":
            return FuzzyComparison(
                mission_id=mission_id,
                mission_name=mission_name,
                domain_infra_repository=domain_infra_repository,
            )
        elif job_name == "update_checklist_table_for_anonymization":
            return UpdateCheckListTableJob(
                mission_id=mission_id,
                mission_name=mission_name,
                domain_infra_repository=domain_infra_repository,
            )
        else:
            raise ValueError(f"Mission is not defind.")
