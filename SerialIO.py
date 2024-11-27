import serial
import struct
import time

idle_timer = 600
class VesselQuaternion:
    def __init__(self):
        self.w = 0.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

class VesselData:
    def __init__(self):
        self.id = 0 #byte
        self.AP = 0.0
        self.PE = 0.0
        self.SemiMajorAxis = 0.0
        self.SemiMinorAxis = 0.0
        self.VVI = 0.0
        self.e = 0.0
        self.inc = 0.0
        self.G = 0.0
        self.TAp = 0.0
        self.TPe = 0.0
        self.TrueAnomaly = 0.0
        self.Density = 0.0
        self.period = 0.0
        self.RAlt = 0.0
        self.Alt = 0.0
        self.Vsurf = 0.0
        self.Lat = 0.0
        self.Lon = 0.0
        self.LiquidFuelTot = 0.0
        self.LiquidFuel = 0.0
        self.OxidizerTot = 0.0
        self.Oxidizer = 0.0
        self.EChargeTot = 0.0
        self.ECharge = 0.0
        self.MonoPropTot = 0.0
        self.MonoProp = 0.0
        self.IntakeAirTot = 0.0
        self.IntakeAir = 0.0
        self.SolidFuelTot = 0.0
        self.SolidFuel = 0.0
        self.XenonGasTot = 0.0
        self.XenonGas = 0.0
        self.LiquidFuelTotS = 0.0
        self.LiquidFuelS = 0.0
        self.OxidizerTotS = 0.0
        self.OxidizerS = 0.0
        self.MissionTime = 0
        self.deltaTime = 0.0
        self.VOrbit = 0.0
        self.MNTime = 0
        self.MNDeltaV = 0.0
        self.Pitch = 0.0
        self.Roll = 0.0
        self.Heading = 0.0
        self.ActionGroups = 0
        self.SOINumber = 0 #byte
        self.MaxOverHeat = 0 #byte
        self.MachNumber = 0.0
        self.IAS = 0.0
        self.CurrentStage = 0 #byte
        self.TotalStage = 0 #byte
        self.TargetDist = 0.0
        self.TargetV = 0.0
        self.NavballSASMode = 0 #byte
        self.ProgradePitch = 0
        self.ProgradeHeading = 0
        self.ManeuverPitch = 0
        self.ManeuverHeading = 0
        self.TargetPitch = 0
        self.TargetHeading = 0
        self.NormalHeading = 0
        self.VQuaternion = VesselQuaternion()

class HandShakePacket:
    def __init__(self):
        self.id = 0
        self.M1 = 3
        self.M2 = 1
        self.M3 = 4

HPacket = HandShakePacket()
VData = VesselData()
Connected = False

ser = serial.Serial(
    port='/dev/ttyS0', 
    baudrate=38400, 
    parity=serial.PARITY_NONE, 
    stopbits=serial.STOPBITS_ONE, 
    bytesize=serial.EIGHTBITS, 
    timeout=1 
)

rx_len = 0
buffer = bytearray(256)  # Buffer for temporary storage and parsing
struct_size = 0
rx_array_idx = 1  # Index for RX parsing buffer
calc_cs = 0  # Calculated checksum
id = 0
address = None
VesselData_format = '=B f f f f f f f f l l f f l f f f f f f f f f f f f f f f f f f f f f f f f f f f H B B f f B B f f f h h h h h h h f f f f'
HandShakePacket_format = '=B B B B'
final_data = None

struct_size = struct.calcsize(HandShakePacket_format)  # Example: size of Handshake struct
struct_size = struct.calcsize(VesselData_format)  # Example: size of VesselData struct

def KSPBoardReceiveData():
    global rx_len, buffer, struct_size, rx_array_idx, calc_cs, id, address, VesselData_format, HandShakePacket_format, final_data

    if rx_len == 0 and ser.in_waiting > 3:
        while ser.read(1) != b'\xBE':
            if ser.in_waiting == 0:
                return False
        
        if ser.read(1) == b'\xEF':
            rx_len = ord(ser.read(1))
            id = ord(ser.read(1))
            rx_array_idx = 1
            
            # Set struct size and address based on id
            if id == 0:
                address = struct.Struct(HandShakePacket_format)
            elif id == 1:
                address = struct.Struct(VesselData_format)
            else:
                return False
            
            # Validate structure size
            if rx_len != struct_size:
                rx_len = 0
                return False
    
    if rx_len != 0:
        while ser.in_waiting and rx_array_idx <= rx_len:
            buffer[rx_array_idx] = ord(ser.read(1))
            rx_array_idx += 1
        buffer[0] = id

        if rx_len == (rx_array_idx - 1):
            # Calculate checksum
            calc_cs = rx_len
            for i in range(rx_len):
                calc_cs ^= buffer[i]
            
            # Verify checksum
            if calc_cs == buffer[rx_array_idx - 1]:
                # Parse buffer into struct fields
                final_data = address.unpack(buffer[1:struct_size + 1])
                rx_len = 0
                rx_array_idx = 1
                return final_data
            else:
                # Checksum failed, reset variables
                rx_len = 0
                rx_array_idx = 1
                return False
    return False

