import sys

from src.main.python.SocialEcosystemAnalyser.database.database_management import \
    DatabaseManagement


class ExitProgram:
    @staticmethod
    def exit_program(status_code: int = 0, exception: Exception = None):
        """ Exit the program"""
        db = DatabaseManagement()
        db.__del__()

        if exception is not None:
            raise exception

        sys.exit(status_code)
