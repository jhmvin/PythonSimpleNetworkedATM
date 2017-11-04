'''
Created on Jul 26, 2017

@author: Jhon Melvin
'''
from socket import*
import threading
import atexit

from Tkinter import Tk
from Tkinter import Label
import json

class AtmServer():
    '''
    classdocs
    '''


    def __init__(self,):
        '''
        Constructor
        '''
        ''' Server Network Configuration '''
        self.HOST = '' # all host are accepted if empty
        self.PORT = 2004 # connection socket
        self.mono_socket = socket(AF_INET, SOCK_STREAM) #protocol implementation
        self.mono_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # socket recycler
        self.mono_socket.bind((self.HOST, self.PORT)) # apply all settings
        self.mono_socket.listen(100) # connection limit
        
        atexit.register(self.safeExitHandler)
        
        #display controls
        self.controlForm()
        pass # end construct
    
    def controlForm(self):
        self.frm_control = Tk()
        self.frm_control.geometry('300x100+310+0')
        self.frm_control.title('Welcome')
        
        Label(self.frm_control,text="ATM Server",font=("Courier", 20)).pack()
        Label(self.frm_control,text="------------------",font=("Courier", 20)).pack()
        Label(self.frm_control,text="ONLINE",font=("Courier", 20)).pack()
        
        self.startServer()
        self.frm_control.mainloop()
        pass
    
    def startServer(self):
        print "Server Started"
        self.isRunning = True
        thread = threading.Thread(target=self.waitForIncommingClients)
        thread.daemon = True
        thread.start()
        pass
    
    ''' Closes the socket for unexpected program termination '''
    def safeExitHandler(self):
        try:
            print "Attempting to Close Sockets . . ."
            self.mono_socket.close()
            print "Sockets Closed Succesfully . . ."
        except Exception as e:
            print "Cannot Close Socket due to an error: " + str(e)
            pass
        pass # handler end
    
    def waitForIncommingClients(self):
        stillWait =1
        while stillWait == 1:
            try:
                print "Waiting for Connection . . ."
                (conn, addr) = self.mono_socket.accept() # checks if there is a incomming connection
                print "Client: ", addr ,"connected."
                con_info = {'con':conn, 'ip':addr} # saves it to a dictionary
            except Exception as  e:
                print "CONNECTION DAEMON:" +  str(e)
                stillWait = 0;
                print "connection is already closed"
                pass
            threading._start_new_thread(self.processClientRequest,(conn,addr))
            pass #end of while
        pass
    
    def processClientRequest(self,connection,address):
        # Forever Starts Here
        stillProcess = 1
        while stillProcess == 1:
            try:
                data = connection.recv(131072)
                ''' Process Data Here '''
                result = self.processData(data)
                connection.sendto(result,address)
                ''' ---------------- '''
            except Exception as exception:
                error_code = str(exception)
                
                if error_code == "[Errno 10054] An existing connection was forcibly closed by the remote host":
                    print str(address) + " Has Been Disconnected!!"
                    stillProcess = 0
                    return
                else:
                    print str(exception)
                    print "Connection with " + str(address) + " has ended up with an error, transaction was cancelled."
                pass # end try
            if data == "":
                    connection.close()
                    print str(address) + "Has Been Disconnected."
                    stillProcess = 0
            pass # end of FOREVER
        
        pass # end client requests
    
    def processData(self,data):
        print data
        json_request = json.loads(data)
        
        if(json_request['request_type'] == 'PERSIST'):
            # saving here
            return self.saveChanges(json_request)
            pass
        
        if(json_request['request_type'] == 'FETCH'):
            accountNumber = json_request['account_number']
            return self.fetchData(accountNumber)
            pass
        
        return "Transaction was not processed, try again."
        pass
    
    def fetchData(self,accountNumber):
        # get values from database
        accounts = open('accounts.txt','r')
        records = accounts.readlines()
        accounts.close()
        records = filter(None,records) #this will remove whitespaces
        #
        for depositor_account in records:
            print depositor_account
            depositor_db = json.loads(depositor_account.strip()) # converts string to json format
            print depositor_db
            if(depositor_db['account_number'] == accountNumber):
                #----------------------------------------------
                depositor_dump = {}
                depositor_dump['account_number'] = depositor_db['account_number']
                depositor_dump['account_name'] = depositor_db['account_name']
                depositor_dump['pin'] = depositor_db['pin']
                depositor_dump['balance'] = depositor_db['balance']
                depositor_dump['created_date'] = depositor_db['created_date']
                json_fetch = json.dumps(depositor_dump, ensure_ascii=False).encode('utf-8')
                return json_fetch
                #----------------------------------------------            
                pass # end if account match
            pass # end of for loop
        
        return "not_exist"
        pass
    
    def saveChanges(self,json_request):
        print "saving . . ."
        # get the values from client
        depositor = {}
        depositor['account_number'] = json_request['account_number']
        depositor['account_name'] = json_request['account_name']
        depositor['pin'] = json_request['pin']
        depositor['balance'] = json_request['balance']
        depositor['created_date'] = json_request['created_date']
        
        # get values from database
        accounts = open('accounts.txt','r')
        records = accounts.readlines()
        accounts.close()
        records = filter(None,records) #this will remove whitespaces
        # now check existence
        isRecordExist = False
        counter = 0
        for depositor_account in records:
            print depositor_account
            depositor_db = json.loads(depositor_account.strip()) # converts string to json format
            print depositor_db
            if(depositor_db['account_number'] == depositor['account_number']):
                #----------------------------------------------
                print "exist"
                accounts = open('accounts.txt','w')
                records.pop(counter)
                #--------------- Change Here
                json_new = json.dumps(depositor, ensure_ascii=False).encode('utf-8') + "\n"
                records.append(json_new)
                #----------------
                accounts.writelines(records)
                accounts.close()
                isRecordExist = True
                return "Account # " + depositor['account_number'] + " Updated Successfully."
                    #----------------------------------------------            
                pass # end if account match
            counter+=1
            pass # end of for loop
        
        ''' if the record is not existed '''
        if not isRecordExist:
            accounts = open('accounts.txt','w')
            json_new = json.dumps(depositor, ensure_ascii=False).encode('utf-8') + "\n"
            records.append(json_new)
            accounts.writelines(records)
            accounts.close()
            return "Account # " + depositor['account_number'] + " Successfully Added."
            pass # end
        pass # end save changes
    
    pass #end class