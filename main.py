from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import mysql.connector

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    password_letter=[]
    for i in range(randint(8,10)):
        a=choice(letters)
        password_letter=password_letter+list(a)
    password_number=[]
    for i in range(randint(2,4)):
        b=choice(numbers)
        password_number=password_number+list(b)
    password_symbol=[]
    for i in range(randint(2,4)):
        c=choice(symbols)
        password_symbol=password_symbol+list(c)
    password_list = password_letter + password_symbol + password_number
    password = "".join(password_list)
    password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    sqlpass=sqlpass_entry.get()
    website=website_entry.get()
    email=email_entry.get()
    password=password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email} "
                                                      f"\nPassword: {password} \nIs it ok to save?")
        if is_ok:
            mydb=mysql.connector.connect(host='localhost',user='root',passwd=sqlpass)
            mycursor=mydb.cursor()
            list1=[]
            mycursor.execute("Show databases")
            for i in mycursor:
                list1+=[i[0]]
            if ('password' in list1):
                pass
            else:
                mycursor.execute('create database password')
            mycursor.execute('use password')
            mycursor.execute('show tables')
            list2=[]
            for i in mycursor:
                list2+=[i[0]]
            if ('passdata' in list2):
                pass
            else:
                mycursor.execute('create table passdata ( Website varchar(1000),Email varchar(1000),Password varchar(1000))')
            mycursor.execute("Insert into passdata values({},{},{})".format(website,email,password))
            mydb.commit()
        
# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200,bg="#000")
project_img = PhotoImage(file="p1.png")
canvas.create_image(100, 100, image=project_img)
canvas.grid(row=0, column=1)

#Labels
sqlpass_label=Label(text="SQL Password:")
sqlpass_label.grid(row=2, column=0)
website_label = Label(text="Website:")
website_label.grid(row=4, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=6, column=0)
password_label = Label(text="Password:")
password_label.grid(row=8, column=0)

#Entries
sqlpass_entry=Entry(width=35)
sqlpass_entry.grid(row=2,column=1,columnspan=2)
website_entry = Entry(width=35)
website_entry.grid(row=4, column=1, columnspan=2)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=6, column=1, columnspan=2)
email_entry.insert(0, "xyz@gmail.com")
password_entry = Entry(width=35)
password_entry.grid(row=8, column=1,columnspan=2)

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password,relief="groove")
generate_password_button.grid(row=9, column=1)
add_button = Button(text="Add", width=36, command=save,relief="groove")
add_button.grid(row=10, column=1, columnspan=2)

window.mainloop()
