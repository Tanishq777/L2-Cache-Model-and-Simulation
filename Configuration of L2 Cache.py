import m5
from m5.objects import *
from caches import *
from optparse import OptionParser

from m5.util import addToPath
addToPath('../')
from common import Options

process = Process()
parser = OptionParser()   # For --help command and cmd args
#Options.addCommonOptions(parser)
Options.addSEOptions(parser)
parser.add_option('--l1i_size', help="L1 instruction cache size")
parser.add_option('--l1d_size', help="L1 data cache size")
parser.add_option('--l2_size', help="Unified L2 cache size")
(options, args) = parser.parse_args()

#multiprocesses = []
inputs = []
outputs = []
errouts = []
pargs = []

workloads = options.cmd.split(';')
if options.input != "":
    inputs = options.input.split(';')
if options.output != "":
    outputs = options.output.split(';')
if options.errout != "":
    errouts = options.errout.split(';')
if options.options != "":
    pargs = options.options.split(';')

idx = 0
for wrkld in workloads:
    process = Process(pid = 100 + idx)
    process.executable = wrkld
    process.cwd = os.getcwd()

    if options.env:
        with open(options.env, 'r') as f:
            process.env = [line.rstrip() for line in f]

    if len(pargs) > idx:
        process.cmd = [wrkld] + pargs[idx].split()
    else:
        process.cmd = [wrkld]

#parser = OptionParser()   # For --help command and cmd args
#Options.addCommonOptions(parser)
#Options.addSEOptions(parser)
#parser.add_option('--l1i_size', help="L1 instruction cache size")
#parser.add_option('--l1d_size', help="L1 data cache size")
#parser.add_option('--l2_size', help="Unified L2 cache size")
#(options, args) = parser.parse_args()
#gem5 built on SimObject type, most of the components :CPUs, caches, memory controllers, buses, etc. gem5 exports all of these objects from their C++ implementation to python. Thus, from the python configuration script you can create any SimObject, set its parameters, and specify the interactions between SimObjects.

system = System()   # A SimObject, Parent of all systems, contain various functions

# CLOCK PART
system.clk_domain = SrcClockDomain()  # creating clock instance
system.clk_domain.clock = '1GHz'  #   setting clock freq. of system
system.clk_domain.voltage_domain = VoltageDomain()  # system power to default

# MEMORY PART
system.mem_mode = 'timing' # 'mode' of memory simulation ('timing' common mode here)
# MinorCPU (for in-order), Deriv03CPU (for out-of-order, but requires separate instructions and data caches).
system.mem_ranges = [AddrRange('512MB')]  # setting memory size

# CPU PART
system.cpu = TimingSimpleCPU() #timing(most simple) based CPU,CPI=1 except memory requests.

# BUS PART
system.membus = SystemXBar() # system-wide memory bus

# L1 CACHES PART
system.cpu.icache = L1ICache(options)  # Creating L1 Caches
system.cpu.dcache = L1DCache(options)
system.cpu.icache.connectCPU(system.cpu) # connect the caches to the CPU ports
system.cpu.dcache.connectCPU(system.cpu)

# L1 and L2 don't connect directly, as L2 has only one port so we need a bus in-between
# CREATING L2 BUS
system.l2bus = L2XBar()
system.cpu.icache.connectBus(system.l2bus) # L1 caches connecting to L2 bus
system.cpu.dcache.connectBus(system.l2bus)

# L2 CACHE PART
system.l2cache = L2Cache(options)   # creating L2 Cache
system.l2cache.connectCPUSideBus(system.l2bus)  # connecting to l2 bus and memory bus
system.l2cache.connectMemSideBus(system.membus)

# CPU CACHE PORTS  (Already connected above)
#system.cpu.icache_port = system.membus.slave   # directly connecting memory L and D
#system.cpu.dcache_port = system.membus.slave   # ports to mem_bus as no caches exist in system

#### Note : each memory object have two ports master and slave, 
#### connection by (either way is fine) : memobject1.master = memobject2.slave  


# PORTS AND CONNECTIONS
# Create I/O Controller on CPU and connect to memory bus + special port for read and write memory and connect to memory bus
# connectinf I/O and interrupt port to memory bus is x86 requirement (don't need in other ISAs).
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

# MEMORY CONTROLLER
system.mem_ctrl = DDR3_1600_8x8() #creating DDR3 controller responsible for entire memory range of syst.
system.mem_ctrl.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# INSTANTIATION COMPLETE OF SYSTEM
# Process for CPU to execute
#process = Process()   # Creating process, a SimObject
#process.cmd = options   # ['tests/test-progs/hello/bin/x86/linux/hello'] 
system.cpu.workload = process
system.cpu.createThreads()

# INSTANTIATE THE SYSTEM
root = Root(full_system = False, system = system) # creating Root object
m5.instantiate() # instantiate simulation, this process goes to all SimObjects in python and convert them in c++ 

# Kick-Off Simulation
print("Beginning simulation!")
exit_event = m5.simulate()
# After simulation, inspecting state of the system
print('Exiting @ tick {} because {}'.format(m5.curTick(),exit_event.getCause()))

### END ###

