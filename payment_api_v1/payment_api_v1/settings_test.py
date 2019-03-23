from payment_api_v1.settings import *


class MigrationDisabler:
    """
    Disable all migrations in all apps when running tests.

    Django's test runner will instead create the needed tables in sqlite
    using the current model configurations at runtime.
    """

    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        pass


MIGRATION_MODULES = MigrationDisabler()

CELERY_ALWAYS_EAGER = True
