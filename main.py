from getpass import getpass
import mysql.connector
from mysql.connector import connect, Error
import tkinter as tk           
from tkinter import font as tkfont
import tkinter.ttk as ttk
from windows_toasts import Toast, WindowsToaster
import os
from PIL import Image

def tkinter_setup():

    global root
    root = tk.Tk()

    root.configure(background='gray')

    screen_width = int(root.winfo_screenwidth() * .33)
    screen_height = int(root.winfo_screenheight() * .33)
    display_size = "%sx%s" % (str(screen_width), str(screen_height))
    root.geometry(display_size)

    root.attributes("-topmost", True)
    return root


#TODO set this up and make it pretty
def setup_login(root):
    login_frame = tk.Frame(root)

    print("Made it")
    screen_width = int(root.winfo_screenwidth() * .33)
    screen_height = int(root.winfo_screenheight() * .33)

 # username

    # username_input = ""
    # ttk.Label(login_frame, text="Username:").place(x=screen_width * .3, y=screen_height * .25, width=screen_width * .15)
    # username_entry = ttk.Entry(login_frame, textvariable=username_input).place(x=screen_width * .45, y=screen_height * .25, width=screen_width * .2)
    # # password
    # global password_input
    # password_input = ""
    # ttk.Label(login_frame, text="Password:").place(x=screen_width * .3, y=screen_height * .45, width=screen_width * .15)
    # password_entry = ttk.Entry(login_frame,  show="*", textvariable=password_input).place(x=screen_width * .45, y=screen_height * .45, width=screen_width * .2)
    # # login button
    # login_button = ttk.Button(login_frame, text="Login",
    #     command = attempt_login).place(x=screen_width * .4, y=screen_height * .7, width=screen_width * .2)

    screen_width = int(root.winfo_screenwidth() * .33)
    screen_height = int(root.winfo_screenheight() * .33)
    label = tk.Label(login_frame, text="Login")
    label.pack(side="top", fill="x", pady=10)
    username_entry = tk.Entry(login_frame)
    username_entry.pack(side="top", fill="x", pady=10, padx= screen_width*.10)
    password_entry = tk.Entry(login_frame)
    password_entry.pack(side="top", fill="x", pady=10, padx= screen_width*.10)
    password_entry.config(show="*")

    login_frame.tkraise()


#TODO - fix login
def login_database(username, passw):
    #Login example obtained from https://realpython.com/python-mysql/
    fail = True
    while fail == True:
        try:
            fail = False
            global connection

            #Take out for interface
            username = "root"
            passw = getpass()

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
                fail = True
                print("Try again")
            #elseif message
    
    try:
        create_db_query = "CREATE DATABASE IF NOT EXISTS to_do_list"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
        return True
    except NameError:
        #Server not found, close it down
        print("Server is Not Running")
        exit()    


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
    try:
        for data in cursorA.fetchall():
            print(data) #Need to pass this out
    except Error as e:
        if str(e) == "No result set to fetch from":
            print("No results match that search")
    connection.commit()


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
    database_message_retrieve(message) 
       

def order_by_date():
    message = """SELECT *
    FROM tasks
    ORDER BY due_date DESC"""
    database_message(message)


def attempt_login():
    #clear_frame(root)
    print("ATTEMPTING LOGIN")
    global login
    usern = login.username_entry.get()
    passw = login.password_entry.get()
    result = login_database(usern, passw)
    print(result)


class loginScreen():
    def __init__(self, master):
        screen_width = int(root.winfo_screenwidth() * .33)
        screen_height = int(root.winfo_screenheight() * .33)
        self.master = master
        logo_image = Image.open("chronokeeper_logo.png")
        logo_size = (int(screen_width * .15),int(screen_width * .15))
        logo_image.resize(logo_size)
        logo = tk.PhotoImage(file="chronokeeper_logo.png")
        self.frame = tk.Frame(self.master)
        self.logo_label = ttk.Label(root, image=logo).place(x=screen_width * .1, y=screen_height * .25, height=screen_width * .75, width=screen_width * .75)
        self.username_label = ttk.Label(root, text="Username:").place(x=screen_width * .3, y=screen_height * .25, width=screen_width * .15)
        self.username_entry = ttk.Entry(root).place(x=screen_width * .45, y=screen_height * .25, width=screen_width * .2)

        # password
        global password_input
        password_input = ""
        self.password_label = ttk.Label(root, text="Password:").place(x=screen_width * .3, y=screen_height * .45, width=screen_width * .15)
        self.password_entry = ttk.Entry(root,  show="*").place(x=screen_width * .45, y=screen_height * .45, width=screen_width * .2)

        # login button
        login_button = ttk.Button(root, text="Login",
             command = attempt_login).place(x=screen_width * .4, y=screen_height * .7, width=screen_width * .2)
        
        # # self.frame.tkraise()    
        # self.master = master
        # self.frame = tk.Frame(self.master)
        # self.entry = tk.Entry(self.master)
        # self.entry.pack()
        # self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
        # self.button1.pack()
        # self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = loginScreen(self.newWindow)


def clear_frame(root):
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
    #notification() #works
    print("Running")
    #Start initial connection
    root = tkinter_setup()
    # app = loginScreen(root)
    
    #setup_login(root)
    login_database(1,2)
    global login
    login = loginScreen(root)
    create_columns() #After login, before anything else
    #add_task("testing", "2023-12-12", "1", "Capstone", 0) #this format works
    
    #SYNTAX
    #modify_task(8, "testing", "2023-12-12", 1, "ME", 0)
    
    #username_input, password_input = show_login(root)

    root.mainloop()
    #task_view(root, cv)
    #show_login(root, cv)

    #remove_task(connection, 1)
    
    #EXAMPLE QUERIES
    #INSERT INTO tasks (name, due_date, priority, source, subtask_of) 
    #VALUES ("test", "2000-11-21" , "1", "Capstone", 0);

if __name__ == "__main__":

    main()
