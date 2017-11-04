'''
Created on Jul 26, 2017

@author: Jhon Melvin
'''
from Tkinter import Tk, Toplevel
from Tkinter import Label
from Tkinter import Button
from Tkinter import PhotoImage
from Tkinter import X
from Tkinter import Entry

from tkMessageBox import showinfo,showerror,showwarning
from Oras import Time
from Depositor import Depositor

'''
Messenger
'''
class Message():
    def __init__(self):
        pass #end construct
    
    @staticmethod
    def info(msg):
        showinfo(title="Information",message=msg)
        pass
    
    @staticmethod
    def error(msg):
        showerror(title="Error",message=msg)
        pass
    
    @staticmethod
    def warning(msg):
        showwarning(title="Warning",message=msg)
        pass
    
    pass# end class

'''
Create Account Class ---------------------------------------------------------------------------------------
'''
class CreateAccount():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.constructWindow()
        pass # end construct
    
    def constructWindow(self):
        self.frm_create = Tk()
        self.frm_create.geometry('300x400+310+0')
        self.frm_create.title('Welcome')
        self.frm_create.resizable(False, False)
        
        self.lbl_menu = Label(self.frm_create,text="New Account",font=("Courier", 20)).pack()
        self.lbl_divider1 = Label(self.frm_create,text="------------------",font=("Courier", 20)).pack()
        
        #
        Label(self.frm_create,text="Account Number",font=("Courier", 15)).pack()
        # account number field
        self.txt_accountNumber = Entry(self.frm_create,justify='center',font=("Courier", 15))
        self.txt_accountNumber.pack(fill=X,padx=30)
        #
        Label(self.frm_create,text="Account Name",font=("Courier", 15)).pack()
        #
        self.txt_accountName = Entry(self.frm_create,justify='center',font=("Courier", 15))
        self.txt_accountName.pack(fill=X,padx=30)
        #
        Label(self.frm_create,text="Pin",font=("Courier", 15)).pack()
        #
        self.txt_pin = Entry(self.frm_create,show="*",justify='center',font=("Courier", 15))
        self.txt_pin.pack(fill=X,padx=30)
        #
        Label(self.frm_create,text="Confirm Pin",font=("Courier", 15)).pack()
        #
        self.txt_confirmPin = Entry(self.frm_create,show="*",justify='center',font=("Courier", 15))
        self.txt_confirmPin.pack(fill=X,padx=30)
        #
        Label(self.frm_create,text="Initial Deposit",font=("Courier", 15)).pack()
        #
        self.txt_initial = Entry(self.frm_create,justify='center',font=("Courier", 15))
        self.txt_initial.pack(fill=X,padx=30)
        #
        
        self.btn_create = Button(self.frm_create,text="Create Account",font=("Courier", 10),bg='#FFFFFF',height='20',command = lambda: self.onCreateAccount())
        self.btn_create.pack(fill=X,padx=10,pady=5)
        
        
        self.frm_create.mainloop()
        pass # end function
    
    
    '''
    button events
    '''
    def onCreateAccount(self):
        self.validateForm()
        pass # end func
    
    ''' class methods'''
   
    def validateForm(self):
        '''
        Empty Field Checker
        '''
        if(self.txt_accountNumber.get() == ""):
            Message.warning("Account Number is Empty")
            return
        
        ''' Check if Existing '''
        depositor = Depositor.getInstance()
        assert isinstance(depositor, Depositor)
        
        res = depositor.fetch(self.txt_accountNumber.get())
        if res:
            Message.warning("Account Number Already Existing.")
            depositor.clearFields()
            return
            pass
        
        ''' ---------------------------------------------'''
        
        if(self.txt_accountName.get() == ""):
            Message.warning("Account Name is Empty")
            return
        
        if(self.txt_pin.get() == ""):
            Message.warning("Pin is Empty")
            return
        
        if(self.txt_confirmPin.get() == ""):
            Message.warning("Confirm Pin is Empty")
            return
        
        if(self.txt_initial.get() == ""):
            Message.warning("Initial Deposit is Empty")
            return
        
        ''' if all fields are filled up proceed to validation '''
       
        if(not self.isValidAccountNumber(self.txt_accountNumber.get())):
            return
        
        ''' if account number is valid '''
        # proceed check if account name is alpha space
        accountName = self.txt_accountName.get()
        
        if not all(x.isalpha() or x.isspace() for x in accountName):
            Message.warning("Account Name must be letters and spaces only.")
            return
            pass
        
        ''' if account name is valid ; check for pin code'''
        
        pin = self.txt_pin.get()
        # check if 4 digits
        if(len(pin) <> 4):
            Message.warning("Pin Code must be Four (4) Digits.")
            return
        
        if(not pin.isdigit()):
            Message.warning("Pin Code must contain Numbers only.")
            return
        
        # if pincode is ok check if match
        
        confirmPin = self.txt_confirmPin.get()
        if(pin <> confirmPin):
            Message.warning("Pin and Confirm Pin does not match.")
            return
        
        # if match
        
        ''' Check initial deposit '''
        initialDeposit = self.txt_initial.get()
        if not all(c.isdigit() or c =="." for c in initialDeposit):
            Message.warning("Invalid Initial Deposit Amount")
            return
        
        if float(initialDeposit) < 2000:
            Message.warning("Insufficient initial deposit, must be atleast P 2000.00")
            return
        
        ''' ---------- Filters all; completed successfully --------------------'''
        

        
        depositor.clearFields() # reset fields
        
        depositor.setAccountNumber(self.txt_accountNumber.get())
        depositor.setAccountName(accountName)
        depositor.setPinCode(pin)
        depositor.setBalance(initialDeposit)
        depositor.setCreatedDate(Time.now())
        result = depositor.save()
        
        depositor.clearFields() # reset fields
        # transaction result
        Message.info(result)
        
        self.frm_create.destroy()
        
        
        pass #end function
   
   # checks the account number
    def isValidAccountNumber(self,accountNumber):
        length = len(accountNumber)
        
        # if not 10 digits
        if (length <> 10):
            Message.warning("Account Number must be Ten (10) Digits.")
            return False
            pass #end if
        # if 10 digits proceed to checking
        # check if all numbers
        if(not accountNumber.isdigit()):
            Message.warning("Account Number must be digits only")
            return False
            pass
        
        # if OK
        return True
        pass #end
    
    
    # end class
    
    '''
    Home Screen Class ---------------------------------------------------------------------------------------
    '''
