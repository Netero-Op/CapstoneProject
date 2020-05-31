#!/usr/bin/python
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
import time
import RPi.GPIO as GPIO
import smtplib
import cv2
import pygame
import pygame.camera
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
lcd = Adafruit_CharLCD(26,19,12,16,20,21,16,2,1)
GPIO.setmode(GPIO.BCM)
#Speaker



#sensor
##GPIO.setup(23, GPIO.IN, GPIO.PUD_UP)
##while (True):
##        time.sleep(2)
##        if GPIO.input(23) == 1:
##            print "Switch is open"
##        else:
##            print "Switch is closed"
##keypad
def KeyPad():
        MATRIX = [ [1,2,3],
                   [4,5,6],
                   [7,8,9],
                   ['*',0,'#'] ]


        ROW = [4,17,27,22]
        COL = [5,6,13]

        for j in range(3):
                GPIO.setup(COL[j], GPIO.OUT)
                GPIO.output(COL[j], 1)

        for i in range(4):
                GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

        try:
                while(True):
                    for j in range(3):
                        GPIO.output(COL[j],0)

                        for i in range(4):
                    
                            if GPIO.input(ROW[i]) == 0:
                                return MATRIX[i][j]
            
                                #lcd.message(str(MATRIX[i][j]))smtplibC
                                while(GPIO.input(ROW[i]) == 0):
                                  pass
                                  time.sleep(0.2)
                                  
                        GPIO.output(COL[j],1)
        except KeyboardInterrupt:
                GPIO.cleanup()
def KeyPad2():
        MATRIX = [ [1,2,3],

                   [4,5,6],
                   [7,8,9],
                   ['*',0,'#'] ]


        ROW = [4,17,27,22]
        COL = [5,6,13]

        for j in range(3):
                GPIO.setup(COL[j], GPIO.OUT)
                GPIO.output(COL[j], GPIO.LOW)

        for i in range(4):
                GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)

        
        rowNum = -1
        for i in range(4):
                tmpRead = GPIO.input(ROW[i])
                if tmpRead == 0:
                        rowNum = i

        if rowNum < 0 or rowNum > 3:
                exit1()
                print rowNum
                return
        
        for j in range(3):
                GPIO.setup(COL[j], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

        GPIO.setup(ROW[rowNum], GPIO.OUT)
        GPIO.output(ROW[rowNum], GPIO.HIGH)

        
        colNum = -1
        for j in range(3):
                tmpRead = GPIO.input(COL[j])
                if tmpRead == 1:
                        colNum = j
                        
        if colNum < 0 or colNum > 2:
                exit1()
                print colNum
                return 

        exit1()
        print rowNum
        print colNum
        print MATRIX[rowNum][colNum]
        return MATRIX[rowNum][colNum]


def exit1():
        ROW = [4,17,27,22]
        COL = [5,6,13]

        # Reinitialize all rows and columns as input at exit
        for i in range(4):
                GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP) 
        for j in range(3):
                GPIO.setup(COL[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)
       
        

def send_mail(filename): #the texting portion
    #TO= '5163077751@txt.att.net'
    TO= '5163077751@mms.att.net'
    #TO= '9178059715@messaging.sprintpcs.com'
    #TO= '6313167773@messaging.sprintpcs.com'
    GMAIL_USER= "fscpi2017@gmail.com"
    PASS= "Cruz12345!"
    SUBJECT = 'Alert! Your Raspberry Pi detected an intruder!'
    msg = MIMEMultipart()
    print "Sending text"
    server = smtplib.SMTP('smtp.gmail.com:587')
    print "Test"
    server.starttls()
    server.login(GMAIL_USER,PASS)
    header = 'To: ' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject: ' + SUBJECT + '\n'
    print header
    msg['Subject'] = 'Alert! Your Raspberry Pi detected an intruder!'
    msg['From'] = GMAIL_USER
    msg['To'] = TO
    #msg.preamble = 'Alert!'
    fp = open(filename+".jpg",'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    
    server.sendmail(GMAIL_USER,TO,msg.as_string())
    server.quit()
    time.sleep(1)
    print "Text sent"
    return 
    
##while True:
##    if GPIO.input(4)==1: #trigger if sensor has detected something
##        send_mail()
##        time.sleep(60*2) #Sleep for 2 minutes
##    else:
##        time.sleep(5) #check every 5 seconds
def camera():
        strtime = datetime.now().strftime('%b %d %H:%M:%S\n')
        pygame.camera.init()
        pygame.camera.list_cameras() #Camera detected or not
        cam = pygame.camera.Camera("/dev/video0",(640,480))
        cam.start()
        img = cam.get_image()
        pygame.image.save(img,strtime+".jpg")
        return strtime

def statusCheck():
        lcd.clear()
	lcd.message("1 to arm")
	while(True):
                if (KeyPad() != 1):
                        lcd.clear()

                        lcd.message("1 to arm")
                else:
                        break
	armProcedure()

def armProcedure():
	password = 1234

	lcd.clear()
	lcd.message("Enter password")
	userpass = usrPassword()
        if (userpass == password):
                lcd.clear()
                lcd.message("1System Armed \nPress 2 disarm")
                armed(password)
	
        else:
                lcd.clear()
                lcd.message("1Wrong Password")
                time.sleep(2)
                armProcedure()
        
def armed(password):
        while(True):
                if(GPIO.input(23) == 0):
                        time.sleep(1)
                        lcd.clear()
                        lcd.message("3System Armed \nPress 2 disarm")
                        time.sleep(1)
                        temp = KeyPad2()
                        if (temp < 2 or temp > 2):
                                lcd.clear()
                                lcd.message("2System Armed\nPress 2 to disarm")
                        else:
                                break
                else:
                        lcd.clear()
                        lcd.message("Sensor is open")
                        temp =camera()
                        send_mail(temp)
                        
                        time.sleep(5)
        lcd.clear()       	
	lcd.message("Enter password \nto Disarm" )
	time.sleep(2)
	userpass = usrPassword()
	if (userpass == password):
                        lcd.clear()   
			lcd.message("System Unarmed/n")
                        
			statusCheck()	
	else:
                lcd.clear()
		lcd.message("2Wrong Password\n Please press 2 to Disarm")
		
		armed(password)
		
def usrPassword():
        user = 0
        lcd.clear()
	lcd.message("Enter password-2")
	time.sleep(.5)
        user += (KeyPad() * 1000)
        time.sleep(.5)
        
        print user
        user += (KeyPad() * 100)
        time.sleep(.5)
        print user
        user += (KeyPad() * 10)
        time.sleep(.5)
        print user
        user += (KeyPad() * 1)
        time.sleep(.5)
        print user
        lcd.clear()
	lcd.message("Enter password-3")
        return user

def passwordChange():

        lcd.clear()
        lcd.message("Enter New password-2")
        time.sleep(.5)
        newPassword = usrPassword()
        global password
        password = newPassword
        lcd.clear()
        lcd.message("Password Changed")
        time.sleep(2)

GPIO.setup(23, GPIO.IN, GPIO.PUD_UP)        
statusCheck()
#KeyPad()
#lcd.message(str(KeyPad()))
