# Import modules
from machine import Pin,ADC # Pins for GPIO pins and ADC for reading analog data from the LDR
from time import sleep_ms   # just for the delays in the code
from network import WLAN , AP_IF # Import WirelessLAN and AccessPoint Internet Family
from socket import socket,AF_INET,SOCK_STREAM  # import socket class 



############### Initial data and variables ##################
### 7 segment lookup tables ###
#Array with data pins values to show any digit on 7 segment
draw_digit=[[0,0,0,0,0,0,1]#0
    ,[1,0,0,1,1,1,1]#1
    ,[0,0,1,0,0,1,0]#2
    ,[0,0,0,0,1,1,0]#3
    ,[1,0,0,1,1,0,0]#4
    ,[0,1,0,0,1,0,0]#5
    ,[0,1,0,0,0,0,0]#6
    ,[0,0,0,1,1,1,1]#7
    ,[0,0,0,0,0,0,0]#8
    ,[0,0,0,0,1,0,0]]#9
#Array with data pins values to show 0 with slow motion
zero_slow=[[0,1,1,1,1,1,1]
    ,[0,0,1,1,1,1,1]
    ,[0,0,0,1,1,1,1]
    ,[0,0,0,0,1,1,1]
    ,[0,0,0,0,0,1,1]
    ,[0,0,0,0,0,0,1]
    ,[0,0,0,0,0,0,1]]
#Array with data pins values to show 9 with slow motion
nine_slow=[[1,1,1,1,1,1,0]
    ,[1,1,1,1,1,0,0]
    ,[0,1,1,1,1,0,0]
    ,[0,0,1,1,1,0,0]
    ,[0,0,0,1,1,0,0]
    ,[0,0,0,0,1,0,0]
    ,[0,0,0,0,1,0,0]]


### initial variable data ###
Counter=0  #Initialize Counter
LDR = ADC(0) # config the analog input
code = 1    # for sending ldr state as coded data
keypad = [] # for taking keypad data from the app
stop_resume = True  # for stop and resume functionality of the whole app



#SET INPUT & OUTPUT PINS
data_pins=[5,16,12,13,15,4,0] #A__B__C__D__E__F__G#
input_pins=[10,2,14] #increase__decrease__reset#
bulb = Pin(3,Pin.OUT)
out_pins = []
in_pins = []
for k in data_pins:
    out_pins.append(Pin(k,Pin.OUT))
for k in input_pins:
    in_pins.append(Pin(k,Pin.IN,Pin.PULL_UP))



############ The main program functions ##################

### to output the counter data to the seven segment display 
def seven_segment(Counter):#Draw Counter on 7 Segment
    if Counter>=0 and Counter<=9:
        for k in range(7):#Draw Counter Normally
            out_pins[k].value(draw_digit[Counter][k])
        sleep_ms(500)
    elif Counter<0:
        for k in range(7):#Draw Nine Slow Motion
            for l in range(7):
                out_pins[l].value(nine_slow[k][l])
            sleep_ms(500)
    else :
        for k in range(7):#Draw Zero Slow Motion
            for l in range(7):
                out_pins[l].value(zero_slow[k][l])
            sleep_ms(500)

#### To change the counter value 
def increase():#Increase Counter Function__is CALLED Any where we need increase counter
    global Counter
    Counter+=1
    seven_segment(Counter)#Send Counter to show on 7 Segment
    if(Counter>9):
        Counter=0
        
def decrease():#Decrease Counter Function__is CALLED Any where we need decrease counter
    global Counter
    Counter-=1
    seven_segment(Counter)#Send Counter to show on 7 Segment
    if(Counter<0):
        Counter=9
        
def reset():#Reset Counter Function__is CALLED Any where we need reset counter
    global Counter
    Counter=0
    seven_segment(Counter)#Send Counter to show on 7 Segment
    
    
    
### for taking the input from the pushbuttons
    
def debounce(pin):#Debouncing Function To Avoid Non Perfect Contact
    previous_value = None#Initial A Temp Variable
    for k in range(10):#Take 10 Samples of Signal
        current_value = pin.value()#Take Sample
        if previous_value != None and previous_value != current_value:
            return None #If Rippled Return None
        previous_value = current_value
    return previous_value#AFTER 10 Samples return New State
    
def increase_interrupt(pin):#Interrupt Routine for Increment
    d = debounce(pin)#Check Bouncing
    if not d:
        increase()#After 10 Samples Excute Increment

def decrease_interrupt(pin):#Interrupt Routine for Decrement
    d = debounce(pin)#Check Bouncing
    if not d:
        decrease()#After 10 Samples Excute Decrement
    
