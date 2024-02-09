from subprocess import Popen
import os
import SetValue
import time
import csv
import TelnetController
import re
import datetime

class Attenuation:
    
    testid=''
    teststatus=''
    com=''
    freq=''
    spliter_port=''
    attenuation=''
    monitor_time=''
    poll_time=''
    
    def execute_cmd(self,com,freq,port_spliter,attenuation):
        self.com=com
        self.freq=freq
        self.port_spliter=port_spliter
        self.attenuation=attenuation
        
        cmd = os.popen('s16 '+self.com+' '+self.freq+' '+self.port_spliter+' '+self.attenuation+ '\n',"r")
        time.sleep(2)
        kill_proc=os.popen('taskkill /IM S16.exe')
        while 1:
              line = cmd.readline()
              if not line: break
              print line,            

        '''cmd=os.system('copy killcmd.txt gokill.txt'+ '\n' \
                      's16 '+com+' '+freq+' '+port_spliter+' '+attenuation+ '\n' )'''
    def getcommand(self,command):
        self.command=command
        startindex=self.command.rfind('=')
        endindex=len(command)
        '''string = self.command[0:startindex+1] + self.command + self.command[endindex+1:]'''
        string = self.command[startindex+1:endindex]
        return string
    def pervalue(self, ldlrblk, ldldblk, ldlblk):
        self.ldlrblk=re.findall('([0-9]+)', ldlrblk)
        self.ldldblk=re.findall('([0-9]+)', ldldblk)
        self.ldlblk=re.findall('([0-9]+)', ldlblk)
        ulblk=''.join(self.ldlrblk)
        dlblk=''.join(self.ldldblk)
        dl=''.join(self.ldlblk)
        dlper1 = int(ulblk) + int(dlblk)
        dlper2 = int(dl)
        if dlper2!=0:
            dlper_almost = (dlper1*1.0 ) / (dlper2*1.0)
            dlper_final = dlper_almost*100.0
        else:
            dlper_final=0
        return str(dlper_final)


            
def main():
    file = open("Performance.csv", "w")
    file.write('Index,SC_IP,Link Name,Channel,TXPower,Radio Mode,Link Mode, DLSINADR1,ULSINADR1,DLSINADR2,ULSINADR2,DLRSSI1,ULRSSI1,DLRSSI2,ULRSSI2,DLUBR,ULUBR,DLPER'+'\n')
    file.close()
    inst=Attenuation()
    log = open("log.txt", "w")
    log.write('Write configuration to device'+'\n')
    log.close()

    counter=0
    
    sc=SetValue.getSC()
    print('Write configuration on devices......')
    config=SetValue.Run()
    time.sleep(5)
    print('Modify attenuation')
  
    testlist  = open('Attenuation.csv', "rb")
    reader = csv.reader(testlist)
    rownum=0
    for row in reader:
        if rownum==0:
            rownum+=1
            continue         
        else:
            Attenuation.testid=row[0]
            Attenuation.teststatus=row[1]
            if Attenuation.testid.startswith('#')==True:
                continue
            if 'true' in Attenuation.teststatus.lower(): 
                Attenuation.com=row[2]
                Attenuation.freq=row[3]
                Attenuation.spliter_port=row[4]
                Attenuation.attenuation=row[5]
                Attenuation.monitor_time=float(row[6])
                Attenuation.poll_time=float(row[7])
                log = open("log.txt", "a")
                log.write(' Set attenuator values Com_port: '+Attenuation.com+' Device Frequency: '+Attenuation.freq+' Spliter Port: '+Attenuation.spliter_port+' Atenuation value: '+Attenuation.attenuation+'\n')

                inst.execute_cmd(Attenuation.com, Attenuation.freq, Attenuation.spliter_port,Attenuation.attenuation)
                time.sleep(15)
                telnet = TelnetController.TelnetController(host_name = sc.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
                telnet.login()
                file = open("Performance.csv", "a")
                file.write('Atenuation value: '+Attenuation.attenuation+'\n')
                file.close()
                start = datetime.datetime.now().second
                abort_after =start+Attenuation.monitor_time 
                log.write(' Start time(): '+str(start)+' End time(sec): '+str(abort_after)+'\n')
                log.close()
                count_time=0                
                while True:
                    counter+=1
                    links_active=telnet.run_command('show links',1).split()
                    for id in range(0,len(links_active),4):
                        linetext=str(counter)+','+sc.rstrip()+','+inst.getcommand(telnet.run_command('set idname '+links_active[id],0))+','+inst.getcommand(telnet.run_command('set chsize',0))+','+inst.getcommand(telnet.run_command('get txpower',0)) +\
                             ','+inst.getcommand(telnet.run_command('set radio',0))+','+inst.getcommand(telnet.run_command('set linkmode '+links_active[id],0))+','+inst.getcommand(telnet.run_command('get ldlsnr '+links_active[id],0)) +\
                             ','+inst.getcommand(telnet.run_command('get lulsnr '+links_active[id],0))+','+inst.getcommand(telnet.run_command('get ldlsnr2 '+links_active[id],0))+','+inst.getcommand(telnet.run_command('get lulsnr2 '+links_active[id],0))+','+inst.getcommand(telnet.run_command('get ldlrssi '+links_active[id],0)) +\
                             ','+inst.getcommand(telnet.run_command('get lulrssi '+links_active[id],0))+','+inst.getcommand(telnet.run_command('get ldlrssi2 '+links_active[id],0))+','+inst.getcommand(telnet.run_command('get lulrssi2 '+links_active[id],0))+','+inst.getcommand(telnet.run_command('get ldlbr '+links_active[id],0)).replace('/','') +\
                             ','+inst.getcommand(telnet.run_command('get lulbr '+links_active[id],0))+','+inst.pervalue(inst.getcommand(telnet.run_command('get ldlrblk '+links_active[id],0)),inst.getcommand(telnet.run_command('get ldldblk '+links_active[id],0)),inst.getcommand(telnet.run_command('get ldlblk '+links_active[id],0)))+'\n'
                        print(linetext)
                        counter+=1
                        file = open("Performance.csv", "a")
                        file.write(linetext)
                        file.close()
                        log = open("log.txt", "a")
                        log.write(linetext+'\n')
                        log.close()
                    count_time+=Attenuation.poll_time
                    start_now=start+count_time
                    delta = start_now
                    if delta >= abort_after:
                        break
                    log = open("log.txt", "a")
                    log.write('Remaining time: '+str(start_now)+'\n')
                    log.close()
                    time.sleep(Attenuation.poll_time)


if __name__ == "__main__": main()
