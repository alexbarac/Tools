import TelnetController
import time
import os

def main():
        print('Modify attenuation')
        cur_dir=os.getcwd()
        exit_code = os.system('cd '+cur_dir+ '\n' \
                              '@echo off'+ '\n' \
                              ':start'+ '\n' \
                              'if exist gokill.txt ('+ '\n' \
                              'timeout /t  1'+ '\n' \
                              'del gokill.txt'+ '\n' \
                              'taskkill /IM S16.exe)'+ '\n' \
							  'goto start'+ '\n' \
                             )    
        start_code = os.system(':start'+ '\n' \
							  'copy killcmd.txt gokill.txt'+ '\n' \
							  's16 '+str(8)+' '+str(3.3)+' '+str(1)+' '+str(2)+ '\n' \
							  'goto start'+ '\n' \
							  )  # Just execute the command, return a success/fail code
        output    =os.popen('@echo off'+ '\n' \
                              ':start'+ '\n' \
                              'if exist gokill.txt ('+ '\n' \
                                'timeout /t  1'+ '\n' \
                                'del gokill.txt'+ '\n' \
                                'taskkill /IM S16.exe)'+ '\n' \
                                ).read()

if __name__ == "__main__": main()