class HomeScreen():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        ''' Start Server '''
        depositor = Depositor.getInstance()
        assert isinstance(depositor, Depositor)
        if not depositor.configureNetwork():
            Message.error("Cannot Connect To Server.")
            exit()
            pass
        ##
        self.constructWindow()
        pass # end construct
    
    
    def constructWindow(self):
        self.frm_home = Tk()
        self.frm_home.geometry('300x370+0+0')
        self.frm_home.title('Welcome')
        self.frm_home.resizable(False, False)
        
        Label(self.frm_home,text="Your Bank Name",font=("Courier", 20)).pack()
        Label(self.frm_home,text="------------------",font=("Courier", 20)).pack()
        #
        Label(self.frm_home,text="Enter Account #",font=("Courier", 15)).pack()
        self.txt_accountNumber = Entry(self.frm_home,justify='center',font=("Courier", 15))
        self.txt_accountNumber.pack(fill=X,padx=30)
        #
        self.img_begin = PhotoImage(file="img_begin.gif")
        self.btn_begin = Button(self.frm_home,text="Begin Transaction",font=("Courier", 10),bg='#FFFFFF',image=self.img_begin,compound='left',command = lambda: self.onBeginTransaction())
        self.btn_begin.pack(fill=X,padx=10,pady=5)
        #
        Label(self.frm_home,text="------- OR -------",font=("Courier", 20)).pack()
        #
        self.img_create = PhotoImage(file="img_add_account.gif")
        self.btn_create = Button(self.frm_home,text="Create Account",anchor='w',font=("Courier", 10),bg='#FFFFFF',image=self.img_create,compound='left',command = lambda: self.onCreate())
        self.btn_create.pack(fill=X,padx=10,pady=5)
        #
        self.img_exit = PhotoImage(file="img_exit.gif")
        self.btn_exit = Button(self.frm_home,text="Exit",anchor='w',font=("Courier", 10),bg='#FFFFFF',image=self.img_exit,compound='left',command = lambda: self.onExit())
        self.btn_exit.pack(fill=X,padx=10,pady=5)
        
        self.frm_home.mainloop()
        pass # end
    
    
    '''
    button events
    '''
   
    def onBeginTransaction(self):
        accountNumber = self.txt_accountNumber.get()
        if accountNumber == "":
            Message.warning("Please Enter Your Account Number To Begin Transaction.")
            return
        
        #-----------------------------------------
        depositor = Depositor.getInstance()
        assert isinstance(depositor, Depositor)
        res = depositor.fetch(accountNumber)
        
        if(res):
            self.frm_home.destroy()
            Menu()
        else:
            Message.error("Account Not Existing")
        #-----------------------------------------

        pass #end
    
    def onCreate(self):
        print "create"
        CreateAccount()
        pass #end
    
    def onExit(self):
        print "exit"
        exit()
        pass #end
    
    
    pass # end class
   
    '''
    Menu Class ---------------------------------------------------------------------------------------
    '''
