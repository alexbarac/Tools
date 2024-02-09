import TelnetController
import time
import os
import subprocess

def main():
        print('Modify attenuation')
        cur_dir=os.getcwd()
        try:
            p1 = subprocess.Popen(['cd '+cur_dir+ '\n' \
                                  '@echo off'+ '\n' \
                                  ':start'+ '\n' \
                                  'if exist gokill.txt ('+ '\n' \
                                  'timeout /t  1'+ '\n' \
                                  'del gokill.txt'+ '\n' \
                                  'taskkill /IM S16.exe)'+ '\n' \
                                  'goto start'+ '\n'], stdout=subprocess.PIPE)
        
        # Run the command
            output1 = p1.communicate()[0]
        
            print output1
        except Exception, e:
            print(str(e))
            

        p2 = subprocess.Popen([':start'+ '\n' \
                              'copy killcmd.txt gokill.txt'+ '\n' \
                              's16 '+str(8)+' '+str(3.3)+' '+str(1)+' '+str(2)+ '\n' \
                              'goto start'+ '\n'], stdout=subprocess.PIPE)
        
        # Run the command
        output2 = p2.communicate()[0]
        
        print output2
        
        
        


if __name__ == "__main__": main()