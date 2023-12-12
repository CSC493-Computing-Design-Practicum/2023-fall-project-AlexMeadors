from getpass import getpass
import mysql.connector
from mysql.connector import connect, Error
import tkinter as tk           
from tkinter import font as tkfont
import tkinter.ttk as ttk
from windows_toasts import Toast, WindowsToaster
import os
from PIL import ImageTk, Image
import pygetwindow as gw
from pywinauto import Desktop


def tkinter_setup():

    global root
    root = tk.Tk()

    root.configure(background='gray')
    root.title("Chronokeeper")

    screen_width = int(root.winfo_screenwidth() * .33)
    screen_height = int(root.winfo_screenheight() * .33)

    display_size = "%sx%s" % (str(screen_width), str(screen_height))
    root.geometry(display_size)

    root.attributes("-topmost", True)
    return root


#TODO - fix login
def login_database(username, passw):
    #Login example obtained from https://realpython.com/python-mysql/
    fail = True
    try:
        fail = False
        global connection
        #Take out for interface
        # username = "root"
        # passw = getpass()
        connection = mysql.connector.connect(
        host="localhost",
        user= username,
        password=passw
        )
    except Error as e:
        message = str(e)
        message = message[:4]
        #The code for a bad login
        if message == "1045":
            print("Bad Login, Try Again")                
            #elseif message
    
    try:
        create_db_query = "CREATE DATABASE IF NOT EXISTS to_do_list"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
        return True
    except NameError:
        #Server not found, close it down
        print("Login Invalid")  


def create_columns():
    #https://www.mysqltutorial.org/mysql-create-table/
    database_message("USE to_do_list")
    database_message("""CREATE TABLE IF NOT EXISTS tasks (
                     name VARCHAR(255) NOT NULL,
                     due_date DATE NOT NULL,
                     priority TINYINT,
                     source VARCHAR(255),
                     subtask_of INT,
                     task_num INT AUTO_INCREMENT KEY,
                     completed BOOL)""")


def database_message(message):
    cursorA = connection.cursor(buffered=True)
    try:
        cursorA.execute(message)
    except Error as e:
        print(e)
    connection.commit()


def database_message_retrieve(message):
    database_message("USE to_do_list")
    cursorA = connection.cursor(buffered=True)
    try:
        cursorA.execute(message)
    except Error as e:
        print(e)
    connection.commit()
    try:
        for data in cursorA.fetchall():
            return data #Need to pass this out
    except Error as e:
        if str(e) == "No result set to fetch from":
            print("No results match that search")


def add_task(name, due_date, priority, source, parent = None):
    message = """INSERT INTO tasks (name, due_date, priority, source, subtask_of, completed)
        VALUES ("%s", "%s" , %s, "%s", %s, 0)""" % (name, due_date, priority, source, parent)
    database_message(message)


def remove_task(task_number):
    message = "DELETE FROM tasks WHERE task_num = %s" % (task_number)
    database_message(message)


def modify_task(task_number, name, due_date, priority, source, completed, parent = None):
    message = """UPDATE tasks
        SET name = "%s",
        due_date = "%s",
        priority = %s,
        source = "%s",
        subtask_of = %s,
        completed = %s
        WHERE task_num = %s;""" % (name, due_date, priority, source, parent, completed, task_number)
    database_message(message)


def retrieve_tasks_bydate(amount):
    order_by_date()
    message = """SELECT *
    FROM tasks
    LIMIT %s""" % (amount)
    database_message_retrieve(message)


def retrieve_task_specific(column, search_term):
    message = """SELECT *
    FROM tasks
    WHERE %s = "%s" """ % (column, search_term)
    output = database_message_retrieve(message) 
    return output
       

def order_by_date():
    message = """SELECT *
    FROM tasks
    ORDER BY due_date DESC"""
    database_message(message)


def attempt_login():
    #clear_frame(root)
    print("ATTEMPTING LOGIN")
    global login
    global mainScr
    usern = login.username_entry.get()
    passw = login.password_entry.get()
    result = login_database(usern, passw)

    if result == True:
        #Clear screen and go to main
        clear_frame()
        mainScr = mainScreen(root)
    print(result)


