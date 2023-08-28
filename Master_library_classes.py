#Last update: 12:06 3/7/23 - Ashu
# Required packages

import minimalmodbus
# import serial
from tabulate import tabulate
import numpy as np
import time
import serial
# import matplotlib.pyplot as plt
# from datetime import datetime
# import pandas as pd

# API

#Global functions
# initialize_RTU(obj,baud,bytesize,stopbits,serial_timeout,address)
# graph_std(obj)

#Classes
# Kstar_Hybrid_RTU(COM,tracked_duration,remote_control,charge_source,discharge_depth,charge_current)
# Fronius_Gen24_RTU(self, COM, tracked_duration)
# SAJ_hybrid_RTU(self, COM, tracked_duration, phase)
# Growatt_TLXH_RTU(self,COM,tracked_duration)
# Sungrow_Hybrid_RTU(self, COM)
# Solaredge_hybrid_RTU(COM)

# def verify_sn(SN):
#     i=0
#     converted_SN=[]
#     while i<len(SN):
#


##Global initial function for RTU interface, TESTED
def initialize_RTU(obj,baud,bytesize,stopbits,serial_timeout,address):
    obj.instrument.serial.baudrate = baud          # Baud
    obj.instrument.serial.bytesize = bytesize
    obj.instrument.serial.parity   = serial.PARITY_NONE
    obj.instrument.serial.stopbits = stopbits
    obj.instrument.serial.timeout  = serial_timeout          # seconds
    obj.instrument.address = address                     # this is the slave address number
    obj.instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
    obj.instrument.clear_buffers_before_each_transaction = True     

##Global graph function, object parsed, values must be read from object. NOT TESTED. Variable names need to be made consistent across classes 
def graph_std1234(obj):
    i = 0;
    while i<(obj.tracked_duration/5):
        figure, ax = plt.subplots(figsize=(8,8))
        plt.ion()
        obj.BATTERYSOC=[]
        obj.POWERBATTERY=[]
        obj.DCPOWER1=[]
        obj.DCPOWER2=[]
        obj.ACPOWER=[]

    
        tijds = list(np.arange(0,i+1))
        tijdslots= [i * 5 for i in tijds]
        time.sleep(0.1)          
        SOCREGISTER = obj.instrument.read_register(3066, 1, 4, False)
        time.sleep(0.1)
        PBAT = obj.instrument.read_register(3065,0, 4, True)
        time.sleep(0.1)
        PDC1 = obj.instrument.read_register(3024, 0, 4, True)
        time.sleep(0.1)
        PDC2 = obj.instrument.read_register(3025, 0, 4, True)
        time.sleep(0.1)
        OUTPUTPOWER = obj.instrument.read_register(3126, 0, 4, True)
        time.sleep(0.1)

        time.sleep(0.1)
        obj.BATTERYSOC.append(SOCREGISTER)
        plt.subplot(1, 2, 1)
        plt.axis([0, obj.amount_of_data*5, 0, 100])
        plt.plot(tijdslots, obj.BATTERYSOC, color='g')
        plt.title("Battery State of Charge (%)")
        plt.xlabel('Time passed in seconds')
        plt.ylabel('SOC')
        plt.legend(['Battery SoC'])
        obj.POWERBATTERY.append(obj.PBAT)
        obj.DCPOWER1.append(obj.PDC1)
        obj.DCPOWER2.append(obj.PDC2)
        obj.ACPOWER.append(obj.OUTPUTPOWER)
        plt.subplot(1, 2, 2)
        plt.axis([0, obj.amount_of_data*5, -3000, 3000])
        plt.plot(tijdslots, obj.POWERBATTERY,color='c')
        plt.plot(tijdslots, obj.DCPOWER1,color='r')
        plt.plot(tijdslots, obj.DCPOWER2,color='g')
        plt.plot(tijdslots, obj.ACPOWER,color='b')
        plt.title("Battery Power (W) (positive power is discharging and negative power is charging)")
        plt.xlabel('Time passed in seconds')
        plt.ylabel('Battery Power (W)')
        plt.legend(['POWERBAT','DCPOWER1','DCPOWER2','ACPOWER'])
        figure.canvas.draw()
        figure.canvas.flush_events()
        plt.show()
        time.sleep(4.7)      

## Solaredge specific functions

def convert_to_binary(value):
    '''
    Converts a float to a 16-bit binary string.
    '''
    n = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0']
    value = value
    if value > 2**15:
        if value > 2**16:
            print('Value too large')
        else:
            n[0] = '1'
            value = value - (2**15)
    if value > 2**14:
        n[1] = '1'
        value = value - (2**14)
    if value > 2**13:
        n[2] = '1'
        value = value - (2**13)
    if value > 2**12:
        n[3] = '1'
        value = value - (2**12)
    if value > 2**11:
        n[4] = '1'
        value = value - (2**11)
    if value > 2**10:
        n[5] = '1'
        value = value - (2**10)
    if value > 2**9:
        n[6] = '1'
        value = value - (2**9)
    if value > 2**8:
        n[7] = '1'
        value = value - (2**8)
    if value > 2**7:
        n[8] = '1'
        value = value - (2**7)
    if value > 2**6:
        n[9] = '1'
        value = value - (2**6)
    if value > 2**5:
        n[10] = '1'
        value = value - (2**5)
    if value > 2**4:
        n[11] = '1'
        value = value - (2**4)
    if value > 2**3:
        n[12] = '1'
        value = value - (2**3)
    if value > 2**2:
        n[13] = '1'
        value = value - (2**2)
    if value > 2**1:
        n[14] = '1'
        value = value - (2**1)
    if value >= 2**0:
        n[15] = '1'
        value = value - (2**0)

    n = ''.join(n)
    n = str(n)
    return str(n)

def convert_back(bin_num):
    """
    Converts binary string to a float.
    """
    value = 0
    print(type(bin_num))
    n = list(bin_num)

    if n[0] == '1':
        value = value + (2 ** 15)
    if n[1] == '1':
        value = value + (2 ** 14)
    if n[2] == '1':
        value = value + (2 ** 13)
    if n[3] == '1':
        value = value + (2 ** 12)
    if n[4] == '1':
        value = value + (2 ** 11)
    if n[5] == '1':
        value = value + (2 ** 10)
    if n[6] == '1':
        value = value + (2 ** 9)
    if n[7] == '1':
        value = value + (2 ** 8)
    if n[8] == '1':
        value = value + (2 ** 7)
    if n[9] == '1':
        value = value + (2 ** 6)
    if n[10] == '1':
        value = value + (2 ** 5)
    if n[11] == '1':
        value = value + (2 ** 4)
    if n[12] == '1':
        value = value + (2 ** 3)
    if n[13] == '1':
        value = value + (2 ** 2)
    if n[14] == '1':
        value = value + (2 ** 1)
    if n[15] == '1':
        value = value + (2 ** 0)
    return value


def convert_binair_float32(Register1, Register2):
    """
    Converts binary string to a float.
    """
    number=0
    Bin_1=convert_to_binary(Register1)
    Bin_2=convert_to_binary(Register2)

    New=f'{Bin_2}{Bin_1}'

    bit1=int(str(New)[0:1])
    bit2=int(str(New)[1:2])
    bit3=int(str(New)[2:3])
    bit4=int(str(New)[3:4])
    bit5=int(str(New)[4:5])
    bit6=int(str(New)[5:6])
    bit7=int(str(New)[6:7])
    bit8=int(str(New)[7:8])
    bit9=int(str(New)[8:9])
    bit10=int(str(New)[9:10])
    bit11=int(str(New)[10:11])
    bit12=int(str(New)[11:12])
    bit13=int(str(New)[12:13])
    bit14=int(str(New)[13:14])
    bit15=int(str(New)[14:15])
    bit16=int(str(New)[15:16])
    bit17=int(str(New)[16:17])
    bit18=int(str(New)[17:18])
    bit19=int(str(New)[18:19])
    bit20=int(str(New)[19:20])
    bit21=int(str(New)[20:21])
    bit22=int(str(New)[21:22])
    bit23=int(str(New)[22:23])
    bit24=int(str(New)[23:24])
    bit25=int(str(New)[24:25])
    bit26=int(str(New)[25:26])
    bit27=int(str(New)[26:27])
    bit28=int(str(New)[27:28])
    bit29=int(str(New)[28:29])
    bit30=int(str(New)[29:30])
    bit31=int(str(New)[30:31])
    bit32=int(str(New)[31:32])
    if bit1==1:
        sign=-1
    else:
        sign=1
    if bit2==1:
        exp7=2**7
    else:
        exp7=0
    if bit3==1:
        exp6=2**6
    else:
        exp6=0
    if bit4==1:
        exp5=2**5
    else:
        exp5=0
    if bit5==1:
        exp4=2**4
    else:
        exp4=0
    if bit6==1:
        exp3=2**3
    else:
        exp3=0
    if bit7==1:
        exp2=2**2
    else:
        exp2=0
    if bit8==1:
        exp1=2**1
    else:
       exp1=0
    if bit9==1:
        exp0=2**0
    else:
        exp0=0
    if bit10==1:
        frac1=2**-1
    else:
        frac1=0
    if bit11==1:
        frac2=2**-2
    else:
        frac2=0
    if bit12==1:
        frac3=2**-3
    else:
        frac3=0
    if bit13==1:
        frac4=2**-4
    else:
        frac4=0
    if bit14==1:
        frac5=2**-5
    else:
        frac5=0
    if bit15==1:
        frac6=2**-6
    else:
        frac6=0
    if bit16==1:
        frac7=2**-7
    else:
        frac7=0
    if bit17==1:
        frac8=2**-8
    else:
        frac8=0
    if bit18==1:
        frac9=2**-9
    else:
        frac9=0
    if bit19==1:
        frac10=2**-10
    else:
        frac10=0
    if bit20==1:
        frac11=2**-11
    else:
        frac11=0
    if bit21==1:
        frac12=2**-12
    else:
        frac12=0
    if bit22==1:
        frac13=2**-13
    else:
        frac13=0
    if bit23==1:
        frac14=2**-14
    else:
        frac14=0
    if bit24==1:
        frac15=2**-15
    else:
        frac15=0
    if bit25==1:
        frac16=2**-16
    else:
        frac16=0
    if bit26==1:
        frac17=2**-17
    else:
        frac17=0
    if bit27==1:
        frac18=2**-18
    else:
        frac18=0
    if bit28==1:
        frac19=2**-19
    else:
        frac19=0
    if bit29==1:
        frac20=2**-20
    else:
        frac20=0
    if bit30==1:
        frac21=2**-21
    else:
        frac21=0
    if bit31==1:
        frac22=2**-22
    else:
        frac22=0
    if bit32==1:
        frac23=2**-23
    else:
        frac23=0

    number=sign*(2**(exp0+exp1+exp2+exp3+exp4+exp5+exp6+exp7-127))*(1+frac1+frac2+frac3+frac4+frac5+frac6+frac7+frac8+frac9+frac10+frac11+frac12+frac13+frac14+frac15+frac16+frac17+frac18+frac19+frac20+frac21+frac22+frac23)
    return number

def convert_dec_int32(Register1, Register2):
    """
    Converts binary string to a float.
    """
    number=0
    Bin_1=convert_to_binary(Register1)
    Bin_2=convert_to_binary(Register2)

    # New=f'{Bin_2}{Bin_1}'
    New=Bin_1+Bin_2
    print(New)
    # TY = int(print(New))
    return New

def convert_bin_to_int(val):
    i=0
    num=0
    while i<len(val):
        num+= pow(2,int(i))*int(val[i])
        print(num)
        i+=1
    return num

