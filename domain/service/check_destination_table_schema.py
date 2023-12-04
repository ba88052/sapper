from domain.domain_infra_port import DomainInfraPort

# 用於把要存的表欄位，跟目標表對齊

class CheckDestinationTableSchema():
    def __init__(self, domain_infra_respository = DomainInfraPort()):
        self.domain_infra_respository = domain_infra_respository
