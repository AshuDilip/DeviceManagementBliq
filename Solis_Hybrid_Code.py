#made by Yorick Niessink, Project Engineer
#Python code to charge/discharge 

import minimalmodbus
import serial
from tabulate import tabulate
import time

#USB-to-RS485 converter settings
#instrument = minimalmodbus.Instrument(port on laptop='COM5',COM-adres inverter=1, debug = True) #debug mode shows in the python when something goes wrong
instrument = minimalmodbus.Instrument('COM4', 1, debug=False)
instrument.serial.baudrate = 9600                         #Baudrate
instrument.serial.bytesize = 8                            #Bytesize
instrument.serial.parity   = serial.PARITY_NONE           #parity setting
instrument.serial.stopbits = 1                            #stopbit setting
instrument.serial.timeout  = 0.3                         #Timeout setting in seconds now 500ms
instrument.serial.write_timeout  = 5         # 2s=2000ms is default for WRITE timeout
instrument.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
instrument.clear_buffers_before_each_transaction = True
instrument.close_port_after_each_call=False
instrument.handle_local_echo=False

#Four functions are made: CONFIGURE, STOP, CHARGE, DISCHARGE
#CONFIGURE: 
#STOP:    
#CHARGE: 
#DISCHARGE:

#To enable a function, change the 0 of ##CONFIGURE = 0 to 1 ---> ###CONFIGURE = 1
#Only have ONE function enabled at the same time
#TimedDischargeCurrent = instrument.write_register(43142, 0, 0, 16, False)#Works! Range=[0,700] [0,70A]
#TimedChargeCurrent = instrument.write_register(43141, 0, 0, 16, False) #Works! Range=[0,700] [0,70A]


CONFIGURE = 0 #These settings will be done by Bliq-installer/Engineer only once
if CONFIGURE > 0:
     EnergyStorageControlSwitch = instrument.write_register(43110, 35, 0, 16, False) #BIT0:Spontaneous mode switch BIT1:timedcharge/discharge BIT5:Allow charge from grid : ALL MUST BE ON
     time.sleep(5)

     print('Inverter succesfully configured') 

CHARGE = 1
if CHARGE > 0:
     TimedDischargeStartHour = instrument.write_register(43147, 23, 0, 16, False) #Works!#Range=[0,24h] 
     time.sleep(5)
     TimedDischargeStartMinute = instrument.write_register(43148, 59, 0, 16, False)#Works! #Range=[0,59m] 
     time.sleep(5)
     TimedDischargeEndHour = instrument.write_register(43149, 0, 0, 16, False) #Works!#Range=[0,24h] 
     time.sleep(5)
     TimedDischargeEndMinute = instrument.write_register(43150, 0, 0, 16, False) #Works! #Range=[0,59m]
     time.sleep(5)
     
     TimedChargeStartHour = instrument.write_register(43143, 0, 0, 16, False) #Works! #Range=[0,24h] 
     time.sleep(5)
     TimedChargeStartMinute = instrument.write_register(43144, 0, 0, 16, False) #Works! #Range=[0,59m] 
     time.sleep(5)
     TimedChargeEndHour = instrument.write_register(43145, 23, 0, 16, False)  #Works! #Range=[0,24h] 
     time.sleep(5)
     TimedChargeEndMinute = instrument.write_register(43146, 59, 0, 16, False)  #Works! #Range=[0,59m] 
     time.sleep(5)

     TimedChargeCurrent = instrument.write_register(43141, 600, 0, 16, False) #Works! Range=[0,700] [0,70A]
     time.sleep(5)

     print('Inverter succesfully Charging')   

     
