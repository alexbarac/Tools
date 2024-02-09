import TelnetController
import time
import os
import subprocess

def main():
        print('Modify attenuation')
        cur_dir=os.getcwd()
        PROCNAME = "S16.exe"
        while True:
            '''if os.path.isfile('gokill.txt'):  
                os.remove('gokill.txt')
            os.system('pkill '+PROCNAME)''' 
            '''p2 = subprocess.Popen([':start'+ '\n' \
                                  'copy killcmd.txt gokill.txt'+ '\n' \
                                  's16 '+str(8)+' '+str(3.3)+' '+str(1)+' '+str(2)+ '\n' \
                                  'goto start'+ '\n'], stdout=subprocess.PIPE)'''
            line=                 'cd C:\Users\pc2\Desktop\VarAtt - R2\Attenuation '+ '\n' \
                                  ':start'+ '\n' \
                                  'copy killcmd.txt gokill.txt'+ '\n' \
                                  's16 '+str(8)+' '+str(3.3)+' '+str(1)+' '+str(2)+ '\n' \
                                  'goto start'+ '\n'
            CommandOutput=os.popen('dir','D:\Python doc\Lynda.com - Python 3 Essential Training\Exercise Files\12 Classes','dir' ).read()
            # Run the command
            #output2 = p2.communicate()[0]
            
            print CommandOutput
        
        
        


if __name__ == "__main__": main()