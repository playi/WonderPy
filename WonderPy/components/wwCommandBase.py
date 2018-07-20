from WonderPy.core.wwConstants import WWRobotConstants
from WonderPy.core import wwMain
from wwComponentBase import WWComponentBase
import time

_rc  = WWRobotConstants.RobotComponent
_rcv = WWRobotConstants.RobotComponentValues


# decorator
def do_not_call_within_connect_or_sensors(func):
    def wrapper(*args, **kwargs):
        in_on_sensors = getattr(wwMain.thread_local_data, 'in_on_sensors', False)
        in_on_connect = getattr(wwMain.thread_local_data, 'in_on_connect', False)
        if in_on_sensors or in_on_connect:
            raise RuntimeWarning("Do not block while within on_sensors() or on_connect().")
        return func(*args, **kwargs)
    return wrapper


class WWCommandBase(WWComponentBase):
    """
    not a whole lot here except some conveniences which might be used by multiple commands
    """

    def __init__(self, robot):
        super(WWCommandBase, self).__init__(robot)

    @staticmethod
    def _block_for_simple_timeout(time_for_command, timeout):
        if timeout == 0:
            return

        if timeout:
            time.sleep(min(timeout, time_for_command))
        else:
            time.sleep(time_for_command)
