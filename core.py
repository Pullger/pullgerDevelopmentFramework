import uuid

import pullgerSquirrel
from pullgerInternalControl import pIC_pMSM
from pullgerInternalControl import pIC_pD

from pullgerMultiSessionManager import apiMSM as pMSM_API
from pullgerSquirrel.connectors.selenium import connector
from django.apps import apps


class DevelopmentFrameworkManager:
    __slots__ = (
        '_sessionsList', 'session_default'
    )

    class _Session:
        __slots__ = ('session', 'uuid_session')

        def __init__(self, session, uuid_session):
            self.session = session
            self.uuid_session = uuid_session

    def __init__(self):
        self._sessionsList = []
        self.session_default = None

    def session_add(self):
        uuid_session = pMSM_API.add_new_session(conn=connector.chrome.standard)
        session = pMSM_API.get_session_by_uuid(uuid_session)

        session_element = self._Session(session, uuid_session)
        self._sessionsList.append(session_element)
        if self.session_default is None:
            self.session_default = session_element