class loginScreen():
    def __init__(self, master):
        screen_width = int(root.winfo_screenwidth() * .33)
        screen_height = int(root.winfo_screenheight() * .33)
        self.master = master

        image = Image.open("chronokeeper_logo.png")
        logo_size = (int(screen_width * .2), int(screen_width * .2))
        resize_image = image.resize(logo_size)
        self.logo = ImageTk.PhotoImage(resize_image)

        self.canvas = tk.Canvas(root,height=screen_width * .15, width=screen_width * .15)
        #self.canvas = tk.Canvas(root, width = 100, height = 100)
        self.canvas.place(x = (screen_width / 2) - logo_size[0] / 2,
                           y = screen_height * .05, width = logo_size[0], height = logo_size[1])
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.logo) 

        #username
        self.username_label = tk.Label(root, text="Username:")
        self.username_label.place(x=screen_width * .3, y=screen_height * .45, width=screen_width * .15)
        self.username_entry = tk.Entry(root)
        self.username_entry.place(x=screen_width * .45, y=screen_height * .45, width=screen_width * .2)

        #password
        self.password_label = tk.Label(root, text="Password:")
        self.password_label.place(x=screen_width * .3, y=screen_height * .6, width=screen_width * .15)

        self.password_entry = tk.Entry(root,  show="*")
        self.password_entry.place(x=screen_width * .45, y=screen_height * .6, width=screen_width * .2)

        #login button
        login_button = tk.Button(root, text="Login",
             command = attempt_login).place(x=screen_width * .4, y=screen_height * .75, width=screen_width * .2)


class mainScreen():
    def __init__(self, master):
        self.master = master
        self.focus = ""
        self.time = 0
        self.order = 0 #0 for due date, 1 for prio
        #Main task display
        screen_width = int(root.winfo_screenwidth()*.33)
        screen_height = int(root.winfo_screenheight()*.33)
        self.taskFrame = tk.Frame(width= screen_width * .9,
                                  height = screen_height * .5)
        self.taskNameLabel = tk.Label(width = int(screen_width * .02),
                                      height = int(screen_height * .005),
                                      text = "Task Name",
                                      background = "blue")
        #Due Date Label
        self.dueDateLabel = tk.Label(width= int(screen_width * .02),
                                      height = int(screen_height * .005),
                                      text= "Due Date",
                                      background= "blue")
        #Source Label
        self.sourceLabel = tk.Label(width= int(screen_width * .02),
                                      height = int(screen_height * .005),
                                      text= "Source",
                                      background= "blue")
        #Priority Label
        self.priorityLabel = tk.Label(width= int(screen_width * .02),
                                      height = int(screen_height * .005),
                                      text= "Priority",
                                      background= "blue")
        #Main Task Label
        self.maintaskLabel = tk.Label(width= int(screen_width * .02),
                                      height = int(screen_height * .005),
                                      text= "Parent Task",
                                      background= "blue")
        
        self.task1 = taskDisplay(root, 1, 1)
        self.task2 = taskDisplay(root, 2, 2)
        self.task3 = taskDisplay(root, 3, 3)
        self.task4 = taskDisplay(root, 4, 4)

        #Order Buttons
        self.orderDateButton = ttk.Button(text='Order by Date', 
                                          width= int(screen_width * .04),
                                          command = setOrderDate)
        self.orderPrioButton = ttk.Button(text='Order by Priority', 
                                          width= int(screen_width * .04),
                                          command = setOrderPrio)

        
        self.windowComboBox = ttk.Combobox(textvariable="Chronokeeper")
        windows = Desktop(backend="uia").windows()

        self.windowsValues = [w.window_text() for w in windows]
        self.windowComboBox['values'] = self.windowsValues
        self.windowComboBox['state'] = 'readonly'
        self.windowComboBox.bind('<<ComboboxSelected>>', setFocus)
        self.display()
        

    def display(self):
        screen_width = int(root.winfo_screenwidth()*.33)
        screen_height = int(root.winfo_screenheight()*.33)
        self.taskFrame.place(x = screen_width * .05,
                             y = screen_height * .05)
        self.taskNameLabel.place(x = int(screen_width * .05),
                                y = int(screen_height * .05))
        self.dueDateLabel.place(x= int(screen_width * .225),
                                  y = int(screen_height * .05))
        self.sourceLabel.place(x= int(screen_width * .4),
                                  y = int(screen_height * .05))
        self.priorityLabel.place(x= int(screen_width * .575),
                                  y = int(screen_height * .05))
        self.maintaskLabel.place(x= int(screen_width * .75),
                                  y = int(screen_height * .05))
        self.orderDateButton.place(x= int(screen_width * .05),
                                  y = int(screen_height * .575))
        self.orderPrioButton.place(x= int(screen_width * .05),
                                  y = int(screen_height * .675))
        self.windowComboBox.place(x= int(screen_width * .05),
                                  y = int(screen_height * .775))
        
    def setOrder(self, order):
        self.order = order
        print(order)
    
    def setFocus(self):
        self.focus = self.windowComboBox.get()
        self.timeCheck()

    def timeCheck(self):
        print("CHECK")
        if gw.getActiveWindow().title != self.focus:
            self.time += 1
            root.after(1000, self.timeCheck)
        if self.time >= 10: #If its been more than 10 minutes, ping
            notification()