class Kstar_Hybrid_RTU:
    def __init__(self,port):
        self.tracked_duration=500
        self.amount_of_data=round(self.tracked_duration/5) ###### CHANGE ME (x*5seconds between data) 1440 amount of data is 2hours of time
        self.COM_port=port;
        self.instrument = minimalmodbus.Instrument(port, 1)  
        self.instrument.serial.port = port                             ##### this is the serial port name
        self.instrument.serial.baudrate = 9600                           ##### Baudrate
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity   = serial.PARITY_NONE
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout  = 0.15                           ##### seconds
        self.instrument.address = 1                                      ##### this is the slave address number
        self.instrument.mode = minimalmodbus.MODE_RTU                    ##### rtu or ascii mode
        self.instrument.clear_buffers_before_each_transaction = True
        
    def configure(self):
        self.instrument.write_register(3185, 1, 0, 6, False) #0: Disabled 1: Enabled
        time.sleep(0.1)

        # self.instrument.write_register(3044, 1, 0, 6, False)  # 0: self consumption 1 peak shift 2 battery prio
        # time.sleep(0.1)
        # print('Peak shift')

        #self.instrument.write_register(3085, 0, 0, 6, False) #0: GRID+PV 1:GRID 2: PV
        #time.sleep(0.1)
        
        self.instrument.write_register(3068, 90, 0, 6, False) #% of SOC that can be discharged [0-100] (must be 80% to be able to discharge to 20%SOC)
        time.sleep(0.1)

        self.instrument.write_register(3082, 100, 0, 6, False) #[0-120]A
        time.sleep(0.1)
        
        #BAT_DISCHG_LIMIT_CURR = instrument.write_register(3071,100, 0, 6, False) #[0-120]A        
        #time.sleep(0.1)
        #BAT_CHG_LIMIT_CURR = instrument.write_register(3070,100, 0, 6, False) #[0-120]A        
        #time.sleep(0.1)
        print('- Inverter and battery settings are configured')

        self.BATTERYSOC=[]
        self.POWERBATTERY=[]
        self.DCPOWER1=[]
        self.DCPOWER2=[]
        self.ACPOWER=[]

    def idle(self):
        # self.instrument.write_register(3086, 0, 0, 6, False)  # 0: Invalid 1:Charge 2: Discharge
        # time.sleep(0.1)
        # self.instrument.write_register(3044, 1, 0, 6, False)  # 0: self consumption 1 peak shift 2 battery prio
        # time.sleep(0.1)
        # print('Peak shift')
        #
        # #self.force_charge_discharge = 0;
        self.discharge(0)
        print('- Inverter has stopped with charging or discharging, and is now in IDLE mode')


    def selfconsumption(self):
        self.instrument.write_register(3086, 0, 0, 6, False)  # 0: Invalid 1:Charge 2: Discharge
        print('Self consumption')
        time.sleep(0.1)
        self.instrument.write_register(3044, 0, 0, 6, False)  # 0: self consumption 1 peak shift 2 battery prio
        time.sleep(0.1)
        print('Self-consumption')
        time.sleep(0.1)
    def charge(self,charge_power):
        self.instrument.write_register(3044, 1, 0, 6, False)  # 0: self consumption 1 peak shift 2 battery prio
        print('Peak shift')
        time.sleep(0.1)
        self.instrument.write_register(3079, charge_power, 0, 6, False) #[0-100%] of the power of inverter
        time.sleep(0.1)
        self.instrument.write_register(3086, 1, 0, 6, False) #0: Invalid 1:Charge 2: Discharge
        time.sleep(0.1)
        print('- Battery is charging with {}%'.format(charge_power))
            
        
    def discharge(self,discharge_power):
        self.instrument.write_register(3044, 1, 0, 6, False)  # 0: self consumption 1 peak shift 2 battery prio
        print('peak shift baby')
        time.sleep(0.1)
        self.instrument.write_register(3078, discharge_power, 0, 6, False) #[0-100%] of the power of inverter
        time.sleep(0.1)
        self.instrument.write_register(3086, 2, 0, 6, False) #0: Invalid 1:Charge 2: Discharge
        time.sleep(0.1)
        print('- Battery is discharging with {}%'.format(discharge_power))
        
    def read_registers(self):
        self.INVSTATE = self.instrument.read_register(3046, 0, 4, False)     ##### Inverter status
        time.sleep(0.1)
        self.BMSSTATE = self.instrument.read_register(3048, 0, 4,False)          ##### BMS Status
        time.sleep(0.1)
        self.WORKMODE = self.instrument.read_register(3044, 0, 4, False)     ##### Workmode / Priority
        time.sleep(0.1)
        self.VDC1 = self.instrument.read_register(3000, 0, 4, False)         ##### DC-input 1 Voltage/10
        time.sleep(0.1)
        self.IDC1 = self.instrument.read_register(3012, 0, 4, True)         ##### DC-input 1 Current/100
        time.sleep(0.1)
        self.PDC1 = self.instrument.read_register(3024, 0, 4, True)         ##### DC-input 1 Power
        time.sleep(0.1)
        self.VDC2 = self.instrument.read_register(3001, 0, 4, False)         ##### DC-input 2 Voltage/10
        time.sleep(0.1)
        self.IDC2 = self.instrument.read_register(3013, 0, 4, True)         ##### DC-input 2 Current/100
        time.sleep(0.1)
        self.PDC2 = self.instrument.read_register(3025, 0, 4, True)            ##### DC-input 2 Power
        time.sleep(0.1)

        #self.INPUTPOWER = self.instrument.read_long(33057,4, True, 0)         ##### Total DC Input Power
        self.OUTPUTPOWER = self.instrument.read_register(3126, 0, 4, True)  ##### Total AC Output Power
        time.sleep(0.1)

        self.VL1 = self.instrument.read_register(3123, 0, 4, False)          ##### Phase 1 Voltage/10
        time.sleep(0.1)
        self.AL1 = self.instrument.read_register(3124, 0, 4, False)          ##### Phase 1 Current/100
        time.sleep(0.1)
        self.FAC1 = self.instrument.read_register(3125, 0, 4, False)         ##### Phase 1 Frequency/100
        time.sleep(0.1)
        #self.VL2 = self.instrument.read_register(40081, 0, 3, False)          ##### Phase 2 Voltage                   
        #self.AL2 = self.instrument.read_register(40074, 0, 3, False)          ##### Phase 2 Current                   
        #self.FAC2 = self.instrument.read_register(40078, 1, 3, False)         ##### Phase 2 Frequency                
        #self.VL3 = self.instrument.read_register(40082, 0, 3, False)          ##### Phase 3 Voltage                   
        #self.AL3 = self.instrument.read_register(40075, 0, 3, False)          ##### Phase 3 Current                   
        #self.FAC3 = self.instrument.read_register(40079, 1, 3, False)         ##### Phase 3 Frequency                 


        self.ETODAY = self.instrument.read_register(3036, 0, 4, False)       ##### Daily Production/10
        time.sleep(0.1)
        self.ETOTAL = self.instrument.read_long(3041,4, False, 0)          ##### Cumulative Productiona/10
        time.sleep(0.1)

        self.PURTODAY = self.instrument.read_register(3109, 0, 4, False)     ##### Daily Energy Purchased/10
        time.sleep(0.1)
        self.PURTOTAL = self.instrument.read_long(3114,4, False, 0)           ##### Cumulative Energy Purchased/10
        time.sleep(0.1)

        self.FEEDINTODAY = self.instrument.read_register(3116, 0, 4, False)  ##### Daily Grid Feed-in/10
        time.sleep(0.1)
        self.FEEDINTOTAL = self.instrument.read_long(3121,4, False, 0)        ##### Cumulative Grid Feed-in/10
        time.sleep(0.1)

        self.PBAT = self.instrument.read_register(3065,0, 4, True)         ##### Battery Power
        time.sleep(0.1)
        self.VBAT = self.instrument.read_register(3063, 0, 4, False)         ##### Battery Voltage/100
        time.sleep(0.1)
        self.ABAT = self.instrument.read_register(3064, 0, 4, True)         ##### Battery Current)/10
        time.sleep(0.1)
        self.SOCBAT = self.instrument.read_register(3066, 0, 4, False)       ##### Charge Capacity/10
        time.sleep(0.1)

        self.TODAYCHARGE = self.instrument.read_register(3301, 0, 4, False)  ##### Daily Charging Energy/10
        time.sleep(0.1)
        self.TOTALCHARGE = self.instrument.read_long(3299,4, False, 0)      ##### Total Charging Energy
        time.sleep(0.1)

        self.TODAYDIS = self.instrument.read_register(3294, 0, 4, False)     ##### Daily Discharging Energy/10
        time.sleep(0.1)
        self.TOTALDIS = self.instrument.read_long(3292,4, False, 0)         ##### Total Discharging Energy
        time.sleep(0.1)

        self.TEMP = self.instrument.read_register(3057, 0, 4, False)         ##### Temperature- Inverter/10
        time.sleep(0.1)
        self.BATTEMP = self.instrument.read_register(3067, 0, 4, False)      ##### Temperature- Battery/10
        time.sleep(0.1)

        #self.Alarmcode1 = self.instrument.read_register(40109, 0, 3, False)   ##### Alarmcode 1                       
        #self.Alarmcode1bat = self.instrument.read_register(57738, 0, 3, False)   ##### Alarmcode 1                       
        #self.Fault1 = self.instrument.read_register(33096, 1, 3, False)       ##### Fault 1

        #####EXTRA BRAND SPECIFIC REGISTERS
        self.BATTYPE = self.instrument.read_register(3062, 0, 4, False)
        time.sleep(0.1)
        self.NUMBEROFPACKS= self.instrument.read_register(3077, 0, 4, False)
        time.sleep(0.1)
        self.DISCHARGEDEPTH = self.instrument.read_register(3068, 0, 4, False)
        time.sleep(0.1)
        self.BATCHARGECURRRENTLIMIT = self.instrument.read_register(3070, 0, 4, False)
        time.sleep(0.1)
        self.BATDISCHARGECURRRENTLIMIT = self.instrument.read_register(3071, 0, 4, False)
        time.sleep(0.1)
        self.BATDISCHARGEPOWERLIMIT = self.instrument.read_register(3078, 0, 4, False)
        time.sleep(0.1)
        self.BATCHARGEPOWERLIMIT = self.instrument.read_register(3079, 0, 4, False)
        time.sleep(0.1)
        self.BATSETCHARGECURRENT =  self.instrument.read_register(3082, 0, 4, False)
        time.sleep(0.1)
        self.CHARGESOURCE = self.instrument.read_register(3085, 0, 4, False)
        time.sleep(0.1)
        self.FORCECHARGEDISCHARGE= self.instrument.read_register(3086, 0, 4, False)
        time.sleep(0.1)
        self.TIMINGCHARGEDISCHARGE= self.instrument.read_register(3176, 0, 4, False)
        time.sleep(0.1)
        self.PVINPUTMODE = self.instrument.read_register(3179, 0, 4, False)
        time.sleep(0.1)
        self.REMOTECONTROLENABLE = self.instrument.read_register(3185, 0, 4, False)
        time.sleep(0.1)
    def tabulate(self):
        self.read_registers();
        self.table1 = [['Register naam', 'Raw data','portal value','Eenheid'],
                    # ['Inverter status', self.INVSTATE,self.INVSTATE,'2: Hybrid On-grid'],
                     ['BMS Status', self.BMSSTATE,self.BMSSTATE,'0: Standy 1:Softboot 2:Charging mode 3:Discharging mode'],
                     ['Workmode / Priority', self.WORKMODE,self.WORKMODE,'0: Untimed charge/discharge 1:Timing Discharge 2: Timing charge'],
                     ['DC-input 1 Voltage', self.VDC1,self.VDC1/10, 'V'],
                     ['DC-input 1 Current', self.IDC1,self.IDC1/100, 'A'],
                     ['DC-input 1 Power',self.PDC1,self.PDC1, 'W'],
                     ['DC-input 2 Voltage', self.VDC2,self.VDC2/10 ,'V'],
                     ['DC-input 2 Current', self.IDC2,self.IDC2/100, 'A'],
                     ['DC-input 2 Power',self.PDC2,self.PDC2, 'W'],
                     #['TOTAL DC INPUT POWER',INPUTPOWER, 'W'],
                     ['TOTAL AC OUTPUT POWER',self.OUTPUTPOWER,self.OUTPUTPOWER ,'W'],
                     ['Phase 1 Voltage',self.VL1,self.VL1/10, 'V'],
                     ['Phase 1 Current', self.AL1,self.AL1/100, 'A'],
                     ['Phase 1 Frequency', self.FAC1,self.FAC1/100, 'Hz'],
                     #['Phase 2 Voltage',self.VL2, 'V'],
                     #['Phase 2 Current', self.AL2, 'A'],
                     #['Phase 2 Frequency', self.FAC2, 'Hz'],
                     #['Phase 3 Voltage',self.VL3, 'V'],
                     #['Phase 3 Current', self.AL3, 'A'],
                     #['Phase 3 Frequency', self.FAC3, 'Hz'],
                     ['Daily production',self.ETODAY,self.ETODAY/10, 'kWh'],
                     ['Cumulative production',self.ETOTAL, self.ETOTAL/10,'kWh'],
                     ['Daily purchased',self.PURTODAY,self.PURTODAY/10, 'kWh'],
                     ['Total purchased',self.PURTOTAL,self.PURTOTAL/10, 'kWh'],
                     ['Daily grid feed-in',self.FEEDINTODAY,self.FEEDINTODAY/10, 'kWh'],
                     ['Total grid feed-in',self.FEEDINTOTAL,self.FEEDINTOTAL/10,'kWh'],
                     ['Battery Power',self.PBAT,self.PBAT, 'W'],
                     ['Battery Voltage',self.VBAT,self.VBAT/100, 'V'],
                     ['Battery Current',self.ABAT,self.ABAT/10, 'A'],
                     ['Charge Capacity',self.SOCBAT,self.SOCBAT/10, '%'],
                     ['Daily charging energy',self.TODAYCHARGE,self.TODAYCHARGE/10, 'kWh'],
                     ['Total charging energy',self.TOTALCHARGE, self.TOTALCHARGE/10,'kWh'],
                     ['Daily discharging energy',self.TODAYDIS,self.TODAYDIS/10, 'kWh'],
                     ['Total discharging energy',self.TOTALDIS,self.TOTALDIS/10, 'kWh'],
                     ['Temperature-Inverter', self.TEMP,self.TEMP/10, 'C'],
                     ['Temperature-Battery', self.BATTEMP,self.BATTEMP/10, 'C']]
                     #['Alarmcode1', self.Alarmcode1, '-'],
                     #['Alarmcode1bat', self.Alarmcode1bat, '-']]


         ##### Generating table: Extra registers:
        self.table2 = [['Register naam', 'Register waarde','Eenheid'],
                  ['BATTYPE',self.BATTYPE,'6: LFP'],
                  ['NUMBEROFPACKS',self.NUMBEROFPACKS,'-'],
                  ['DISCHARGEDEPTH', self.DISCHARGEDEPTH, '%'],
                  ['BATCHARGECURRRENTLIMIT', self.BATCHARGECURRRENTLIMIT, 'A'],
                  ['BATDISCHARGECURRRENTLIMIT', self.BATDISCHARGECURRRENTLIMIT, 'A'],
                  ['BATCHARGEPOWERLIMIT', self.BATCHARGEPOWERLIMIT, '%'],
                  ['BATDISCHARGEPOWERLIMIT', self.BATDISCHARGEPOWERLIMIT, '%'],
                  ['BATSETCHARGECURRENT', self.BATSETCHARGECURRENT, 'A'],
                  ['CHARGESOURCE', self.CHARGESOURCE, '0: GRID+PV 1:GRID 2: PV'] ,
                  ['FORCECHARGEDISCHARGE', self.FORCECHARGEDISCHARGE, '0: invalid 1:Charge 2:Discharge'],
                  ['TIMINGCHARGEDISCHARGE', self.TIMINGCHARGEDISCHARGE, '-'],
                  ['PVINPUTMODE', self.PVINPUTMODE, '0: Independent 1:Parallel 2: Constant voltage input'],
                  ['REMOTECONTROLENABLE', self.REMOTECONTROLENABLE, '0: Disabled 1:Enabled']]

         #Show the Table
        print(tabulate(self.table1, headers='firstrow', tablefmt='fancy_grid'))
        print(tabulate(self.table2, headers='firstrow', tablefmt='fancy_grid'))
    def graph(self,i,figure,tijds,tijdslots):
       
        
            
        time.sleep(0.1)          
        SOCREGISTER = self.instrument.read_register(3066, 1, 4, False)
        time.sleep(0.1)
        PBAT = self.instrument.read_register(3065,0, 4, True)
        time.sleep(0.1)
        PDC1 = self.instrument.read_register(3024, 0, 4, True)
        time.sleep(0.1)
        PDC2 = self.instrument.read_register(3025, 0, 4, True)
        time.sleep(0.1)
        OUTPUTPOWER = self.instrument.read_register(3126, 0, 4, True)
        time.sleep(0.1)

        time.sleep(0.1)
        self.BATTERYSOC.append(SOCREGISTER)
        plt.subplot(1, 2, 1)
        plt.axis([0, self.amount_of_data*5, 0, 100])
        plt.plot(tijdslots, self.BATTERYSOC, color='g')
        plt.title("Battery State of Charge (%)")
        plt.xlabel('Time passed in seconds')
        plt.ylabel('SOC')
        plt.legend(['Battery SoC'])
        self.POWERBATTERY.append(PBAT)
        self.DCPOWER1.append(PDC1)
        self.DCPOWER2.append(PDC2)
        self.ACPOWER.append(OUTPUTPOWER)
        plt.subplot(1, 2, 2)
        plt.axis([0, self.amount_of_data*5, -3000, 3000])
        plt.plot(tijdslots, self.POWERBATTERY,color='c')
        plt.plot(tijdslots, self.DCPOWER1,color='r')
        plt.plot(tijdslots, self.DCPOWER2,color='g')
        plt.plot(tijdslots, self.ACPOWER,color='b')
        plt.title("Battery Power (W) (positive power is discharging and negative power is charging)")
        plt.xlabel('Time passed in seconds')
        plt.ylabel('Battery Power (W)')
        plt.legend(['POWERBAT','DCPOWER1','DCPOWER2','ACPOWER'])
        figure.canvas.draw()
        figure.canvas.flush_events()
        plt.show()
        time.sleep(4.7)              

##Not tested, uses global functions        

class Fronius_Gen24_RTU:
    def __init__(self, COM):
        self.instrument = minimalmodbus.Instrument(COM, 1, debug=False)
        self.tracked_duration = 500
        initialize_RTU(self,9600,8,1,0.5,1)

    def ASHURANDOMFUNCTION123(self):
        print('u suck loser')

    def configure(self):
        self.ChaGriSet = self.instrument.write_register(40360, 1, 0, 6, False)
        self.MinRsvPct = self.instrument.write_register(40350, 1000, 0, 6, False)
        print('Inverter successfully configured')


    def self_consumption(self):
        self.OutWRte = self.instrument.write_register(40355, 0, 0, 6, True)  # percentage of max discharge rate [0,100%]
        time.sleep(10)
        self.InWRte = self.instrument.write_register(40356, 0, 0, 6, True)  # percentage of max charging rate [0,100%]
        time.sleep(10)
        self.StorCtl_Mod = self.instrument.write_register(40348, 0, 0, 6, False)  # Now enable: [1 activate charge limit, 2 activate discharge limit, 3 activate both limits]
        time.sleep(10)
        print('Self-consumption')

    def self_consumption_new(self):
        self.timeout = self.instrument.write_register(40368, 0,0,6,False)
        print('Self-consumption')

    def idle(self):
        CHA_RATE=self.instrument.read_register(40356,0,3,True)
        DISCHA_RATE=self.instrument.read_register(40355,0,3,True)

        if CHA_RATE>DISCHA_RATE: #If you are coming from chg
            self.OutWRte = self.instrument.write_register(40355,0,0,6,True) #percentage of max discharge rate [0,100%]
            time.sleep(10)
            self.InWRte = self.instrument.write_register(40356,0,0,6,True) # percentage of max charging rate [0,100%]
            time.sleep(10)
            self.StorCtl_Mod = self.instrument.write_register(40348,3,0,6,False) #Now enable: [1 activate charge limit, 2 activate discharge limit, 3 activate both limits]
            time.sleep(10)
            print('Stopped charging, idle mode')

        if CHA_RATE<DISCHA_RATE: #If you are coming from disch
            self.InWRte = self.instrument.write_register(40356,0,0,6,True) # percentage of max charging rate [0,100%]
            time.sleep(10)
            self.OutWRte = self.instrument.write_register(40355,0,0,6,True) #percentage of max discharge rate [0,100%]
            time.sleep(10)
            self.StorCtl_Mod = self.instrument.write_register(40348,3,0,6,False) #Now enable: [1 activate charge limit, 2 activate discharge limit, 3 activate both limits]
            time.sleep(10)
            print('Stopped discharging, idle mode')

        if CHA_RATE==DISCHA_RATE: #If you are coming from Self CSM or IDLE
            self.StorCtl_Mod = self.instrument.write_register(40348, 3, 0, 6, False)  # Now enable: [1 activate charge limit, 2 activate discharge limit, 3 activate both limits]
            time.sleep(10)
            print('Idle mode')

    def charge(self,charge_rate):
        self.InWRte = self.instrument.write_register(40356,charge_rate*100,0,6,True) # percentage of max charging rate [0,100%] sf=-2
        time.sleep(10)
        self.OutWRte = self.instrument.write_register(40355,charge_rate*-100,0,6,True) #percentage of max discharge rate [0,100%] sf=-2
        time.sleep(10)
        self.StorCtl_Mod = self.instrument.write_register(40348,3,0,6,False) #Now enable: [1 discharge, 2 charge, 3 activate both limits]
        time.sleep(10)
        print('Charging')

    def discharge(self,discharge_rate):
        #self.MinRsvPct = self.instrument.write_register(40350, 2000, 0, 6,False)  # Now enable: input range[0,10000] meaning 0-100% SOC as minimum/or target SO
        self.OutWRte = self.instrument.write_register(40355,discharge_rate*100,0,6,True) #percentage of max discharge rate [0,100%] sf=-2
        time.sleep(10)
        self.InWRte = self.instrument.write_register(40356,discharge_rate*-100,0,6,True) # percentage of max charging rate [0,100%] sf=-2
        time.sleep(10)
        self.StorCtl_Mod = self.instrument.write_register(40348,3,0,6,False) #Now enable: [1 discharge, 2 charge, 3 activate both limits]
        time.sleep(10)
        print('Discharging')
        
    def read_registers(self):
        self.WChaMax = self.instrument.read_register(40345, 0, 3, False) #charge capacity in W
        self.WChaGra = self.instrument.read_register(40346,0,3,False) #setpoint for max charge rate [%]
        self.WDisChaGra = self.instrument.read_register(40347,0,3,False) #setpoint for max discharge rate [%]
        self.StorCtl_Mod = self.instrument.read_register(40348,0,3,False)
        self.MinRsvPct = self.instrument.read_register(40350,0,3,False) #sf=-2
        self.ChaState = self.instrument.read_register(40351, 2, 3, False)
        self.ChaGridSet = self.instrument.read_register(40360,0,3,False)
        #BATTERY READ DATA:
        self.ChaSt = self.instrument.read_register(40354, 0, 3, False) #operating status [1 OFF, 2 EMPTY, 3 DISCHARGING, 4 CHARGING, 5 FULL, 6 HOLDING, 7 TESTING]
        self.Battery_voltage_charge = self.instrument.read_register(40313, 0, 3, False) #/100
        self.Battery_current_charge = self.instrument.read_register(40312,0,3,False) #/10000
        self.Battery_power_charge = self.instrument.read_register(40314,0,3,False) #/10 and /1000(kW) for kW

        self.Battery_voltage_discharge = self.instrument.read_register(40333, 0, 3, False) #/100
        self.Battery_current_discharge = self.instrument.read_register(40332, 0, 3, False)#1000
        self.Battery_power_discharge = self.instrument.read_register(40334, 0, 3, False)#/10 and /1000(kW) for kW
        self.TOTALCHARGE = self.instrument.read_long(40315,3, False, 0)   
        self.TOTALDIS = self.instrument.read_long(40335,3, False, 0)   
        self.AC_Cumulitive_production = self.instrument.read_long(40093,3, False, 0)   
        #self.TODAYDIS = self.instrument.read_long(40335,3, False, 0)   

          #   = self.instrument.read_register(40354, 0, 3, False)
        #       = self.instrument.read_register(40354, 0, 3, False)
              
        self.OutWRte = self.instrument.read_register(40355,0,3,False)
        self.InWRte = self.instrument.read_register(40356,0,3,False)
        self.InOutWRte_RvrtTms = self.instrument.read_register(40358,0,3,False)
        #self.WChaMax_SF = self.instrument.read_register(40361,0,3,False) 
        #self.WChaDisChaGra_SF = self.instrument.read_register(40362,0,3,False)
        #self.MinRsvPct_SF = self.instrument.read_register(40364,0,3,False)

        #READ DATA:
        self.DC1_voltage = self.instrument.read_register(40273,0,3,False) #/100
        self.DC1_current = self.instrument.read_register(40272,0,3,False) #/100
        self.DC1_power = self.instrument.read_register(40274,0,3,False)#/10 and /1000(kW) for kW
        self.DC2_voltage = self.instrument.read_register(40293,0,3,False) #/100
        self.DC2_current = self.instrument.read_register(40292,0,3,False) #/100
        self.DC2_power = self.instrument.read_register(40294,0,3,False)#/10 and /1000(kW) for kW
        self.DC1_cumulitive = self.instrument.read_long(40275,3, False, 0)   
        self.DC2_cumulitive = self.instrument.read_long(40295,3, False, 0)   

        #self.DC_power = self.instrument.read_register(40100,0,3,False)#/10 and /1000(kW) for kW

        #    = self.instrument.read_register(40358,0,3,False)
     

        #self.Phase_voltage_AB = self.instrument.read_register(40076,0,3,False) #/10 SUPPORT/NOT SUPPORTED depends on grid connection
        self.Phase_voltage_AN = self.instrument.read_register(40079,0,3,False) #/10
        self.AC_current = self.instrument.read_register(40071,0,3,False) #/1000
        self.Phase_A_current = self.instrument.read_register(40072,0,3,False) #/1000
        self.Phase_B_current = self.instrument.read_register(40073,0,3,False) #/1000
        self.AC1_frequency = self.instrument.read_register(40085,0,3,False) #/100

        self.AC_power_output = self.instrument.read_register(40083,0,3,True) #/10 W

        self.Cabinet_Temperature = self.instrument.read_register(40102,0,3,False)
        # = self.instrument.read_register(40358,0,3,False)

        self.A_SF= self.instrument.read_register(40075,0,3,True)
        self.V_SF=  self.instrument.read_register(40082,0,3,True)
        self.W_SF=  self.instrument.read_register(40084,0,3,True)
        self.DCW_SF= self.instrument.read_register(40101,0,3,True)
        self.Hz_SF = self.instrument.read_register(40086, 0, 3, True)
        self.WH_SF = self.instrument.read_register(40095,0,3,True)
        self.DCA_SF = self.instrument.read_register(40097, 0, 3, True)
        self.DCV_SF = self.instrument.read_register(40099, 0, 3, True)
        self.DCWH_SF = self.instrument.read_register(40258, 0, 3, True)

    def tabulate(self):
        self.read_registers()
        self.table = [['Max Charge/Discharge range(WChaMax)','40345',self.WChaMax,self.WChaMax, 'W'],
         #['Max charge rate (WChaGra)',self.WChaGra, '%'],
         #['Max discharge rate (WDisChaGra)',self.WDisChaGra, '%'],
         #['Storage mode (StorCtl_Mod)',self.StorCtl_Mod, '-'],
         #['Min % of nominal max storage (MinRsvPct)',self.MinRsvPct/100, '%'],#set at 20%
#BATTERY READ DATA
         ['storage charge level(ChaState)','40351',self.ChaState,self.ChaState, '%'],
         ['Bat Voltage Charge','40313',self.Battery_voltage_charge,self.Battery_voltage_charge/100,'V'],
         ['Bat Current Charge','40312',self.Battery_current_charge,self.Battery_current_charge/1000,'A'],
         ['Bat Power Charge','40314',self.Battery_power_charge,(self.Battery_power_charge/10),'W'],
         ['Bat Voltage Discharge','40333',self.Battery_voltage_discharge,self.Battery_voltage_discharge/100,'V'],
         ['Bat Current Discharge','40332',self.Battery_current_discharge,self.Battery_current_discharge/1000,'A'],
         ['Bat Power Discharge','40334',self.Battery_power_discharge,(self.Battery_power_discharge/10),'W'],
         ['TOTALCHARGE ','40315', self.TOTALCHARGE , self.TOTALCHARGE/1000000,'kWh'],
         ['TOTALDIS ','40335', self.TOTALDIS , self.TOTALDIS/1000000,'kWh'],
         ['AC_Cumulitive_production','40093', self.AC_Cumulitive_production,  self.AC_Cumulitive_production/1000000,'W'],
        ['DC1_cumulitive','40275',self.DC1_cumulitive,self.DC1_cumulitive/1000000, 'kWh'],
        ['DC2_cumulitive','40295',self.DC2_cumulitive,self.DC2_cumulitive/1000000, 'kWh'],
#INVERTER READ DATA
        ['DC1 voltage         ','40273',self.DC1_voltage,self.DC1_voltage/100,'V'],
        ['DC1 Current (read when discharging)        ','40272',self.DC1_current,self.DC1_current/1000,'A'],
        ['DC1 Current (read when charging)        ','40272',self.DC1_current,self.DC1_current/10000,'A'],
        ['DC1 Power       ','40274',self.DC1_power,(self.DC1_power/10),'W'],
        ['DC2 voltage         ','40293',self.DC2_voltage,self.DC2_voltage/100,'V'],
        ['DC2 Current        ','40292',self.DC2_current,self.DC2_current/1000,'A'],
        ['DC2 Power       ','40294',self.DC2_power,(self.DC2_power/10),'W'],
        ['Phase_voltage_AN (AC1 voltage)        ','40079',self.Phase_voltage_AN,self.Phase_voltage_AN/10,'V'],
        ['AC Current         ','40071',self.AC_current,self.AC_current/1000,'A'],
        ['Phase A Current (AC1 current)        ','40072',self.Phase_A_current,self.Phase_A_current/1000,'A'],
        ['(AC1) Line Frequency    ','40085',self.AC1_frequency,self.AC1_frequency/100 ,'Hz'],
        ['AC Power Output','40083',self.AC_power_output,((self.AC_power_output/10)),'W'],
        ['Cabinet_Temperature','40102',self.Cabinet_Temperature,self.Cabinet_Temperature/10,'C'],
        ['A_SF','40075',self.A_SF],
        ['V_SF','40082',self.V_SF],
        ['W_SF','40084',self.W_SF],
        ['DCW_SF','40101',self.DCW_SF],
        ['Hz_SF','40086',self.Hz_SF],
        ['WH_SF','40095',self.WH_SF],
        ['DCA_SF','40097',self.DCA_SF],
        ['DCV_SF','40099',self.DCV_SF],
        ['DCWH_SF','40258',self.DCWH_SF]]

        print(tabulate(self.table, tablefmt='fancy_grid'))
                    
    def graph(self):

        graph_std(self)

