from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# -------------------- GENERATE PASSWORD ------------------- #

def generate_password():
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
               "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    symbols = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "?", "+", "=", "/", "~",]

    pwd_letters = random.randint(8,12)
    pwd_symbol = random.randint(3,5)
    pwd_numbers = random.randint(2,4)

    new_letter = [random.choice(letters) for _ in range(pwd_letters)]
    new_symbol = [random.choice(symbols) for _ in range(pwd_symbol)]
    new_number = [random.choice(numbers) for _ in range(pwd_numbers)]

    password_list = new_letter + new_symbol +new_number
    random.shuffle(password_list)

    password_created = "".join(password_list)
    password_entry.insert(0,password_created)
    pyperclip.copy(password_created)


# --------------- SAVE PASSWORD ----------------- #
def save_data():
    website = website_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if website == '' or password == '' or email == '':
        messagebox.showerror(title='Error', message='Please fill all fields')
    else:
        is_ok = messagebox.askyesno(title=website,message=f"Do you want to save this details?  \n Email:{email}  \n Password:{password}")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    ## this is used to read data in a json file
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    ## this is used to write data into a  json file
                    json.dump(new_data, data_file, indent=4)
            else:
                ## this is used to update a json file
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    ## this is used to save the updated json file
                    json.dump(data, data_file, indent=4)
            finally:
                    website_entry.delete(0, END)
                    email_entry.delete(0, END)
                    password_entry.delete(0, END)

def find_data():
    website = website_entry.get()
    try:
        with open("data.json","r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No data found in the file.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message= f"Email: {email}\nPassword:{password}")
        else:
            messagebox.showerror(title="Error", message= "No data for this website.")


# ---------------- UI SETUP ------------- #

window = Tk()
window.title(" My Password Manager")
window.config(padx=30, pady=30,bg="green")

canvas = Canvas(width=180, height=190, background="green",highlightthickness=0)
image = PhotoImage(file="my pass_logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=1)

#  Label
website = Label(text="Website:  ", fg="black", bg="Yellow")
# website.config(width=4,height=1)
website.grid(column=0, row=1)

email = Label(text="Email/Username:  ", fg="black", bg="Yellow")
# website.config(width=14,height=2)
email.grid(column=0, row=2)

password_label = Label(text="Password:  ", fg="black", bg="Yellow")
# website.config(width=14,height=2)
password_label.grid(column=0, row=3)

# -------------------------  Buttons ----------------------- #

password = Button(text="Generate Password", bg="white",command=generate_password)
# password.config(width=15, height=1)
password.grid(column=3, row=3)

add = Button(text="Add", bg="white")
add.config(width=30, height=1, command=save_data)
add.grid(column=1, row=5,columnspan=2)

search = Button(text="Search",bg="white")
search.config(width= 12,command=find_data)
search.grid(column=3, row=1,)

# -----------------------  Entry ---------------------- #

website_entry = Entry(width=35)
website_entry.grid(row = 1, column = 1,columnspan=2)
website_entry.focus()

password_entry = Entry(width=30)
password_entry.grid(row = 3, column = 1,columnspan=2)

email_entry = Entry(width=35)
email_entry.grid(row = 2, column = 1,columnspan=2)



window.mainloop()