def setOrderDate():
    global mainScr
    mainScr.setOrder(0)


def setOrderPrio():
    global mainScr
    mainScr.setOrder(1)


class taskDisplay():
    def __init__(self, master, tasknum, displaySlot):
        self.master = master
        self.displaySlot = displaySlot
        self.getTask(tasknum)
        self.tasknum = tasknum
        screen_height = int(root.winfo_screenheight()*.33)
        self.offset = (displaySlot-1) * .1 * screen_height
        self.displayTask()

    def getTask(self, tasknum):
        data = retrieve_task_specific("task_num", tasknum)
        self.name = data[0]
        self.duedate = data[1]
        self.priority = data[2]
        self.source = data[3]
        self.maintask = data[4]


    def displayTask(self):
        screen_width = int(root.winfo_screenwidth()*.33)
        screen_height = int(root.winfo_screenheight()*.33)
        #Name Display
        self.nameLabel = tk.Label(width= int(screen_width * .02),
                                      height = int(screen_height * .005),
                                      text= self.name,
                                      background= "blue")
        self.nameLabel.place(x = int(screen_width * .05),
                                y = int(screen_height * .15 + self.offset))
        #Date Display
        self.duedateLabel = tk.Label(width= int(screen_width * .02),
                                      height = int(screen_height * .005),
                                      text= self.duedate,
                                      background= "blue")
        self.duedateLabel.place(x= int(screen_width * .225),
                                y = int(screen_height * .15 + self.offset))
        #Source Display
        self.duedateLabel = tk.Label(width= int(screen_width * .02),
                                      height = int(screen_height * .005),
                                      text= self.source,
                                      background= "blue")
        self.duedateLabel.place(x= int(screen_width * .4),
                                y = int(screen_height * .15 + self.offset))
        #Priority Display
        self.duedateLabel = tk.Label(width= int(screen_width * .02),
                                      height = int(screen_height * .005),
                                      text= self.priority,
                                      background= "blue")
        self.duedateLabel.place(x= int(screen_width * .575),
                                y = int(screen_height * .15 + self.offset))
        #Parent Display
        self.duedateLabel = tk.Label(width= int(screen_width * .02),
                                      height = int(screen_height * .005),
                                      text= self.maintask,
                                      background= "blue")
        self.duedateLabel.place(x= int(screen_width * .75),
                                y = int(screen_height * .15 + self.offset))


def setFocus(none):
    global mainScr
    mainScr.setFocus()


def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()


def notification():
    #https://pypi.org/project/Windows-Toasts/
    toaster = WindowsToaster('Focus')
    newToast = Toast()
    newToast.text_fields = ['Back on task time']
    newToast.on_activated = lambda _: print('Toast clicked!')
    toaster.show_toast(newToast)


def main():
    print(gw.getActiveWindow().title)
    #notification() #works
    print("Running")
    #Start initial connection
    login_database("root","100RacecaR001!!!")
    root = tkinter_setup()
    # app = loginScreen(root)
    
    global login
    global mainScr
    #login = loginScreen(root)
    mainScr = mainScreen(root)

    #create_columns() #After login, before anything else
    #add_task("testing", "2023-12-12", "1", "Capstone", 0) #this format works
    
    #SYNTAX
    #modify_task(8, "testing", "2023-12-12", 1, "ME", 0)
    
    #username_input, password_input = show_login(root)

    root.mainloop()    
    #EXAMPLE QUERIES
    #INSERT INTO tasks (name, due_date, priority, source, subtask_of) 
    #VALUES ("test", "2000-11-21" , "1", "Capstone", 0);

if __name__ == "__main__":

    main()
