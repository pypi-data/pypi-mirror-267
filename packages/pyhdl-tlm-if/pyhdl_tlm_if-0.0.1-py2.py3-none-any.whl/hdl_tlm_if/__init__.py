
from .decorators import *
from .impl.stream_rgy import StreamRgy

# Ensure everything has registered
async def initialize():
    rgy = StreamRgy.inst()
    await rgy.initialize()

def get_interfaces():
    rgy = StreamRgy.inst()
    return rgy.get_interfaces()

async def connect_if(ifc, ifc_path, match=False):
    rgy = StreamRgy.inst()
    await rgy.connect_if(ifc, ifc_path, match)