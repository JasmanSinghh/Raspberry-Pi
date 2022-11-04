import RPi.GPIO as GPIO
import time
import random
from tkinter import*
import tkinter.messagebox

class MyGUI:
    def __init__(self):
        self.main_window=Tk()
        self.main_window.geometry("300x300+700+100")
        self.main_window.title("Project 3")
        
        label1 = Label(self.main_window, text = "Select the amount of LIVES: ")
        label1.place(x=10,y=10)
        
        label2 = Label(self.main_window, text = "Select the SENSITIVITY: ")
        label2.place(x=10,y=80)
        
        self.entry1 = Entry(self.main_window , width=10)
        self.entry1.place(x=10,y=40)
        
        self.var = DoubleVar()
        self.scale = Scale(self.main_window,orient = HORIZONTAL,from_=1, to=5,tickinterval = 0.5,variable = self.var)
        self.scale.place(x=10,y=100)
        
        button = Button(self.main_window, text="Okay", command=self.do_this)
        button.place(x=150, y=200)
        button1 = Button(self.main_window, text="Quit", command=self.main_window.destroy)
        button1.place(x=150, y=240)
        mainloop()
        
    def do_this(self):

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(18,GPIO.OUT) #TRIGGER 1
        GPIO.setup(9,GPIO.OUT) #TRIGGER 2
        GPIO.setup(23,GPIO.OUT) #BUZZER
        GPIO.setup(24,GPIO.IN) #ECHO 1
        GPIO.setup(11,GPIO.IN) #ECHO 2
        GPIO.setup(20,GPIO.OUT) #RED
        GPIO.setup(21,GPIO.OUT) #GREEN
        GPIO.setup(25,GPIO.IN, pull_up_down = GPIO.PUD_UP) #Button

        #7-Segment ONE
        GPIO.setup(4,GPIO.OUT) #A
        GPIO.setup(17,GPIO.OUT) #B
        GPIO.setup(27,GPIO.OUT) #C
        GPIO.setup(22,GPIO.OUT) #D
        GPIO.setup(5,GPIO.OUT) #E
        GPIO.setup(6,GPIO.OUT) #F
        GPIO.setup(13,GPIO.OUT) #G
        def light_up_number_1(number_1):
            for i in range(7):
                GPIO.output(LED_1[i],numbers_1 [number_1][i])
        LED_1 = [4,17,27,22,5,6,13]
        numbers_1 = {
            0: [1,1,1,1,1,1,0],
            1: [0,1,1,0,0,0,0],
            2: [1,1,0,1,1,0,1],
            3: [1,1,1,1,0,0,1],
            4: [0,1,1,0,0,1,1],
            5: [1,0,1,1,0,1,1],
            6: [1,0,1,1,1,1,1],
            7: [1,1,1,0,0,0,0], 
            8: [1,1,1,1,1,1,1],
            9: [1,1,1,1,0,1,1]}
        
        #7-Segment TWO
        GPIO.setup(14,GPIO.OUT) #A
        GPIO.setup(15,GPIO.OUT) #B
        GPIO.setup(8,GPIO.OUT) #C
        GPIO.setup(7,GPIO.OUT) #D
        GPIO.setup(12,GPIO.OUT) #E
        GPIO.setup(16,GPIO.OUT) #F
        GPIO.setup(26,GPIO.OUT) #G
        def light_up_number_2(number_2):
            for l in range(7):
                GPIO.output(LED_2[l],numbers_2[number_2][l])
        LED_2 = [14,15,8,7,12,16,26]
        numbers_2 = {
            0: [1,1,1,1,1,1,0],
            1: [0,1,1,0,0,0,0],
            2: [1,1,0,1,1,0,1],
            3: [1,1,1,1,0,0,1],
            4: [0,1,1,0,0,1,1],
            5: [1,0,1,1,0,1,1],
            6: [1,0,1,1,1,1,1],
            7: [1,1,1,0,0,0,0], 
            8: [1,1,1,1,1,1,1],
            9: [1,1,1,1,0,1,1]}

        GPIO.output(21,False)
        n_1 = int(self.entry1.get())
        n_2 = int(self.entry1.get())
        if n_1 > 9:
            tkinter.messagebox.showinfo('Error',"Sorry, You cannot have more than 9 players")
        else:
            light_up_number_1(n_1)
            light_up_number_2(n_2)
            while True:
                #Distance Sensor ONE
                def PlayerOne():
                    GPIO.output(18,True)
                    time.sleep(0.00001)
                    GPIO.output(18,False)
                    start_time_1 = time.time()
                    stop_time_1 = time.time()
                    while GPIO.input(24) == 0:
                        start_time_1 = time.time()
                    while GPIO.input(24) == 1:
                        stop_time_1 = time.time()
                    time_gone_1 = stop_time_1 - start_time_1
                    PlayerOne = (time_gone_1 * 34300) /2
                    return PlayerOne
                time.sleep(.5)
                new_distance_1 = PlayerOne()
                
                #Distance Sensor TWO
                def PlayerTwo():
                    GPIO.output(9,True)
                    time.sleep(0.00001)
                    GPIO.output(9,False)
                    start_time_2 = time.time()
                    stop_time_2 = time.time()
                    while GPIO.input(11) == 0:
                        start_time_2 = time.time()
                    while GPIO.input(11) == 1:
                        stop_time_2 = time.time()
                    time_gone_2 = stop_time_2 - start_time_2
                    PlayerTwo = (time_gone_2 * 34300) /2
                    return PlayerTwo
                time.sleep(.5)
                new_distance_2 = PlayerTwo()
                
                count = 0
                while count < 5:
                        GPIO.output(20,True) #RED LED
                        GPIO.output(21,False)
                        count += 1
                        time.sleep(0.01)
                        distOne = PlayerOne()
                        distTwo = PlayerTwo()
                        print("Measured Distance One = %.1f cm" % distOne)
                        print("Measured Distance Two = %.1f cm" % distTwo)
                        time.sleep(1)
                        sensitivity = self.scale.get()
                        if PlayerOne() <= ((new_distance_1)-sensitivity): #Can't move forward 0.0077
                            n_1 -=1
                            light_up_number_1(n_1)
                            print('One',n_1)
                            for j in range(100): #Buzzer
                                GPIO.output(23,GPIO.HIGH)
                                time.sleep(0.01)
                                GPIO.output(23,GPIO.LOW)
                                time.sleep(0.01)
                            for k in range(5):
                                GPIO.output(20,True)
                                time.sleep(.1)
                                GPIO.output(20,False)
                                time.sleep(.1)
                            count = 5
                            
                        if PlayerTwo() <= ((new_distance_2)-sensitivity): #Can't move forward 0.0077
                            n_2-=1
                            light_up_number_2(n_2)
                            print('Two',n_2)
                            for j in range(100): #Buzzer
                                GPIO.output(23,GPIO.HIGH)
                                time.sleep(0.01)
                                GPIO.output(23,GPIO.LOW)
                                time.sleep(0.01)
                            for k in range(5):
                                GPIO.output(20,True)
                                time.sleep(.1)
                                GPIO.output(20,False)
                                time.sleep(.1)
                            count = 5
                            
                if count == 5:
                    GPIO.output(21,True) #GREEN LED
                    time.sleep(5)
                    GPIO.output(21,False)
                if n_1 == 0:
                    print("Player Two Won")
                    time.sleep(5)
                    light_up_number_1(n_1)
                    light_up_number_2(n_2)
                    exit()
                if n_2 == 0:
                    print("Player One Won")
                    time.sleep(5)
                    light_up_number_1(n_1)
                    light_up_number_2(n_2)
                    exit()

            GPIO.cleanup()
my_gui=MyGUI()