DISCHARGE = 0
if DISCHARGE > 0:
     TimedChargeStartHour = instrument.write_register(43143, 23, 0, 16, False) #Works! #Range=[0,24h] 
     time.sleep(5)
     TimedChargeStartMinute = instrument.write_register(43144, 59, 0, 16, False) #Works! #Range=[0,59m] 
     time.sleep(5)
     TimedChargeEndHour = instrument.write_register(43145, 0, 0, 16, False)  #Works! #Range=[0,24h] 
     time.sleep(5)
     TimedChargeEndMinute = instrument.write_register(43146, 0, 0, 16, False)  #Works! #Range=[0,59m] 
     time.sleep(5)
     
     TimedDischargeStartHour = instrument.write_register(43147, 0, 0, 16, False) #Works!#Range=[0,24h] 
     time.sleep(5)
     TimedDischargeStartMinute = instrument.write_register(43148, 0, 0, 16, False)#Works! #Range=[0,59m] 
     time.sleep(5)
     TimedDischargeEndHour = instrument.write_register(43149, 23, 0, 16, False) #Works!#Range=[0,24h] 
     time.sleep(5)
     TimedDischargeEndMinute = instrument.write_register(43150, 59, 0, 16, False) #Works! #Range=[0,59m]
     time.sleep(5)


     TimedDischargeCurrent = instrument.write_register(43142, 600, 0, 16, False)#Works! Range=[0,700] [0,70A]
     time.sleep(5)
     print('Inverter succesfully Discharging') 

Idle_Mode_Discharge = 0  
if Idle_Mode_Discharge > 0:
     TimedChargeStartHour = instrument.write_register(43143, 23, 0, 16, False) #Works! #Range=[0,24h] 
     time.sleep(5)
     TimedChargeStartMinute = instrument.write_register(43144, 59, 0, 16, False) #Works! #Range=[0,59m] 
     time.sleep(5)
     TimedChargeEndHour = instrument.write_register(43145, 0, 0, 16, False)  #Works! #Range=[0,24h] 
     time.sleep(5)
     TimedChargeEndMinute = instrument.write_register(43146, 0, 0, 16, False)  #Works! #Range=[0,59m]
     
     time.sleep(5)
     TimedDischargeStartHour = instrument.write_register(43147, 0, 0, 16, False) #Works!#Range=[0,24h] 
     time.sleep(5)
     TimedDischargeStartMinute = instrument.write_register(43148, 0, 0, 16, False)#Works! #Range=[0,59m] 
     time.sleep(5)
     TimedDischargeEndHour = instrument.write_register(43149, 23, 0, 16, False) #Works!#Range=[0,24h] 
     time.sleep(5)
     TimedDischargeEndMinute = instrument.write_register(43150, 59, 0, 16, False) #Works! #Range=[0,59m]
     time.sleep(5)

     TimedDischargeCurrent = instrument.write_register(43142, 600, 0, 16, False)#Works! Range=[0,700] [0,70A]
     time.sleep(5)

     print('Idle Discharge 0W')

Idle_Mode_charge = 0  
if Idle_Mode_charge > 0:
     TimedDischargeStartHour = instrument.write_register(43147, 23, 0, 16, False) #Works!#Range=[0,24h] 
     time.sleep(5)
     TimedDischargeStartMinute = instrument.write_register(43148, 59, 0, 16, False)#Works! #Range=[0,59m] 
     time.sleep(5)
     TimedDischargeEndHour = instrument.write_register(43149, 0, 0, 16, False) #Works!#Range=[0,24h] 
     time.sleep(5)
     TimedDischargeEndMinute = instrument.write_register(43150, 0, 0, 16, False) #Works! #Range=[0,59m]
     time.sleep(5)
     
     TimedChargeStartHour = instrument.write_register(43143, 0, 0, 16, False) #Works! #Range=[0,24h] 
     time.sleep(5)
     TimedChargeStartMinute = instrument.write_register(43144, 0, 0, 16, False) #Works! #Range=[0,59m] 
     time.sleep(5)
     TimedChargeEndHour = instrument.write_register(43145, 23, 0, 16, False)  #Works! #Range=[0,24h] 
     time.sleep(5)
     TimedChargeEndMinute = instrument.write_register(43146, 59, 0, 16, False)  #Works! #Range=[0,59m] 
     time.sleep(5)

     TimedChargeCurrent = instrument.write_register(43141, 0, 0, 16, False) #Works! Range=[0,700] [0,70A]
     time.sleep(5)

     print('Idle charge 0W') 

