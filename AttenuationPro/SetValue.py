import TelnetController
import threading
import sys

def getcommand(command):
    startindex=command.rfind('=')
    endindex=len(command)
    string = command[startindex+1:endindex]
    return string

def getSC():
    iplist = open('iplist.txt')
    for ip in iplist.readlines():
        telnet = TelnetController.TelnetController(host_name = ip.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
        telnet.login()
        devicetype=getcommand(telnet.run_command('set sysmode',0))
        if devicetype.find('pmpsc')!=-1:
            return ''.join(ip)
    
        
        

def worker(num):

    radiotype=''
    login_status=False
    telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
    login_status=telnet.login()
    if login_status==False:
        print('Error: Unable to start a telnet session on device  '+num+'\n')
        return
    radiotype=getcommand(telnet.run_command('get radiotype',0))
    cmdlist = open('commands.txt')
    if login_status==True:
        for cmd in cmdlist.readlines():
            try:
                if '#' in cmd:
                    continue
                if 'upgrade' in cmd:
                    if 'RDL3KR2' in cmd and (radiotype.find('T502A')!=-1 or radiotype.find('T352A')!=-1):
                        resp=telnet.run_command(cmd.rstrip(), 0)
                        continue
                    elif 'RDL3000' in cmd and radiotype.find('T502')!=-1:
                        resp=telnet.run_command(cmd.rstrip(), 0)
                        continue
                    elif 'RDL3KR4_0225' in cmd and (radiotype.find('T072A')!=-1 or radiotype.find('T072AH1')!=-1 or radiotype.find('T212A')!=-1 or radiotype.find('T202A')!=-1 or radiotype.find('T352B')!=-1 or radiotype.find('T502C')!=-1):
                        resp=telnet.run_command(cmd.rstrip(), 0)
                        continue
                    elif 'RDL3KR4_0300' in cmd and (radiotype.find('T072A')!=-1 or radiotype.find('T072AH1')!=-1 or radiotype.find('T212A')!=-1 or radiotype.find('T202A')!=-1 or radiotype.find('T352B')!=-1 or radiotype.find('T502C')!=-1):
                        resp=telnet.run_command(cmd.rstrip(), 0)
                        continue
                    elif 'RL80PMP' in cmd and (radiotype.find('T35i')!=-1 or radiotype.find('T49i')!=-1 or radiotype.find('T54i')!=-1 or radiotype.find('T58i')!=-1):
                        resp=telnet.run_command(cmd.rstrip(), 0)
                        continue
                else:
                    resp=telnet.run_command(cmd.rstrip(), 0)
            except Exception, e:
                print(str(e))
                if 'chgver' in cmd: 
                    pass
    telnet.logout() 

def Run():               
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
        
