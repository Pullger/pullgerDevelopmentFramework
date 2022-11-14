import importlib
from django.conf import settings


def lib_reloader(lib_set):
    if settings.LIBRARY_RELOADING:
        for cur_library in lib_set:
            importlib.reload(cur_library)
