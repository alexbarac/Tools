"""
Created on Sep 18, 2014

@author: abarac
"""
import tftpy
import time

import TelnetController
import os

class Provision:

    def __init__(self):
        pass

    @staticmethod
    def createProv(num,idlink,ssmac,ssip,dict):

        flag_run=False
        #createProv(self,num,idlink,ssmac,ssip,idgroup,idservice,vlangr,vlanser,tftpip)
        #sw=Device.Device().getswversion(num)
        global i
        servicevlan=dict['servicevlan']
        dlubr=dict['dlubr']
        ulubr=dict['ulubr']
        serviceid=len(servicevlan.split(','))
        tftpip=dict['tftp']
        modulation=dict['modulation']
        radiomode=dict['radio']
        cp=dict['cp']
        channel=dict['channel']
        frequency=dict['frequency']
        cir=dict['cir']
        pir=dict['pir']
        user=dict['user']
        pasw=dict['pasw']
        vlanfilter=dict['vlanfilter']
        syslog=dict['syslog']

        telnet = TelnetController.TelnetController(host_name = num.rstrip(), user_name = user, password = pasw, prompt = '#')
        telnet.login()
        telnet.run_command('clear idtable',0)
        telnet.run_command('apply config',0)

        count=0
        cmd=''
        cmdgroup=''
        cmdservice=''
        vlangrlist=servicevlan.split(',')
        vlanserlist=servicevlan.split(',')
        service_count=160
        for i in range (4,idlink+4,1):
            ii=str(i)
            cmd= cmd+'new link '+ii+'\n' \
                 'set idname '+ii+' '+ssip[count]+'\n' \
                 'set peermac '+ii+' '+ssmac[count]+'\n' \
                 'set linkmode '+ii+' mimoab'+'\n' \
                 'set dlrate '+ii+' '+dlubr+'\n' \
                 'set ulrate '+ii+' '+ulubr+'\n' \
                 'set adaptmod '+ii+' '+modulation+'\n' \
                 'set dlminrate '+ii+ ' 0'+'\n' \
                 'set ulminrate '+ii+ ' 0'+'\n' \
                 'set ldlpir '+ii+' '+pir+'\n' \
                 'set lulpir '+ii+' '+pir+'\n' \
                 'set lrfmode '+ii+' '+'auto'+'\n' \
                 'set lautoscan '+ii+' off'+'\n' \
                 'set ltimeautoscan '+ii+' 600'+'\n' \
                 'set lstickytime '+ii+' 15'+'\n' \
                 'enable '+ii+'\n'
            count+=1
        #telnet.run_command(cmd,0)

        count=0
        for i in range (128,serviceid+128,1):
            ii=str(i)
            cmdgroup=cmdgroup+'new group '+ii+'\n' \
                    'set idname '+ii+' Group'+ii+'\n' \
                    'set bsporten '+ii+' on'+'\n' \
                    'set grpviden '+ii+' on'+'\n' \
                    'set grpvid '+ii+' '+vlangrlist[count]+'\n' \
                    'set grppri '+ii+' 0'+'\n' \
                    'set grpcir '+ii+' 500'+'\n' \
                    'set grprate '+ii+' auto'+'\n' \
                    'set sstoss '+ii+' off'+'\n' \
                    'set grppir '+ii+' 50000'+'\n' \
                    'set groupmode '+ii+' mimoab'+'\n' \
                    'set grpdot1pena '+ii+' off'+'\n' \
                    'set grpdot1p0 '+ii+' 0'+'\n' \
                    'set grpdot1p1 '+ii+' 0'+'\n' \
                    'set grpdot1p2 '+ii+' 1'+'\n' \
                    'set grpdot1p3 '+ii+' 1'+'\n' \
                    'set grpdot1p4 '+ii+' 2'+'\n' \
                    'set grpdot1p5 '+ii+' 2'+'\n' \
                    'set grpdot1p6 '+ii+' 3'+'\n' \
                    'set grpdot1p7 '+ii+' 3'+'\n' \
                    'enable ' +ii+'\n'
            #telnet.run_command(cmdgroup,0)

            count+=1
        for l in range (4,idlink+4,1):
            linkid=str(l)
            count=0
            grp_count=128
            for i in range (service_count ,serviceid+service_count,1):
                ii=str(i)

                cmdservice=cmdservice+'new service ' +ii+'\n' \
                        'set idname '+ii+' Service'+ii+'\n' \
                        'set conlid '+ii+' '+str(linkid)+'\n' \
                        'set congid '+ii+' '+str(grp_count)+'\n' \
                        'set dlcir '+ii+' '+cir+'\n' \
                        'set ulcir '+ii+' '+cir+'\n' \
                        'set conviden '+ii+ ' on'+'\n' \
                        'set convid '+ii+' '+vlanserlist[count]+'\n' \
                        'set conpri '+ii+' 0'+'\n' \
                        'set dlpir '+ii+' '+pir+'\n' \
                        'set ulpir '+ii+' '+pir+'\n' \
                        'set srvdot1pena '+ii+' off'+'\n' \
                        'set srvdot1p0 '+ii+' 0'+'\n' \
                        'set srvdot1p1 '+ii+' 0'+'\n' \
                        'set srvdot1p2 '+ii+' 1'+'\n' \
                        'set srvdot1p3 '+ii+' 1'+'\n' \
                        'set srvdot1p4 '+ii+' 2'+'\n' \
                        'set srvdot1p5 '+ii+' 2'+'\n' \
                        'set srvdot1p6 '+ii+' 3'+'\n' \
                        'set srvdot1p7 '+ii+' 3'+'\n' \
                        'enable ' +ii+'\n'
                #telnet.run_command(cmdservice,0)
                grp_count+=1
                count+=1
            service_count=i+1
        aux_command= channel+ '\n' \
                     +frequency+'\n' \
                     +cp+'\n' \
                     +radiomode+'\n' \
                     +vlanfilter+'\n' \
                     +syslog+'\n'
        cmdlog= cmd+cmdgroup+cmdservice+aux_command+'save config'+'\n'
        #os.remove('log.cfg') if os.path.exists('log.cfg') else None
        log = open("log.cfg", "w")
        log.write(cmdlog)
        log.close()
        print 'Start tftp client'
        client = tftpy.TftpClient(tftpip, 69)
        client.upload('log.cfg', 'log.cfg')
        #tftpy.TftpServer.root
        telnet.run_command('load script '+tftpip+' log.cfg',0)

        #telnet.run_command('save config',0)
        #telnet.run_command(cmd,0)
        telnet.run_command('logout',1)

        telnet.logout()
        flag_run=True
        return flag_run

        