Self_Consumption = 0  
if Self_Consumption > 0:
     TimedDischargeStartHour = instrument.write_register(43147, 0, 0, 16, False) #Works!#Range=[0,24h] 
     time.sleep(5)
     TimedDischargeStartMinute = instrument.write_register(43148, 0, 0, 16, False)#Works! #Range=[0,59m] 
     time.sleep(5)
     TimedDischargeEndHour = instrument.write_register(43149, 0, 0, 16, False) #Works!#Range=[0,24h] 
     time.sleep(5)
     TimedDischargeEndMinute = instrument.write_register(43150, 0, 0, 16, False) #Works! #Range=[0,59m]
     time.sleep(5)
     
     TimedChargeStartHour = instrument.write_register(43143, 0, 0, 16, False) #Works! #Range=[0,24h] 
     time.sleep(5)
     TimedChargeStartMinute = instrument.write_register(43144, 0, 0, 16, False) #Works! #Range=[0,59m] 
     time.sleep(5)
     TimedChargeEndHour = instrument.write_register(43145, 0, 0, 16, False)  #Works! #Range=[0,24h] 
     time.sleep(5)
     TimedChargeEndMinute = instrument.write_register(43146, 0, 0, 16, False)  #Works! #Range=[0,59m] 
     time.sleep(5)
     print('Self consumption') 

LIST_INV_AC_TYPE_OUTPUT=[]
LIST_INV_PHASE_VOLTAGE=[]
LIST_INV_AC_POWER=[]
LIST_INV_STANDARD_WORKING_MODE=[]
LIST_INV_TEMP=[]
LIST_INV_CURRENT_STATUS=[]
LIST_OPERATING_STATUS=[]
LIST_OPERATING_MODE=[]
LIST_STORAGE_CONTROL=[]
LIST_BAT_VOL=[]
LIST_BAT_CURRENT =[]
LIST_BAT_CURRENT_DIRECTION =[]
LIST_BAT_POWER=[]
LIST_BAT_SOC=[]
LIST_BMS_VOL=[]
LIST_BMS_CURRENT=[]
LIST_BMS_CHARGE_CURRENT_LIMITATION=[]
LIST_BMS_DISCHARGE_CURRENT_LIMITATION=[]
LIST_BAT_CHARGEDISHCARGE_ENABLE=[]
LIST_BAT_CHARGEDISHCARGE_CURRENT=[]
LIST_BAT_CHARGE_MAX_CURRENT=[]
LIST_BAT_DISCHARGE_MAX_CURRENT=[]
LIST_CURRENT_BATTERY_MODULE=[]
LIST_OVERCHARGE_SOC=[]
LIST_OVERDISCHARGE_SOC=[]
LIST_MAX_CHARGE_CURRENT=[]
LIST_MAX_DISCHARGE_CURRENT=[]
LIST_AMBIENT_TEMPERATURE_SETTING=[]
LIST_LIMIT_POWER_SETTING=[]
LIST_STORAGE_CONTROL_SWITCH =[]
LIST_BAT_MAX_CHARGE_CURRENT=[]
LIST_BAT_MAX_DISCHARGE_CURRENT=[]
LIST_BAT_CHARGE_LIMIT_POWER=[]
LIST_BAT_DISCHARGE_LIMIT_POWER=[]
LIST_TIMED_CHARGE_CURRENT=[]
LIST_TIMED_DISCHARGE_CURRENT=[]
LIST_MAX_GRID_CHARGING_CURRENT=[]

