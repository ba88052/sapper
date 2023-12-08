class Task:
    def execute():
        """
        用來規範子任務class都要有def execute，不然會報錯
        """
        raise ValueError(f"execute function is not defind.")
