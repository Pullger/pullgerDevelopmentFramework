from django.test import TestCase
# from django.apps import apps
# from pullgerMultiSessionManager import api, core
from pullgerDevelopmentFramework import api


class Unit_001_GeneralOperation(TestCase):
    def test_001_00_00_get_page(self):

        # for i in range(2):
        #     if i == 0:
        #         uuid_session = UnitOperations.add_new_session_selenium_standard(self)
        #     elif i == 1:
        #         uuid_session = UnitOperations.add_new_session_selenium_headless(self)

        api.sessions_add()

        # uuid_session = UnitOperations.add_new_session_selenium_standard(self)

        pass