import json
import subprocess
import tkinter
from tkinter import messagebox

def getCarriers():
    carriers = subprocess.check_output(['adb','shell','getprop','gsm.sim.operator.alpha'],text=True)
    carriers = carriers.split('\n')[0]
    carriers = carriers.split(',')
    if(carriers[0] == '' and carriers[1]==''):
        return 'Carriers:'
    if(carriers[0] != '' and carriers[1]!=''):
        return 'Carriers:'+carriers[0]+','+carriers[1]
    if(carriers[0] != '' or carriers[1]!=''):
        if(carriers[0 != '']):
            return 'Carrier:'+carriers[0]
        else:
            return 'Carrier:'+carriers[1]

def getModel():
    model = subprocess.check_output(['adb','shell','getprop','ro.product.model'],text=True)
    return "Model: "+model[:-1]

def getOS():
    os = subprocess.check_output(['adb','shell','getprop','ro.build.version.release'],text=True)
    return "Android Version: "+os[:-1]

def extractAccount(aString):
    accounts = list()
    accountsA = list()
    accounts.append('Accouts:\n')
    acString = aString.find('Accounts:')
    acStart = aString.find('\n',acString)+5
    acEnd = aString.find('AccountId')-6
    acString = aString[acStart:acEnd]
    acString = acString.split('\n')
    for ac in acString :
        if('com.google' in ac):
            accountPosI = ac.find('name=')+5
            accountPosF = ac.find(',')
            account = ac[accountPosI:accountPosF]
            accountsA.append("Google: "+account)

        if('com.osp.app.signin' in ac):
            accountPosI = ac.find('name=')+5
            accountPosF = ac.find(',')
            account = ac[accountPosI:accountPosF]
            accountsA.append("Samsung: "+account)
    for ac in accountsA :
        accounts.append(ac+'\n') 
    return accounts

def getAccounts():
        aString = subprocess.check_output(['adb','shell','dumpsys','account'],text=True)
        tc = aString.find('Accounts:')+10
        if((tc == 1)or('com.google' in aString)or('com.osp.app.signin' in aString)):
            return extractAccount(aString)
        else:
            return "Accounts: " 

def getAppVersion(pName,Name):
    pkgv = subprocess.check_output(['adb','shell','dumpsys','package',pName,'|','grep','versionName'],text=True)
    versionPosI = pkgv.find('=')+1
    versionPosF = pkgv.find('\n',versionPosI-1)
    version = pkgv[versionPosI:versionPosF]

    return Name+': '+version+'\n'

def createDefaultConfigFile():
    data = {}
    data['temp'] = {
        "id":True,
        "pass":True,
        "model":False,
        "os":False,
        "binary":False,
        "csc":False,
        "carriers":False,
        "accounts":False,
        "issues":False
    }
    with open('config.json','w') as config:
         json.dump(data,config)
    return data

def checkConfigFile():
    try:
        with open('config.json','r') as config:
            configdata = json.load(config)
            return configdata
    except:
            configdata = createDefaultConfigFile()
            return configdata

def checkPhone():
    subprocess.run(['adb','kill-server'],text=True)
    subprocess.run(['adb','start-server'],text=True)
    subprocess.run(['adb','wait-for-devices'],text=True)
                  
def wrap():
    #checkPhone()
    configData = checkConfigFile()

def getSettingsInfo(op):
    wrap()
    aVersions = list()
    if(getOS == 'Android Version: 8.1'):
        #caso seja android go, falta tratar isso ainda
        return
    if(op == 0):#Versoes de phone
        aVersions.append(getAppVersion('com.samsung.android.dialer','Phone')) 
        aVersions.append(getAppVersion('com.samsung.android.app.telephonyui','Phnone UI'))
        aVersions.append(getAppVersion('com.samsung.android.app.contacts','Contacts'))
        aVersions.append(getAppVersion('com.samsung.android.mdecservice', 'CMC'))

    if(op == 1):#versoes de Message
        aVersions.append(getAppVersion('com.samsung.android.messaging','Message'))
        aVersions.append(getAppVersion('com.samsung.android.mdecservice', 'CMC'))
        aVersions.append(getAppVersion('com.microsoft.appmanager', 'Link To Windows'))
    if(op == 2):
        aVersions.append(getAppVersion('com.sec.android.inputmethod','Keyboard'))

    if(op == 3):#3rd party
        aVersions.append(getAppVersion('com.bradesco','Bradesco'))
        aVersions.append(getAppVersion('br.com.bb.android', 'Banco do Brasil'))
        aVersions.append(getAppVersion('br.cm.gabba.Caixa','Caixa'))
        aVersions.append(getAppVersion('com.itau','Itau'))
    if(op == 4):
        aVersions.append(getAppVersion('com.samsung.android.app.contacts','Contacts'))
        aVersions.append(getAppVersion('com.samsung.android.app.telephonyui','Phnone UI'))
        aVersions.append(getAppVersion('com.samsung.android.dialer','Phone'))
        aVersions.append(getAppVersion('com.samsung.android.messaging','Message'))
        aVersions.append(getAppVersion('com.sec.android.inputmethod','Keyboard'))
        aVersions.append(getAppVersion('com.samsung.android.mdecservice', 'CMC'))
        aVersions.append(getAppVersion('com.microsoft.appmanager', 'Link To Windows'))
        aVersions.append(getAppVersion('com.santander.app','Santander'))
        aVersions.append(getAppVersion('com.bradesco','Bradesco'))
        aVersions.append(getAppVersion('br.com.bb.android', 'Banco do Brasil'))
        aVersions.append(getAppVersion('br.cm.gabba.Caixa','Caixa'))
        aVersions.append(getAppVersion('com.itau','Itau'))
    
