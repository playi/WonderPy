import threading
import WonderPy


def start(delegate_instance):
    WonderPy.core.wwBTLEMgr.WWBTLEManager(delegate_instance).run()


thread_local_data = threading.local()
