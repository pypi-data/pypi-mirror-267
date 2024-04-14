
def tlm_if(*args, **kwargs):
    from .impl.tlm_interface_decorator_impl import TlmInterfaceDecoratorImpl
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return TlmInterfaceDecoratorImpl([], {})(args[0])
    else:
        return TlmInterfaceDecoratorImpl(args, kwargs)

def req_fifo(*args, **kwargs):
    from .impl.req_fifo_decorator_impl import ReqFifoDecoratorImpl
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return ReqFifoDecoratorImpl([], {})(args[0])
    else:
        return ReqFifoDecoratorImpl(args, kwargs)

def rsp_fifo(*args, **kwargs):
    from .impl.rsp_fifo_decorator_impl import RspFifoDecoratorImpl
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return RspFifoDecoratorImpl([], {})(args[0])
    else:
        return RspFifoDecoratorImpl(args, kwargs)

def reqrsp_fifo(*args, **kwargs):
    pass

def req_mbox(*args, **kwargs):
    pass

def rsp_mbox(*args, **kwargs):
    pass