class SAJ_hybrid_RTU:

    def __init__(self, COM, phase):
        if phase!=1 and phase!=3:
            print('Wrong value entered for phase, please enter 1 or 3')
        self.instrument=minimalmodbus.Instrument(COM, 1, debug= True)
        self.tracked_duration = 500
        self.phase=phase
        initialize_RTU(self,9600,8,1,1,1)

    def stop(self):
        self.Device_Control_Enable = self.instrument.write_register(13895,0,0,6,False) #Set 0X3647 as 0X0E - SET 13895 to 14
        time.sleep(5)
        print('App mode is now 0, battery has stopped charging or discharging.')

    def charge(self, charge_power):
        if self.phase==3:      
            self.Device_Control_Enable = self.instrument.write_register(13895,14,0,6,False) #for 1phase=3 for 3phase its 14
            time.sleep(5)
            self.Appmode = self.instrument.write_register(13896,2,0,6,False) #### Set 0X3648: SET 13896  1 for discharge, 2 for charge
            time.sleep(5)   
            self.Aging_Buy_power_limit = self.instrument.write_register(13900,charge_power*10,0,6,False) #currently at 60% power ###Charge power: 0X364C: SET 13900 to %(1-1000)=0.1-100%) % of rated power
            time.sleep(5)
            print('Set to charge')
        if self.phase==1:
            self.Device_Control_Enable = self.instrument.write_register(13895,3,0,6,False) #for 1phase=3 for 3phase its 14
            self.passive_charge_dicharge = self.instrument.write_register(13878,2,0,6,False) #### Set 0X3648: SET 13896  1 for discharge, 2 for charge
            time.sleep(5)
            print('Set to charge')
            #passive_Charge_power_grid = instrument.write_register(13879,600,0,6,False) #currently at 60% power ###Charge power: 0X364C: SET 13900 to %(1-1000)=0.1-100%) % of rated power
            #time.sleep(5)
            self.passive_Charge_power_batt = self.instrument.write_register(13881,charge_power*10,0,6,False) #currently at 60% power ###Charge power: 0X364C: SET 13900 to %(1-1000)=0.1-100%) % of rated power
            time.sleep(5)
        if self.phase!=1 and self.phase!=3:
            print('Wrong value entered for phase, please enter 1 or 3 while initializing an object of the SAJ_hybrid_RTU class')

    def discharge(self, discharge_power):
        if self.phase==3:      
            self.Device_Control_Enable = self.instrument.write_register(13895,14,0,6,False) #for 1phase=3 for 3phase its 14
            time.sleep(5)
            self.Appmode = self.instrument.write_register(13896,1,0,6,False) #### Set 0X3648: SET 13896  1 for discharge, 2 for charge
            time.sleep(5)   
            self.Aging_Buy_power_limit = self.instrument.write_register(13900,discharge_power*10,0,6,False) #currently at 60% power ###Charge power: 0X364C: SET 13900 to %(1-1000)=0.1-100%) % of rated power
            time.sleep(5)
            print('Set to discharge')
        if self.phase==1:
            self.Device_Control_Enable = self.instrument.write_register(13895,3,0,6,False) #for 1phase=3 for 3phase its 14
            self.passive_charge_dicharge = self.instrument.write_register(13878,1,0,6,False) #### Set 0X3648: SET 13896  1 for discharge, 2 for charge
            time.sleep(5)
            print('Set to discharge')
            #passive_Charge_power_grid = instrument.write_register(13879,600,0,6,False) #currently at 60% power ###Charge power: 0X364C: SET 13900 to %(1-1000)=0.1-100%) % of rated power
            #time.sleep(5)
            self.passive_DisCharge_power_batt = self.instrument.write_register(13880,discharge_power*10,0,6,False) #currently at 60% power ###Charge power: 0X364C: SET 13900 to %(1-1000)=0.1-100%) % of rated power
            time.sleep(5)
            print('Discharge power set')
        if self.phase!=1 and self.phase!=3:
            print('Wrong value entered for phase, please enter 1 or 3 while initializing an object of the SAJ_hybrid_RTU class')
    def StopBat1ph(self):
        self.Device_Control_Enable = self.instrument.write_register(13895, 3, 0, 6, False)
        time.sleep(5)
        self.Passive_chg_enable = self.instrument.write_register(13879, 1, 0, 6, False)  # for 1phase=3 for 3phase its 14
        time.sleep(5)
        self.Passive_grid_disch_power = self.instrument.write_register(13880, 1100, 0, 6, False)  # for 1phase=3 for 3phase its 14
        time.sleep(5)
        self.Passive_bat_chg_power = self.instrument.write_register(13881, 0, 0, 6, False)  # for 1phase=3 for 3phase its 14
        time.sleep(5)
        print('Battery stopped using new 1ph method 1')
    def StopBat1phMethod2(self):
        self.Device_Control_Enable = self.instrument.write_register(13895, 14, 0, 6, False)
        time.sleep(5)
        self.Agingmode = self.instrument.write_register(13896, 0, 0, 6, False)  # for 1phase=3 for 3phase its 14
        time.sleep(5)
        self.Aging_sell_power_limit = self.instrument.write_register(13899, 0, 0, 6, False)  # for 1phase=3 for 3phase its 14
        time.sleep(5)
        self.Aging_bat_disch_limit = self.instrument.write_register(13897, 0, 0, 6, False)  # for 1phase=3 for 3phase its 14
        time.sleep(5)
        self.Aging_bat_chg_limit = self.instrument.write_register(13898, 0, 0, 6, False)  # for 1phase=3 for 3phase its 14
        time.sleep(5)
        print('Battery stopped using new 1ph method 2')
    def StopBat1phMethod2DISABLE(self):
        # self.Agingmode = self.instrument.write_register(13896, 1, 0, 6, False)  # for 1phase=3 for 3phase its 14
        # time.sleep(5)
        # self.Aging_sell_power_limit = self.instrument.write_register(13899, 1100, 0, 6, False)  # for 1phase=3 for 3phase its 14
        # time.sleep(5)
        # self.Aging_bat_disch_limit = self.instrument.write_register(13897, 1100, 0, 6, False)  # for 1phase=3 for 3phase its 14
        # time.sleep(5)
        # self.Aging_bat_chg_limit = self.instrument.write_register(13898, 1100, 0, 6, False)  # for 1phase=3 for 3phase its 14
        # time.sleep(5)
        self.Device_Control_Enable = self.instrument.write_register(13895, 3, 0, 6, False)
        time.sleep(5)
        print('Battery stopped using new 1ph method 2')

            

    def read_registers(self):
        self.type_model = self.instrument.read_register(36608,0,3,False) 
        self.rated_power = self.instrument.read_register(36609,0,3,False)
       

    #Electricity generation:
        
        self.DC1_voltage = self.instrument.read_register(16497,0,3,False) 
        self.DC1_current = self.instrument.read_register(16498,0,3,False) 
        self.DC1_power = self.instrument.read_register(16499,0,3,False) 

        self.DC2_voltage = self.instrument.read_register(16500,0,3,False) 
        self.DC2_current = self.instrument.read_register(16501,0,3,False) 
        self.DC2_power = self.instrument.read_register(16502,0,3,False) 

        self.DC3_voltage = self.instrument.read_register(16503,0,3,False) 
        self.DC3_current = self.instrument.read_register(16504,0,3,False) 
        self.DC3_power = self.instrument.read_register(16505,0,3,False) 
     
        self.DC4_voltage = self.instrument.read_register(16506,0,3,False) 
        self.DC4_current = self.instrument.read_register(16507,0,3,False) 
        self.DC4_power = self.instrument.read_register(16508,0,3,False) 

        self.AC1_voltage = self.instrument.read_register(16433,0,3,False) 
        self.AC1_current = self.instrument.read_register(16434,0,3,False) 
        self.AC1_frequency = self.instrument.read_register(16435,0,3,False) 

        self.AC2_voltage = self.instrument.read_register(16440,0,3,False) 
        self.AC2_current = self.instrument.read_register(16441,0,3,False) 
        self.AC2_frequency = self.instrument.read_register(16442,0,3,False) 

        self.AC3_voltage = self.instrument.read_register(16447,0,3,False) 
        self.AC3_current = self.instrument.read_register(16448,0,3,False) 
        self.AC3_frequency = self.instrument.read_register(16449,0,3,False) 

    #Power grid
        
        self.AC1_Power = self.instrument.read_register(16437,0,3,True)
        self.AC2_Power = self.instrument.read_register(16444,0,3,True) 
        self.AC3_Power = self.instrument.read_register(16451,0,3,True)
        
    #size 2: (next 6 data names)    
        self.Cumulative_production = self.instrument.read_long(16581,3,False,0) 
        self.Daily_production = self.instrument.read_long(16575,3,False,0) 

        self.Cumulative_grid_feedin = self.instrument.read_long(16629,3,False,0) 
        self.Daily_grid_feedin = self.instrument.read_long(16623,3,False,0) 
        
        self.Cumulative_energy_purchased = self.instrument.read_long(16637,3,False,0) 
        self.Daily_energy_purchased = self.instrument.read_long(16631,3,False,0) 


        
    #Battery
        self.Device_Control_Enable1 =  self.instrument.read_register(13895,0,3,False) #Set 0X3647 as 0X0E - SET 13895 to 14
        self.charge_dicharge1 =  self.instrument.read_register(13896,0,3,False)
        self.Charge_power1 =  self.instrument.read_register(13900,0,3,False) 
        self.DisCharge_power1 =  self.instrument.read_register(13899,0,3,False) 

        self.VBAT = self.instrument.read_register(16489, 0, 3, False)
        self.ABAT = self.instrument.read_register(16490, 0, 3, True)
        self.PBAT = self.instrument.read_register(16493, 0, 3, True)
        self.SOCBAT = self.instrument.read_register(16495, 0, 3, False)
        
    #size 2: (next 4 data names)    
        
        self.TOTALCHARGE = self.instrument.read_long(16589,3,False,0) 
        self.TODAYCHARGE = self.instrument.read_long(16583,3,False,0) 

        self.TOTALDIS = self.instrument.read_long(16597,3, False, 0)
        self.TODAYDIS = self.instrument.read_long(16591,3, False, 0)

        self.Metermodeset = self.instrument.read_register(16432, 0, 3, False)

        self.TEMP = self.instrument.read_register(16400, 0, 3, False)
        self.BATTEMP = self.instrument.read_register(16494, 0, 3, False)

        
        self.UpperBat_soc = self.instrument.read_register(16425, 0, 3, False)
        self.LowerBat_soc = self.instrument.read_register(16426, 0, 3, False)
        
        self.Bat_DOD = self.instrument.read_register(16427, 0, 3, False)
        self.Bat_Res_soc = self.instrument.read_register(16428, 0, 3, False)
        
        self.Meter_mode_set = self.instrument.read_register(16429, 0, 3, False)

        self.BMSWorkStatus = self.instrument.read_register(16423, 0, 3, False) 
        self.InverterWorkMode = self.instrument.read_register(16388, 0, 3, False)
        self.SetAppMode = self.instrument.read_register(16418, 0, 3, False)
        self.BatProtocolSet = self.instrument.read_register(16424, 0, 3, False)
                                          
    def tabulate(self):
            self.read_registers()
            self.table = [['Name','Adress (dec)','Adress (hex)','Raw data','How to display','Unit'],
#Basic information
             ['rated_power','36609','8F01',self.rated_power,self.rated_power/1000,'KW'],
             ['type_model','36608','8F00',self.type_model,self.type_model,'-'],
#Electricity generation

             ['DC1_voltage','16497','4071',self.DC1_voltage,self.DC1_voltage/10,'V'],
             ['DC1_current','16498','4072',self.DC1_current,self.DC1_current/100,'A'],
             ['DC1_power','16499','4073',self.DC1_power,self.DC1_power,'W'],

             ['DC2_voltage','16500','4074',self.DC2_voltage,self.DC2_voltage/10,'V'],
             ['DC2_current','16501','4075',self.DC2_current,self.DC2_current/100,'A'],
             ['DC2_power','16502','4076',self.DC2_power,self.DC2_power,'W'],

             ['DC3_voltage','16503','4077',self.DC3_voltage,self.DC3_voltage/10,'V'],
             ['DC3_current','16504','4078',self.DC3_current,self.DC3_current/100,'A'],
             ['DC3_power','16505','4079',self.DC3_power,self.DC3_power,'W'],

             ['DC4_voltage','16506','4080',self.DC4_voltage,self.DC4_voltage/10,'V'],
             ['DC4_current','16507','4081',self.DC4_current,self.DC4_current/100,'A'],
             ['DC4_power','16508','4082',self.DC4_power,self.DC4_power,'W'],

             ['AC1_voltage','16433', '4031',self.AC1_voltage,self.AC1_voltage/10,'V'],
             ['AC1_current','164534','4032',self.AC1_current,self.AC1_current/100,'A'],
             ['AC1_frequency','16435','4033',self.AC1_frequency,self.AC1_frequency/100,'Hz'],

             ['AC2_voltage','16440','4038',self.AC2_voltage,self.AC2_voltage/10,'V'],
             ['AC2_current','16441','4039',self.AC2_current,self.AC2_current/100,'A'],
             ['AC2_frequency','16442','403A',self.AC2_frequency,self.AC2_frequency/100,'Hz'],

             ['AC3_voltage','16447','403F',self.AC3_voltage,self.AC3_voltage/10,'V'],
             ['AC3_current','16448','4040',self.AC3_current,self.AC3_current/100,'A'],
             ['AC3_frequency','16449','4041',self.AC3_frequency,self.AC3_frequency/100,'Hz'],
#Power grid
             ['AC1_Power','16437','4035',self.AC1_Power,self.AC1_Power,'W'],
             ['AC2_Power','16444','403C',self.AC2_Power,self.AC2_Power,'W'],
             ['AC3_Power','16451','4043',self.AC3_Power,self.AC3_Power,'W'],

             ['Cumulative_production','16581-82','40C5',self.Cumulative_production,self.Cumulative_production/100,'kWh'],
             ['Daily_production','16575-76','40BF',self.Daily_production,self.Daily_production/100,'kWh'],

             ['Cumulative_grid_feedin','16629-30','40F5',self.Cumulative_grid_feedin,self.Cumulative_grid_feedin/100,'kWh'],
             ['Daily_grid_feedin','16623-24','40EF',self.Daily_grid_feedin,self.Daily_grid_feedin/100,'kWh'],

             ['Cumulative_energy_purchased','16637-38','40FD',self.Cumulative_energy_purchased,self.Cumulative_energy_purchased/100,'kWh'],
             ['Daily_energy_purchased','16631-32','40F7',self.Daily_energy_purchased,self.Daily_energy_purchased/100,'kWh'],
#BATTERY
             ['App Mode','13895','3647',self.Device_Control_Enable1,self.Device_Control_Enable1, '-'],
             ['charge_dicharge1','13896','3648',self.charge_dicharge1,self.charge_dicharge1,'-'],
             ['Charge_power1','13900','364C',self.Charge_power1,self.Charge_power1/10, '%'],
             ['DisCharge_power1','13899','364B',self.DisCharge_power1,self.DisCharge_power1/10,'%'],

             ['Bat voltage','16489','4069',self.VBAT,self.VBAT/10, 'V'],
             ['Bat current','16490','406A',self.ABAT,self.ABAT/100,'A'],
             ['Bat Power','16493','406D',self.PBAT,-self.PBAT, 'W'],
             ['Bat SOC','16495','406F',self.SOCBAT,self.SOCBAT/100,'%'],

             ['TOTALCHARGE','16589-90','40CD',self.TOTALCHARGE,(self.TOTALCHARGE)/100,'kWh'],
             ['TODAYCHARGE','16583-984','40C7',self.TODAYCHARGE,(self.TODAYCHARGE)/100,'kWh'],
             ['TOTALDIS','165897-98','40D5',self.TOTALDIS,(self.TOTALDIS)/100,'kWh'],
             ['TODAYDIS','165891-92','40CF',self.TODAYDIS,(self.TODAYDIS)/100,'kWh'],

             ['Bat temperature','16494','406E',self.BATTEMP,(self.BATTEMP/10),'C'],
             ['Cabinet_Temperature','16400','4010',self.TEMP,self.TEMP/10,'C'],
             ['UpperBat_soc','16425','4029',self.UpperBat_soc  ,self.UpperBat_soc ,'-'],
             ['LowerBat_soc','16426','402A',self.LowerBat_soc ,self.LowerBat_soc, '-'],

             ['Bat_DOD','16427','402B',self.Bat_DOD,self.Bat_DOD,'-'],
             ['Bat_Res_soc','16428','402C',self.Bat_Res_soc ,self.Bat_Res_soc,'-'],

             ['Meter_mode_set ','16429','402D',self.Meter_mode_set ,self.Meter_mode_set ,'-'],

             ['BMSWorkStatus','16423','4027',self.BMSWorkStatus,self.BMSWorkStatus,'-'],
             ['InverterWorkMode','16388','4004',self.InverterWorkMode,self.InverterWorkMode,'-'],
             ['SetAppMode','16418','4022',self.SetAppMode,self.SetAppMode,'-'],
             ['BatProtocolSet','16424','4028',self.BatProtocolSet,self.BatProtocolSet,'-']]
            print(tabulate(self.table, tablefmt='fancy_grid'))