class Menu():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.constructWindow()
        pass # end construct
    
    
    '''
    creates the main menu window
    '''
    def constructWindow(self):
        self.frm_menu = Tk()
        self.frm_menu.geometry('400x450+0+0')
        self.frm_menu.title('Main Menu')
        self.frm_menu.resizable(False, False)
        
        Label(self.frm_menu,text="ATM Menu",font=("Courier", 30)).pack()
        Label(self.frm_menu,text="Select Your Transaction",font=("Courier", 10)).pack()
        self.lbl_menu = Label(self.frm_menu,text="Account # 0123456789",font=("Courier", 10))
        self.lbl_menu.pack()
        
        depositor = Depositor.getInstance()
        assert isinstance(depositor, Depositor)
        self.lbl_menu.config(text="Account # " +depositor.getAccountNumber())
        
        '''
        buttons
        '''
        self.img_deposit = PhotoImage(file="img_deposit.gif")
        self.btn_deposit = Button(self.frm_menu,text="Deposit",anchor='w',font=("Courier", 10),bg='#FFFFFF',image=self.img_deposit,compound='left',command = lambda:self.onDeposit())
        self.btn_deposit.pack(fill=X,padx=10)
        
        #
        self.img_withdraw = PhotoImage(file="img_withdraw.gif")
        self.btn_withdraw = Button(self.frm_menu,text="Withdraw",anchor='w',font=("Courier", 10),bg='#FFFFFF',image=self.img_withdraw,compound='left',command = lambda:self.onWithraw())
        self.btn_withdraw.pack(fill=X,padx=10)
        #
        self.img_balance = PhotoImage(file="img_balance.gif")
        self.btn_balance = Button(self.frm_menu,text="Balance Inquiry",anchor='w',font=("Courier", 10),bg='#FFFFFF',image=self.img_balance,compound='left',command = lambda:self.onBalance())
        self.btn_balance.pack(fill=X,padx=10)
        #
        self.img_change = PhotoImage(file="img_change_pin.gif")
        self.btn_changepin = Button(self.frm_menu,text="Change Pin",anchor='w',font=("Courier", 10),bg='#FFFFFF',image=self.img_change,compound='left',command = lambda:self.onPinChange())
        self.btn_changepin.pack(fill=X,padx=10)
        #
        self.img_view = PhotoImage(file="img_view_account.gif")
        self.btn_view = Button(self.frm_menu,text="View Account",anchor='w',font=("Courier", 10),bg='#FFFFFF',image=self.img_view,compound='left',command = lambda:self.onViewInfo())
        self.btn_view.pack(fill=X,padx=10)
        #
        self.img_end = PhotoImage(file="img_end_transaction.gif")
        self.btn_end = Button(self.frm_menu,text="End Transaction",anchor='w',font=("Courier", 10),bg='#FFFFFF',image=self.img_end,compound='left',command = lambda:self.onEndTransaction())
        self.btn_end.pack(fill=X,padx=10)


        
        '''
        display the window
        '''
        self.frm_menu.mainloop()
        pass #end
    
    '''
    button events
    '''
    def verify(self):
        try:
            verify = popupWindow(self.frm_menu)
            self.frm_menu.wait_window(verify.top)
            
            depositor = Depositor.getInstance()
            assert isinstance(depositor, Depositor)
            
            if(verify.value == depositor.getPinCode()):
                return True
            else:
                Message.info("Wrong Pin Code")
                return False
        
        except:
            Message.info("Transaction Cancelled")
            return False
            pass
        pass

    #
    def onDeposit(self):
        print "deposit"
        
        if self.verify():
            DepositWindow()
        pass # end func
    
    def onWithraw(self):
        print "withdraw"
        if self.verify():
            WithdrawWindow()
        pass #end func
    
    def onBalance(self):
        print "balance"
        if self.verify():
            BalanceWindow()
        pass #end func
    
    def onViewInfo(self):
        print "view"
        if self.verify():
            ViewWindow()
        pass #end func
    
    def onPinChange(self):
        if self.verify():
            ChangePinWindow()
        print "change"
        pass #end func
    
    def onEndTransaction(self):
        print "end"    
        depositor = Depositor.getInstance()
        assert isinstance(depositor, Depositor)
        
        depositor.clearFields()
        
        self.frm_menu.destroy()
        HomeScreen()
        pass #end func
    
        
        
    pass # end class

