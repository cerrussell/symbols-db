from symbols_db import logger

class Projects:

    def __init__(
        self,
        project_name=None,
        purl=None,
        github=None,
        commit_hash=None,
        executables_list=None,
    ):
        self.project_name = project_name
        self.purl = purl
        self.github = github
        self.commit_hash = commit_hash
        self.executables_list = executables_list