class Growatt_TLXH_RTU:
    
    def __init__(self,COM):
        self.instrument=minimalmodbus.Instrument(COM, 1, debug= False)
        initialize_RTU(self,9600,8,1,10,1)
            
    def read_registers(self):
       
        self.INVSTATE = self.instrument.read_register(3000, 0, 3, False)
        time.sleep(0.5)
        self.BMSSTATE = self.instrument.read_register(3212, 0, 4, False)
        time.sleep(0.5)
        self.PRIORITY = self.instrument.read_register(118, 0, 4, False)
        time.sleep(0.5)
        self.VDC1 = self.instrument.read_register(3003, 1, 4, False)
        time.sleep(0.5)
        self.IDC1 = self.instrument.read_register(3004, 1, 4, False)
        time.sleep(0.5)
        self.PDC1 = self.instrument.read_register(3006, 1, 4, False)
        time.sleep(0.5)
        self.VDC2 = self.instrument.read_register(3007, 1, 4, False)
        time.sleep(0.5)
        self.IDC2 = self.instrument.read_register(3008, 1, 4, False)
        time.sleep(0.5)
        self.PDC2 = self.instrument.read_register(3010, 1, 4, False)
        time.sleep(0.5)
        self.INPUTPOWER = self.instrument.read_register(3002, 1, 4, False) #2 SPH
        time.sleep(0.5)
        self.OUTPUTPOWER = self.instrument.read_register(3024, 1, 4, True) #36 SPH
        time.sleep(0.5)
        self.VL1 = self.instrument.read_register(3026, 1, 4, False) 
        time.sleep(0.5)
        self.AL1 = self.instrument.read_register(3027, 1, 4, False) 
        time.sleep(0.5)
        self.FAC = self.instrument.read_register(3025, 2, 4, False) 
        time.sleep(0.5)
        self.ETODAY = self.instrument.read_register(3050, 1, 4, False) 
        time.sleep(0.5)
        self.ETOTAL = self.instrument.read_register(3052, 1, 4, False) 
        time.sleep(0.5)
        self.PURTODAY = self.instrument.read_register(3134, 1, 4, False)
        time.sleep(0.5)
        self.PURTOTAL = self.instrument.read_register(3136, 1, 4, False)
        time.sleep(0.5)
        self.FEEDINTODAY = self.instrument.read_register(3072, 1, 4, False)
        time.sleep(0.5)
        self.FEEDINTOTAL = self.instrument.read_register(3074, 1, 4, False)
        time.sleep(0.5)
        self.PBATCHARGE = self.instrument.read_register(3181, 1, 4, False)
        time.sleep(0.5)
        self.PBATDIS = self.instrument.read_register(3179, 1, 4, False)
        time.sleep(0.5)
        self.VBAT = self.instrument.read_register(3216, 2, 4, False)
        time.sleep(0.5)
        self.ABAT = self.instrument.read_register(3170, 2, 4, False)
        time.sleep(0.5)
        self.SOCBAT = self.instrument.read_register(3171, 0, 4, False)
        time.sleep(0.5)
        self.TODAYCHARGE = self.instrument.read_register(3130, 0, 4, False)
        time.sleep(0.5)
        self.TOTALCHARGE = self.instrument.read_register(3132, 0, 4, False)
        time.sleep(0.5)
        self.TODAYDIS = self.instrument.read_register(3126, 0, 4, False)
        time.sleep(0.5)
        self.TOTALDIS = self.instrument.read_register(3128, 0, 4, False)
        time.sleep(0.5)
        self.TEMP = self.instrument.read_register(3093, 1, 4, False)
        time.sleep(0.5)
        self.BATTEMP = self.instrument.read_register(3176, 1, 4, False)
        time.sleep(0.5)

    def tabulate(self):
        self.read_registers()
        self.table1 = [['Register naam', 'Register waarde','Eenheid'],
         ['Inverter state', self.INVSTATE,'0x00: waitingmodule0x01: Self-testmode,0x03:faultmodule0x04:flashmodule0x05|0x06|0x07|0x08:normalmodule'],
         ['BMSSTATE', self.BMSSTATE,'-'],
         ['PRIORITY', self.PRIORITY,'0.Load/1.Battery/2.Grid'],
         ['DC1 voltage', self.VDC1, 'V'],
         ['DC1 current', self.IDC1, 'A'],
         ['DC1 power',self.PDC1, 'W'],
         ['DC2 voltage', self.VDC2, 'V'],
         ['DC2 current', self.IDC2, 'A'], ['DC2 power',self.PDC2, 'W'],
         ['TOTAL DC INPUT POWER',self.INPUTPOWER, 'W'],
         ['TOTAL AC OUTPUT POWER',self.OUTPUTPOWER, 'W'],
         ['L1 Voltage',self.VL1, 'V'],
         ['L1 Amperage', self.AL1, 'A'],
         ['Freqeuentie', self.FAC, 'Hz'],
         ['Daily production',self.ETODAY, 'kWh'],
         ['Cumulative production',self.ETOTAL, 'kWh'],
         ['Daily purchased',self.PURTODAY, 'kWh'],
         ['Total purchased',self.PURTOTAL, 'kWh'],
         ['Daily grid feed-in',self.FEEDINTODAY, 'kWh'],
         ['Total grid feed-in',self.FEEDINTOTAL, 'kWh'],
         ['Battery charge power',self.PBATCHARGE, 'W'],
         ['Battery discharge power',self.PBATDIS, 'W'],
         ['Battery voltage',self.VBAT, 'V'],
         ['Battery current',self.ABAT, 'A'],
         ['Battery capacity',self.SOCBAT, '%'],
         ['Daily charging energy',self.TODAYCHARGE, 'kWh'],
         ['Total charging energy',self.TOTALCHARGE, 'kWh'],
         ['Daily discharging energy',self.TODAYDIS, 'kWh'],
         ['Total discharging energy',self.TOTALDIS, 'kWh'],
         ['Temperatuur omvormer', self.TEMP, 'C'],
         ['Temperatuur batterij', self.BATTEMP, 'C']]
        print(tabulate(self.table1, headers='firstrow', tablefmt='fancy_grid'))      

    def configure(self):
        GridExportMaxPower=self.instrument.write_register(3,100,0,6,False) #[0-100%]
        time.sleep(5)
        batFirstStopSOC = self.instrument.write_register(3048, 100, 0, 6, False) #Now 99%: Stop Charge SOC When Bat First 1%. Range=[0,100]
        time.sleep(5)
        GridFirstStopSOC = self.instrument.write_register(3037, 5, 0, 6, False) # Now 20%: Stop Discharge SOC When Grid First. Range=[0,100]
        time.sleep(5)
        print('- Inverter and battery settings are configured')      

    def charge(self,charge_power):
        BatFirstPowerRate = self.instrument.write_register(3047, charge_power, 0, 6, False) #Now 99%: Charge Power Rate When Bat First 1%. Range=[0,100]
        time.sleep(5)
        ACChargeSwitch = self.instrument.write_register(3049, 1, 0, 6, False) #Now enabled: [0 disable, 1 enable]
        time.sleep(5)
        BatFirstEnable1 = self.instrument.write_register(3038, 40960, 0, 6, False) #Now enable: [0 disable, 1 enable]
        time.sleep(5)
        BatFirstEnable2 = self.instrument.write_register(3039, 5947, 0, 6, False) #Now enable: [0 disable, 1 enable]
        time.sleep(5)
        print('- Battery is charging with {}%'.format(charge_power))

    def discharge(self,discharge_power):
        GridFirstDischargePowerRate = self.instrument.write_register(3036, discharge_power, 0, 6, False) #Now 99%: Discharge Power Rate When Grid First 1%. Range=[0,100]
        time.sleep(5)
        GridFirstEnable = self.instrument.write_register(3038,49152,0,6,False) #Now enable: [0 disable, 1 enable]
        time.sleep(5)
        GridFirstEnable2 = self.instrument.write_register(3039,5947,0,6,False)
        print('- Battery is discharging with {}%'.format(discharge_power))

    def stop(self):
        ACChargeSwitch = self.instrument.write_register(3049, 0, 0, 6, False) #Now disabled: [0 disable, 1 enable]
        time.sleep(5)
        GridFirstDischargePowerRate = self.instrument.write_register(3036, 1, 0, 6, False)
        time.sleep(5)
        BatFirstPowerRate = self.instrument.write_register(3047, 1, 0, 6, False)
        time.sleep(5)
        DisableGridandBatFirst1=self.instrument.write_register(3038, 0, 0, 6, False)
        time.sleep(5)
        DisableGridandBatFirst2=self.instrument.write_register(3039, 0, 0, 6, False)        
        print('Inverter has stopped with charging or discharging')

    def stopgrid():
        GridExportMaxPower=self.instrument.write_register(3,0,0,6,False) #[0-100%]
        time.sleep(5)
        ACChargeSwitch = self.instrument.write_register(3049, 0, 0, 6, False) #Now enabled: [0 disable, 1 enable]
        time.sleep(5)
        
class Sungrow_Hybrid_RTU():
    def __init__(self, COM):
        self.instrument = minimalmodbus.Instrument(COM, 1, debug=False)
        initialize_RTU(self, 9600, 8, 1, 10, 1)
    def read_registers(self):

        self.DC1_voltage = self.instrument.read_register(5010, 0, 4, False)  #
        self.DC1_current = self.instrument.read_register(5011, 0, 4, False)  #
        self.DC2_voltage = self.instrument.read_register(5012, 0, 4, False)  #
        self.DC2_current = self.instrument.read_register(5013, 0, 4, False)  #
        self.TotalDCinputpower = self.instrument.read_register(5016, 0, 4, False)  #
        # self.TotalDCinputpower = self.instrument.read_long(5016,4, False, 0)
        self.AC1_voltage = self.instrument.read_register(5018, 0, 4, False)  #
        self.AC1_current = self.instrument.read_register(13030, 0, 4, True)
        self.AC2_voltage = self.instrument.read_register(5019, 0, 4, False)  #
        self.AC2_current = self.instrument.read_register(13031, 0, 4, True)  #
        # self.AC3_voltage = self.instrument.read_register(5020,0,4,False) #
        # self.AC3_current = self.instrument.read_register(35132,0,4,True) #
        self.AC_frequency = self.instrument.read_register(5035, 0, 4, False)  #
        # Power grid
        self.Totalactivepower = self.instrument.read_register(13033, 0, 4, True)
        self.Totaloutputenergy = self.instrument.read_register(5003, 0, 4, False)
        # self.Totalactivepower = self.instrument.read_long(13033,4, True, 0)
        self.Daily_produciton = self.instrument.read_register(13001, 0, 4, False)
        self.Cumulitive_produciton = self.instrument.read_register(13002, 0, 4, False)
        #   self.Cumulitive_produciton = self.instrument.read_long(13002,4, False, 0)
        self.Cumulitive_gridfeedin = self.instrument.read_register(13045, 0, 4, False)
        #   self.Cumulitive_gridfeedin = self.instrument.read_long(13045,4, False, 0)
        self.Daily_grid_feedin = self.instrument.read_register(13044, 0, 4, False)
        self.Cumilitive_energy_purchased = self.instrument.read_register(13036, 0, 4, False)
        # self.Cumilitive_energy_purchased = self.instrument.read_long(13036,4, False, 0)
        self.Daily_energy_purchased = self.instrument.read_register(13035, 0, 4, False)
        # self.Electricty consumption
        self.Totalenergyconsumption = self.instrument.read_register(13017, 0, 4, False)
        #  self.Totalenergyconsumption = self.instrument.read_long(13017,4, False, 0)
        # Battery
        self.PBAT = self.instrument.read_register(13021, 0, 4, True)
        self.VBAT = self.instrument.read_register(13019, 0, 4, True)
        self.ABAT = self.instrument.read_register(13020, 0, 4, True)
        self.SOCBAT = self.instrument.read_register(13022, 0, 4, True)
        self.TODAYCHARGE = self.instrument.read_register(13039, 0, 4, False)
        self.TOTALCHARGE = self.instrument.read_register(13040, 0, 4, False)
        # self.TOTALCHARGE  = self.instrument.read_long(13040,4, False, 0)
        self.TODAYDIS = self.instrument.read_register(13025, 0, 4, False)
        self.TOTALDIS = self.instrument.read_register(13026, 0, 4, False)
        #  self.TOTALDIS = self.instrument.read_long(13026,4, False, 0)
        self.TEMP = self.instrument.read_register(5007, 0, 4, False)
        self.BATTEMP = self.instrument.read_register(13024, 0, 4, False)
        self.Max_Soc = self.instrument.read_register(13057, 0, 4, False)
        self.Min_Soc = self.instrument.read_register(13058, 0, 4, False)

    def tabulate(self):
        self.read_registers()
        self.table = [['DC1_voltage', '5010', self.DC1_voltage, self.DC1_voltage / 10, 'V'],
                 ['DC1_current', '5011', self.DC1_current, self.DC1_current / 10, 'A'],

                 # ['DC2_voltage','5012',self.DC2_voltage,self.DC2_voltage/10,'V'],
                 #  ['DC2_current','5013',self.DC2_current,self.DC2_current/10,'A'],
                 ['TotalDCpower', '5016', self.TotalDCinputpower, self.TotalDCinputpower, 'W'],
                 ['AC1_voltage', '5018', self.AC1_voltage, self.AC1_voltage / 10, 'V'],
                 ['AC1_current', '13030', self.AC1_current, self.AC1_current / 10, 'A'],
                 # ['AC2_voltage','5019',self.AC2_voltage,self.AC2_voltage,'V'],
                 # ['AC2_current','31031',self.AC2_current,self.AC2_current,'A'],
                 # ['AC3_voltage','5020',self.AC3_voltage,self.AC3_voltage,'V'],
                 # ['AC3_current','13032',self.AC3_current,self.AC3_current,'A'],
                 ['AC_frequency', '5035', self.AC_frequency, self.AC_frequency / 10, 'Hz'],
                 # Power grid
                 ['Totaloutputenergy', '5003', self.Totaloutputenergy, self.Totaloutputenergy / 10, 'kWh'],
                 ['Totalactivepower', '13033', self.Totalactivepower, self.Totalactivepower, 'W'],
                 ['Daily_produciton', '13001', self.Daily_produciton, self.Daily_produciton / 10, 'kWh'],
                 ['Cumulitive_produciton', '13002', self.Cumulitive_produciton, self.Cumulitive_produciton / 10, 'kWh'],
                 ['Cumulitive_gridfeedin', '13045', self.Cumulitive_gridfeedin, self.Cumulitive_gridfeedin / 10, 'kWh'],
                 ['Daily_grid_feedin', '13044', self.Daily_grid_feedin, self.Daily_grid_feedin / 10, 'kWh'],
                 ['Cumilitive_energy_purchased', '13036', self.Cumilitive_energy_purchased, self.Cumilitive_energy_purchased / 10,
                  'kWh'],
                 ['Daily_energy_purchased', '13035', self.Daily_energy_purchased, self.Daily_energy_purchased / 10, 'kWh'],
                 # electricity consumption
                 ['Totalenergyconsumption', '13017', self.Totalenergyconsumption, self.Totalenergyconsumption / 10, 'kWh'],
                 # BATTERY READ DATA
                 ['Bat Power', '13021', self.PBAT, self.PBAT, 'W'],
                 ['Bat voltage', '13019', self.VBAT, self.VBAT / 10, 'V'],
                 # ['Bat Voltage Charge','40313',self.Battery_voltage_charge,self.Battery_voltage_charge/100,'V'],
                 ['Bat current', '13020', self.ABAT, self.ABAT / 10, 'A'],
                 # ['Bat Power','40314',self.Battery_power_charge,self.(Battery_power_charge/10),'W'],
                 ['Bat SOC', '13022', self.SOCBAT, self.SOCBAT / 10, '%'],
                 ['TODAYCHARGE', '13039', self.TODAYCHARGE, self.TODAYCHARGE / 10, 'kWh'],
                 ['TOTALCHARGE ', '13040', self.TOTALCHARGE, self.TOTALCHARGE / 10, 'kWh'],
                 # ['Bat Voltage Charge','40313',self.Battery_voltage_charge,self.Battery_voltage_charge/100,'V'],
                 ['TODAYDIS', '13025', self.TODAYDIS, self.TODAYDIS / 10, 'WKh'],
                 # ['Bat Power','40314',self.Battery_power_charge,(self.Battery_power_charge/10),'W'],
                 ['TOTALDIS', '13026', self.TOTALDIS, self.TOTALDIS / 10, 'kWh'],
                 # ['Bat temperature','13024',self.BATTEMP,(self.BATTEMP/10),'C'],
                 ['Max_Soc', '13057', self.Max_Soc, (self.Max_Soc), '%'],
                 ['Min_Soc', '13058', self.Min_Soc, (self.Min_Soc), '%']]
        #  ['Cabinet_Temperature','5007',self.TEMP,self.TEMP/10,'C']]

        print(tabulate(self.table, tablefmt='fancy_grid'))

    def charge(self,charge_power): #Charge power in W
        self.ems_mode = self.instrument.write_register(13049, 2, 0, 6, False)  # 0: Self consumption 2:forced
        time.sleep(3)
        # self.max_soc = self.instrument.write_register(13057, 1000, 0, 6, False)
        # time.sleep(10)
        self.charge = self.instrument.write_register(13050, 170, 0, 6, False)  # diScharge (187), charge(170), stop(204)
        time.sleep(3)
        self.Battery_power = self.instrument.write_register(13051, charge_power, 0, 6, False)  # charge/discharge power
        time.sleep(3)
        print('Charging with ', charge_power, ' [W]')
    def discharge(self,discharge_power): #Discharge power in W
        self.ems_mode = self.instrument.write_register(13049, 2, 0, 6, False)  # 0: Self consumption 2:forced    /  percentage of max charging rate [0,100%] sf=-2
        time.sleep(3)
        self.dicharge = self.instrument.write_register(13050, 187, 0, 6, False)  # diScharge (187), charge(170), stop(204)
        time.sleep(3)
        self.Battery_power = self.instrument.write_register(13051,discharge_power, 0, 6, False)  # charge/discharge power
        time.sleep(3)
        print('Discharging with ',discharge_power, ' [W]')
    def stop(self):
        self.ems_mode = self.instrument.write_register(13049, 0, 0, 6, False)  # percentage of max charging rate [0,100%] sf=-2   0: Self consumption 2:forcded
        time.sleep(10)
        self.charge_dicharge = self.instrument.write_register(13050, 204, 0, 6, False)  # diScharge (187), charge(170), stop(204)
        time.sleep(10)
        self.Battery_power = self.instrument.write_register(13051, 0, 0, 6, False)  # charge/discharge power
        time.sleep(10)
        print('Stopped')

