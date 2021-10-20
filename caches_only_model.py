# gem5 have two distinct subsystem to model on-chip cache: "Classic caches" and "Ruby" ruby is designed for cache coherence, classic has simple and inflexible coherence
# choose based upon coherence priority

from m5.objects import Cache    # cache is as SimObject 

class L1Cache(Cache): # extending BaseCache Class
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 2
    mshrs = 4
    tgts_per_mshr = 20
    
    def __init__(self,options=None):
        super(L1Cache,self).__init__()
        pass
    def connectCPU(self,cpu):
        raise NotImplementedError
    def connectBus(self,bus):
        self.mem_side = bus.slave


class L1ICache(L1Cache):    # sub-classes of L1Cache
    size = '16kB'
    def connectCPU(self, cpu):
        self.cpu_side = cpu.icache_port
    def __init__(self,options=None):
        super(L1ICache,self).__init__(options)
        if not options or not options.l1i_size:
            return
        self.size = options.l1i_size

class L1DCache(L1Cache):
    size = '16kB'
    def connectCPU(self, cpu):
        self.cpu_side = cpu.dcache_port
    def __init__(self,options=None):
        super(L1DCache,self).__init__(options)
        if not options or not options.l1d_size:
            return
        self.size = options.l1d_size

class L2Cache(Cache):  # extending BaseCache class again
    size = '256kB'
    assoc = 4
    tag_latency = 20
    data_latency = 10
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
    
    def __init__(self,options=None):
        super(L2Cache,self).__init__()
        if not options or not options.l2_size:
            return
        self.size = options.l2_size
        self.assoc = options.assoc
    def connectCPUSideBus(self, bus):
        self.cpu_side = bus.master
    def connectMemSideBus(self, bus):
        self.mem_side = bus.slave
        

        