def reset_interrupt(pin):#Interrupt Routine for Reset
    d = debounce(pin)#Check Bouncing
    if not d:
        reset()#After 10 Samples Excute Reset
        
        
        
# SET Interrupts Pins
handlers=[increase_interrupt,decrease_interrupt,reset_interrupt]
for k in range(3):
    in_pins[k].irq(trigger=Pin.IRQ_FALLING, handler=handlers[k])

##### the main web page we manage the web site as serverside rendering web application 

def web_page(Counter, code):
    title= str(Counter)+str(code)   # the data we send 
    html_page = """<html>
    <head>
        <title>""" + title + """</title>
    <meta content="width=device-width, initial-scale=1" name="viewport"></meta>
    <style>
        .button {
            background-color:blue;
            width:250px;
            border:none;
            color:white;
            padding:15px 32px;
            margin:1vw;
            font-size:16px;
            }
    </style>
    </head>
    <center><body style="background-color:f5f5f5">
        <div>
            <p style="font-size:4vw;font-weight:bold;">The Project Team</p>
            <p style="font-size:2vw">Seven Segment Control Project</p>
        </div>
        <hr/>
        <p style="font-size:2vw">7 Segment Dispaly Value """ + str(Counter) + """</p>
        <p style="font-size:2vw">The light bulb intensity is """ + state + """</p>
        <div><form>
            <button class="button" name="increase" type="submit" value="">Increase</button>
            <br>
            <button class="button" name="decrease" type="submit" value="">Decrease</button>
            <br>
            <button class="button" name="reset" type="submit" value="">Reset</button>
            <br>
            <button class="button" name="refresh" type="submit" value="">Refresh</button>
            <br>
            <button class="button" name="on" type="submit" value="">ON</button>
            <br>
            <button class="button" name="off" type="submit" value="">OFF</button>
        </form></div>
    </body></center>
    </html>"""
    return html_page


###### creating and initialization of wifi access point ########

WIFI = WLAN(AP_IF) # Create a WLAN object as AccessPoint
WIFI.config(essid='Seven Segment Controller',password='7777*7777',authmode=4) #Configure Access Point Name , Encryption and Password
WIFI.active(True)  #Turn Access Point on
while not WIFI.isconnected():
        pass   # Don't Skip until Connection Success  Note That ESP IP is 192.168.4.1 in Default
    

###### creating and initialization of sockets ########
#Create Object of socket Class
s = socket(AF_INET,SOCK_STREAM)   #AddressFamily:IP v4 | TCP Protocol
s.bind(('',80))  #Assign socket to ESP Address on Port 80 (HTTP PORT)
s.listen(10)  #Start accepting TCP connections with maximum 10 connections


######   initialization seven segment with 0 value ########
seven_segment(0)#Initialize 7 Segment Dispaly to ZERO


########## The main loop of the program #############

while(1):
    try:
        ####### connection and request part #########
        #Start Accepting New connection and make new accept object to use and take client address and port
        connection,sender_address=s.accept()
        connection.settimeout(3)#Set Connection timeout to 3 Seconds
        request=connection.recv(1024) # receive data with maximum 1024 Bytes
        connection.settimeout(None) # Unlimited Timeout
        request = str(request)#Cast Byte Object to String
        
        
        ####### filtering the request and request part #########
        increase_request =request.find('GET /?increase')#Search for increase parameter
        decrease_request = request.find('GET /?decrease')#Search for decrease parameter
        reset_request = request.find('GET /?reset')#Search for reset parameter
        on_request = request.find('GET /?on')#Search for decrease parameter
        off_request = request.find('GET /?off')#Search for reset parameter
        stop_resume_request = request.find('GET /?sr')#Search for reset parameter
        
        # keypad code
        for i in range(10):
            keypad.append(request.find('GET /?num'+str(i)))#Search for reset parameter
        
        for i in range(10):
            if (keypad[i] != -1):
                Counter = i
                
        if(stop_resume != -1):
                stop_resume = not stop_resume
        if stop_resume:
            #Excute operation according to the parameter found
            if(increase_request != -1):
                increase()
                
            elif(decrease_request != -1):
                decrease()
            
            elif(reset_request != -1):
                reset()
                
            # The LDR Value
            ldr_value = LDR.read()
            if ldr_value > 30:
                state = "weak"
                code = 1
            if ldr_value > 250:
                state = "moderate"
                code = 2
            if ldr_value > 900:
                state = "intensive"
                code = 3
            #   Relay (bulb) control
            if(on_request != -1):
                bulb.value(1)
            elif(off_request != -1):
                bulb.value(0)
        
        #send web page after updating counter
        connection.sendall(web_page(Counter, code))
        connection.close()#close connection 
        
    except :
        connection.close()#In case error close connection

