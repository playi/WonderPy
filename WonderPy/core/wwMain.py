import threading
import WonderPy


def start(delegate_instance, arguments=None):
    WonderPy.core.wwBTLEMgr.WWBTLEManager(delegate_instance, arguments).run()


thread_local_data = threading.local()