Interval=0.3 #based on protocol 300ms frame interval communication
count = 0
while count < 500:
    INV_AC_TYPE_OUTPUT = instrument.read_register(33047,0,4, False)
    time.sleep(Interval)
    INV_PHASE_VOLTAGE = instrument.read_register(33073,1,4, False)
    time.sleep(Interval)
    INV_AC_POWER = instrument.read_long(33079,4, True, 0)
    time.sleep(Interval)
    INV_STANDARD_WORKING_MODE = instrument.read_register(33091,0,4, False)
    time.sleep(Interval)
    INV_TEMP = instrument.read_register(33093, 1, 4, True)
    time.sleep(Interval)
    INV_CURRENT_STATUS = instrument.read_register(33095,0,4, False)
    time.sleep(Interval)
    
    OPERATING_STATUS = instrument.read_register(33121,0,4, False)
    time.sleep(Interval)
    OPERATING_MODE = instrument.read_register(33122,0,4, False)
    time.sleep(Interval)
    STORAGE_CONTROL = instrument.read_register(33132,0,4, False)
    time.sleep(Interval)

    BAT_VOL = instrument.read_register(33133, 1, 4, False)
    time.sleep(Interval)
    BAT_CURRENT = instrument.read_register(33134, 1, 4, True)
    time.sleep(Interval)
    BAT_CURRENT_DIRECTION = instrument.read_register(33135, 1, 4, True)
    time.sleep(Interval)
    BAT_POWER = instrument.read_long(33149,4, True, 0)
    time.sleep(Interval)
    BAT_SOC = instrument.read_register(33139, 0, 4, False)
    time.sleep(Interval)

    BMS_VOL = instrument.read_register(33141, 2, 4, False)
    time.sleep(Interval)
    BMS_CURRENT = instrument.read_register(33142, 1, 4, True)
    time.sleep(Interval)
    BMS_CHARGE_CURRENT_LIMITATION = instrument.read_register(33143, 1, 4, False)
    time.sleep(Interval)
    BMS_DISCHARGE_CURRENT_LIMITATION = instrument.read_register(33144, 1, 4, False)
    time.sleep(Interval)

    BAT_CHARGEDISHCARGE_ENABLE = instrument.read_register(33203, 0, 4, False)
    time.sleep(Interval)
    BAT_CHARGEDISHCARGE_CURRENT = instrument.read_register(33204, 0, 4, False)
    time.sleep(Interval)
    BAT_CHARGE_MAX_CURRENT = instrument.read_register(33206, 1, 4, False)
    time.sleep(Interval)
    BAT_DISCHARGE_MAX_CURRENT = instrument.read_register(33207, 0, 4, False)
    time.sleep(Interval)

    CURRENT_BATTERY_MODULE = instrument.read_register(43009, 0, 3, False)
    time.sleep(Interval)
    OVERCHARGE_SOC = instrument.read_register(43010, 0, 3, False)
    time.sleep(Interval)
    OVERDISCHARGE_SOC = instrument.read_register(43011, 0, 3, False)
    time.sleep(Interval)
    MAX_CHARGE_CURRENT = instrument.read_register(43012, 1, 3, False)
    time.sleep(Interval)
    MAX_DISCHARGE_CURRENT = instrument.read_register(43013, 1, 3, False)
    time.sleep(Interval)
    AMBIENT_TEMPERATURE_SETTING = instrument.read_register(43028, 0, 3, False)
    time.sleep(Interval)
    LIMIT_POWER_SETTING = instrument.read_register(43052, 2, 3, False)
    time.sleep(Interval)
    STORAGE_CONTROL_SWITCH = instrument.read_register(43110, 0, 3, False)
    time.sleep(Interval)

    BAT_MAX_CHARGE_CURRENT = instrument.read_register(43117,1, 3, False)
    time.sleep(Interval)
    BAT_MAX_DISCHARGE_CURRENT = instrument.read_register(43118, 1, 3, False)
    time.sleep(Interval)
    BAT_CHARGE_LIMIT_POWER =  instrument.read_register(43130, 0, 3, False)
    time.sleep(Interval)
    BAT_DISCHARGE_LIMIT_POWER =  instrument.read_register(43131, 0, 3, False)
    time.sleep(Interval)

    TIMED_CHARGE_CURRENT = instrument.read_register(43141, 1, 3, False)
    time.sleep(Interval)
    TIMED_DISCHARGE_CURRENT = instrument.read_register(43142, 1, 3, False)
    time.sleep(Interval)
    MAX_GRID_CHARGING_CURRENT =  instrument.read_register(43342, 1, 3, False)
    time.sleep(Interval)
    
    TimedDischargeCurrent = instrument.read_register(43142, 0, 3, False)
    time.sleep(Interval)
    TimedDischargeStartHour= instrument.read_register(43147, 0, 3, False)
    time.sleep(Interval)
    TimedDischargeStartMinute= instrument.read_register(43148, 0, 3, False)
    time.sleep(Interval)
    TimedDischargeEndHour= instrument.read_register(43149, 0, 3, False)
    time.sleep(Interval)
    TimedDischargeEndMinute= instrument.read_register(43150, 0, 3, False)
    time.sleep(Interval)

    TimedChargeStartHour= instrument.read_register(43143, 0, 3, False)
    time.sleep(Interval)
    TimedChargeStartMinute= instrument.read_register(43144, 0, 3, False)
    time.sleep(Interval)
    TimedChargeEndHour= instrument.read_register(43145, 0, 3, False)
    time.sleep(Interval)
    TimedChargeEndMinute= instrument.read_register(43146, 0, 3, False)
    time.sleep(Interval)

    table = [['REgister',"Value", 'Unit'],
             [ "INV_AC_TYPE_OUTPUT",INV_AC_TYPE_OUTPUT ,"-" ],
             [ "INV_PHASE_VOLTAGE",INV_PHASE_VOLTAGE ,"V" ],
               [ "INV_AC_POWER",INV_AC_POWER ,"W" ],
               [ "INV_STANDARD_WORKING_MODE",INV_STANDARD_WORKING_MODE ,"-" ],
               [ "INV_TEMP",INV_TEMP ,"C" ],
               [ "INV_CURRENT_STATUS",INV_CURRENT_STATUS ,"-" ],
               [ "OPERATING_STATUS",OPERATING_STATUS ,"-" ],
               [ "OPERATING_MODE ", OPERATING_MODE ,"-" ],
               [ "STORAGE_CONTROL",STORAGE_CONTROL ,"-" ],
               [ "BAT_VOL ",BAT_VOL  ,"V" ],
               [ "BAT_CURRENT", BAT_CURRENT,"A" ],
               [ "BAT_CURRENT_DIRECTION", BAT_CURRENT_DIRECTION,"0:Charge 1:Discharge" ],
               [ "BAT_POWER", BAT_POWER,"W" ],
               [ "BAT_SOC",BAT_SOC ,"%" ],
               [ "BMS_VOL", BMS_VOL,"V" ],
               [ "BMS_CURRENT", BMS_CURRENT,"A" ],
               [ "BMS_CHARGE_CURRENT_LIMITATION", BMS_CHARGE_CURRENT_LIMITATION,"A" ],
               [ "BMS_DISCHARGE_CURRENT_LIMITATION",BMS_DISCHARGE_CURRENT_LIMITATION ,"A" ],
               [ "BAT_CHARGEDISHCARGE_ENABLE ", BAT_CHARGEDISHCARGE_ENABLE ,"- " ],
               [ "BAT_CHARGEDISHCARGE_CURRENT",BAT_CHARGEDISHCARGE_CURRENT ,"A" ],
               [ "BAT_CHARGE_MAX_CURRENT", BAT_CHARGE_MAX_CURRENT ,"A" ],
               [ "BAT_MAX_DISCHARGE_CURRENT", BAT_MAX_DISCHARGE_CURRENT,"A" ],
               [ "CURRENT_BATTERY_MODULE",CURRENT_BATTERY_MODULE ,"-" ],
               [ "OVERCHARGE_SOC",OVERCHARGE_SOC ,"%" ],
               [ "OVERDISCHARGE_SOC ",OVERDISCHARGE_SOC  ,"%" ],
               [ "MAX_CHARGE_CURRENT",MAX_CHARGE_CURRENT ,"A" ],
               [ "MAX_DISCHARGE_CURRENT",MAX_DISCHARGE_CURRENT ,"A" ],
               [ "AMBIENT_TEMPERATURE_SETTING",AMBIENT_TEMPERATURE_SETTING ,"-" ],
               [ "LIMIT_POWER_SETTING", LIMIT_POWER_SETTING,"-" ],
               [ "STORAGE_CONTROL_SWITCH ",STORAGE_CONTROL_SWITCH  ,"-" ],
               [ "TIMED_CHARGE_CURRENT",TIMED_CHARGE_CURRENT ,"A" ],
               [ "TIMED_DISCHARGE_CURRENT",TIMED_DISCHARGE_CURRENT ,"A" ],
               [ "MAX_GRID_CHARGING_CURRENT",MAX_GRID_CHARGING_CURRENT ,"A" ]]
    
    LIST_INV_AC_TYPE_OUTPUT.append(str(INV_AC_TYPE_OUTPUT)+" ")
    LIST_INV_PHASE_VOLTAGE.append(str(INV_PHASE_VOLTAGE)+" ")
    LIST_INV_AC_POWER.append(str(INV_AC_POWER)+" ")
    LIST_INV_STANDARD_WORKING_MODE.append(str(INV_STANDARD_WORKING_MODE)+" ")
    LIST_INV_TEMP.append(str(INV_TEMP)+" ")
    LIST_INV_CURRENT_STATUS.append(str(INV_CURRENT_STATUS)+" ")
    LIST_OPERATING_STATUS.append(str(OPERATING_STATUS)+" ")
    LIST_OPERATING_MODE.append(str(OPERATING_MODE)+" ")
    LIST_STORAGE_CONTROL.append(str(STORAGE_CONTROL)+" ")
    LIST_BAT_VOL.append(str(BAT_VOL)+" ")
    LIST_BAT_CURRENT.append(str(BAT_CURRENT)+" ")
    LIST_BAT_CURRENT_DIRECTION.append(str(BAT_CURRENT)+" ")
    LIST_BAT_POWER.append(str(BAT_POWER)+" ")
    LIST_BAT_SOC.append(str(BAT_SOC)+" ")
    LIST_BMS_VOL.append(str(BMS_VOL)+" ")
    LIST_BMS_CURRENT.append(str(BMS_CURRENT)+" ")
    LIST_BMS_CHARGE_CURRENT_LIMITATION.append(str(BMS_CHARGE_CURRENT_LIMITATION)+" ")
    LIST_BMS_DISCHARGE_CURRENT_LIMITATION.append(str(BMS_DISCHARGE_CURRENT_LIMITATION)+" ")
    LIST_BAT_CHARGEDISHCARGE_ENABLE.append(str(BAT_CHARGEDISHCARGE_ENABLE)+" ")
    LIST_BAT_CHARGEDISHCARGE_CURRENT.append(str(BAT_CHARGEDISHCARGE_CURRENT)+" ")
    LIST_BAT_CHARGE_MAX_CURRENT.append(str(BAT_CHARGE_MAX_CURRENT)+" ")
    LIST_BAT_DISCHARGE_MAX_CURRENT.append(str(BAT_DISCHARGE_MAX_CURRENT)+" ")
    LIST_CURRENT_BATTERY_MODULE.append(str(CURRENT_BATTERY_MODULE)+" ")
    LIST_OVERCHARGE_SOC.append(str(OVERCHARGE_SOC)+" ")
    LIST_OVERDISCHARGE_SOC.append(str(OVERDISCHARGE_SOC)+" ")
    LIST_MAX_CHARGE_CURRENT.append(str(MAX_CHARGE_CURRENT)+" ")
    LIST_MAX_DISCHARGE_CURRENT.append(str(MAX_DISCHARGE_CURRENT)+" ")
    LIST_AMBIENT_TEMPERATURE_SETTING.append(str(AMBIENT_TEMPERATURE_SETTING)+" ")
    LIST_LIMIT_POWER_SETTING.append(str(LIMIT_POWER_SETTING)+" ")
    LIST_STORAGE_CONTROL_SWITCH.append(str(STORAGE_CONTROL_SWITCH)+" ")
    LIST_BAT_MAX_CHARGE_CURRENT.append(str(BAT_MAX_CHARGE_CURRENT)+" ")
    LIST_BAT_MAX_DISCHARGE_CURRENT.append(str(BAT_MAX_DISCHARGE_CURRENT)+" ")
    LIST_BAT_CHARGE_LIMIT_POWER.append(str(BAT_CHARGE_LIMIT_POWER)+" ")
    LIST_BAT_DISCHARGE_LIMIT_POWER.append(str(BAT_DISCHARGE_LIMIT_POWER)+" ")
    LIST_TIMED_CHARGE_CURRENT.append(str(TIMED_CHARGE_CURRENT)+" ")
    LIST_TIMED_DISCHARGE_CURRENT.append(str(TIMED_DISCHARGE_CURRENT)+" ")
    LIST_MAX_GRID_CHARGING_CURRENT.append(str(MAX_GRID_CHARGING_CURRENT)+" ")
    
    file = open(r'C:\Users\yorick.niessink\Documents\Solis Research\Solis_Readings_Charge.txt','w')
    file.writelines(LIST_INV_AC_POWER)
    file.write("\n")
    file.writelines(LIST_INV_TEMP)
    file.write("\n")
    file.writelines(LIST_BAT_VOL)
    file.write("\n")
    file.writelines(LIST_BAT_CURRENT)
    file.write("\n")
    file.writelines(LIST_BAT_CURRENT_DIRECTION)
    file.write("\n")
    file.writelines(LIST_BAT_POWER)
    file.write("\n")
    file.writelines(LIST_BAT_SOC)
    file.write("\n")
    file.writelines(LIST_BMS_CURRENT)
    file.write("\n")
    file.writelines(LIST_BMS_CHARGE_CURRENT_LIMITATION)
    file.write("\n")
    file.writelines(LIST_BMS_DISCHARGE_CURRENT_LIMITATION)
    file.write("\n")
    file.writelines(LIST_BAT_CHARGEDISHCARGE_CURRENT)
    file.write("\n")
    file.writelines(LIST_BAT_CHARGE_MAX_CURRENT)
    file.write("\n")
    file.writelines( LIST_BAT_DISCHARGE_MAX_CURRENT)
    file.write("\n")
    file.writelines(LIST_MAX_DISCHARGE_CURRENT)
    file.write("\n")
    file.writelines(LIST_STORAGE_CONTROL_SWITCH)
    file.write("\n")
    file.writelines(LIST_BAT_MAX_CHARGE_CURRENT)
    file.write("\n")
    file.writelines(LIST_BAT_MAX_DISCHARGE_CURRENT)
    file.write("\n")
    file.writelines(LIST_BAT_CHARGE_LIMIT_POWER)
    file.write("\n")
    file.writelines( LIST_TIMED_CHARGE_CURRENT)
    file.write("\n")
    file.writelines(LIST_TIMED_DISCHARGE_CURRENT)
    file.close()         

    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    count += 1 



