import telnetlib
import TelnetController
import time
import re
import csv
from datetime import datetime

class CLI:
    testid=''
    devicetype=''
    command=''
    response=''
    postaction=''
    
    
    def replacecmd(self,command):
        self.command=command
        startindex=self.command.rfind('$')
        endindex=len(command)
        '''string = self.command[0:startindex+1] + self.command + self.command[endindex+1:]'''
        string = self.command[startindex+1:endindex]
        return string

    def getcmd(self,command):
        self.command=command
        startindex=self.command.rfind('$')
        endindex=len(command)
        '''string = self.command[0:startindex+1] + self.command + self.command[endindex+1:]'''
        string = self.command[0:startindex-1]
        return string
    
class TestSuite:
    testid=''
    teststatus=''
    testfile=''
    deviceip=''
    description=''
    devicetype=''
    
def main():
    
    cli=CLI()
    suite=TestSuite()
    file_name="ReportTestCLI"+str(datetime.now())+".csv"

    file = open(file_name, "w")
    file.write('TestId,Command,Response,Expected Response, Results'+'\n')
    file.close()

    testlist  = open('TestSuite.csv', "rb")
    reader = csv.reader(testlist)
    rownum=0
    
    for row in reader:
        if rownum==0:
            rownum+=1
            continue        
        else:
            suite.teststatus=row[1]
            if 'true' in suite.teststatus.lower(): 
                suite.testid=row[0]
                suite.deviceip=row[2]
                suite.testfile=row[4]
                suite.description=row[5]
                suite.devicetype=row[3]

                file = open(file_name, "a")
                file.write(10*'*'+suite.devicetype+' - '+suite.description+10*'*'+"\n")
                file.close()
                
                testfile  = open(suite.testfile, "rb")
                readerfile = csv.reader(testfile)
                rowfilecount=0
                global id 
                global result      
                global postaction
                for rowfile in readerfile:
                    if rowfilecount==0:
                        rowfilecount+=1
                        telnet = TelnetController.TelnetController(host_name = suite.deviceip.rstrip(), user_name = 'admin', password = 'admin', prompt = '#')
                        telnet.login()
                        
                        continue 
                    else:
                        if suite.devicetype.find('Connect')!=-1:
                            cli.testid=rowfile[0]
                            cli.command=rowfile[1]
                            cli.response=rowfile[2]
                            #result=cli.getcommand(telnet.run_command(cli.command, 0))
                            result=telnet.run_command(cli.command, 0)
                            telnet.run_command('apply config', 0)

                            if result.find(cli.response)!=-1 and result.find('Error')==-1 and result.find('^Syntax')==-1:
                                file = open(file_name, "a")
                                file.write(cli.testid+','+cli.command+','+result+','+cli.response+','+'PASS'+"\n")
                                file.close()
                            else:
                                file = open(file_name, "a")
                                file.write(cli.testid+','+cli.command+','+result+','+cli.response+','+'FAIL'+'\n')
                                file.close()
                        elif suite.devicetype.find('RDL300')!=-1:
                            cli.testid=rowfile[0]
                            cli.command=rowfile[4]
                            cli.response=rowfile[5]
                            cli.postaction=rowfile[6]
                            if cli.postaction!='':
                                cli.postaction=rowfile[6]
                                postaction=cli.postaction
                                result_id=telnet.run_command(cli.command, 0)
                                id = re.sub(r'\D', "", result_id)
                            #result=cli.getcommand(telnet.run_command(cli.command, 0))
                            if cli.command.find('$')!=-1:
                                cli.command=cli.command.replace('$'+postaction,id)
                                result=telnet.run_command(cli.command, 0)
                                #telnet.run_command(' ', 0)
                                
                            else:
                                result=telnet.run_command(cli.command, 0)
                                #telnet.run_command(' ', 0)
                            result_temp=result.replace(' ','')
                            cli_temp=cli.response.replace(' ','')

                            if result_temp.find(cli_temp)!=-1:
                                file = open(file_name, "a")
                                file.write(cli.testid+','+cli.command+','+result.strip('\r\n')+','+cli.response+','+'PASS'+"\n")
                                file.close()
                            else:
                                file = open(file_name, "a")
                                file.write(cli.testid+','+cli.command+','+result.strip('\n')+','+cli.response+','+'FAIL'+'\n')
                                file.close()

                             
                        
if __name__ == "__main__": main()
            

            
            
        
