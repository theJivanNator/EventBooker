import sys
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication,QFileDialog,QPushButton, QMessageBox
from ui_EventBooking import *
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from PyQt5.QtWidgets import QTableWidgetItem

import mysql.connector as mc

class MyForm(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

#Subwindows
        subwindow_winLogin=self.ui.mdiArea.addSubWindow(self.ui.winLogin)
        subwindow_winWelcome=self.ui.mdiArea.addSubWindow(self.ui.winWelcome)
        subwindow_winLogin=self.ui.mdiArea.addSubWindow(self.ui.winViewData)
        subwindow_winLogin=self.ui.mdiArea.addSubWindow(self.ui.winBookingsMaintenance)
        subwindow_winLogin=self.ui.mdiArea.addSubWindow(self.ui.winViewBookings)
        self.ui.winLogin.showMinimized()
        self.ui.winWelcome.showMaximized()
        self.ui.winViewData.showMinimized()
        self.ui.winBookingsMaintenance.showMinimized()
        self.ui.winViewBookings.showMinimized()
        
        self.ui.mdiArea.setActiveSubWindow(self.ui.mdiArea.subWindowList()[1])

        #Buttons        
        #Welcome page
        self.ui.btnClick.clicked.connect(self.buttonContinue)

        #Login page
        self.ui.btnLogin.clicked.connect(self.login)

        #Menu bar
        self.ui.actionView_Data.triggered.connect(self.viewData)
        self.ui.actionMake_Bookings.triggered.connect(self.makeBooking)
        self.ui.actionView_Bookings.triggered.connect(self.viewBooking)

        #View data
        #combo box
        self.ui.cmbTables.currentIndexChanged.connect(self.selectionchange)

        #Add booking data
        self.ui.btnAdd.clicked.connect(self.addbooking)
        
        #Edit booking data
        self.ui.btnEdit.clicked.connect(self.editbooking)

        #Delete booking
        self.ui.btnDelete.clicked.connect(self.deletebooking)
        #view events
        self.ui.btnViewEventDetails.clicked.connect(self.viewevents)

#Welcome button 
    def buttonContinue(self):
        self.ui.winLogin.showMaximized()        
        self.ui.mdiArea.setActiveSubWindow(self.ui.mdiArea.subWindowList()[0])

#Login button        
    def login(self):
        user=self.ui.plainTextEdit.toPlainText()
        
        password=self.ui.plainTextEdit_2.toPlainText()
        if(len(user))>0 and (len(password)):
            
            try:
                
                #Connect the database
                db = mc.connect(host="localhost",user="root",password="",database="myevents")
                cursor = db.cursor()
                     
                #SQL
                cursor.execute("select * from employee_admins")
                
                               #Get all the result from the sql
                result = cursor.fetchall()            

                my_list =[]
                #insert data
                for row_number,row_data in enumerate(result):
                    o=[]
                    for column_number,data in enumerate(row_data):
                        o.append(str(data))
                            

                    my_list.append(o)
                        
                usernames=[]
                passwords=[]
                    
                for x in my_list:
                    i=3    
                    for t in x:                
                        if (i % 2) == 0:
                            passwords.append(t)                        
                        else:
                            usernames.append(t)
                        i=i+1  
                isFound=False
                for num in range(len(usernames)):
                    if(user==usernames[num])and (password==passwords[num]):
                        isFound=True
                        break
                if isFound:
                    #Menu Buttons enabled
                    self.ui.actionView_Data.setEnabled(True)
                    self.ui.actionMake_Bookings.setEnabled(True)
                    self.ui.actionView_Bookings.setEnabled(True)

                    #Change view
                    self.viewData()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Information Invalid")
                    msg.exec_()

               
                    self.ui.plainTextEdit.setPlainText('')       
                    self.ui.plainTextEdit_2.setPlainText('') 
            except mc.Error as e:
                print(e)
       
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Information Invalid")
            msg.exec_()

               
        self.ui.plainTextEdit.setPlainText('')       
        self.ui.plainTextEdit_2.setPlainText('')        
        
#Change View to data view
    def viewData(self):
        self.ui.winViewData.showMaximized()        
        self.ui.mdiArea.setActiveSubWindow(self.ui.mdiArea.subWindowList()[2])
        try:
            #Connect the database
            db = mc.connect(host="localhost",user="root",password="",database="myevents")
            cursor = db.cursor()
                 
            #SQL
            cursor.execute("SHOW TABLES")
            
            #Loop and get all data from sql result
            cmbList=[]
            for data in cursor:                
                cmbList.append(str(data))
                
            
            #format string
            out_list=[]

            #Remove quotes and punctuation
            for s in cmbList:
                findQuoteStart= s.find('\'')
                
                out_list.append(s[findQuoteStart+1:(len(s))-3])

            out_list.remove('employee_admins')
            #Add the table names
            self.ui.cmbTables.clear()
            self.ui.cmbTables.addItems(out_list)
            

        except mc.Error as e:
            print(e)
       
        

#Change View to Make booking view
    def makeBooking(self):
        self.ui.winBookingsMaintenance.showMaximized()        
        self.ui.mdiArea.setActiveSubWindow(self.ui.mdiArea.subWindowList()[3])
        try:
            #Connect the database
            db = mc.connect(host="localhost",user="root",password="",database="myevents")
            cursor = db.cursor()
                 
            #SQL
            cursor.execute("select event_Name from theevents")
            
            #Loop and get all data from sql result
            cmbList=[]
            for data in cursor:                
                cmbList.append(str(data))
                
            
            #format string
            out_list=[]

            #Remove quotes and punctuation
            for s in cmbList:
                findQuoteStart= s.find('\'')
                
                out_list.append(s[findQuoteStart+1:(len(s))-3])

            #Add the event names
            self.ui.cmbEventAdd.clear()
            self.ui.cmbEventAdd.addItems(out_list)
            self.ui.cmbEventDelete.clear()
            self.ui.cmbEventDelete.addItems(out_list)
            

        except mc.Error as e:
            print(e)
       

#Change View to Booking view
    def viewBooking(self):
        self.ui.winViewBookings.showMaximized()        
        self.ui.mdiArea.setActiveSubWindow(self.ui.mdiArea.subWindowList()[4])
        self.viewbookings()

#Display Event Details-table
    def displayEvent(self):

        try:
            #Connect the database
            db = mc.connect(host="localhost",user="root",password="",database="myevents")
            cursor = db.cursor()            

            #SQL
            cursor.execute("select * from theevents")

            #Get all the result from the sql
            result = cursor.fetchall()
            
            #Column
            col_names= [names[0] for names in cursor.description]   
            self.ui.tableWidget.setRowCount(0)
            
            self.ui.tableWidget.setColumnCount(len(col_names))

            #Table Labels
            col=['Event Name','Event Date','Event Time','Contact No.','Manager Name','Venue','No. Tickets Available']
            self.ui.tableWidget.setHorizontalHeaderLabels(col)
            
            #insert data
            for row_number,row_data in enumerate(result):                
                self.ui.tableWidget.insertRow(row_number)
                
                for column_number,data in enumerate(row_data):
                    item=QtWidgets.QTableWidgetItem(str(data))
                    self.ui.tableWidget.setItem(row_number,column_number,item)
                 
        except mc.Error as e:
            print(e)

#Display Bookings booking-table
    def displaybooking(self):

        try:
            #Connect the database
            db = mc.connect(host="localhost",user="root",password="",database="myevents")
            cursor = db.cursor()            

            #SQL
            cursor.execute("select * from booking")

            #Get all the result from the sql
            result = cursor.fetchall()
            
            #Column
            col_names= [names[0] for names in cursor.description]   
            self.ui.tableWidget.setRowCount(0)
            
            self.ui.tableWidget.setColumnCount(len(col_names))

            #Table Labels
            col=['Invoice No.','Event Name','Customer Name','Contact No.']
            self.ui.tableWidget.setHorizontalHeaderLabels(col)
            
            #insert data
            for row_number,row_data in enumerate(result):                
                self.ui.tableWidget.insertRow(row_number)
                
                for column_number,data in enumerate(row_data):
                    item=QtWidgets.QTableWidgetItem(str(data))
                    self.ui.tableWidget.setItem(row_number,column_number,item)
                 
        except mc.Error as e:
            print(e)

#on combo box change
    def selectionchange(self,i):
        tableName =self.ui.cmbTables.currentText()
        if tableName=='theevents':
            self.displayEvent()
        else:
            self.displaybooking()
        
#Add booking-table
    def addbooking(self):

        eventName=self.ui.cmbEventAdd.currentText()
        
        name=self.ui.edtFullNameAdd.toPlainText()
        
        phoneNumber=self.ui.edtPhoneNumberAdd.toPlainText()
        if (len(name))>0 and (len(phoneNumber))==10:
                       
            try:
                #Connect the database
                db = mc.connect(host="localhost",user="root",password="",database="myevents")
                cursor = db.cursor()            

                #SQL
                cursor.execute("select event_Name,phoneNumber from booking")
                
                #Get all the result from the sql
                result = cursor.fetchall()            

                my_list =[]
                #insert data
                for row_number,row_data in enumerate(result):
                    o=[]
                    for column_number,data in enumerate(row_data):
                        o.append(str(data))
                        

                    my_list.append(o)
                    
                eventNameList=[]
                phoneNumberList=[]
                
                for x in my_list:
                    i=3    
                    for t in x:                
                        if (i % 2) == 0:
                            phoneNumberList.append(t)                        
                        else:
                            eventNameList.append(t)
                        i=i+1    
                isNotFound=False    
                for num in range(len(phoneNumberList)):
                    if ((eventName==eventNameList[num]) and (phoneNumber==phoneNumberList[num])):
                        isNotFound=True
                        break
                if not isNotFound:
                    cursor = db.cursor()            

                    #SQL
                    cursor.execute("Insert into booking (event_Name,name,phoneNumber) values(\'"+eventName+"\',\'"+name+"\',\'"+phoneNumber+"\')")                   
                    cursor.execute("UPDATE theevents SET tickets_Available = tickets_Available-1 where event_Name =\'"+eventName+"\'")       
                        
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Booking successful")
                    msg.exec_()
                else:                    
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Their is a booking already for "+eventName+" and the person that has this phone number :"+phoneNumber)
                    msg.exec_()                 
                    
                
            except mc.Error as e:
                print(e)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Information Invalid")
            msg.exec_()

               
        self.ui.edtFullNameAdd.setPlainText('')       
        self.ui.edtPhoneNumberAdd.setPlainText('')
#Edit booking-table
    def editbooking(self):        
        name=self.ui.edtFullNameEdit.toPlainText()      
       
        bookingId=self.ui.edtID.toPlainText()
        if (len(name))>0 and (len(bookingId))>0:
                       
            try:
                #Connect the database
                db = mc.connect(host="localhost",user="root",password="",database="myevents")
                cursor = db.cursor()            

                #SQL
                cursor.execute("select id from booking")
                
                #Get all the result from the sql
                result = cursor.fetchall()            
                
                my_list =[]
                #insert data
                for row_number,row_data in enumerate(result):
                   
                    for column_number,data in enumerate(row_data):
                        my_list.append(str(data))
                        

                
                isFound= bool(False)    
                for num in range(len(my_list)):
                    if (bookingId==my_list[num]):
                        isFound=True
                        break


                if isFound:
                    cursor = db.cursor()            

                    #SQL
                        
                                        
                    cursor.execute("UPDATE booking SET name =\'"+name+"\'where id ="+bookingId)
                         
                        
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Booking successful")
                    msg.exec_()
                    
                else:                    
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Their is a booking already for "+eventName+" and the person that has this phone number :"+phoneNumber)
                    msg.exec_()                 
                    
                
            except mc.Error as e:
                print(e)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Information Invalid")
            msg.exec_()
     
        self.ui.edtFullNameEdit.setPlainText('')       
        self.ui.edtID.setPlainText('')
#delete booking-table
    def deletebooking(self):
        msg = QMessageBox()
        isSure = msg.question(self,'', "Are you sure you want to cancel the booking?", msg.Yes | msg.No)

        if isSure == msg.Yes :
            eventName=self.ui.cmbEventDelete.currentText()
            phoneNumber=self.ui.edtPhoneNumberDelete.toPlainText()        

            if (len(phoneNumber))==10:
                try:
                    #Connect the database
                    db = mc.connect(host="localhost",user="root",password="",database="myevents")
                    cursor = db.cursor()            

                    #SQL
                    cursor.execute("select event_Name,phoneNumber from booking")
                    
                    #Get all the result from the sql
                    result = cursor.fetchall()            

                    my_list =[]
                    #insert data
                    for row_number,row_data in enumerate(result):
                        o=[]
                        for column_number,data in enumerate(row_data):
                            o.append(str(data))
                            

                        my_list.append(o)
                        
                    eventNameList=[]
                    phoneNumberList=[]
                    
                    for x in my_list:
                        i=3    
                        for t in x:                
                            if (i % 2) == 0:
                                phoneNumberList.append(t)                        
                            else:
                                eventNameList.append(t)
                            i=i+1    
                    isFound=False  
                    for num in range(len(phoneNumberList)):
                        if ((eventName==eventNameList[num]) and (phoneNumber==phoneNumberList[num])):
                            isFound=True
                            break              
                    if isFound:
                        cursor = db.cursor()            

                        #SQL                   
                                               
                        cursor.execute("Delete from booking where event_Name =\'"+eventName+"\'and phoneNumber =\'"+phoneNumber+"\'")
                        cursor.execute("UPDATE theevents SET tickets_Available = tickets_Available+1 where event_Name =\'"+eventName+"\'")     
                            
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Booking canceled")
                        msg.exec_()
                            
                    else:                    
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("Their is a booking already for "+eventName+" and the person that has this phone number :"+phoneNumber)
                        msg.exec_()  
                    
                except mc.Error as e:
                    print(e)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Information Invalid")
                msg.exec_()
         
                 
            self.ui.edtPhoneNumberDelete.setPlainText('')
#Display Bookings booking-text
    def viewbookings(self):

        try:
            #Connect the database
            db = mc.connect(host="localhost",user="root",password="",database="myevents")
            cursor = db.cursor()            

           #SQL
            cursor.execute("select id,event_Name,name,phoneNumber from booking")
            
            #Get all the result from the sql
            result = cursor.fetchall()            

            my_list =[]
            #insert data
            for row_number,row_data in enumerate(result):
                o=[]
                for column_number,data in enumerate(row_data):
                    o.append(str(data))
                    

                my_list.append(o)

            invoice=[]    
            eventNameList=[]
            names=[]
            phoneNumberList=[]
            
            for x in my_list:
                i=1    
                for t in x:                
                    if i == 1:
                        invoice.append(t)
                        
                    if i==2:
                        eventNameList.append(t)
                    if i==3:
                        names.append(t)
                    if i==4:
                        phoneNumberList.append(t)
                    i=i+1

            display="----Bookings----"
            for j in range(len(invoice)):
                display=display+"\n\n\n Invoice No.: "+invoice[j]+"\n Event Name :"+eventNameList[j]+"\n Name :"+names[j]+"\n Contact No.:"+phoneNumberList[j]

            self.ui.edtDisplay.setPlainText(display)         
        except mc.Error as e:
            print(e)
#see event event-table
    def viewevents(self):
        eventName=self.ui.cmbEventAdd.currentText()     
        try:
            
            #Connect the database
            db = mc.connect(host="localhost",user="root",password="",database="myevents")
            cursor = db.cursor()            

            #SQL
            cursor.execute("SELECT * FROM theevents where event_Name =\'"+eventName+"\'")
                
            #Get all the result from the sql
            result = cursor.fetchall()            

            my_list =[]
            #insert data
            for row_number,row_data in enumerate(result):
                
                for column_number,data in enumerate(row_data):
                    
                    my_list.append(str(data))
            display="--Event--\nEvent Name :"+my_list[0]+"\nEvent Date :"+my_list[1]+"\nEvent Time :"+my_list[2]+"\nContact No.:"+my_list[3]+"\nManager name :"+my_list[4]+"\nVenue :"+my_list[5]+"\nTickets :"+my_list[6]
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)

            msg.setText("Event Details")
            msg.setInformativeText("This is additional information")
            msg.setWindowTitle("Event")
            msg.setDetailedText(display)
            msg.exec_()
            
        except mc.Error as e:
            print(e)
#Start
if __name__=="__main__":
    
    app = QApplication(sys.argv)

    
    
    w= MyForm()
    w.show()
    sys.exit(app.exec_())