'''
    Window Classes ---------------------------------------------------------------------------------------
    
    Deposit Window
'''

class DepositWindow():
    def __init__(self):
        self.constructWindow()
        pass # end cons
    
    def constructWindow(self):
        self.frm_deposit = Tk()
        self.frm_deposit.geometry('400x200+405+115')
        self.frm_deposit.title('Transaction')
        self.frm_deposit.resizable(False, False)
        
        Label(self.frm_deposit,text="Deposit",font=("Courier", 20)).pack()
        Label(self.frm_deposit,text="------------------",font=("Courier", 20)).pack()
        
        Label(self.frm_deposit,text="Enter Amount",font=("Courier", 15)).pack()
        self.txt_amount = Entry(self.frm_deposit,justify='center',font=("Courier", 15))
        self.txt_amount.pack(fill=X,padx=30)
        #
        self.btn_deposit = Button(self.frm_deposit,text="Deposit",font=("Courier", 10),bg='#FFFFFF',height = 15,command = lambda: self.onDeposit())
        self.btn_deposit.pack(fill=X,padx=10,pady=5)
        
        self.frm_deposit.mainloop()
        pass # end function
    
    def onDeposit(self):
        amount = self.txt_amount.get()
        
        try:
            peso = float(amount)
            if peso < 1.00:
                Message.warning("Insufficient Amount !, Minimum is One (1) pesos/s")
                return
            
            self.depositFunds(peso)
            pass
        except:
            
            Message.error("Cannot Deposit, Invalid Amount !")
            pass
        pass
    
    def depositFunds(self,peso):
        depositor = Depositor.getInstance()
        assert isinstance(depositor, Depositor)
        
        current_funds = float(depositor.getBalance()) + peso
        depositor.setBalance(str(current_funds))
        
        result = depositor.save()
        Message.info("Deposit Transaction: " + result)
        
        self.frm_deposit.destroy()
        pass
    
    pass # end class


