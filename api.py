from pullgerMultiSessionManager import apiMSM
from pullgerSquirrel.connectors.selenium import connector
from django.apps import apps


def sessions_add():
    msm_app = apps.get_app_config('pullgerDevelopmentFramework')
    msm_app.development_framework.session_add()

    # msm_app.development_framework.taskStack.delete_task(uuid_task)
    # uuid_session = api.add_new_session(conn=connector.chrome.standard)
    # session = api.get_session_by_uuid(uuid_session)

    pass


def domain_get_list():
    pass


def domain_connect():
    pass


def domain_add():
    pass
