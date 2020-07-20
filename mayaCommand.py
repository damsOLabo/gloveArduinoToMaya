import maya.cmds as cmds
import maya.mel as mel

port_id = "7777"
host_adress = "127.0.0.1:{0}".format(port_id)

proc_name="portData"

initialized = False
driven = "hand_0"
finger_1 = ["joint1", "joint2", "joint3"]
# Our mel global proc.
melproc = """
global proc %s(string $arg){
    python(("%s(\\"" + $arg + "\\")"));
}
"""%(proc_name, proc_name)
mel.eval(melproc)

def open_port():
    # Open the commandPort. 
    # The 'prefix' argument string is calling to the defined
    # mel script above (which then calls to our Python function 
    # of the same name):
    cmds.commandPort(
        name=host_adress,
        echoOutput=False,
        noreturn=False,
        prefix=proc_name,
        returnNumCommands=True
    )
    cmds.commandPort(
        name=port_id,
        echoOutput=False,
        noreturn=False,
        prefix=proc_name,
        returnNumCommands=True
    )

# Our Python function that can be changed to do whatever we want:
def portData(arg):
    """
    Read the 'serial' data passed in from the commandPort
    """
    print "Recieved!: ", arg
    

    if "ypr" in arg and "overflow" not in arg and "nan" not in arg:
        parts = arg.split("\t")[1:]
        values = parts[:3]

        values_offsets = parts[3:-1]

        create_key = int(parts[-2])
        finger1_angle = int(parts[-1])
        
        for fing in finger_1:
            cmds.setAttr(fing + ".rz", - finger1_angle/3)
            
        offset_x = float(values_offsets[2])
        offset_y = -float(values_offsets[0])
        offset_z = float(values_offsets[1])
        
        cmds.xform(
            driven,
            ws=False,
            ro=[
                float(values[2]) - offset_x,
                -float(values[0])  - offset_y,
                float(values[1]) - offset_z
            ]
        )
        
        if create_key:
            cmds.setKeyframe(driven + ".r")

open_port()