'''
   Withdraw Window ---------------------------------------------------------------------- 
'''

class WithdrawWindow():
    
    def __init__(self):
        self.constructWindow()
        pass # end construct
    
    def constructWindow(self):
        self.frm_withdraw = Tk()
        self.frm_withdraw.geometry('400x200+405+170')
        self.frm_withdraw.title('Transaction')
        self.frm_withdraw.resizable(False, False)
        
        Label(self.frm_withdraw,text="Withdraw",font=("Courier", 20)).pack()
        Label(self.frm_withdraw,text="------------------",font=("Courier", 20)).pack()
        
        Label(self.frm_withdraw,text="Enter Amount",font=("Courier", 15)).pack()
        self.txt_amount = Entry(self.frm_withdraw,justify='center',font=("Courier", 15))
        self.txt_amount.pack(fill=X,padx=30)
        #
        self.btn_withdraw = Button(self.frm_withdraw,text="Withdraw",font=("Courier", 10),bg='#FFFFFF',height = 15,command = lambda: self.onWithdraw())
        self.btn_withdraw.pack(fill=X,padx=10,pady=5)
        
        self.frm_withdraw.mainloop()
        pass # EF
    
    def onWithdraw(self):
        amount = self.txt_amount.get()
        try:
            peso = float(amount)
            butal = peso % 100            
            if(butal == 50.00 or butal == 0.00):
                self.withdrawFunds(peso)
                pass
            else:
                Message.warning("Unsupported Denomination, Please Withdraw with Fifty(50) as the lowest bill.")
                pass      
            pass
        except Exception as e:
            Message.error("Cannot Withdraw, Invalid Amount !")
            pass
        pass
    
    def withdrawFunds(self,peso):
        depositor = Depositor.getInstance()
        assert isinstance(depositor, Depositor)
        
        # check if have sufficient funds
        current_funds = float(depositor.getBalance())
        if (current_funds - peso) >= 0.00 and (current_funds - peso) < 2000.00:
            Message.warning("Cannot Withdraw, Must Maintain atleast P 2000.00")
            return
            pass
            
        if (current_funds - peso) < 0:
            Message.warning("Insufficient Funds")
            return
        
        current_funds = current_funds - peso
        depositor.setBalance(str(current_funds))
        
        result = depositor.save()
        Message.info("Withdraw Transaction: " + result)
        
        self.frm_withdraw.destroy()
        pass
    
    pass #end class
'''
Balance -------------------------------------------------------------------------
'''
class BalanceWindow():
    
    def __init__(self):
        self.constructWindow()
        pass # end construct
    
    def constructWindow(self):
        self.frm_withdraw = Tk()
        self.frm_withdraw.geometry('400x200+405+225')
        self.frm_withdraw.title('Transaction')
        self.frm_withdraw.resizable(False, False)
        
        Label(self.frm_withdraw,text="Balance Inquiry",font=("Courier", 20)).pack()
        Label(self.frm_withdraw,text="------------------",font=("Courier", 20)).pack()
        Label(self.frm_withdraw,text="Remaining Balance",font=("Courier", 15)).pack()
        self.lbl_balance = Label(self.frm_withdraw,text="P 150000",font=("Courier", 30))
        self.lbl_balance.pack()
        

        depositor = Depositor.getInstance()
        assert isinstance(depositor, Depositor)
        
        self.lbl_balance.config(text = "P " + depositor.getBalance())
        
        self.frm_withdraw.mainloop()
        pass # EF
    
    
    pass #end class

