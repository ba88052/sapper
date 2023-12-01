
from domain.service.task.customize_select_task import CallSeonFraudApiTask

class TaskSelectorDomainService:
    def select(self, task_name, mission_id, mission_name, domain_infra_respository):
        if task_name == "call_seon_fraud_api":
            return CallSeonFraudApiTask(mission_id=mission_id, mission_name=mission_name, domain_infra_respository=domain_infra_respository)
        # elif mission == "gdt_individual_business_financial_spider":
            # return GdtIndividualBusinessFinancialCleaner()
        else:
            raise ValueError(f"Mission is not defind.")
