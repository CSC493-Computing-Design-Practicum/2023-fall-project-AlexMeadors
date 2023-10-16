from getpass import getpass
import mysql.connector
from mysql.connector import connect, Error
from tkinter import *
import tkinter.ttk as ttk
from windows_toasts import Toast, WindowsToaster
import os

def tkinter_setup():

    global root
    root = Tk()

    root.configure(background='gray')
    
    root.overrideredirect(1)
    screen_width = int(root.winfo_screenwidth() * .33)
    screen_height = int(root.winfo_screenheight() * .33)
    display_size = "%sx%s" % (str(screen_width), str(screen_height))
    root.geometry(display_size)

    
    button = ttk.Button(root, text="Close", command = root.destroy).grid(column = 50, row = 50, sticky=E, padx=5, pady=5)
    return root


#TODO - fix login
def login_database(username, passw):
    #Login example obtained from https://realpython.com/python-mysql/

    username = "root"
    passw = "100RacecaR001!!!"
    try:
        global connection
        connection = mysql.connector.connect(
        host="localhost",
        user= username,
        password=passw
        )
    except Error as e:
        print(e) 
    try:
        create_db_query = "CREATE DATABASE IF NOT EXISTS to_do_list"
        with connection.cursor() as cursor:
            cursor.execute(create_db_query)
        clear_frame(root)
        return True
    except Error as e:
        print(e)    


def create_columns():
    #https://www.mysqltutorial.org/mysql-create-table/
    database_message("USE to_do_list")
    database_message("""CREATE TABLE IF NOT EXISTS tasks (
                     name VARCHAR(255) NOT NULL,
                     due_date DATE NOT NULL,
                     priority TINYINT,
                     source VARCHAR(255),
                     subtask_of INT,
                     task_num INT AUTO_INCREMENT KEY)""")


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
    for data in cursorA.fetchall():
        print(data)
    connection.commit()

def add_task(name, due_date, priority, source, parent = None):
    message = """INSERT INTO tasks (name, due_date, priority, source, subtask_of)
        VALUES ("%s", "%s" , %s, "%s", %s)""" % (name, due_date, priority, source, parent)
    database_message(message)


def remove_task(task_number):
    message = "DELETE FROM tasks WHERE task_num = %s" % (task_number)
    database_message(message)

#TODO
def modify_task(task_number, name, due_date, priority, source, parent = None):
    message = """UPDATE tasks
        SET (name, due_date, priority, source, subtask_of)
        VALUES ("%s", "%s" , %s, "%s", %s)""" % (name, due_date, priority, source, parent)
    database_message(message)


def retrieve_tasks_bydate(amount):
    order_by_date()
    message = """SELECT name
    FROM tasks
    LIMIT %s""" % (amount)
    database_message_retrieve(message)


def retrieve_task_specific(field, task_num):
    message = """SELECT %s
    FROM tasks
    WHERE task_num = %s""" % (field, task_num)
    #print(message)
    database_message_retrieve(message) 
       

def order_by_date():
    message = """SELECT *
    FROM tasks
    ORDER BY due_date DESC"""
    database_message(message)


def attempt_login():
    clear_frame(root)
    #username_input = username_entry.get()
    result = 0
    result = login_database(username_input, password_input)
    show_task(1,2,2)
    print(result)


def show_login(root):
        #https://www.simplifiedpython.net/python-gui-login/

        # username
        global username_input
        username_input = ""
        ttk.Label(root, text="Username:").grid(column=0, row=0, sticky=W, padx=5, pady=5)
        username_entry = ttk.Entry(root, textvariable=username_input).grid(column=1,
            row=0, sticky=E, padx=5, pady=5)

        # password
        global password_input
        password_input = ""
        ttk.Label(root, text="Password:").grid(column=0, row=1, sticky=W, padx=5, pady=5)
        password_entry = ttk.Entry(root,  show="*", textvariable=password_input).grid(column=1,
            row=1, sticky=E, padx=5, pady=5)

        # login button
        login_button = ttk.Button(root, text="Login",
            command = attempt_login).grid(column=1, row=3, sticky=E, padx=5, pady=5)


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

def show_task(task_num, x, y):
    task_info = retrieve_task_specific("name", task_num)
    #print(task_info)
    ttk.Label(root, text=task_info).grid(column=x, row=y, sticky=S, padx=20, pady=20, rowspan=5)
    task_info = retrieve_task_specific("due_date", task_num)
    ttk.Label(root, text=task_info).grid(column=x+5, row=y, sticky=S, padx=20, pady=20)


def task_view():
    print()  


def main():
    print("Running")
    #Start initial connection
    root = tkinter_setup()
    login_database(1,2)

    show_login(root)
    #notification()
    show_task(1,2,2)
    print(retrieve_task_specific("name",1))
    while True:
        root.update_idletasks()
        root.update()
    #remove_task(connection, 1)


if __name__ == '__main__':
    main()