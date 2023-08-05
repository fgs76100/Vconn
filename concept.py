"""
Two main principles:
    1. connect same naming input and output together among instances
    2. unconnect pins treats as IOs
"""
import dataclasses

INPUT = 0
OUTPUT = 1
INOUT = 2

@dataclasses.dataclass
class VestVerilogPort:
    name: str
    direction: int
    dataType: str

    @staticmethod
    def translate_direction(direction):
        if direction == INPUT:
            return "input"
        elif direction == OUTPUT:
            return "output"
        elif direction == INOUT:
            return "inout"
        else:
            raise ValueError()


@dataclasses.dataclass
class VestVerilogModule:
    instanceCounts = 0
    instances = []

    def __getitem__(self, index):
        """
        Let user could get attribute using: obj[index]
        """
        return index
    
    def __setitem__(self, index, value):
        """
        Let user could set attribute using: obj[index] = value
        """
        print(index, value)

    def __getattr__(self, name):
        """
        Let user could get attribute using: obj.name 
        """
        return name

    def __setattr__(self, name, value):
        """
        Let user could set attribute using: obj.name = value
        """
        print(name, value)

    def create_inst(self, module: "VestVerilogModule"=None):
        module.instanceCounts += 1
        inst = VestVerilogInstance(module)
        self.instances.append(inst)
        return inst
    
    def connect(self, *args, **kwargs):
        pass
    
    ...

class VestVerilogInstance:
    ...

class UNCONNECTED:
    ...

class TIE:
    ...

if 0:
    top = VestVerilogModule("top")
    m0 = VestVerilogModule("m0")
    m1 = VestVerilogModule("m1")
    m2 = VestVerilogModule("m2")
    x0 = VestVerilogModule("x0")

    top.create_input_port("rg_m0_bus", dataType="wire rg_bus_t")
    top.create_input_port("rg_m1_bus", dataType="wire rg_bus_t")
    pp_clk_i = top.create_input_port("pp_clk_i")
    yy_arvalid_o = top.create_output_port("yy_arvalid_o")

    i0 = top.create_inst(m0)
    i1 = top.create_inst(m1)
    i2 = top.create_inst(m2)
    x0 = top.create_inst(x0)

    top.connect(i0.arvalid_o, i1.xx_arvalid_i, x0.mon_arvalid_i, net="xx_mon_arvalid")
    top.connect(i0.clk_i, i1.xx_clk_i, x0.clk_i, new_port="sclk_gated",)
    top.connect("hreset_b_sync_sclk_gated", i0.reset_b_i, i1.xx_clk_i, x0.hresetb, new_port=True)
    top.connect("xreset_b_sync_sclk_gated", i0.xreset_b_i, i1.xreset_i, x0.xresetb, new_port=True)

    i0.arcache_o = UNCONNECTED()
    UNCONNECTED(i0.awache_o)

    i0.arsize_i = TIE(0x4)
    TIE(i0.awsize_i, 0x4)

    top.connect(pp_clk_i, i0.clk_i, i2.yy_clk_i)
    top.connect(yy_arvalid_o, i0.arvalid_o, i2.yy_arvalid_i)

    for rg_port in i0.iter_ports("rg*"):
        top.connect(f"rg_m0_bus.{rg_port.name}", rg_port)

    for rg_port in i1.iter_ports("rg*"):
        top.connect(f"rg_m1_bus.{rg_port.name}", rg_port)