class Solaredge_hybrid_RTU():
    def __init__(self,COM,configure):
        self.instrument = minimalmodbus.Instrument(COM, 1, debug=False)
        initialize_RTU(self,9600,8,1,5,1)
        if configure>0:
            print('Configuring StorEdge inverter...')
            # self.AdvancedPwrControlEn = self.instrument.write_register(61762, 1, 0, 6, False)  # 1:enable, 0:disable (default)
            # time.sleep(5)
            # self.ReactivePwrConfig = self.instrument.write_register(61700, 4, 0, 6, False)  # 0: (Fixed CosPhi mode), 1: ,2: , 3:, 4: (RRCR mode)
            # time.sleep(5)
            # self.Commit_Power_Control_Settings = self.instrument.write_register(61696, 0, 0, 6, False)  #
            # time.sleep(5)
            self.ExportConf_Ctrl = self.instrument.write_register(57344, 0, 0, 6, False)  # 0: disable Export configuration,
            time.sleep(5)
            self.StorageConf_CtrlMode = self.instrument.write_register(57348, 4, 0, 6, False)  # 4: remote, 0-4
            time.sleep(5)
            self.StorageConf_AcChargePolicy = self.instrument.write_register(57349, 1, 0, 6, False)  # 0: disabled, 1: Always allowed, 0-3
            time.sleep(5)
            # self.StorageConf_AcChargeLimit = self.instrument.write_register(57350, 0, 0, 6, False) #0-Max_Float, RELEVANT ONLY FOR SOTRAGE AC CHARGE POLICY MODES 2 AND 3 SO NOT NEEDED
            # time.sleep(25)
            # self.StorageConf_BackupReserved = self.instrument.write_register(57352, 0, 0, 6, False) #0-100%
            # time.sleep(25)
            # default mode when remote control mode has expired
            self.Set_StorageConf_DefaultMode = self.instrument.write_register(57354, 7, 0, 6, False)  # 0:OFF, 1:charges excess pv only,2:charge from pv first before producing ac power, 3:charge from pv+ac to max battery power with priority pv,-7
            time.sleep(5)
            print('Configuration complete.')

    def read_registers(self):
            self.INVSTATE = self.instrument.read_register(40108, 0, 3, False)  ##### Inverter status                   #
            self.BMSSTATE = 0#self.instrument.read_register(57734, 0, 3, False)  ##### Battery status
            #self.WORKMODE = self.instrument.read_register(33132, 0, 3, False)     ##### Workmode / Priority
            self.VDC1 = self.instrument.read_register(40099, 1, 3, False)  ##### DC-input 1 Voltage                #IGEN READS: 98
            self.IDC1 = self.instrument.read_register(40097, 4, 3, False)  ##### DC-input 1 Current                #IGEN READS: 96
            self.PDC1 = self.instrument.read_register(40101, 1, 3, True)  ##### DC-input 1 Power                   #IGEN READS: 100
            # self.VDC2 = self.instrument.read_register(33051, 1, 4, False)         ##### DC-input 2 Voltage
            # self.IDC2 = self.instrument.read_register(33052, 1, 4, False)         ##### DC-input 2 Current
            # self.PDC2 = self.instrument.read_register(10, 1, 4, False)            ##### DC-input 2 Power
            # self.INPUTPOWER = self.instrument.read_long(33057,4, True, 0)         ##### Total DC Input Power
            self.OUTPUTPOWER = self.instrument.read_register(40083, 0, 3, True)  ##### Total AC Output Power              #
            self.VL1 = self.instrument.read_register(40076, 1, 3, False)  ##### Phase 1 Voltage                   #
            self.AL1 = self.instrument.read_register(40073, 3, 3, False)  ##### Phase 1 Current                   #
            self.FAC1 = self.instrument.read_register(40085, 3, 3, False)  ##### Phase 1 Frequency                 #
            self.VL2 = self.instrument.read_register(40077, 1, 3, False)  ##### Phase 2 Voltage                   #
            self.AL2 = self.instrument.read_register(40074, 3, 3, False)  ##### Phase 2 Current                   #
            # self.FAC2 = self.instrument.read_register(40078, 1, 3, False)         ##### Phase 2 Frequency
            self.VL3 = self.instrument.read_register(40078, 1, 3, False)  ##### Phase 3 Voltage                   #
            self.AL3 = self.instrument.read_register(40075, 3, 3, False)  ##### Phase 3 Current                   #
            #self.FAC3 = self.instrument.read_register(40079, 1, 3, False)         ##### Phase 3 Frequency

            # self.ETODAY = self.instrument.read_register(33035, 1, 4, False)       ##### Daily Production
            # self.ETOTAL = self.instrument.read_long(33029,4, True, 0)             ##### Cumulative Production
            # self.PURTODAY = self.instrument.read_register(33171, 1, 4, False)     ##### Daily Energy Purchased
            # self.PURTOTAL = self.instrument.read_long(33169,4, True, 0)           ##### Cumulative Energy Purchased
            # self.FEEDINTODAY = self.instrument.read_register(33175, 1, 4, False)  ##### Daily Grid Feed-in
            # self.FEEDINTOTAL = self.instrument.read_long(33173,4, True, 0)        ##### Cumulative Grid Feed-in

            # self.PBAT1 = self.instrument.read_register(57716, 0, 3, False)  ##### Battery Power
            # self.PBAT2 = self.instrument.read_register(57717, 0, 3, False)  ##### Battery Power
            # self.PBATxx = self.instrument.read_registers(57716, 2, 3)
            # self.PBAT = convert_binair_float32(self.PBATxx[0], self.PBATxx[1])  ##### Battery Power

            # self.PBAT=self.instrument.read_registers(57716,2,3)
            self.PBAT=self.instrument.read_long(57716,3,True)
            # print(self.PBAT)

            # self.VBAT1 = self.instrument.read_register(57712, 0, 4, False)  ##### Battery Voltage
            # self.VBAT2 = self.instrument.read_register(57713, 0, 4, False)  ##### Battery Voltage
            # self.VBATxx = self.instrument.read_registers(57712, 2, 3)
            # self.VBAT = convert_binair_float32(self.VBATxx[0], self.VBATxx[1])  ##### Battery Voltage
            self.VBAT = self.instrument.read_long(57712, 3, True)

            # self.ABAT1 = self.instrument.read_register(57714, 0, 3, False)  ##### Battery Current)
            # self.ABAT2 = self.instrument.read_register(57715, 0, 3, False)  ##### Battery Current
            # self.ABATxx = self.instrument.read_registers(57714, 2, 3)
            # self.ABAT = convert_binair_float32(self.ABATxx[0], self.ABATxx[1])  ##### Battery Current
            self.ABAT = self.instrument.read_long(57714, 3, True)

            # self.SOCBAT1 = self.instrument.read_register(57732, 0, 3, False)  ##### Charge Capacity
            # self.SOCBAT2 = self.instrument.read_register(57733, 0, 3, False)  ##### Charge Capacity
            self.SOCBATxx = self.instrument.read_registers(57732, 2, 3)
            self.SOCBAT = convert_binair_float32(self.SOCBATxx[0], self.SOCBATxx[1])  ##### Charge Capacity

            # self.MAXENERGY1 = self.instrument.read_register(57726, 0, 3, False)  ##### Charge Capacity
            # self.MAXENERGY2 = self.instrument.read_register(57727, 0, 3, False)  ##### Charge Capacity
            self.MAXENERGY = 0#convert_binair_float32(self.MAXENERGY1, self.MAXENERGY2)  ##### Charge Capacity

            # self.AVAILABLEENERGY1 =0# self.instrument.read_register(57728, 0, 3, False)  ##### Charge Capacity
            # self.AVAILABLEENERGY2 = 0#self.instrument.read_register(57729, 0, 3, False)  ##### Charge Capacity
            self.AVAILABLEENERGY = 0#convert_binair_float32(self.AVAILABLEENERGY1, self.AVAILABLEENERGY2)  ##### Charge Capacity

            # self.TODAYCHARGE = self.instrument.read_register(33163, 1, 4, False)  ##### Daily Charging Energy
            # self.TOTALCHARGE = self.instrument.read_long(33161,4, True, 0)        ##### Total Charging Energy
            # self.TODAYDIS = self.instrument.read_register(33167, 1, 4, False)     ##### Daily Discharging Energy
            # self.TOTALDIS = self.instrument.read_long(33165,4, True, 0)           ##### Total Discharging Energy

            self.TEMP = self.instrument.read_register(40103, 2, 3, True)  ##### Temperature- Inverter             #
            # self.BATTEMP1 = self.instrument.read_register(57708, 0, 3, False)  ##### Temperature- Battery
            # self.BATTEMP2 = self.instrument.read_register(57709, 0, 3, False)  ##### Temperature- Battery
            self.BATTEMPxx = self.instrument.read_registers(57708, 2, 3)
            self.BATTEMP = convert_binair_float32(self.BATTEMPxx[0], self.BATTEMPxx[1])  ##### Temperature- Battery

            # self.MAXBATTEMP1 = self.instrument.read_register(57710, 0, 3, False)  ##### Temperature- Battery
            # self.MAXBATTEMP2 = self.instrument.read_register(57711, 0, 3, False)  ##### Temperature- Battery
            self.MAXBATTEMPxx = self.instrument.read_registers(57710, 2, 3)
            self.MAXBATTEMP =convert_binair_float32(self.MAXBATTEMPxx[0], self.MAXBATTEMPxx[1])  ##### Temperature- Battery

            self.Alarmcode1 = self.instrument.read_register(40109, 0, 3, False)  ##### Alarmcode 1                       #
            self.Alarmcode1bat = self.instrument.read_register(57738, 0, 3, False)  ##### Alarmcode 1                       #
            # self.Fault1 = self.instrument.read_register(33096, 1, 3, False)       ##### Fault 1
            #
            self.ACPSF=self.instrument.read_register(40084,0,3,True)
            time.sleep(0.1)
            # self.C_P = self.instrument.read_long(40093,3,False,0)
            # self.C_Pxx = self.instrument.read_registers(40093,2,3)
            # self.C_P=int(convert_dec_int32(self.C_Pxx[0],self.C_Pxx[1]),2)
            self.C_P=self.instrument.read_long(40093,3,False)
            time.sleep(0.1)
            self.ACLSF = self.instrument.read_register(40095, 0, 3, False)
            time.sleep(0.1)
            self.T_D_Exx = self.instrument.read_registers(57718, 4, 3)
            self.T_D_E = int(convert_dec_int32(self.T_D_Exx[1],self.T_D_Exx[0]),2)
            # self.T_D_E=self.instrument.read_long(57718,4,3)
            time.sleep(0.1)
            self.T_C_Exx = self.instrument.read_registers(57722, 4, 3)
            self.T_C_E = int(convert_dec_int32(self.T_C_Exx[1], self.T_C_Exx[0]), 2)
            # self.T_C_E = self.instrument.read_long(57722,4, 3)
            time.sleep(0.1)
            # self.MTEExx = self.instrument.read_registers(40226, 2, 3)
            # print(self.MTEExx)
            # self.MTEE = int(convert_dec_int32(self.MTEExx[0], self.MTEExx[1]), 2)
            self.MTEE=self.instrument.read_long(40226,3,False)
            time.sleep(0.1)
            # self.MTIExx = self.instrument.read_registers(40234, 2, 3)
            # self.MTIE = int(convert_dec_int32(self.MTIExx[0], self.MTIExx[1]), 2)
            self.MTIE=self.instrument.read_long(40234,3,False)
            time.sleep(0.1)
            self.MTRP = self.instrument.read_register(40206,0, 3, True)
            time.sleep(0.1)
            self.MACPSF = self.instrument.read_register(40210, 0, 3, True)
            time.sleep(0.1)

            self.MTEEAxx = self.instrument.read_registers(40243, 2, 3)
            self.MTEEA = int(convert_dec_int32(self.MTEEAxx[0], self.MTEEAxx[1]), 2)
            time.sleep(0.1)
            self.MTIEAxx = self.instrument.read_registers(40251, 2, 3)
            self.MTIEA = int(convert_dec_int32(self.MTIEAxx[0], self.MTIEAxx[1]), 2)
            time.sleep(0.1)

    def tabulate(self):
        self.read_registers()
        self.table = [['Register naam', 'Register waarde', 'Eenheid'],
                 ['Inverter status', self.INVSTATE, '-'],
                 ['BMS Status', self.BMSSTATE, '-'],
                 # ['Workmode / Priority', self.WORKMODE,'-'],
                 ['DC-input 1 Voltage', self.VDC1, 'V'],
                 ['DC-input 1 Current', self.IDC1, 'A'],
                 ['DC-input 1 Power', self.PDC1, 'W'],
                 # ['DC-input 2 Voltage', self.VDC2, 'V'],
                 # ['DC-input 2 Current', self.IDC2, 'A'],
                 # ['DC-input 2 Power',self.PDC2, 'W'],
                 # ['TOTAL DC INPUT POWER',self.INPUTPOWER, 'W'],
                 ['TOTAL AC OUTPUT POWER', self.OUTPUTPOWER, 'W'],
                 ['Phase 1 Voltage', self.VL1, 'V'],
                 ['Phase 1 Current', self.AL1, 'A'],
                 ['Phase 1 Frequency', self.FAC1, 'Hz'],
                 ['Phase 2 Voltage', self.VL2, 'V'],
                 ['Phase 2 Current', self.AL2, 'A'],
                 # ['Phase 2 Frequency', self.FAC2, 'Hz'],
                 ['Phase 3 Voltage', self.VL3, 'V'],
                 ['Phase 3 Current', self.AL3, 'A'],
                 # ['Phase 3 Frequency', self.FAC3, 'Hz'],
                 # ['Daily production',self.ETODAY, 'kWh'],
                 # ['Cumulative production',self.ETOTAL, 'kWh'],
                 # ['Daily purchased',self.PURTODAY, 'kWh'],
                 # ['Total purchased',self.PURTOTAL, 'kWh'],
                 # ['Daily grid feed-in',self.FEEDINTODAY, 'kWh'],
                 # ['Total grid feed-in',self.FEEDINTOTAL, 'kWh'],
                 ['Battery Power', self.PBAT, 'W'],
                 ['Battery Voltage', self.VBAT, 'V'],
                 ['Battery Current', self.ABAT, 'A'],
                 ['Charge Capacity', self.SOCBAT, '%'],
                 ['MAXENERGY', self.MAXENERGY, 'WH'],
                 [' AVAILABLEENERGY', self.AVAILABLEENERGY, 'WH'],
                 # ['Daily charging energy',self.TODAYCHARGE, 'kWh'],
                 # ['Total charging energy',self.TOTALCHARGE, 'kWh'],
                 # ['Daily discharging energy',self.TODAYDIS, 'kWh'],
                 # ['Total discharging energy',self.TOTALDIS, 'kWh'],
                 ['Temperature-Inverter', self.TEMP, 'C'],
                 ['Temperature-Battery', self.BATTEMP, 'C'],
                 ['Maximum Temperature-Battery', self.MAXBATTEMP, 'C'],
                 ['Alarmcode1', self.Alarmcode1, '-'],
                 ['Alarmcode1bat', self.Alarmcode1bat, '-'],
                 ['AC power scale factor', self.ACPSF, '-'],
                 ['AC lifetime energy production', self.C_P],
                 ['AC power energy production scale factor', self.ACLSF],
                 ['Bat lifetime export', self.T_D_E],
                 ['Bat lifetime import', self.T_C_E],
                 ['Meter total export', self.MTEE],
                 ['Meter total import', self.MTIE],
                 ['Meter total real power', self.MTRP],
                 ['Meter AC real power SF', self.MACPSF],
                 ['Meter total export apparent', self.MTEEA],
                 ['Meter total import apparent', self.MTIEA]]

        # Show the Table
        print('Reading data Registers SolarEdge StorEdge')
        print(tabulate(self.table, headers='firstrow', tablefmt='fancy_grid'))
    def charge(self,charge_power): #in [W]
        # self.StorageRemoteCtrl_CommandTimeout = self.instrument.write_register(57355, 86400, 0, 6, False)  # 0-86400(24h)
        # time.sleep(25)
        self.StorageRemoteCtrl_CommandTimeout = self.instrument.write_registers(57355, [1,20864])  # 0-86400(24h)
        time.sleep(5)
        self.StorageRemoteCtrl_CommandMode = self.instrument.write_register(57357, 3, 0, 6, False)  # 0-7 (3:charge full from AC+PV, 4: discharge)
        time.sleep(5)
        # self.StorageRemoteCtrl_ChargeLimit = self.instrument.write_register(53758, charge_power, 0, 6, False)  # 0-Battery Max Power (W)
        # time.sleep(5)
        self.StorageRemoteCtrl_ChargeLimit = self.instrument.write_registers(53758, [0,charge_power])  # 0-Battery Max Power (W)
        time.sleep(5)
        # StorageRemoteCtrl_DischargeLimit = instrument.write_register(57360, 0, 0, 6, False) #0-Battery Max Power
        # time.sleep(5)
        print('Inverter succesfully charging')
    def discharge(self,discharge_power): #in [W]
        self.StorageRemoteCtrl_CommandTimeout = self.instrument.write_register(57355, 86400, 0, 6, False)  # 0-86400(24h)
        time.sleep(5)
        self.StorageRemoteCtrl_CommandMode = self.instrument.write_register(57357, 4, 0, 6, False)  # 0-7 (3:charge full from AC+PV, 4: discharge)
        time.sleep(5)
        # self.StorageRemoteCtrl_ChargeLimit = self.instrument.write_register(57358, 0, 0, 6, False)  # 0-Battery Max Power (W)
        # time.sleep(5)
        StorageRemoteCtrl_DischargeLimit = instrument.write_register(57360, discharge_power, 0, 6, False) #0-Battery Max Power
        time.sleep(5)
        print('Inverter succesfully disharging')
    # def stop(self):

class Huawei_hybrid_RTU():
    def __init__(self,COM, configure,address):
        self.instrument = minimalmodbus.Instrument(COM, 1, debug=False)
        initialize_RTU(self, 9600, 8, 1, 5, address)
        if configure:
            self.MaximumChargingPower = self.instrument.write_long(47075, 3500, False, 0)  # Max. Charge power. Range=[0,Upper treshhold (default 3500)]. Rightnow 2000W
            time.sleep(5)
            self.MaximumDischargingPower = self.instrument.write_long(47077, 3500, False, 0)  # Max. Discharge power. Range=[0,upper treshhold (default 3500)]. Rightnow 2000W
            time.sleep(5)
            self.ChargingCutoffCapacity = self.instrument.write_register(47081, 1000, 0, 6, False)  # MAX SOC. Range=[90,100]. Rightnow 95%
            time.sleep(5)
            self.DischargingCutoffCapacity = self.instrument.write_register(47082, 120, 0, 6, False)  # MIN SOC. Range=[12,20] Right now 20%
            time.sleep(5)
            self.GridChargeCutoffSOC = self.instrument.write_register(47088, 1000, 0, 6, False)  # When charge from grid, MAX SOC. Range=[30,70]. Right now 70%
            time.sleep(5)
            self.ForcibleChargeDischargeSettingMode = self.instrument.write_register(47246, 1, 0, 6, False)  # Work mode battery. Range=[0=time period, 1=Target SOC]. Rightnow Target SOC.
            time.sleep(5)
            self.PowerofChargeFromGrid = self.instrument.write_long(47242, 4000, False, 0)  # Charge power from grid: Formula: Charge Power inverter = PV power + Add the needed power from AC to match forcible charge power. range=[0,2200 (default 2000, but different with every inverter)]
            time.sleep(5)
            print('Inverter succesfully configured')
    def charge(self,charge_power):
        self.ChargeFromGridFunction = self.instrument.write_register(47087, 1, 0, 6, False)  # Inverter can charge from grid, not just PV. Range=[0=disable,1=enable]. Rightnow value 1
        time.sleep(5)
        self.TargetSOC = self.instrument.write_register(47101, 1000, 0, 6, False)  # Target SOC Charge. Range=[0,100]. Right now 950%
        time.sleep(5)
        self.ForcibleChargePower = self.instrument.write_long(47247, charge_power, False, 0)  # Charge power. range=[0,Maximum charge Power]. Right now 2000W
        time.sleep(5)
        self.ForcibleChargeDischarge = self.instrument.write_register(47100, 1, 0, 6, False)  # Inverter modus. Range=[0=disable,1=Charge,2=Discharge]. Rightnow value 1.
        time.sleep(5)
        print('Inverter succesfully Charging')
    def discharge(self,discharge_power):
        self.TargetSOC = self.instrument.write_register(47101, 120, 0, 6, False)  # Target SOC Charge. Range=[0,100]. Right now 950%
        time.sleep(5)
        self.ForcibleChargePower = self.instrument.write_long(47249, discharge_power, False, 0)  # Charge power. range=[0,Maximum charge Power]. Right now 2000W
        time.sleep(5)
        self.ForcibleChargeDischarge = self.instrument.write_register(47100, 2, 0, 6, False)  # Inverter modus. Range=[0=disable,1=Charge,2=Discharge]. Rightnow value 1.
        time.sleep(5)
        print('Inverter succesfully Discharging')
    def stop(self):
        self.ForcibleChargeDischarge = self.instrument.write_register(47100, 0, 0, 6, False)  # Inverter modus. Range=[0=disable,1=Charge,2=Discharge]. Rightnow value 1.
        time.sleep(5)
        self.ChargeFromGridFunction = self.instrument.write_register(47087, 0, 0, 6, False)  # Inverter can charge from grid, not just PV. Range=[0=disable,1=enable]. Rightnow value 1
        time.sleep(5)
        print('Inverter succesfully stopped')
    def read_registers(self):
        self.MaximumChargingPower = self.instrument.read_long(47075, 3, False, 0)
        time.sleep(0.1)
        self.MaximumDischargingPower = self.instrument.read_long(47077, 3, False, 0)
        time.sleep(0.1)
        self.ChargingCutoffCapacity = self.instrument.read_register(47081, 1, 3, False)
        time.sleep(0.1)
        self.DischargingCutoffCapacity = self.instrument.read_register(47082, 1, 3, False)
        time.sleep(0.1)
        self.GridChargeCutoffSOC = self.instrument.read_register(47088, 1, 3, False)
        time.sleep(0.1)
        self.ForcibleChargeDischargeSettingMode = self.instrument.read_register(47246, 0, 3, False)
        time.sleep(0.1)
        self.PowerofChargeFromGrid = self.instrument.read_long(47242, 3, False, 0)
        time.sleep(0.1)
        self.ChargeFromGridFunction = self.instrument.read_register(47087, 0, 3, False)
        time.sleep(0.1)
        self.TargetSOC = self.instrument.read_register(47101, 0, 3, False)
        time.sleep(0.1)
        self.ForcibleChargePower = self.instrument.read_long(47247, 3, False, 0)
        time.sleep(0.1)
        self.ForcibleChargeDischarge = self.instrument.read_register(47100, 0, 3, False)
        time.sleep(0.1)
        self.ForcibleDischargePower = self.instrument.read_long(47249, 3, False, 0)
        time.sleep(0.1)
        self.OUTPUTPOWER = self.instrument.read_long(32080, 3, True, 0)
        time.sleep(0.1)
        self.PBAT = self.instrument.read_long(37004, 3, True, 0)
        # self.PBAT=self.instrument.read_registers(37001, 2, 3)
        # self.PBAT=self.PBATxx[1]
        time.sleep(0.1)
        self.SOCBAT = self.instrument.read_register(37738, 1, 3, False)
        time.sleep(0.1)
        self.L1Volt = self.instrument.read_register(32069, 1, 3, False)
        time.sleep(0.1)
        self.MaxPowerofChargeFromGrid = self.instrument.read_long(47244, 3, False, 0)
        time.sleep(0.1)
        self.WORKMODE = self.instrument.read_register(37006, 0, 3, False)
        time.sleep(0.1)
        self.VDC1 = self.instrument.read_register(32016, 1, 3, True)
        time.sleep(0.1)
        self.IDC1 = self.instrument.read_register(32017, 2, 3, True)
        time.sleep(0.1)
        self.VDC2 = self.instrument.read_register(32018, 1, 3, True)
        time.sleep(0.1)
        self.IDC2 = self.instrument.read_register(32019, 2, 3, True)
        time.sleep(0.1)
        self.INPUTPOWER = self.instrument.read_long(32064, 3, True, 0)
        time.sleep(0.1)
        self.OUTPUTPOWER = self.instrument.read_long(32080, 3, True, 0)

    def tabulate(self):
        self.read_registers()
        self.table = [['Work mode', self.WORKMODE, '-'],
                 ['DC1 voltage', self.VDC1, 'V'],
                 ['DC1 current', self.IDC1, 'A'],
                 ['L1 Voltage', self.L1Volt],
                 ['DC2 voltage', self.VDC2, 'V'],
                 ['DC2 current', self.IDC2, 'A'],
                 ['TOTAL DC INPUT POWER', self.INPUTPOWER, 'W'],
                 ['TOTAL AC OUTPUT POWER', self.OUTPUTPOWER, 'W'], [' MaximumChargingPower', self.MaximumChargingPower, 'W'],
                 [' MaximumDischargingPower', self.MaximumDischargingPower, 'W'],
                 ['ChargingCutoffCapacity ', self.ChargingCutoffCapacity, '%'],
                 ['DischargingCutoffCapacity ', self.DischargingCutoffCapacity, '%'],
                 ['GridChargeCutoffSOC', self.GridChargeCutoffSOC, '%'],
                 [' ForcibleChargeDischargeSettingMode', self.ForcibleChargeDischargeSettingMode, '-'],
                 ['PowerofChargeFromGrid', self.PowerofChargeFromGrid, '-'],
                 [' ChargeFromGridFunction', self.ChargeFromGridFunction, 'W'],
                 ['TargetSOC', self.TargetSOC, '%'],
                 [' ForcibleChargePower', self.ForcibleChargePower, 'W'],
                 ['ForcibleChargeDischarge', self.ForcibleChargeDischarge, '-'],
                 [' ForcibleDischargePower', self.ForcibleDischargePower, 'W'],
                 ['TOTAL AC OUTPUT POWER', self.OUTPUTPOWER, 'W'],
                 ['Power Batterij', self.PBAT, 'W'],
                 ['SOCBAT', self.SOCBAT, '%'],
                 ['MaxPowerofChargeFromGrid', self.MaxPowerofChargeFromGrid, 'W'], ]
        print(tabulate(self.table, headers='firstrow', tablefmt='fancy_grid'))