'''
Change Pin -------------------------------------------------------------------------
'''
class ChangePinWindow():
    
    def __init__(self):
        self.constructWindow()
        pass # end construct
    
    def constructWindow(self):
        self.frm_change_pin = Tk()
        self.frm_change_pin.geometry('400x250+405+280')
        self.frm_change_pin.title('Transaction')
        self.frm_change_pin.resizable(False, False)
        
        Label(self.frm_change_pin,text="Change Pin",font=("Courier", 20)).pack()
        Label(self.frm_change_pin,text="------------------",font=("Courier", 20)).pack()
        
        Label(self.frm_change_pin,text="Enter New Pin",font=("Courier", 15)).pack()
        self.txt_old = Entry(self.frm_change_pin,show="*",justify='center',font=("Courier", 15))
        self.txt_old.pack(fill=X,padx=30)
        #
        Label(self.frm_change_pin,text="Confirm New Pin",font=("Courier", 15)).pack()
        self.txt_new = Entry(self.frm_change_pin,show="*",justify='center',font=("Courier", 15))
        self.txt_new.pack(fill=X,padx=30)
        #
        self.btn_withdraw = Button(self.frm_change_pin,text="Change",font=("Courier", 10),bg='#FFFFFF',height = 15,command = lambda: self.onChange())
        self.btn_withdraw.pack(fill=X,padx=10,pady=5)
        
        self.frm_change_pin.mainloop()
        pass # EF
    
    def onChange(self):
        new_pin = self.txt_old.get()
        confirm_pin = self.txt_new.get()
        try:
            int(new_pin)
            
            if(len(new_pin) <> 4):
                Message.warning("Pin Code Must Be Four (4) Digits")
                return
            
            if(confirm_pin <> new_pin):
                Message.warning("New Pin and Confirm New Pin Does Not Match.")
                return
            
            # Pin Change
            self.changePin(new_pin)
            pass
        except:
            Message.warning("Invalid New Pin Code")
            pass
        pass
    
    def changePin(self,new_pin):
        depositor = Depositor.getInstance()
        assert isinstance(depositor, Depositor)
        
        depositor.setPinCode(new_pin)
        
        result = depositor.save()
        Message.info("Pin Change Transaction: " + result)
        
        self.frm_change_pin.destroy()
        pass
    
    pass #end class
'''
Change Pin -------------------------------------------------------------------------
'''
class ViewWindow():
    
    def __init__(self):
        self.constructWindow()
        pass # end construct
    
    def constructWindow(self):
        self.frm_withdraw = Tk()
        self.frm_withdraw.geometry('400x250+405+335')
        self.frm_withdraw.title('Transaction')
        self.frm_withdraw.resizable(False, False)
        
        Label(self.frm_withdraw,text="Account Information",font=("Courier", 20)).pack()
        Label(self.frm_withdraw,text="------------------",font=("Courier", 20)).pack()
        #
        Label(self.frm_withdraw,text="Account #",font=("Courier", 15,'bold')).pack()
        self.lbl_accountNumber = Label(self.frm_withdraw,text="01210120112",font=("Courier", 15))
        self.lbl_accountNumber.pack()
        #
        Label(self.frm_withdraw,text="Account Name",font=("Courier", 15,'bold')).pack()
        self.lbl_accountName = Label(self.frm_withdraw,text="Juan Dela Cruz",font=("Courier", 15))
        self.lbl_accountName.pack()
        #
        Label(self.frm_withdraw,text="Date Created",font=("Courier", 15,'bold')).pack()
        self.lbl_date = Label(self.frm_withdraw,text="07/26/2017",font=("Courier", 15))
        self.lbl_date.pack()
        
        depositor = Depositor.getInstance()
        assert isinstance(depositor, Depositor)
        self.lbl_accountNumber.config(text = depositor.getAccountNumber())
        self.lbl_accountName.config(text = depositor.getAccountName())
        self.lbl_date.config(text = depositor.getCreatedDate())
        

        
        self.frm_withdraw.mainloop()
        pass # EF
    
    
    pass #end class

class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.top.geometry('250x100+405+100')
        self.top.title("Verification")
        self.top.resizable(False, False)
        self.l=Label(top,text="Enter Pin",font=("Courier", 20))
        self.l.pack()
        self.e=Entry(top,show="*",justify='center')
        self.e.pack(fill=X,padx=30)
        self.b=Button(top,text='Proceed',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

    pass

    