def KSPBoardSendData(address, len):
   checksum = len
   ser.write(bytes([0xBE, 0xEF, len]))

   for i in range(len):
       byte = address[i]
       checksum ^= byte
       ser.write(bytes([byte]))

   ser.write(bytes([checksum]))

def size_of(package):
    return struct.calcsize(package)

def input():
    global Connected, returnValue, id, final_data
    start_time = time.time()
    now = (time.time() - start_time) * 1000

    if(KSPBoardReceiveData()):
        dead_time_old = now
        returnValue = id
        if (id == 0):
            KSPBoardSendData(HPacket, size_of(HPacket))
            
        elif (id == 1):
            VData.id = final_data[0]
            VData.AP = final_data[1]
            VData.PE = final_data[2]
            VData.SemiMajorAxis = final_data[3]
            VData.SemiMinorAxis = final_data[4]
            VData.VVI = final_data[5]
            VData.e = final_data[6]
            VData.inc = final_data[7]
            VData.G = final_data[8]
            VData.TAp = final_data[9]
            VData.TPe = final_data[10]
            VData.TrueAnomaly = final_data[11]
            VData.Density = final_data[12]
            VData.period = final_data[13]
            VData.RAlt = final_data[14]
            VData.Alt = final_data[15]
            VData.Vsurf = final_data[16]
            VData.Lat = final_data[17]
            VData.Lon = final_data[18]
            VData.LiquidFuelTot = final_data[19]
            VData.LiquidFuel = final_data[20]
            VData.OxidizerTot = final_data[21]
            VData.Oxidizer = final_data[22]
            VData.EChargeTot = final_data[23]
            VData.ECharge = final_data[24]
            VData.MonoPropTot = final_data[25]
            VData.MonoProp = final_data[26]
            VData.IntakeAirTot = final_data[27]
            VData.IntakeAir = final_data[28]
            VData.SolidFuelTot = final_data[29]
            VData.SolidFuel = final_data[30]
            VData.XenonGasTot = final_data[31]
            VData.XenonGas = final_data[32]
            VData.LiquidFuelTotS = final_data[33]
            VData.LiquidFuelS = final_data[34]
            VData.OxidizerTotS = final_data[35]
            VData.OxidizerS = final_data[36]
            VData.MissionTime = final_data[37]
            VData.deltaTime = final_data[38]
            VData.VOrbit = final_data[39]
            VData.MNTime = final_data[40]
            VData.MNDeltaV = final_data[41]
            VData.Pitch = final_data[42]
            VData.Roll = final_data[43]
            VData.Heading = final_data[44]
            VData.ActionGroups = final_data[45]
            VData.SOINumber = final_data[46]
            VData.MaxOverHeat = final_data[47]
            VData.MachNumber = final_data[48]
            VData.IAS = final_data[49]
            VData.CurrentStage = final_data[50]
            VData.TotalStage = final_data[51]
            VData.TargetDist = final_data[52]
            VData.TargetV = final_data[53]
            VData.NavballSASMode = final_data[54]
            VData.ProgradePitch = final_data[55]
            VData.ProgradeHeading = final_data[56]
            VData.ManeuverPitch = final_data[57]
            VData.ManeuverHeading = final_data[58]
            VData.TargetPitch = final_data[59]
            VData.TargetHeading = final_data[60]
            VData.NormalHeading = final_data[61]
            VData.VQuaternion.w = final_data[62]
            VData.VQuaternion.x = final_data[63]
            VData.VQuaternion.y = final_data[64]
            VData.VQuaternion.z = final_data[65]

        Connected = True
    else:
        deadtime = now - dead_time_old
        if(deadtime > idle_timer):
            dead_time_old = now
            Connected = False

    return returnValue

def main():
    if(not ser.is_open):
        ser.open()

    while (ser.is_open):
        input()

        if (Connected):
            print(" Alt: ")
            print(VData.Alt)
            print(" Quat w: ")
            print(VData.VQuaternion.w)
            print(" Quat x: ")
            print(VData.VQuaternion.x)
            print(" Quat y: ")
            print(VData.VQuaternion.y)
            print(" Quat z: ")
            print(VData.VQuaternion.z)
            
main()