class Deye_hybrid_RTU():
    def __init__(self, COM):
        self.instrument=minimalmodbus.Instrument(COM,1,debug=False)
        # self.instrument.close_port_after_each_call=True
        initialize_RTU(self,9600,8,1,5,1)

    def configure(self):
        self.all_timeslots=self.instrument.write_registers(148,[0, 600, 1200, 1600, 2000, 2200])
        self.all_time_chg_enable = self.instrument.write_registers(172, [1, 1, 1, 1, 1, 1])
        self.all_time_powers = self.instrument.write_registers(154, [0, 0, 0, 0, 0, 0])

        self.maximum_chg_current = self.instrument.write_register(108, 100, 0, 16, False)
        self.maximum_dischg_current = self.instrument.write_register(109, 100, 0, 16, False)

        # self.remote_control = self.instrument.write_register(60,0,0,16,False)
        # self.battery_charge_type=self.instrument.write_register(98,1,0,16,False)
        # self.maximum_chg_current=self.instrument.write_register(108,100,0,16,False)
        # self.maximum_dischg_current = self.instrument.write_register(109, 100, 0, 16, False)
        # self.mains_to_battery_current=self.instrument.write_register(128, 100, 0, 16, False)
        # self.Energy_management_model = self.instrument.write_register(141, 2, 0, 16, False) #0 bat first / 1 load first
        # self.chg_from_grid_enable = self.instrument.write_register(130, 1, 0, 16, False)
        # self.max_sell_power=self.instrument.write_register(143,8000,0,16,False)

    def idle(self):
        self.all_time_powers = self.instrument.write_registers(154,[0, 0, 0, 0, 0, 0])
        self.all_desired_SOC = self.instrument.write_registers(166, [100, 100, 100, 100, 100, 100])
        self.maximum_chg_current = self.instrument.write_register(108, 0, 0, 16, False)
        self.maximum_dischg_current = self.instrument.write_register(109, 0, 0, 16, False)

        print('Set to idle')

    def charge(self,charge_power):
        self.maximum_chg_current = self.instrument.write_register(108, 100, 0, 16, False)
        self.maximum_dischg_current = self.instrument.write_register(109, 100, 0, 16, False)

        self.all_time_powers = self.instrument.write_registers(154, [charge_power, charge_power, charge_power, charge_power, charge_power, charge_power])
        self.all_desired_SOC = self.instrument.write_registers(166, [100, 100, 100, 100, 100, 100])

        print('Set to charge at',charge_power,'W')

    def discharge(self,discharge_power):
        self.maximum_chg_current = self.instrument.write_register(108, 100, 0, 16, False)
        self.maximum_dischg_current = self.instrument.write_register(109, 100, 0, 16, False)

        self.all_time_powers = self.instrument.write_registers(154, [discharge_power, discharge_power, discharge_power, discharge_power, discharge_power, discharge_power])
        self.all_desired_SOC=self.instrument.write_registers(166,[20,20,20,20,20,20])

        print('Set to discharge at',discharge_power,'W')

    def read_registers(self):
        self.typeinfo=self.instrument.read_register(0,0,3,False)
        time.sleep(0.1)
        self.SN = self.instrument.read_string(3,5,3)
        time.sleep(0.1)

        self.SOCBAT=self.instrument.read_register(214,0,3,False)
        time.sleep(0.1)
        self.BATTEMP = self.instrument.read_register(217, 1, 3, False) - 100
        time.sleep(0.1)
        self.BAT_MANUFACTURER = self.instrument.read_register(229, 0, 3, False)
        time.sleep(0.1)

        self.AL1 = self.instrument.read_register(610, 2, 3, True)
        time.sleep(0.1)
        self.AL2 = self.instrument.read_register(611, 2, 3, True)
        time.sleep(0.1)
        self.AL3 = self.instrument.read_register(612, 2, 3, True)
        time.sleep(0.1)
        self.VL1 = self.instrument.read_register(598, 1, 3, False)
        time.sleep(0.1)
        self.VL2 = self.instrument.read_register(599, 1, 3, False)
        time.sleep(0.1)
        self.VL3 = self.instrument.read_register(600, 1, 3, False)
        time.sleep(0.1)
        self.FAC = self.instrument.read_register(609, 2, 3, False)
        time.sleep(0.1)
        self.PAC = self.instrument.read_register(619, 0, 3, True)
        time.sleep(0.1)

        self.VBAT = self.instrument.read_register(587, 2, 3, False)
        time.sleep(0.1)
        self.PBAT = self.instrument.read_register(590, 0, 3, True)
        time.sleep(0.1)
        self.ABAT = self.instrument.read_register(591, 2, 3, True)
        time.sleep(0.1)

        self.DC1_voltage = self.instrument.read_register(676, 1, 3, False)
        time.sleep(0.1)
        self.DC1_current = self.instrument.read_register(677, 1, 3, False)
        time.sleep(0.1)
        self.DC2_voltage = self.instrument.read_register(678, 1, 3, False)
        time.sleep(0.1)
        self.DC2_current = self.instrument.read_register(679, 1, 3, False)
        time.sleep(0.1)
        self.PDC1 = self.instrument.read_register(672, 0, 3, False)
        time.sleep(0.1)
        self.PDC2 = self.instrument.read_register(673, 1, 3, False)
        time.sleep(0.1)

        self.INVSTATE =  self.instrument.read_register(500, 0, 3, False)
        time.sleep(0.1)
        self.Totaloutputenergy = self.instrument.read_register(504, 1, 3, True)
        time.sleep(0.1)
        self.Todayoutputenergy = self.instrument.read_register(501, 1, 3, True)
        time.sleep(0.1)
        self.FEEDINTOTAL = self.instrument.read_register(505, 1, 3, False)
        time.sleep(0.1)
        self.TODAYDIS = self.instrument.read_register(515, 1, 3, False)
        time.sleep(0.1)
        self.TOTALCHARGE = self.instrument.read_register(516, 1, 3, False)
        time.sleep(0.1)
        self.TODAYCHARGE = self.instrument.read_register(514, 1, 3, False)
        time.sleep(0.1)
        self.TOTALDIS = self.instrument.read_register(518, 1, 3, False)
        time.sleep(0.1)
        self.Daily_energy_purchased = self.instrument.read_register(520, 1, 3, False)
        time.sleep(0.1)
        self.Daily_grid_feedin = self.instrument.read_register(521, 1, 3, False)
        time.sleep(0.1)
        self.PURTOTAL = self.instrument.read_register(522, 1, 3, False)
        time.sleep(0.1)
        self.FEEDINTOTAL = self.instrument.read_register(524, 1, 3, False)
        time.sleep(0.1)
        self.Daily_load_consumption = self.instrument.read_register(526, 1, 3, False)
        time.sleep(0.1)
        self.Total_load_consumption = self.instrument.read_register(527, 1, 3, False)
        time.sleep(0.1)
        self.Daily_production = self.instrument.read_register(529, 1, 3, False)
        time.sleep(0.1)
        self.Total_production = self.instrument.read_register(535, 1, 3, False)
        time.sleep(0.1)

        self.battery_charge_type=self.instrument.read_register(98,0,3,False)
        self.battery_capacity = self.instrument.read_register(102, 0, 3, False)

    def tabulate(self):
        self.read_registers()
        self.table = [['SN', self.SN],
                      ['INV STATE', self.INVSTATE],
                      ['Inv type info', self.typeinfo],
                      ['SOC', self.SOCBAT],
                      ['Battery current', self.ABAT],
                      ['Battery voltage', self.VBAT],
                      ['Battery power', self.PBAT],
                      ['Bat temp', self.BATTEMP],
                      ['Battery Manufacturer', self.BAT_MANUFACTURER],
                      ['Current L1', self.AL1],
                      ['Current L2', self.AL2],
                      ['Current L3', self.AL3],
                      ['Voltage L1', self.VL1],
                      ['Voltage L2', self.VL2],
                      ['Voltage L3', self.VL3],
                      ['Frequency AC', self.FAC],
                      ['Power AC (Total)', self.PAC],
                      ['DC1 voltage', self.DC1_voltage],
                      ['DC1 current', self.DC1_current],
                      ['DC2 voltage', self.DC2_voltage],
                      ['DC2 current', self.DC2_current],
                      ['DC1 power', self.PDC1],
                      ['DC2 power', self.PDC2],
                      ['Total output energy', self.Totaloutputenergy],
                      ['Today output energy',self.Todayoutputenergy],
                      ['FEED IN TOTAL', self.FEEDINTOTAL],
                      ['TODAY CHG',self.TODAYCHARGE],
                      ['TODAY DIS', self.TODAYDIS],
                      ['TOTAL CHARGE BATTERY', self.TOTALCHARGE],
                      ['TOTAL DISCHARGE BATTERY', self.TOTALDIS],
                      ['DAILY ENERGY PURCHASED', self.Daily_energy_purchased],
                      ['DAILY GRID FEED IN', self.Daily_grid_feedin],
                      ['TOTAL ENERGY PURCHASED', self.PURTOTAL],
                      ['TOTAL GRID FEED IN ', self.FEEDINTOTAL],
                      ['Daily_load_consumption', self.Daily_load_consumption],
                      ['Total load consumption', self.Total_load_consumption],
                      ['Daily production', self.Daily_production],
                      ['Total production', self.Total_production],
                      ['Battery charge type [0:lead 1: lithium]',self.battery_charge_type],
                      ['Battery capacity (Ah)',self.battery_capacity]]
        print(tabulate(self.table, headers='firstrow', tablefmt='fancy_grid'))

#DO NOT USE THESE
    def read_timeslots(self):
        print('Time1 =',self.instrument.read_register(148,0,3,False))
        print('Time2 =', self.instrument.read_register(149, 0, 3, False))
        print('Time3 =', self.instrument.read_register(150, 0, 3, False))
        print('Time4 =', self.instrument.read_register(151, 0, 3, False))
        print('Time5 =', self.instrument.read_register(152, 0, 3, False))
        print('Time6 =', self.instrument.read_register(153, 0, 3, False))
    def read_voltage_limits(self):
        print('Time1volt =', self.instrument.read_register(160, 2, 3, False))
        print('Time2volt =', self.instrument.read_register(161, 2, 3, False))
        print('Time3volt =', self.instrument.read_register(162, 2, 3, False))
        print('Time4volt =', self.instrument.read_register(163, 2, 3, False))
        print('Time5volt =', self.instrument.read_register(163, 2, 3, False))
        print('Time6volt =', self.instrument.read_register(165, 2, 3, False))
    def single_time_configure(self):
        self.remote_control = self.instrument.write_register(60,0,0,16,False)
        self.battery_charge_type=self.instrument.write_register(98,1,0,16,False)
        self.maximum_chg_current=self.instrument.write_register(108,100,0,16,False)
        self.maximum_dischg_current = self.instrument.write_register(109, 100, 0, 16, False)
        self.mains_to_battery_current=self.instrument.write_register(128, 100, 0, 16, False)
        self.Energy_management_model = self.instrument.write_register(141, 2, 0, 16, False) #0 bat first / 1 load first
        self.chg_from_grid_enable = self.instrument.write_register(130, 1, 0, 16, False)
        self.max_sell_power=self.instrument.write_register(143,8000,0,16,False)

        self.time1 = self.instrument.write_register(148, 0, 0, 16, False)
        time.sleep(0.1)
        self.time2 = self.instrument.write_register(149, 2355, 0, 16, False)
        time.sleep(0.1)
        self.time3 = self.instrument.write_register(150, 0, 0, 16, False)
        time.sleep(0.1)
        self.time4 = self.instrument.write_register(151, 0, 0, 16, False)
        time.sleep(0.1)
        self.time5 = self.instrument.write_register(152, 0, 0, 16, False)
        time.sleep(0.1)
        self.time6 = self.instrument.write_register(153, 0, 0, 16, False)
        time.sleep(0.1)

        self.time1_chg_enable = self.instrument.write_register(172, 1, 0, 16, False)
        time.sleep(0.1)
        self.time2_chg_enable = self.instrument.write_register(173, 1, 0, 16, False)
        time.sleep(0.1)
        self.time3_chg_enable = self.instrument.write_register(174, 1, 0, 16, False)
        time.sleep(0.1)
        self.time4_chg_enable = self.instrument.write_register(175, 1, 0, 16, False)
        time.sleep(0.1)
        self.time5_chg_enable = self.instrument.write_register(176, 1, 0, 16, False)
        time.sleep(0.1)
        self.time6_chg_enable = self.instrument.write_register(177, 1, 0, 16, False)
        time.sleep(0.1)

        self.time1power = self.instrument.write_register(154, 0, 0, 16, False)
        time.sleep(0.1)
        self.time2power = self.instrument.write_register(155, 0, 0, 16, False)
        time.sleep(0.1)
        self.time3power = self.instrument.write_register(156, 0, 0, 16, False)
        time.sleep(0.1)
        self.time4power = self.instrument.write_register(157, 0, 0, 16, False)
        time.sleep(0.1)
        self.time5power = self.instrument.write_register(158, 0, 0, 16, False)
        time.sleep(0.1)
        self.time6power = self.instrument.write_register(159, 0, 0, 16, False)
        time.sleep(0.1)
    def single_time_charge(self, single_charge_power):
        self.time1power = self.instrument.write_register(154, single_charge_power, 0, 16, False)
        time.sleep(0.1)
        self.time1_desired_SOC = self.instrument.write_register(166, 100, 0, 16, False)
        time.sleep(0.1)
        self.time1 = self.instrument.write_register(148, 0, 0, 16, False)
        time.sleep(0.1)
        self.time2 = self.instrument.write_register(149, 2355, 0, 16, False)
        time.sleep(0.1)
    def single_time_discharge(self, single_discharge_power):
        self.time1power = self.instrument.write_register(154, single_discharge_power, 0, 16, False)
        time.sleep(0.1)
        self.time1_desired_SOC = self.instrument.write_register(166, 20, 0, 16, False)
        time.sleep(0.1)
        self.time1 = self.instrument.write_register(148, 0, 0, 16, False)
        time.sleep(0.1)
        self.time2 = self.instrument.write_register(149, 2355, 0, 16, False)
        time.sleep(0.1)

