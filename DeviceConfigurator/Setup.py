'''
Created on Sep 19, 2014

@author: abarac
'''
import xml.etree.ElementTree as ET
class Setup:

    def GetSetupName(self,name):
        tree = ET.parse('SetupList.xml')
        root = tree.getroot()


        sslist=[]
        sc=''
        for setup in root.findall('setup'):
            #sc = setup.find('sc').text
            if setup.get('name')==name:
                sc=setup.find('sc').text
                ss = setup.find('ss').text
                break
        return sc+'\n'+ss.replace(';','\n')
