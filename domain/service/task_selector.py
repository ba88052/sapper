
from domain.service.task.customize_select_task import CustomizeSelect
from domain.service.task.flatten_json_task import FlattenJson

class TaskSelectorDomainService:
    def select(self, task_name, mission_id, mission_name, domain_infra_respository):
        if task_name == "flatten_json":
            return FlattenJson(mission_id=mission_id, mission_name=mission_name, domain_infra_respository=domain_infra_respository)
        elif task_name == "customize_select":
            return CustomizeSelect(mission_id=mission_id, mission_name=mission_name, domain_infra_respository=domain_infra_respository)
        else:
            raise ValueError(f"Mission is not defind.")