class Growatt_SPH_RTU():
    def __init__(self,COM):
        self.instrument = minimalmodbus.Instrument(COM, 1, debug=False)
        initialize_RTU(self, 9600, 8, 1, 3, 1)
    def configure(self):
        self.batFirstStopSOC = self.instrument.write_register(1091, 99, 0, 6, False)  # Now 99%: Stop Charge SOC When Bat First 1%. Range=[0,100]
        time.sleep(5)
        self.GridFirstStopSOC = self.instrument.write_register(1071, 5, 0, 6, False)  # Now 20%: Stop Discharge SOC When Grid First. Range=[0,100]
        time.sleep(5)
        self.GridFirstStart = self.instrument.write_register(1080, 0, 0, 6, False) #Now 00:00    High Bit 0-23 low bit 0-59
        time.sleep(5)
        self.GridFirstStop = self.instrument.write_register(1081, 5947, 0, 6, False) #Now 23:59  High Bit 0-23 low bit 0-59 (See Excel document how this is calculated)
        time.sleep(5)
        self.BatFirstStart = self.instrument.write_register(1100, 0, 0, 6, False) #Now 00:00    High Bit 0-23 low bit 0-59
        time.sleep(5)
        self.BatFirstStop = self.instrument.write_register(1101, 5947, 0, 6, False) #Now 23:59  High Bit 0-23 low bit 0-59 (See Excel document how this is calculated)
        time.sleep(5)
        self.LoadFirstStart = self.instrument.write_register(1110, 0, 0, 6,False)  # Now 00:00    High Bit 0-23 low bit 0-59
        time.sleep(5)
        self.LoadFirstStop = self.instrument.write_register(1111, 5947, 0, 6,False)  # Now 23:59  High Bit 0-23 low bit 0-59 (See Excel document how this is calculated)
        time.sleep(5)
        print('- Inverter and battery settings are configured')

    def self_consumption(self):
        self.BatFirstEnable = self.instrument.write_register(1102, 0, 0, 6,False)  # Now disabled, because we want to discharge: [0 disable, 1 enable]
        time.sleep(5)
        self.GridFirstEnable = self.instrument.write_register(1082, 0, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        self.LoadFirstEnable = self.instrument.write_register(1112, 1, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        print('- Self-consumption')

    def stop(self):
        self.ACChargeSwitch = self.instrument.write_register(1092, 0, 0, 6, False)  # Now disabled:  [0 disable, enable]
        time.sleep(5)
        self.BatFirstEnable = self.instrument.write_register(1102, 0, 0, 6, False)  # Now disabled: [0 disable, 1 enable]
        time.sleep(5)
        self.GridFirstEnable = self.instrument.write_register(1082, 0, 0, 6, False)  # Now disabled: [0 disable, enable]
        time.sleep(5)
        print('- Inverter has stopped with charging or discharging')
        time.sleep(0.1)
    def charge(self,charge_power):
        self.BatFirstPowerRate = self.instrument.write_register(1090, charge_power, 0, 6, False)  # Now 99%: Charge Power Rate When Bat First 1%. Range=[0,100]
        time.sleep(5)
        self.ACChargeSwitch = self.instrument.write_register(1092, 1, 0, 6, False)  # Now enabled: [0 disable, 1 enable]
        time.sleep(5)
        self.LoadFirstEnable = self.instrument.write_register(1112, 0, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        self.GridFirstEnable = self.instrument.write_register(1082, 0, 0, 6, False)  # Now disabled, because we want to charge: [0 disable, 1 enable]
        time.sleep(5)
        self.BatFirstEnable = self.instrument.write_register(1102, 1, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        print('- Battery is charging with {}%'.format(charge_power))
    def discharge(self,discharge_power):
        self.GridFirstStopSOC = self.instrument.write_register(1071, 20, 0, 6, False)  # Now 20%: Stop Discharge SOC When Grid First. Range=[0,100]
        time.sleep(5)
        self.GridFirstDischargePowerRate = self.instrument.write_register(1070, discharge_power, 0, 6, False)  # Now 99%: Discharge Power Rate When Grid First 1%. Range=[0,100]
        time.sleep(5)
        self.LoadFirstEnable = self.instrument.write_register(1112, 0, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        self.BatFirstEnable = self.instrument.write_register(1102, 0, 0, 6, False)  # Now disabled, because we want to discharge: [0 disable, 1 enable]
        time.sleep(5)
        self.GridFirstEnable = self.instrument.write_register(1082, 1, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        print('- Battery is discharging with {}%'.format(discharge_power))
    def idle_timeslots(self):
        self.BatFirstEnable = self.instrument.write_register(1102, 0, 0, 6,False)  # Now disabled, because we want to discharge: [0 disable, 1 enable]
        time.sleep(5)
        self.GridFirstEnable = self.instrument.write_register(1082, 0, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        self.LoadFirstEnable = self.instrument.write_register(1112, 1, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        self.LoadFirstStart = self.instrument.write_register(1110, 0, 0, 6, False)  # Now 00:00    High Bit 0-23 low bit 0-59
        time.sleep(5)
        self.LoadFirstStop = self.instrument.write_register(1111, 1, 0, 6, False)  # Now 23:59  High Bit 0-23 low bit 0-59 (See Excel document how this is calculated)
        time.sleep(5)
    def idle_targetsoc_disch(self):
        self.BatFirstEnable = self.instrument.write_register(1102, 0, 0, 6,False)  # Now disabled, because we want to discharge: [0 disable, 1 enable]
        time.sleep(5)
        self.GridFirstEnable = self.instrument.write_register(1082, 0, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        self.LoadFirstEnable = self.instrument.write_register(1112, 1, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        self.GridFirstStopSOC = self.instrument.write_register(1071, 100, 0, 6, False)  # Now 20%: Stop Discharge SOC When Grid First. Range=[0,100]
        time.sleep(5)
        self.batFirstStopSOC = self.instrument.write_register(1091, 10, 0, 6, False)  # Now 99%: Stop Charge SOC When Bat First 1%. Range=[0,100]
        time.sleep(5)
        print('IDLE mode')
    def idle_targetsoc_chg(self):
        self.LoadFirstEnable = self.instrument.write_register(1112, 0, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        self.GridFirstEnable = self.instrument.write_register(1082, 0, 0, 6, False)  # Now enable: [0 disable, 1 enable]
        time.sleep(5)
        self.BatFirstEnable = self.instrument.write_register(1102, 1, 0, 6,False)  # Now disabled, because we want to discharge: [0 disable, 1 enable]
        time.sleep(5)
        self.batFirstStopSOC = self.instrument.write_register(1091, 10, 0, 6, False)  # Now 99%: Stop Charge SOC When Bat First 1%. Range=[0,100]
        time.sleep(5)
        self.BatFirstPowerRate = self.instrument.write_register(1090, 80, 0, 6, False)  # Now 99%: Charge Power Rate When Bat First 1%. Range=[0,100]
        time.sleep(5)
        print('IDLE mode')
    def read_registers(self):
        self.INVSTATE = self.instrument.read_register(1000, 0, 4, False)
        time.sleep(0.1)
        self.BMSSTATE = self.instrument.read_register(1083, 0, 4, False)
        time.sleep(0.1)
        self.PRIORITY = self.instrument.read_register(118, 0, 4, False)
        time.sleep(0.1)
        self.VDC1 = self.instrument.read_register(3, 1, 4, False)
        time.sleep(0.1)

        self.IDC1 = self.instrument.read_register(4, 2, 4, False)
        time.sleep(0.1)
        self.PDC1 = self.instrument.read_register(6, 1, 4, False)
        time.sleep(0.1)
        self.VDC2 = self.instrument.read_register(7, 1, 4, False)
        time.sleep(0.1)
        self.IDC2 = self.instrument.read_register(8, 2, 4, False)
        time.sleep(0.1)
        self.PDC2 = self.instrument.read_register(10, 1, 4, False)
        time.sleep(0.1)


        self.INPUTPOWER = self.instrument.read_register(2, 1, 4, False)
        time.sleep(0.1)
        self.OUTPUTPOWER = self.instrument.read_register(36, 1, 4, False)
        time.sleep(0.1)


        self.VL1 = self.instrument.read_register(38, 1, 4, False)
        time.sleep(0.1)
        self.AL1 = self.instrument.read_register(39, 1, 4, False)
        time.sleep(0.1)
        self.FAC = self.instrument.read_register(37, 2, 4, False)
        time.sleep(0.1)


        self.ETODAY = self.instrument.read_register(54, 1, 4, False)
        time.sleep(0.1)
        self.ETOTAL = self.instrument.read_register(56, 1, 4, False)
        time.sleep(0.1)

        self.PURTODAY = self.instrument.read_register(1045, 1, 4, False)
        time.sleep(0.1)
        self.PURTOTAL = self.instrument.read_register(1047, 1, 4, False)
        time.sleep(0.1)
        self.FEEDINTODAY = self.instrument.read_register(1049, 1, 4, False)
        time.sleep(0.1)
        self.FEEDINTOTAL = self.instrument.read_register(1051, 1, 4, False)
        time.sleep(0.1)


        # self.PBATCHARGE = self.instrument.read_register(1012, 1, 4, False)
        # time.sleep(0.1)
        self.PBATCHARGE = self.instrument.read_long(1011,4,False)
        time.sleep(0.1)
        # self.PBATDIS = self.instrument.read_register(1010, 1, 4, False)
        # time.sleep(0.1)
        self.PBATDIS = self.instrument.read_long(1009, 4, False)
        time.sleep(0.1)
        self.VBAT = self.instrument.read_register(1087, 2, 4, False)
        time.sleep(0.1)
        self.ABAT = self.instrument.read_register(1088, 2, 4, False)
        time.sleep(0.1)
        self.SOCBAT = self.instrument.read_register(1086, 0, 4, False)
        time.sleep(0.1)
        self.TODAYCHARGE = self.instrument.read_register(1057, 1, 4, False)
        time.sleep(0.1)
        self.TOTALCHARGE = self.instrument.read_register(1059, 1, 4, False)
        time.sleep(0.1)
        self.TODAYDIS = self.instrument.read_register(1053, 1, 4, False)
        time.sleep(0.1)
        self.TOTALDIS = self.instrument.read_register(1055, 1, 4, False)
        time.sleep(0.1)


        self.TEMP = self.instrument.read_register(93, 1, 4, False)
        time.sleep(0.1)
        self.BATTEMP = self.instrument.read_register(1089, 0, 4, False)
        time.sleep(0.1)
        self.Firmware = self.instrument.read_string(9, 3, 3)
        time.sleep(0.1)

    def tabulate(self):
        self.read_registers()
        self.table1 = [['Register naam', 'Register waarde', 'Eenheid'],
                  ['Inverter state', self.INVSTATE,
                   '0x00: waitingmodule0x01: Self-testmode,0x03:faultmodule0x04:flashmodule0x05|0x06|0x07|0x08:normalmodule'],
                  ['BMSSTATE', self.BMSSTATE, '-'],
                  ['PRIORITY', self.PRIORITY, '0.Load/1.Battery/2.Grid'],
                  ['DC1 voltage', self.VDC1, 'V'],
                  ['DC1 current', self.IDC1, 'A'],
                  ['DC1 power', self.PDC1, 'W'],
                  ['DC2 voltage', self.VDC2, 'V'],
                  ['DC2 current', self.IDC2, 'A'], ['DC2 power', self.PDC2, 'W'],
                  ['TOTAL DC INPUT POWER', self.INPUTPOWER, 'W'],
                  ['TOTAL AC OUTPUT POWER', self.OUTPUTPOWER, 'W'],
                  ['L1 Voltage', self.VL1, 'V'],
                  ['L1 Amperage', self.AL1, 'A'],
                  ['Freqeuentie', self.FAC, 'Hz'],
                  ['Daily production', self.ETODAY, 'kWh'],
                  ['Cumulative production', self.ETOTAL, 'kWh'],
                  ['Daily purchased', self.PURTODAY, 'kWh'],
                  ['Total purchased', self.PURTOTAL, 'kWh'],
                  ['Daily grid feed-in', self.FEEDINTODAY, 'kWh'],
                  ['Total grid feed-in', self.FEEDINTOTAL, 'kWh'],
                  ['Battery charge power', self.PBATCHARGE/10, 'W'],
                  ['Battery discharge power', self.PBATDIS/10, 'W'],
                  ['Battery voltage', self.VBAT, 'V'],
                  ['Battery current', self.ABAT, 'A'],
                  ['Battery capacity', self.SOCBAT, '%'],
                  ['Daily charging energy', self.TODAYCHARGE, 'kWh'],
                  ['Total charging energy', self.TOTALCHARGE, 'kWh'],
                  ['Daily discharging energy', self.TODAYDIS, 'kWh'],
                  ['Total discharging energy', self.TOTALDIS, 'kWh'],
                  ['Temperatuur omvormer', self.TEMP, 'C'],
                  ['Temperatuur batterij', self.BATTEMP, 'C'],
                  ['Inverter firmware',self.Firmware]]
        print(tabulate(self.table1, headers='firstrow', tablefmt='fancy_grid'))


class Solis_Hybrid_RTU:
    def __init__(self,port):
        self.tracked_duration=500
        self.amount_of_data=round(self.tracked_duration/5) ###### CHANGE ME (x*5seconds between data) 1440 amount of data is 2hours of time

        self.instrument = minimalmodbus.Instrument(port, 1, debug=False)
        self.tracked_duration = 500
        initialize_RTU(self, 9600, 8, 1, 0.3, 1)

        # self.instrument.serial.port = port                             ##### this is the serial port name
        # self.instrument.serial.baudrate = 9600                           ##### Baudrate
        # self.instrument.serial.bytesize = 8
        # self.instrument.serial.parity   = serial.PARITY_NONE
        # self.instrument.serial.stopbits = 1
        # self.instrument.serial.timeout  = 0.3                           ##### seconds
        # self.instrument.serial.write_timeout  = 5         # 2s=2000ms is default for WRITE timeout
        # self.instrument.address = 1                                      ##### this is the slave address number
        # self.instrument.mode = minimalmodbus.MODE_RTU                    ##### rtu or ascii mode
        self.instrument.clear_buffers_before_each_transaction = True
        self.instrument.close_port_after_each_call=False
        self.instrument.handle_local_echo=False
        
    def configure(self):
     #USE ONLY FOR SOLIS RHI INVERTERS
     #SOLIS RAI NEEDS CAN ONLY BE SET LOCALLY
        self.EnergyStorageControlSwitch = self.instrument.write_register(43110, 35, 0, 16, False) #BIT0:Spontaneous mode switch BIT1:timedcharge/discharge BIT5:Allow charge from grid : ALL MUST BE ON
        time.sleep(5)
        print('Inverter succesfully configured')    

    def idle_discharge(self):
        self.TimedChargeStartHour = self.instrument.write_register(43143, 23, 0, 16, False) #Works! #Range=[0,24h]
        time.sleep(5)
        self.TimedChargeStartMinute = self.instrument.write_register(43144, 59, 0, 16, False) #Works! #Range=[0,59m]
        time.sleep(5)
        self.TimedChargeEndHour = self.instrument.write_register(43145, 0, 0, 16, False)  #Works! #Range=[0,24h]
        time.sleep(5)
        self.TimedChargeEndMinute = self.instrument.write_register(43146, 0, 0, 16, False)  #Works! #Range=[0,59m]
     
        time.sleep(5)
        self.TimedDischargeStartHour = self.instrument.write_register(43147, 0, 0, 16, False) #Works!#Range=[0,24h]
        time.sleep(5)
        self.TimedDischargeStartMinute = self.instrument.write_register(43148, 0, 0, 16, False)#Works! #Range=[0,59m]
        time.sleep(5)
        self.TimedDischargeEndHour = self.instrument.write_register(43149, 23, 0, 16, False) #Works!#Range=[0,24h]
        time.sleep(5)
        self.TimedDischargeEndMinute = self.instrument.write_register(43150, 59, 0, 16, False) #Works! #Range=[0,59m]
        time.sleep(5)

        self.TimedDischargeCurrent = self.instrument.write_register(43142, 0, 0, 16, False)#Works! Range=[0,700] [0,70A]
        print('Idle Discharge 0W')

    def idle_charge(self):     
        time.sleep(5)
        self.TimedDischargeStartHour = self.instrument.write_register(43147, 23, 0, 16, False) #Works!#Range=[0,24h]
        time.sleep(5)
        self.TimedDischargeStartMinute = self.instrument.write_register(43148, 59, 0, 16, False)#Works! #Range=[0,59m]
        time.sleep(5)
        self.TimedDischargeEndHour = self.instrument.write_register(43149, 0, 0, 16, False) #Works!#Range=[0,24h]
        time.sleep(5)
        self.TimedDischargeEndMinute = self.instrument.write_register(43150, 0, 0, 16, False) #Works! #Range=[0,59m]
        time.sleep(5)

        self.TimedChargeStartHour = self.instrument.write_register(43143, 0, 0, 16, False) #Works! #Range=[0,24h]
        time.sleep(5)
        self.TimedChargeStartMinute = self.instrument.write_register(43144, 0, 0, 16, False) #Works! #Range=[0,59m]
        time.sleep(5)
        self.TimedChargeEndHour = self.instrument.write_register(43145, 23, 0, 16, False)  #Works! #Range=[0,24h]
        time.sleep(5)
        self.TimedChargeEndMinute = self.instrument.write_register(43146, 59, 0, 16, False)  #Works! #Range=[0,59m]

        self.TimedChargeCurrent = self.instrument.write_register(43141, 0, 0, 16, False)#Works! Range=[0,700] [0,70A]
        print('Idle charge 0W')

    def selfconsumption(self):
        self.TimedDischargeStartHour = self.instrument.write_register(43147, 0, 0, 16, False) #Works!#Range=[0,24h]
        time.sleep(5)
        self.TimedDischargeStartMinute = self.instrument.write_register(43148, 0, 0, 16, False)#Works! #Range=[0,59m]
        time.sleep(5)
        self.TimedDischargeEndHour = self.instrument.write_register(43149, 0, 0, 16, False) #Works!#Range=[0,24h]
        time.sleep(5)
        self.TimedDischargeEndMinute = self.instrument.write_register(43150, 0, 0, 16, False) #Works! #Range=[0,59m]
        time.sleep(5)

        self.TimedChargeStartHour = self.instrument.write_register(43143, 0, 0, 16, False) #Works! #Range=[0,24h]
        time.sleep(5)
        self.TimedChargeStartMinute = self.instrument.write_register(43144, 0, 0, 16, False) #Works! #Range=[0,59m]
        time.sleep(5)
        self.TimedChargeEndHour = self.instrument.write_register(43145, 0, 0, 16, False)  #Works! #Range=[0,24h]
        time.sleep(5)
        self.TimedChargeEndMinute = self.instrument.write_register(43146, 0, 0, 16, False)  #Works! #Range=[0,59m]
        print("Inverter in self-consumption")
    def charge(self,charge_current):
        self.TimedDischargeStartHour = self.instrument.write_register(43147, 23, 0, 16, False) #Works!#Range=[0,24h]
        time.sleep(5)
        self.TimedDischargeStartMinute = self.instrument.write_register(43148, 59, 0, 16, False)#Works! #Range=[0,59m]
        time.sleep(5)
        self.TimedDischargeEndHour = self.instrument.write_register(43149, 0, 0, 16, False) #Works!#Range=[0,24h]
        time.sleep(5)
        self.TimedDischargeEndMinute = self.instrument.write_register(43150, 0, 0, 16, False) #Works! #Range=[0,59m]
        time.sleep(5)
     
        self.TimedChargeStartHour = self.instrument.write_register(43143, 0, 0, 16, False) #Works! #Range=[0,24h]
        time.sleep(5)
        self.TimedChargeStartMinute = self.instrument.write_register(43144, 0, 0, 16, False) #Works! #Range=[0,59m]
        time.sleep(5)
        self.TimedChargeEndHour = self.instrument.write_register(43145, 23, 0, 16, False)  #Works! #Range=[0,24h]
        time.sleep(5)
        self.TimedChargeEndMinute = self.instrument.write_register(43146, 59, 0, 16, False)  #Works! #Range=[0,59m]
        time.sleep(5)

        self.TimedChargeCurrent = self.instrument.write_register(43141, charge_current, 0, 16, False) #Works! Range=[0,700] [0,70A]
        print('Inverter successfully Charging') 
            
    def discharge(self,discharge_current):
     #DEPENDING ON THE BATTERY THE BATTERY CURRENT RANGE CHANGES
        self.TimedChargeStartHour = self.instrument.write_register(43143, 23, 0, 16, False) #Works! #Range=[0,24h]
        time.sleep(5)
        self.TimedChargeStartMinute = self.instrument.write_register(43144, 59, 0, 16, False) #Works! #Range=[0,59m]
        time.sleep(5)
        self.TimedChargeEndHour = self.instrument.write_register(43145, 0, 0, 16, False)  #Works! #Range=[0,24h]
        time.sleep(5)
        self.TimedChargeEndMinute = self.instrument.write_register(43146, 0, 0, 16, False)  #Works! #Range=[0,59m]
        time.sleep(5)
     
        self.TimedDischargeStartHour = self.instrument.write_register(43147, 0, 0, 16, False) #Works!#Range=[0,24h]
        time.sleep(5)
        self.TimedDischargeStartMinute = self.instrument.write_register(43148, 0, 0, 16, False)#Works! #Range=[0,59m]
        time.sleep(5)
        self.TimedDischargeEndHour = self.instrument.write_register(43149, 23, 0, 16, False) #Works!#Range=[0,24h]
        time.sleep(5)
        self.TimedDischargeEndMinute = self.instrument.write_register(43150, 59, 0, 16, False) #Works! #Range=[0,59m]
        time.sleep(5)

        self.TimedDischargeCurrent = self.instrument.write_register(43142, discharge_current, 0, 16, False)#Works! Range=[0,700] [0,70A]
        print('Inverter succesfully Discharging') 
        
    def read_registers(self):
        self.Interval=0.3 #based on protocol 300ms frame interval communication
        
        self.INV_AC_TYPE_OUTPUT = self.instrument.read_register(33047,0,4, False)
        time.sleep(self.Interval)
        self.INV_PHASE_VOLTAGE = self.instrument.read_register(33073,1,4, False)
        time.sleep(self.Interval)
        self.INV_AC_POWER = self.instrument.read_long(33079,4, True, 0)
        time.sleep(self.Interval)
        self.INV_STANDARD_WORKING_MODE = self.instrument.read_register(33091,0,4, False)
        time.sleep(self.Interval)
        self.INV_TEMP = self.instrument.read_register(33093, 1, 4, True)
        time.sleep(self.Interval)
        self.INV_CURRENT_STATUS = self.instrument.read_register(33095,0,4, False)
        time.sleep(self.Interval)
        
        self.OPERATING_STATUS = self.instrument.read_register(33121,0,4, False)
        time.sleep(self.Interval)
        self.OPERATING_MODE = self.instrument.read_register(33122,0,4, False)
        time.sleep(self.Interval)
        self.STORAGE_CONTROL = self.instrument.read_register(33132,0,4, False)
        time.sleep(self.Interval)


        
        self.BAT_VOL = self.instrument.read_register(33133, 1, 4, False)
        time.sleep(self.Interval)
        self.BAT_CURRENT = self.instrument.read_register(33134, 1, 4, True)
        time.sleep(self.Interval)
        self.BAT_CURRENT_DIRECTION = self.instrument.read_register(33135, 1, 4, True)
        time.sleep(self.Interval)
        self.BAT_POWER = self.instrument.read_long(33149,4, True, 0)
        time.sleep(self.Interval)
        self.BAT_SOC = self.instrument.read_register(33139, 0, 4, False)
        time.sleep(self.Interval)
        
        self.BMS_VOL = self.instrument.read_register(33141, 2, 4, False)
        time.sleep(self.Interval)
        self.BMS_CURRENT = self.instrument.read_register(33142, 1, 4, True)
        time.sleep(self.Interval)
        self.BMS_CHARGE_CURRENT_LIMITATION = self.instrument.read_register(33143, 1, 4, False)
        time.sleep(self.Interval)
        self.BMS_DISCHARGE_CURRENT_LIMITATION = self.instrument.read_register(33144, 1, 4, False)
        time.sleep(self.Interval)
        
        self.BAT_CHARGEDISHCARGE_ENABLE = self.instrument.read_register(33203, 0, 4, False)
        time.sleep(self.Interval)
        self.BAT_CHARGEDISHCARGE_CURRENT = self.instrument.read_register(33204, 0, 4, False)
        time.sleep(self.Interval)
        self.BAT_CHARGE_MAX_CURRENT = self.instrument.read_register(33206, 1, 4, False)
        time.sleep(self.Interval)
        self.BAT_DISCHARGE_MAX_CURRENT = self.instrument.read_register(33207, 0, 4, False)
        time.sleep(self.Interval)
        
        self.CURRENT_BATTERY_MODULE = self.instrument.read_register(43009, 0, 3, False)
        time.sleep(self.Interval)
        self.OVERCHARGE_SOC = self.instrument.read_register(43010, 0, 3, False)
        time.sleep(self.Interval)
        self.OVERDISCHARGE_SOC = self.instrument.read_register(43011, 0, 3, False)
        time.sleep(self.Interval)
        self.MAX_CHARGE_CURRENT = self.instrument.read_register(43012, 1, 3, False)
        time.sleep(self.Interval)
        self.MAX_DISCHARGE_CURRENT = self.instrument.read_register(43013, 1, 3, False)
        time.sleep(self.Interval)
        self.AMBIENT_TEMPERATURE_SETTING = self.instrument.read_register(43028, 0, 3, False)
        time.sleep(self.Interval)
        self.LIMIT_POWER_SETTING = self.instrument.read_register(43052, 2, 3, False)
        time.sleep(self.Interval)
        self.STORAGE_CONTROL_SWITCH = self.instrument.read_register(43110, 0, 3, False)
        time.sleep(self.Interval)
        
        self.BAT_MAX_CHARGE_CURRENT = self.instrument.read_register(43117,1, 3, False)
        time.sleep(self.Interval)
        self.BAT_MAX_DISCHARGE_CURRENT = self.instrument.read_register(43118, 1, 3, False)
        time.sleep(self.Interval)
        self.BAT_CHARGE_LIMIT_POWER =  self.instrument.read_register(43130, 0, 3, False)
        time.sleep(self.Interval)
        self.BAT_DISCHARGE_LIMIT_POWER =  self.instrument.read_register(43131, 0, 3, False)
        time.sleep(self.Interval)
        
        self.TIMED_CHARGE_CURRENT = self.instrument.read_register(43141, 1, 3, False)
        time.sleep(self.Interval)
        self.TIMED_DISCHARGE_CURRENT = self.instrument.read_register(43142, 1, 3, False)
        time.sleep(self.Interval)
        self.MAX_GRID_CHARGING_CURRENT =  self.instrument.read_register(43342, 1, 3, False)
        time.sleep(self.Interval)
        
        self.TimedDischargeCurrent = self.instrument.read_register(43142, 0, 3, False)
        time.sleep(self.Interval)
        self.TimedDischargeStartHour= self.instrument.read_register(43147, 0, 3, False)
        time.sleep(self.Interval)
        self.TimedDischargeStartMinute= self.instrument.read_register(43148, 0, 3, False)
        time.sleep(self.Interval)
        self.TimedDischargeEndHour= self.instrument.read_register(43149, 0, 3, False)
        time.sleep(self.Interval)
        self.TimedDischargeEndMinute= self.instrument.read_register(43150, 0, 3, False)
        time.sleep(self.Interval)
        
        self.TimedChargeStartHour= self.instrument.read_register(43143, 0, 3, False)
        time.sleep(self.Interval)
        self.TimedChargeStartMinute= self.instrument.read_register(43144, 0, 3, False)
        time.sleep(self.Interval)
        self.TimedChargeEndHour= self.instrument.read_register(43145, 0, 3, False)
        time.sleep(self.Interval)
        self.TimedChargeEndMinute= self.instrument.read_register(43146, 0, 3, False)
        time.sleep(self.Interval)

        self.Cumulative_production = self.instrument.read_long(33029, 4, True, 0)
        time.sleep(self.Interval)
        self.Cumulative_grid_feed_in = self.instrument.read_long(33173, 4, True, 0)
        time.sleep(self.Interval)
        self.Cumulative_energy_purchased = self.instrument.read_long(33169, 4, True, 0)
        time.sleep(self.Interval)

    def tabulate(self):
        self.read_registers()
        self.table = [['REgister',"Value", 'Unit'],
        [ "INV_AC_TYPE_OUTPUT",self.INV_AC_TYPE_OUTPUT ,"-" ],
        [ "INV_PHASE_VOLTAGE",self.INV_PHASE_VOLTAGE ,"V" ],
        [ "INV_AC_POWER",self.INV_AC_POWER ,"W" ],
        [ "INV_STANDARD_WORKING_MODE",self.INV_STANDARD_WORKING_MODE ,"-" ],
        [ "INV_TEMP",self.INV_TEMP ,"C" ],
        [ "INV_CURRENT_STATUS",self.INV_CURRENT_STATUS ,"-" ],
        [ "OPERATING_STATUS",self.OPERATING_STATUS ,"-" ],
        [ "OPERATING_MODE ", self.OPERATING_MODE ,"-" ],
        [ "STORAGE_CONTROL",self.STORAGE_CONTROL ,"-" ],
        [ "BAT_VOL ",self.BAT_VOL  ,"V" ],
        [ "BAT_CURRENT", self.BAT_CURRENT,"A" ],
        [ "BAT_CURRENT_DIRECTION", self.BAT_CURRENT_DIRECTION,"0:Charge 1:Discharge" ],
        [ "BAT_POWER", self.BAT_POWER,"W" ],
        [ "BAT_SOC",self.BAT_SOC ,"%" ],
        [ "BMS_VOL",self.BMS_VOL,"V" ],
        [ "BMS_CURRENT", self.BMS_CURRENT,"A" ],
        [ "BMS_CHARGE_CURRENT_LIMITATION", self.BMS_CHARGE_CURRENT_LIMITATION,"A" ],
        [ "BMS_DISCHARGE_CURRENT_LIMITATION",self.BMS_DISCHARGE_CURRENT_LIMITATION ,"A" ],
        [ "BAT_CHARGEDISHCARGE_ENABLE ", self.BAT_CHARGEDISHCARGE_ENABLE ,"- " ],
        [ "BAT_CHARGEDISHCARGE_CURRENT",self.BAT_CHARGEDISHCARGE_CURRENT ,"A" ],
        [ "BAT_CHARGE_MAX_CURRENT", self.BAT_CHARGE_MAX_CURRENT ,"A" ],
        [ "BAT_MAX_DISCHARGE_CURRENT", self.BAT_MAX_DISCHARGE_CURRENT,"A" ],
        [ "CURRENT_BATTERY_MODULE",self.CURRENT_BATTERY_MODULE ,"-" ],
        [ "OVERCHARGE_SOC",self.OVERCHARGE_SOC ,"%" ],
        [ "OVERDISCHARGE_SOC ",self.OVERDISCHARGE_SOC  ,"%" ],
        [ "MAX_CHARGE_CURRENT",self.MAX_CHARGE_CURRENT ,"A" ],
        [ "MAX_DISCHARGE_CURRENT",self.MAX_DISCHARGE_CURRENT ,"A" ],
        [ "AMBIENT_TEMPERATURE_SETTING",self.AMBIENT_TEMPERATURE_SETTING ,"-" ],
        [ "LIMIT_POWER_SETTING", self.LIMIT_POWER_SETTING,"-" ],
        [ "STORAGE_CONTROL_SWITCH ",self.STORAGE_CONTROL_SWITCH  ,"-" ],
        [ "TIMED_CHARGE_CURRENT",self.TIMED_CHARGE_CURRENT ,"A" ],
        [ "TIMED_DISCHARGE_CURRENT",self.TIMED_DISCHARGE_CURRENT ,"A" ],
        [ "TIMED_DISCHARGE_CURRENT",self.TIMED_DISCHARGE_CURRENT ,"kWh" ],
        [ "Cumulative_production",self.Cumulative_production ,"kWh" ],
        [ "Cumulative grid feed-in",self.Cumulative_grid_feed_in ,"kWh" ],
        [ "Cumulative energy purchased",self.Cumulative_energy_purchased,"kWh"]]
        print(tabulate(self.table, headers='firstrow', tablefmt='fancy_grid'))

    def Log_All_Data_Hour(self):
        self.LIST_INV_AC_TYPE_OUTPUT=[]
        self.LIST_INV_PHASE_VOLTAGE=[]
        self.LIST_INV_AC_POWER=[]
        self.LIST_INV_STANDARD_WORKING_MODE=[]
        self.LIST_INV_TEMP=[]
        self.LIST_INV_CURRENT_STATUS=[]
        self.LIST_OPERATING_STATUS=[]
        self.LIST_OPERATING_MODE=[]
        self.LIST_STORAGE_CONTROL=[]
        self.LIST_BAT_VOL=[]
        self.LIST_BAT_CURRENT =[]
        self.LIST_BAT_CURRENT_DIRECTION =[]
        self.LIST_BAT_POWER=[]
        self.LIST_BAT_SOC=[]
        self.LIST_BMS_VOL=[]
        self.LIST_BMS_CURRENT=[]
        self.LIST_BMS_CHARGE_CURRENT_LIMITATION=[]
        self.LIST_BMS_DISCHARGE_CURRENT_LIMITATION=[]
        self.LIST_BAT_CHARGEDISHCARGE_ENABLE=[]
        self.LIST_BAT_CHARGEDISHCARGE_CURRENT=[]
        self.LIST_BAT_CHARGE_MAX_CURRENT=[]
        self.LIST_BAT_DISCHARGE_MAX_CURRENT=[]
        self.LIST_CURRENT_BATTERY_MODULE=[]
        self.LIST_OVERCHARGE_SOC=[]
        self.LIST_OVERDISCHARGE_SOC=[]
        self.LIST_MAX_CHARGE_CURRENT=[]
        self.LIST_MAX_DISCHARGE_CURRENT=[]
        self.LIST_AMBIENT_TEMPERATURE_SETTING=[]
        self.LIST_LIMIT_POWER_SETTING=[]
        self.LIST_STORAGE_CONTROL_SWITCH =[]
        self.LIST_BAT_MAX_CHARGE_CURRENT=[]
        self.LIST_BAT_MAX_DISCHARGE_CURRENT=[]
        self.LIST_BAT_CHARGE_LIMIT_POWER=[]
        self.LIST_BAT_DISCHARGE_LIMIT_POWER=[]
        self.LIST_TIMED_CHARGE_CURRENT=[]
        self.LIST_TIMED_DISCHARGE_CURRENT=[]
        self.LIST_MAX_GRID_CHARGING_CURRENT=[]

        while count < 500:
            try:
                self.read_registers()
                self.LIST_INV_AC_TYPE_OUTPUT.append(str(self.INV_AC_TYPE_OUTPUT)+", ")
                self.LIST_INV_PHASE_VOLTAGE.append(str(self.INV_PHASE_VOLTAGE)+", ")
                self.LIST_INV_AC_POWER.append(str(self.INV_AC_POWER)+", ")
                self.LIST_INV_STANDARD_WORKING_MODE.append(str(self.INV_STANDARD_WORKING_MODE)+", ")
                self.LIST_INV_TEMP.append(str(self.INV_TEMP)+", ")
                self.LIST_INV_CURRENT_STATUS.append(str(self.INV_CURRENT_STATUS)+", ")
                self.LIST_OPERATING_STATUS.append(str(self.OPERATING_STATUS)+", ")
                self.LIST_OPERATING_MODE.append(str(self.OPERATING_MODE)+", ")
                self.LIST_STORAGE_CONTROL.append(str(self.STORAGE_CONTROL)+", ")
                self.LIST_BAT_VOL.append(str(self.BAT_VOL)+", ")
                self.LIST_BAT_CURRENT.append(str(self.BAT_CURRENT)+", ")
                self.LIST_BAT_CURRENT_DIRECTION.append(str(self.BAT_CURRENT)+", ")
                self.LIST_BAT_POWER.append(str(self.BAT_POWER)+", ")
                self.LIST_BAT_SOC.append(str(self.BAT_SOC)+", ")
                self.LIST_BMS_VOL.append(str(self.BMS_VOL)+", ")
                self.LIST_BMS_CURRENT.append(str(self.BMS_CURRENT)+", ")
                self.LIST_BMS_CHARGE_CURRENT_LIMITATION.append(str(self.BMS_CHARGE_CURRENT_LIMITATION)+", ")
                self.LIST_BMS_DISCHARGE_CURRENT_LIMITATION.append(str(self.BMS_DISCHARGE_CURRENT_LIMITATION)+", ")
                self.LIST_BAT_CHARGEDISHCARGE_ENABLE.append(str(self.BAT_CHARGEDISHCARGE_ENABLE)+", ")
                self.LIST_BAT_CHARGEDISHCARGE_CURRENT.append(str(self.BAT_CHARGEDISHCARGE_CURRENT)+", ")
                self.LIST_BAT_CHARGE_MAX_CURRENT.append(str(self.BAT_CHARGE_MAX_CURRENT)+", ")
                self.LIST_BAT_DISCHARGE_MAX_CURRENT.append(str(self.BAT_DISCHARGE_MAX_CURRENT)+", ")
                self.LIST_CURRENT_BATTERY_MODULE.append(str(self.CURRENT_BATTERY_MODULE)+", ")
                self.LIST_OVERCHARGE_SOC.append(str(self.OVERCHARGE_SOC)+", ")
                self.LIST_OVERDISCHARGE_SOC.append(str(self.OVERDISCHARGE_SOC)+", ")
                self.LIST_MAX_CHARGE_CURRENT.append(str(self.MAX_CHARGE_CURRENT)+", ")
                self.LIST_MAX_DISCHARGE_CURRENT.append(str(self.MAX_DISCHARGE_CURRENT)+" ,")
                self.LIST_AMBIENT_TEMPERATURE_SETTING.append(str(self.AMBIENT_TEMPERATURE_SETTING)+", ")
                self.LIST_LIMIT_POWER_SETTING.append(str(self.LIMIT_POWER_SETTING)+", ")
                self.LIST_STORAGE_CONTROL_SWITCH.append(str(self.STORAGE_CONTROL_SWITCH)+", ")
                self.LIST_BAT_MAX_CHARGE_CURRENT.append(str(self.BAT_MAX_CHARGE_CURRENT)+", ")
                self.LIST_BAT_MAX_DISCHARGE_CURRENT.append(str(self.BAT_MAX_DISCHARGE_CURRENT)+", ")
                self.LIST_BAT_CHARGE_LIMIT_POWER.append(str(self.BAT_CHARGE_LIMIT_POWER)+", ")
                self.LIST_BAT_DISCHARGE_LIMIT_POWER.append(str(self.BAT_DISCHARGE_LIMIT_POWER)+", ")
                self.LIST_TIMED_CHARGE_CURRENT.append(str(self.TIMED_CHARGE_CURRENT)+", ")
                self.LIST_TIMED_DISCHARGE_CURRENT.append(str(self.TIMED_DISCHARGE_CURRENT)+", ")
                self.LIST_MAX_GRID_CHARGING_CURRENT.append(str(self.MAX_GRID_CHARGING_CURRENT)+", ")
                
                self.file = open(r'C:\Users\yorick.niessink\Documents\Solis Research\Solis_Readings_Discharge.txt','w')
                self.file.writelines(self.LIST_INV_AC_POWER)
                self.file.write("\n")
                self.file.writelines(self.LIST_INV_TEMP)
                self.file.write("\n")
                self.file.writelines(self.LIST_BAT_VOL)
                self.file.write("\n")
                self.file.writelines(self.LIST_BAT_CURRENT)
                self.file.write("\n")
                self.file.writelines(self.LIST_BAT_CURRENT_DIRECTION)
                self.file.write("\n")
                self.file.writelines(self.LIST_BAT_POWER)
                self.file.write("\n")
                self.file.writelines(self.LIST_BAT_SOC)
                self.file.write("\n")
                self.file.writelines(self.LIST_BMS_CURRENT)
                self.file.write("\n")
                self.file.writelines(self.LIST_BMS_CHARGE_CURRENT_LIMITATION)
                self.file.write("\n")
                self.file.writelines(self.LIST_BMS_DISCHARGE_CURRENT_LIMITATION)
                self.file.write("\n")
                self.file.writelines(self.LIST_BAT_CHARGEDISHCARGE_CURRENT)
                self.file.write("\n")
                self.file.writelines(self.LIST_BAT_CHARGE_MAX_CURRENT)
                self.file.write("\n")
                self.file.writelines(self.LIST_BAT_DISCHARGE_MAX_CURRENT)
                self.file.write("\n")
                self.file.writelines(self.LIST_MAX_DISCHARGE_CURRENT)
                self.file.write("\n")
                self.file.writelines(self.LIST_STORAGE_CONTROL_SWITCH)
                self.file.write("\n")
                self.file.writelines(self.LIST_BAT_MAX_CHARGE_CURRENT)
                self.file.write("\n")
                self.file.writelines(self.LIST_BAT_MAX_DISCHARGE_CURRENT)
                self.file.write("\n")
                self.file.writelines(self.LIST_BAT_CHARGE_LIMIT_POWER)
                self.file.write("\n")
                self.file.writelines(self.LIST_TIMED_CHARGE_CURRENT)
                self.file.write("\n")
                self.file.writelines(self.LIST_TIMED_DISCHARGE_CURRENT)
                self.file.close()         
                
                print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
                self.count += 1
                print(self.count)
            except:
                print("pass")
                pass


    def Log_Pri_Data_Hour(self,logtime,filepath):
        self.LIST_INV_AC_POWER = []
        self.LIST_INV_TEMP = []

        self.LIST_BAT_POWER = []
        self.LIST_BAT_SOC = []
        self.LIST_BAT_CURRENT_DIRECTION = [] ## Solis Specific

        self.LIST_CUM_Production = []
        self.LIST_CUM_GRID_FEED_IN = []
        self.LIST_CUM_ENERGY_PURCHASED = []

        self.count=0
        self.start_time=time.time()
        while self.count <= logtime:

            try:
                self.read_registers()
                self.LIST_INV_AC_POWER.append(str(self.INV_AC_POWER) + ", ")
                self.LIST_INV_TEMP.append(str(self.INV_TEMP) + ", ")

                self.LIST_BAT_CURRENT_DIRECTION.append(str(self.BAT_CURRENT_DIRECTION) + ", ")
                self.LIST_BAT_POWER.append(str(self.BAT_POWER) + ", ")
                self.LIST_BAT_SOC.append(str(self.BAT_SOC) + ", ")

                self.LIST_CUM_Production.append(str(self.Cumulative_production) + ", ")
                self.LIST_CUM_GRID_FEED_IN.append(str(self.Cumulative_grid_feed_in) + ", ")
                self.LIST_CUM_ENERGY_PURCHASED.append(str(self.Cumulative_energy_purchased) + ", ")

                self.file = open(filepath, 'w')
                self.file.write("Inv AC power: ")
                self.file.writelines(self.LIST_INV_AC_POWER)
                self.file.write("\n")
                self.file.write("Inv temperature: ")
                self.file.writelines(self.LIST_INV_TEMP)
                self.file.write("\n")
                self.file.write("Bat curent direction: ")
                self.file.writelines(self.LIST_BAT_CURRENT_DIRECTION)
                self.file.write("\n")
                self.file.write("Battery power: ")
                self.file.writelines(self.LIST_BAT_POWER)
                self.file.write("\n")
                self.file.write("Battery SOC: ")
                self.file.writelines(self.LIST_BAT_SOC)
                self.file.write("\n")
                self.file.write("Cum production: ")
                self.file.writelines(self.LIST_CUM_Production)
                self.file.write("\n")
                self.file.write("CUM grid feed-in: ")
                self.file.writelines(self.LIST_CUM_GRID_FEED_IN)
                self.file.write("\n")
                self.file.write("cum energy purchased: ")
                self.file.writelines(self.LIST_CUM_ENERGY_PURCHASED)
                self.file.close()

                self.count = time.time() - self.start_time
                print('Total time: ', self.count)

            except:
                print("pass")
                self.count = time.time() - self.start_time
                print('Total time: ', self.count)
                pass




























 
