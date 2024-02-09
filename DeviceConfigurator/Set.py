import TelnetController
import threading
import sys
import os


def getcommand(command):
    startindex=command.rfind('=')
    endindex=len(command)
    string = command[startindex+1:endindex]
    return string


def worker(num,cmdlist):

    radiotype=''
    login_status=False

    response = os.system("ping " +num.rstrip()+ " -n 1")
    if response != 0:
        print('Error: Device is not up  '+num+'\n')
        return
    
    telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
    login_status=telnet.login()
    if login_status==False:
        print('Error: Unable to start a telnet session on device  '+num+'\n')
        return
    radiotype=getcommand(telnet.run_command('get radiotype',0))
    #cmdlist = open('commands.txt')
    if login_status==True:
        for cmd in cmdlist:
            try:
                if '#' in cmd:
                    continue
                if 'sysname' in cmd:
                    resp=telnet.run_command(cmd+'_'+num.rstrip(), 0)
                    continue
                if 'upgrade' in cmd:
                    if 'RDL3KR2' in cmd and (radiotype.find('T502A')!=-1 or radiotype.find('T352A')!=-1):
                        resp=telnet.run_command(cmd.rstrip(), 0)
                        continue
                    elif 'RDL3000' in cmd and radiotype.find('T502')!=-1:
                        resp=telnet.run_command(cmd.rstrip(), 0)
                        continue
                    elif 'RDL3KR4_0225' in cmd and (radiotype.find('T072AH1')!=-1 or radiotype.find('T212A')!=-1 or radiotype.find('T202A')!=-1 or radiotype.find('T352B')!=-1 or radiotype.find('T502C')!=-1):
                        resp=telnet.run_command(cmd.rstrip(), 0)
                        continue
                    elif 'RDL3KR4_0227' in cmd and (radiotype.find('T072AH1')!=-1 or radiotype.find('T212A')!=-1 or radiotype.find('T202A')!=-1 or radiotype.find('T352B')!=-1 or radiotype.find('T502C')!=-1):
                        resp=telnet.run_command(cmd.rstrip(), 0)
                        continue
                    elif 'RDL3KR4_0300' in cmd and (radiotype.find('T072AH1')!=-1 or radiotype.find('T212A')!=-1 or radiotype.find('T202A')!=-1 or radiotype.find('T352B')!=-1 or radiotype.find('T502C')!=-1):
                        resp=telnet.run_command(cmd.rstrip(), 0)
                        continue
                    elif 'RL80PMP' in cmd and (radiotype.find('T35i')!=-1 or radiotype.find('T49i')!=-1 or radiotype.find('T54i')!=-1 or radiotype.find('T58i')!=-1):
                        resp=telnet.run_command(cmd.rstrip(), 0)
                        continue
                else:
                    resp=telnet.run_command(cmd, 0)
            except Exception, e:
                print(str(e))
                if 'chgver' in cmd: 
                    pass
    telnet.logout()                
'''def main():
    threads = []
    log = open("log.txt", "w")
    log.write('Starting log file')
    iplist = open('iplist.txt')
    for ip in iplist.readlines():
        print(ip.rstrip())
        t = threading.Thread(target=worker, args=(ip,))
        threads.append(t)
        t.start()
    log.close()
        
    
    
if __name__ == "__main__": main()'''
