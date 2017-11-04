'''
Created on Jul 26, 2017

@author: Jhon Melvin
'''
from socket import*
import json

class Depositor():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        ''' Class Variables'''
        print "DEPOSITOR OBJECT INITIALIZED"
        self.accountNumber = ""
        self.accountName = ""
        self.pinCode = ""
        self.balance = ""
        self.accountCreated = ""
        
        self.isConfiguredNetwork = False
        pass # end construct
    
    
    DEPOSITOR_INSTANCE = None
    '''Singleton'''
    @staticmethod
    def getInstance():
        if Depositor.DEPOSITOR_INSTANCE is None:
            Depositor.DEPOSITOR_INSTANCE = Depositor()
            pass
        return Depositor.DEPOSITOR_INSTANCE
        pass
    
    ''' Getters '''
    def getAccountNumber(self):
        return self.accountNumber
    
    def getAccountName(self):
        return self.accountName
    
    def getPinCode(self):
        return self.pinCode
    
    def getBalance(self):
        return self.balance
    
    def getCreatedDate(self):
        return self.accountCreated
    
    ''' Setters '''
    def setAccountNumber(self,accNumber):
        self.accountNumber = accNumber
    
    def setAccountName(self,accName):
        self.accountName = accName
        
    def setPinCode(self,pin):
        self.pinCode = pin
    
    def setBalance(self,bal):
        self.balance = bal
        
    def setCreatedDate(self,date):
        self.accountCreated = date
    
    
    def clearFields(self):
        self.accountNumber = ""
        self.accountName = ""
        self.pinCode = ""
        self.balance = ""
        self.accountCreated = ""
        pass
    
    
    
    ''' Network Configuration '''
        
    def configureNetwork(self):
        if self.isConfiguredNetwork:
            # if network is already configured
            return True
        
        self.HOST = '127.0.0.1'
        self.PORT = 2004
        try:
            self.mono_socket = socket(AF_INET, SOCK_STREAM)
            self.mono_socket.connect((self.HOST,self.PORT))
            self.isConfiguredNetwork = True
            return True
        except:
            return False
            pass
        
    # sends data to server
    def senData(self,data):
        try:
            self.mono_socket.send(data)
        except:
            return -1
        pass
    
    
    ''' Class Methods '''
    # request must be a dictionary
    def persist(self,request):
        data_json = json.dumps(request, ensure_ascii=False).encode('utf-8')
        self.senData(data_json)
        ''' wait for server reply '''
        return self.mono_socket.recv(131072)
        pass
    
    pass #end class

    def fetch(self,accountNumber):
        # request params
        depositor_dump = {}
        depositor_dump['request_type'] = 'FETCH'
        depositor_dump['account_number'] = accountNumber
        # serialize
        data_json = json.dumps(depositor_dump, ensure_ascii=False).encode('utf-8')
        self.senData(data_json)
        
        depositor_result = self.mono_socket.recv(131072)
        
        if(depositor_result == "not_exist"):
            return False
        
        depositor_object = json.loads(depositor_result)
        self.accountNumber = depositor_object['account_number']
        self.accountName = depositor_object['account_name']
        self.pinCode = depositor_object['pin']
        self.balance = depositor_object['balance']
        self.accountCreated = depositor_object['created_date']
        return True
        pass

    def save(self):
        depositor_dump = {}
        depositor_dump['request_type'] = 'PERSIST'
        depositor_dump['account_number'] = self.accountNumber
        depositor_dump['account_name'] = self.accountName
        depositor_dump['pin'] = self.pinCode
        depositor_dump['balance'] = self.balance
        depositor_dump['created_date'] = self.accountCreated
        
        result = self.persist(depositor_dump)
        return result
        pass
    
    def closeSocket(self):
        try:
            self.mono_socket.close()
            return True
        except Exception as e:
            return False
            pass
        pass
        
