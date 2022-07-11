from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
from datetime import datetime as dt
RED = "#FF6363"
ORANGE = "#FFAB76"
YELLOW = "#FFFDA2"
GREEN = "#BAFFB4"
DATA_PATH = "data.json"
EMAIL = "joangelaphyton@gmail.com"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    password_entry.delete(0,END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_list = password_numbers + password_letters + password_symbols

    random.shuffle(password_list)

    password = "".join(password_list)
    # password = ""
    # for char in password_list:
    #   password += char
    pyperclip.copy(password)
    copy_to_clip.config(text="password has been copied to Clip Board!")
    password_entry.insert(0,password)

# ---------------------------- Back up Data ------------------------------- #
def back_up():
    date_now = dt.now()
    date_now_string = str(date_now.date()).replace("-","@")


    with open(DATA_PATH, "r") as data:
        #Reading old data
        data_read = json.load(data)

    with open(f"data{date_now_string}.json", "w") as data:
        json.dump(data_read, data, indent=4)

    messagebox.showinfo(title="Success",message="Data was backed_up")

# ---------------------------- Copy Password to clipboard ------------------------------- #
def copy():
    password = password_entry.get()
    pyperclip.copy(password)
    copy_to_clip.config(text="password has been copied to Clip Board!")

# ---------------------------- REMOVE FROM LIST ------------------------------- #
def remove_from_list():
    #takes the entry's text
    website = website_entry.get().title()
    email = email_username_entry.get()
    password = password_entry.get()

    #opens the json so we can read
    with open(DATA_PATH, "r") as data:
        item_exist = False

        # Reading data
        data_read = json.load(data)

        #checks if theres a web name with the same password and email for caution so we wont delete someting we need
        for web_name in data_read.items():
            if website == web_name[0] and email == web_name[1]["email"] and password == web_name[1]["password"]:
                #if the item was found then true
                item_exist = True

        if item_exist:
            #if item do exist then ask us if we are sure that we want to delete the item
            if messagebox.askyesno(title="Are you sure you want to delete that item?",
                                   message=f"Are you sure you want to delete {website} details?"):

                #deletes the website entry
                del data_read[website]

                #successes message
                messagebox.showinfo(title="Successes",message=f"{website} details were deleted!")
        else:
            #if item does not exist then show error item was not found
            messagebox.showinfo(title="ERROR",message="Item was not found")

    #after we modified the data we need to save it again or else all the data will be deleted so we use the dump
    # and tell the func to get the data_read which is the old data without the password we wanted to delete
    with open('data.json', 'w') as data:
        new_data = json.dump(data_read, data, indent= 4)



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website_entry.focus()

    website = website_entry.get().title()
    email = email_username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email" : email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        empty = messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open(DATA_PATH,"r") as data:
                # Reading old data
                data_read = json.load(data)

        except FileNotFoundError:
            #if file was not found then create a file
            with open(DATA_PATH,"w") as data:
                json.dump(new_data,data, indent=4)

        else:
            #Updating old data with new data
            data_read.update(new_data)

            with open(DATA_PATH,"w") as data:
                # Saving updated data
                json.dump(data_read, data, indent=4)

        finally:
            website_entry.delete(0,END)
            password_entry.delete(0, END)

# ---------------------------- Show which websites do I have ------------------------------- #
def show_list():
    try:
        with open(DATA_PATH,"r") as data:
            # reading data
            data_fetch = json.load(data)
    except FileNotFoundError:
        no_data_pop_up = messagebox.showerror(title="error", message="No Data file found. "
                                                                     "Please create a new file before you search.")
    else:
        #fetching data and making it a list
        names_lst = [name for name in data_fetch.keys()]

        #making data a string that goes down a bar
        names_string = "\n".join(names_lst)

        #show the pop up with the names
        pop_up_names = messagebox.showinfo(title="Websites", message=f"{names_string}")


# ---------------------------- Search Data ------------------------------- #
def search():
    password_entry.delete(0,END)
    email_username_entry.delete(0,END)
    website = website_entry.get().title()
    try:
        with open(DATA_PATH,"r") as data:
            # reading data
            data_fetch = json.load(data)
    except FileNotFoundError:
        no_data_pop_up = messagebox.showerror(title="Error", message="No Data file found."
                                                                     " Please create a new file before"
                                                                     " you search.")
    else:
        try:
            #fetching data
            email = data_fetch[f"{website}"]["email"]
            password = data_fetch[f"{website}"]["password"]

        except KeyError:
            no_key_pop_up = messagebox.showerror(title="NO WEBSITE FOUND",message="There is no data"
                                                                                  " for that website.")
        else:
            #showing data on a popup
            popup_info = messagebox.showinfo(title=f"{website}",message=f"Email:               {email}"
                                                                        f"\nPassword:        {password}")
            if messagebox.askyesno(title="Grab items",message=f"Do you want to grab {website} details?"):
                password_entry.insert(END, password)
                email_username_entry.insert(END, email)



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50,pady=50,bg=YELLOW)
window.resizable(width=False, height=False)

#logo
canvas = Canvas(width=200,height=200, bg=YELLOW, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(130,100, image=logo)
canvas.grid(row=0,column=1)

#labels
copy_to_clip = Label(text="",fg="black",bg=YELLOW, highlightthickness=0)
copy_to_clip.grid(row=9,column=1,columnspan=2)

website = Label(text="Website:",bg=YELLOW, highlightthickness=0)
website.grid(row=1, column=0,sticky=W)

email_username = Label(text="Email/Username:",bg=YELLOW, highlightthickness=0)
email_username.grid(row=2, column=0,sticky=W)

password = Label(text="Passowrd:",bg=YELLOW, highlightthickness=0)
password.grid(row=3, column=0,sticky=W)

#entry
website_entry = Entry(width=33)
website_entry.grid(row=1,column=1, columnspan=2,sticky=W)
website_entry.focus()


email_username_entry = Entry(width=52)
email_username_entry.grid(row=2,column=1, columnspan=2,sticky=W)
email_username_entry.insert(END, EMAIL)


password_entry = Entry(width=33)
password_entry.grid(row=3,column=1,sticky=W)


#buttons
generate_password = Button(text="Generate Password:",command=password_generator, bg=ORANGE)
generate_password.grid(row=3, column=2,sticky=NW)

search_button = Button(text="Search",width=14,command=search, bg=ORANGE)
search_button.grid(row=1,column=2)

add = Button(text='Add', width=44, command=save_password, bg=GREEN)
add.grid(row=4,column=1,columnspan=2,sticky=W)

show_list = Button(text="Show List", width=44, command=show_list, bg=ORANGE)
show_list.grid(row=5, column=1, columnspan=2, sticky=W)

copy_to_clip_button = Button(text="Copy Password", width=44, command=copy, bg=ORANGE)
copy_to_clip_button.grid(row=6, column=1, columnspan=2 ,sticky=W)

remove_from_list_button = Button(text="Remove from List",width=44, command=remove_from_list, bg=RED)
remove_from_list_button.grid(row=8, column=1, columnspan=2,sticky=W)

back_up_button = Button(text="Back Up Data",width=44, command=back_up, bg=GREEN)
back_up_button.grid(row=7, column=1, columnspan=2 ,sticky=W)





window.mainloop()
