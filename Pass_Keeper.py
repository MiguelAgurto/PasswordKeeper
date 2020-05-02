from tkinter import Tk, Label, Button, Entry
import sqlite3

db_main = sqlite3.connect('passwordKeeper.sqlite')
db_main.execute(
    'CREATE TABLE IF NOT EXISTS login (username TEXT NOT NULL PRIMARY KEY, password TEXT NOT NULL)')


def log_in():
    db = sqlite3.connect('passwordKeeper.sqlite')
    username = username_input.get()
    password = password_input.get()
    try:
        cursor_login = db.cursor()
        cursor_login.execute("""
                SELECT password FROM login
                WHERE username = ?        
                """, (username,))
        db_password = cursor_login.fetchone()

        if db_password[0] == password:
            print('Welcome {}'.format(username))
        else:
            print('Invalid Username or Password')
    except:
        print('Invalid username')

    username_input.delete(0, "end")
    password_input.delete(0, "end")


def create_account():
    """"
        First check if there is an account, in case there is one already with the same username
        print "There is already an account with the same username".
        Otherwise create a new account.
    """
    username = username_input.get()
    password = password_input.get()

    cursor2 = db_main.execute("""SELECT username FROM login""")
    db_username = cursor2.fetchall()
    user_list = []

    for row in db_username:
        for i in row:
            user_list.append(i)

    if username not in user_list:
        cursor2.execute("""
                            INSERT INTO login (username, password)
                            VALUES (? , ?)
                        """, (username, password))
        print('New Account Created')
        cursor2.connection.commit()
    else:
        print('There is already an account with this username. Choose a different username')

    username_input.delete(0, "end")
    password_input.delete(0, "end")


mainWindow = Tk()  # Main window
mainWindow.geometry("300x210")
mainWindow.title('Password Keeper v.1')

mainWindow.rowconfigure([5, 6], minsize=40)
mainWindow.columnconfigure([1, 2, 3, 4, 5], minsize=15, weight=1)

# Widgets
welcomeLabel = Label(
    mainWindow, text='Welcome to Password Keeper v.1\n Log in or create an account.')
usernameLabel = Label(mainWindow, text='Username')
passwordLabel = Label(mainWindow, text='Password')
username_input = Entry(mainWindow)
password_input = Entry(mainWindow, show='*')
login_button = Button(mainWindow, text='Log-in', width=10, command=log_in)
create_account = Button(mainWindow, text='Create',
                        width=10, command=create_account)

# Configuration of widgets
welcomeLabel.grid(row=0, column=2, columnspan=3)
usernameLabel.grid(row=1, column=2, columnspan=3)
username_input.grid(row=2, column=2, columnspan=3)
passwordLabel.grid(row=3, column=2, columnspan=3)
password_input.grid(row=4, column=2, columnspan=3)
login_button.grid(row=5, column=3)
create_account.grid(row=6, column=3)

mainWindow.mainloop()
