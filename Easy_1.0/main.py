from calendar import c
from msilib.schema import CheckBox
from select import select
from tkinter import *
from tkinter import messagebox
import datetime
import pytz
import sqlite3
import random
from cryptography.fernet import Fernet
from requests import head









storeName_font = ("Bahnschrift Light", 30, "bold")
font_1 = ("Bahnschrift Light ", 20)
font_2 = ("Bahnschrift Light ", 15, "bold")
font_3 = ("Bahnschrift Light ", 13, "bold")
font_4 = ("Bahnschrift Light", 15, "bold")
font_5 = ("Bahnschrift Light", 11, "bold")
font_6 = ("Bahnschrift Light", 10, "bold")

default_titlle = "Easy POS"
default_icon = "images/user.png"
default_background_image = "images/bg_image2_b.png"
register = True
cursordataid = {}
sellsDataId = {}
updatelist = []

salesDataList = []
salesDataListAmount = []

entry_bg = "#0D3F7C"
entry_fg = "white"
entry_bd = 2
activeBGC = '#06264D'
activeFGC= 'white'

button_bg = "#1F4A9E"
button_fg = "white"
button_width= 15
fg_color = "#0D3F7C"
dateTime = ""
deleteAuth = 0

update_id = []
saleCount = 0
salesPrDic = {}
userAuth = 0

userUpdataData = {}
userUserData = {}




database_conn1 = sqlite3.connect("Data/main.db")
database_conn2 = sqlite3.connect("Data/user_infor.db")
database_conn3 = sqlite3.connect("Data/settingss.db")


def load_key():
    return open("Data/secret.key", "rb").read()

load_key()

def encryptPassword(password):
    key = load_key()
    encoded_password = password.encode()
    f = Fernet(key)
    encrypted_p = f.encrypt(encoded_password)

    return  encrypted_p

def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_password)
    password = decrypted_message.decode()
    return  password
   

getData = database_conn2.cursor()
getData.execute("SELECT rowid, * FROM  storedata")
storesData = getData.fetchall()
storeName = str(storesData[0][1])
setCurrency = storesData[0][2]
loggedUser = ""

getDeleteAuth = database_conn3.cursor()
getDeleteAuth.execute("SELECT * FROM settingd")
deletedata =  getDeleteAuth.fetchall()
deleteAuth = deletedata[0][1]



date = datetime.datetime.now(tz=pytz.UTC)
dateTime = (date.strftime('%D'))

def verify_entry_fun():
    global userAuth
    global loggedUser 
    user_name = name_entry.get()
    user_password = password_entry.get()
    getUserData = database_conn2.cursor()
    getUserData.execute("SELECT * FROM userdata")
    mydata = getUserData.fetchall()
    check_adminlist = []
    check_admins = 0
    for data in mydata:
        if data[2] == 1:
            check_adminlist.append(1)
            break
    if len(check_adminlist) < 1:
        check_admins = 1

    

    if len(mydata) < 1:
        userAuth = 1
        login_window.destroy()
        verify_entry()
        
    
    else:
        for user in mydata:
            password = decrypt_password(user[1])
            if user_name == user[0]:
                if user_password == password:
                    if user[2] == 1:
                        userAuth = 1
                        loggedUser = user[0] 
                    elif user[2] != 1 & check_admins == 1:
                        userAuth = 1
                        loggedUser = user[0]
                       

                    login_window.destroy()
                    verify_entry()
                    break
                else:
                    messagebox.showwarning(title="Warning", message="Wrong Password")
                    break            
        
    
    

# USER AUTH
def checkUserAuth():
    if(userAuth == 1):
        return 1
    else:
        return 0
# REOPEN DIRECTORY
def reopen_window():
    pass

def return_director(event):
    register_main.destroy()
    window.loadtk()
    verify_entry()

def return_directorad(event):
    admin_main.destroy()
    window.loadtk()
    verify_entry()

# 
# 
# 
# 
# ADMIN WINDOW



# ADMIN FUNCTIONS START


def listdisplay():
    count = 0
    inventory_list.delete(0,END)
    cursordataid.clear()
    inventory = sqlite3.connect("Data/main.db")
    product_infor = inventory.cursor()
    product_infor.execute("SELECT  rowid, * FROM inventory")
    return_products = product_infor.fetchall()
    
    for product_in in return_products:
        cursordataid[count] = product_in[0]
        count += 1
        
        product_deatils = f"Product Name: {product_in[1]} /// Product Code:{product_in[4]} /// Product Quantity:{product_in[2]} /// Product Unit Price:{product_in[3]} /// Product Description:{product_in[5]}"
        inventory_list.insert(int(product_in[0]), product_deatils) 
        
    
     

def generate_code2():
    code_confirm = True

    while code_confirm:
        code = random.randint(1000, 9999)
        check_code = sqlite3.connect("Data/main.db")
        codes = check_code.cursor()
        codes.execute(f"SELECT  * FROM inventory WHERE product_code = {code}")
        codel = codes.fetchall()
        if(len(codel)  == 0):
            update_code_input.delete(0, END)
            update_code_input.insert(0, str(code))
            code_confirm = False
        else:
            code = random.randint(1000, 9999)

def generate_code():
    
    
    code_confirm = True

    while code_confirm:
        code = random.randint(1000, 9999)
        check_code = sqlite3.connect("Data/main.db")
        codes = check_code.cursor()
        codes.execute(f"SELECT  * FROM inventory WHERE product_code = {code}")
        codel = codes.fetchall()
        if(len(codel)  == 0):
            product_code_input.delete(0, END)
            product_code_input.insert(0, str(code))
            code_confirm = False
        else:
            code = random.randint(1000, 9999)


def save_product():
    enter_pw.wm_attributes("-topmost", 0)
    enter_pw.focus_force()
    date = datetime.datetime.now(tz=pytz.UTC)
    dateTime = (date.strftime('%D'))
    product_name = str(product_name_input.get())
    product_quantity =  str(product_quantity_input.get())
    product_unitp =  str(product_uniteprice_input.get())
    product_code =  str(product_code_input.get())
    product_description =  str(product_description_input.get())

    length_check = [product_name, product_quantity, product_unitp, product_code, product_description,]
    store = [product_name, product_quantity, product_unitp, product_code, product_description,dateTime]
    item_name = sqlite3.connect("Data/main.db")
    name = item_name.cursor()
    name.execute(f"SELECT  * FROM inventory")
    return_name = name.fetchall()

    name_list = []
    for item in return_name:
        item_name  = str(item[0])
        item_name = item_name.lower()
        name_list.append(item_name)

    
    if product_name.lower() in name_list:
        messagebox.showinfo(title="Warning", message=f'Product Name \"{product_name}\" already exists!')
        enter_pw.focus_force()
        enter_pw.wm_attributes("-topmost", 1)

    
    elif product_name.lower() not in name_list:
        for item in length_check:
            if(len(item) < 1):
                messagebox.showinfo(title="Warning", message='Ensure No Fields Are Empty')
                enter_pw.focus_force()
                enter_pw.wm_attributes("-topmost", 1)
                
                break
            else:
                if(product_code.isdigit() and product_unitp.isdigit()):
                    try:
                        data_entrie = ''' INSERT INTO inventory(
                                                                                    product_name,
                                                                                    product_quantity,
                                                                                    product_unit_price,product_code ,product_description,
                                                                                    entry_date)
                                                                                    VALUES(?,?,?,?,?,?) '''

                        connection_1 =  database_conn1.cursor()
                        connection_1.execute(data_entrie, store)
                        database_conn1.commit()
                        clearentries()
                        listdisplay()
                        break
                    except :
                        print("Somthing Went Wrong")
                    
                else:
                    messagebox.showinfo(title="Warning", message='Ensure \"Product Unit Price\" and \"Product Quantity\" are numbers ')
                    enter_pw.focus_force()
                    enter_pw.wm_attributes("-topmost", 1)
                    break

def update_product():
    update_pw.focus_get()
    update_pw.wm_attributes("-topmost", 0)
    date = datetime.datetime.now(tz=pytz.UTC)
    dateTime = (date.strftime('%D'))
    update_name = str(update_name_input.get())
    update_quantity = str(update_quantity_input.get())
    update_unitp = str(update_uniteprice_input.get())
    update_code = str(update_code_input.get())
    update_description = str(update_description_input.get())

    length_check = [update_name, update_quantity,update_unitp,update_code,update_description]
    
    item_name = sqlite3.connect("Data/main.db")
    name = item_name.cursor()
    name.execute(f"SELECT  * FROM inventory")
    return_name = name.fetchall()

    name_list = []
    itemslist = []

    for itemsindex in reversed(inventory_list.curselection()):
        itemslist.append(itemsindex)
        
    itemin = itemslist[0]
    cursordataidvalue = cursordataid[itemin]
    print(f"the id is {cursordataidvalue}")
    for item in return_name:
        item_name  = str(item[0])
        item_name = item_name.lower()
        name_list.append(item_name)

    if update_name.lower() in name_list:
        messagebox.showinfo(title="Warning", message=f'Product Name \"{update_name}\" already exists!')
        update_pw.focus_force()
        update_pw.wm_attributes("-topmost", 1)
    
    elif update_name.lower() not in name_list:
        for item in length_check:
            if(len(item) < 1):
                messagebox.showinfo(title="Warning", message='Ensure No Fields Are Empty')
                update_pw.focus_force()
                update_pw.wm_attributes("-topmost", 1)
                break
            else:

                # myuse = cursordataid[itemslist[0]]

                if(update_code.isdigit() and update_unitp.isdigit()):
                    store = [update_name, update_quantity,update_unitp,update_code,update_description,dateTime]
                    data_entrie = f'''UPDATE inventory SET 
                                                                                product_name = '{update_name}',
                                                                                product_quantity = '{update_quantity}',
                                                                                product_unit_price = '{update_unitp}',
                                                                                product_code = '{update_code}',
                                                                                product_description = '{update_description}',
                                                                                entry_date = '{dateTime}'  WHERE rowid = '{cursordataidvalue}' '''

                    connection_1 =  database_conn1.cursor()
                    connection_1.execute(data_entrie)
                    database_conn1.commit()
                    clearupdate_entries()
                    break
                   
                else:
                    messagebox.showinfo(title="Warning", message='Ensure \"Product Unit Price\" and \"Product Quantity\" are numbers ')
                    update_pw.focus_force()
                    update_pw.wm_attributes("-topmost", 1)
                    break


def clearupdate_entries():
    update_name_input.delete(0, END)
    update_quantity_input.delete(0, END)
    update_uniteprice_input.delete(0, END)
    update_code_input.delete(0, END)
    update_description_input.delete(0, END)
    
def clearentries():
    product_name_input.delete(0,END)
    product_quantity_input.delete(0,END)
    product_uniteprice_input.delete(0,END)
    product_code_input.delete(0,END)
    product_description_input.delete(0,END)


def enter_product():
    global product_name_input
    global product_quantity_input
    global product_uniteprice_input
    global product_code_input
    global product_description_input
    global enter_pw
    enter_pw = Toplevel()
    enter_pw.wm_attributes("-topmost", 1)
    enter_pw.focus_force()
    enter_pw.title(default_titlle)
    enter_pw.geometry("630x500")
    windowWidth = enter_pw.winfo_reqwidth()
    windowHeight = enter_pw.winfo_reqheight()
    positionRight = int(enter_pw.winfo_screenwidth()/2 - windowWidth * 1.5)
    positionDown = int(enter_pw.winfo_screenheight()/2 - windowHeight *  1.4)
    enter_pw.geometry("+{}+{}".format(positionRight, positionDown))
    enter_pw.resizable(0,0)
    background_image = PhotoImage(file = "images/bg_image2_b.png")

    background_i = Label(enter_pw, bg="white")
    background_i.place(x=0, y=0, relheight=1, relwidth=1)
    
    enter_title = Label(enter_pw, text="Enter Item", font=font_4, fg=fg_color, bg="white", anchor='w')
    enter_title.grid(row=0, column=0, sticky='w', padx=5, pady=5)

    product_name_label = Label(enter_pw, text="Enter Product Name", font=font_3, fg=fg_color, bg="white",anchor='w')
    product_name_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)

    productin_frame = Frame(enter_pw, bg=button_bg)
    product_name_input = Entry(productin_frame, font=font_3, fg=fg_color , bg='#F0F0F0' , width=35, relief=FLAT, insertbackground=fg_color)
    product_name_input.grid(row=0, column=0, sticky='w', padx=1, pady=1)

    productin_frame.grid(row=1, column=1, sticky='w', padx=5, pady=5)

    product_quantity_label = Label(enter_pw, text="Enter Product Quantity", font=font_3, fg=fg_color, bg="white",anchor='w')
    product_quantity_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)

    productq_frame = Frame(enter_pw, bg=button_bg)
    product_quantity_input = Entry(productq_frame,  font=font_3, fg=fg_color , bg='#F0F0F0' , width=35, relief=FLAT, insertbackground=fg_color)
    product_quantity_input.grid(row=1, column=1, sticky='w', padx=1, pady=1)
    productq_frame.grid(row=2, column=1, sticky='w', padx=5, pady=5)

    product_uniteprice_label = Label(enter_pw, text="Enter Product Unit Price", font=font_3, fg=fg_color, bg="white",anchor='w')
    product_uniteprice_label.grid(row=3, column=0, sticky='w', padx=5, pady=5)

    pu_frame = Frame(enter_pw, bg=button_bg)
    product_uniteprice_input = Entry(pu_frame,  font=font_3, fg=fg_color , bg='#F0F0F0' , width=35, relief=FLAT, insertbackground=fg_color)
    product_uniteprice_input.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    pu_frame.grid(row=3, column=1, sticky='w', padx=5, pady=5)

    product_code = Button(enter_pw, text="Generate Product Code", font=font_5, bg=button_bg, fg=button_fg, command=generate_code, relief=FLAT,activebackground=activeBGC, activeforeground=activeFGC)
    product_code.grid(row=4, column=0, sticky='w', padx=5, pady=5)

    pd_frame = Frame(enter_pw, bg=button_bg)
    product_code_input = Entry(pd_frame,  font=font_3, fg=fg_color , bg='#F0F0F0' , width=35, relief=FLAT, insertbackground=fg_color)
    product_code_input.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    pd_frame.grid(row=4, column=1, sticky='w', padx=5, pady=5)

    product_description_label = Label(enter_pw, text="Enter Product Description\n (max characters 150)", font=font_3, fg=fg_color, bg="white",anchor='w')
    product_description_label.grid(row=5, column=0, sticky='w', padx=5, pady=5)

    pdd_frame = Frame(enter_pw, bg=button_bg)
    product_description_input = Entry(pdd_frame,  font=font_3, fg=fg_color , bg='#F0F0F0' , width=68, relief=FLAT, insertbackground=fg_color)
    product_description_input.grid(row=0, column=0,  sticky='w', padx=1, pady=1)
    pdd_frame.grid(row=6, column=0, columnspan=2, sticky='w', padx=5, pady=5)

    clear_entries =Button(enter_pw, text="Clear Entries", fg=button_fg, bg=button_bg, font = font_5, width=30, anchor='w', command=clearentries, relief=FLAT,activebackground=activeBGC, activeforeground=activeFGC)
    clear_entries.grid(row=7, column=0, sticky='w',  padx=5, pady=4)

    save_entry =Button(enter_pw, text="Save Product", fg=button_fg, bg=button_bg, font=font_5, width=30, anchor='w', command=save_product, relief=FLAT,activebackground=activeBGC, activeforeground=activeFGC)
    save_entry.grid(row=8, column=0, sticky='w', padx=5)


    
def update_in():
    global update_name_input
    global update_quantity_input
    global update_uniteprice_input
    global update_code_input
    global update_description_input
    global update_pw
    items = []
    
    for index in reversed(inventory_list.curselection()):
        items.append(index)
    
    if(len(items) > 1):
        messagebox.showwarning(title="Warning", message="You can only update item at a time")
    elif(len(items) == 0):
        messagebox.showerror(title="Error", message="Ensure that an entry has been selected")
    
    else:
        touse = items[0]
        update_id = cursordataid[touse]
        inventory = sqlite3.connect("Data/main.db")
        product_infor = inventory.cursor()
        product_infor.execute(f"SELECT  rowid, * FROM inventory  WHERE rowid = {update_id}")
        return_products = product_infor.fetchall()

       
        
        
        update_pw = Toplevel()
        update_pw.wm_attributes("-topmost", 1)
        update_pw.focus_force()
        update_pw.title(default_titlle)
        update_pw.geometry("630x500")
        windowWidth = update_pw.winfo_reqwidth()
        windowHeight = update_pw.winfo_reqheight()
        positionRight = int(update_pw.winfo_screenwidth()/2 - windowWidth * 1.5)
        positionDown = int(update_pw.winfo_screenheight()/2 - windowHeight *  1.4)
        update_pw.geometry("+{}+{}".format(positionRight, positionDown))
        update_pw.resizable(0,0)
        

        background_i = Label(update_pw, bg="white")
        background_i.place(x=0, y=0, relheight=1, relwidth=1)
        
        enter_title = Label(update_pw, text="Update Item", font=font_4, fg=fg_color, bg="white", anchor='w')
        enter_title.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        update_name_label = Label(update_pw, text="Enter Product Name", font=font_3, fg=fg_color, bg="white",anchor='w')
        update_name_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)

        upn_frame = Frame(update_pw, bg=button_bg)
        update_name_input = Entry(upn_frame, font=font_3, fg=fg_color , bg='#F0F0F0' , width=35, relief=FLAT, insertbackground=fg_color)
        update_name_input.grid(row=0, column=0, sticky='w', padx=1, pady=1)
        update_name_input.insert(0, return_products[0][1])
        upn_frame.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        update_quantity_label = Label(update_pw, text="Enter Product Quantity", font=font_3, fg=fg_color, bg="white",anchor='w')
        update_quantity_label.grid(row=2, column=0, sticky='w', padx=5, pady=5)

        updq_frame = Frame(update_pw, bg=button_bg)
        update_quantity_input = Entry(updq_frame, font=font_3, fg=fg_color , bg='#F0F0F0' , width=35, relief=FLAT, insertbackground=fg_color)
        update_quantity_input.grid(row=0, column=0, sticky='w', padx=1, pady=1)
        update_quantity_input.insert(0, return_products[0][2])
        updq_frame.grid(row=2, column=1, sticky='w', padx=5, pady=5)


        update_uniteprice_label = Label(update_pw, text="Enter Product Unit Price", font=font_3, fg=fg_color, bg="white",anchor='w')
        update_uniteprice_label.grid(row=3, column=0, sticky='w', padx=5, pady=5)
       


        updu_frame = Frame(update_pw, bg=button_bg)
        update_uniteprice_input = Entry(updu_frame, font=font_3, fg=fg_color , bg='#F0F0F0' , width=35, relief=FLAT, insertbackground=fg_color)
        update_uniteprice_input.grid(row=0, column=0, sticky='w', padx=1, pady=1)
        update_uniteprice_input.insert(0, return_products[0][3])
        updu_frame.grid(row=3, column=1, sticky='w', padx=5, pady=5)


        update_code = Button(update_pw, text="Generate Product Code", font=font_5, bg=button_bg, fg=button_fg, command=generate_code2, relief=FLAT,activebackground=activeBGC, activeforeground=activeFGC)
        update_code.grid(row=4, column=0, sticky='w', padx=5, pady=5)

        updc_frame = Frame(update_pw, bg=button_bg)
        update_code_input = Entry(updc_frame, font=font_3, fg=fg_color , bg='#F0F0F0' , width=35, relief=FLAT, insertbackground=fg_color)
        update_code_input.grid(row=0, column=0, sticky='w', padx=1, pady=1)
        update_code_input.insert(0, return_products[0][4])
        updc_frame.grid(row=4, column=1, sticky='w', padx=5, pady=5)

        update_description_label = Label(update_pw, text="Enter Product Description\n (max characters 150)", font=font_3, fg=fg_color, bg="white",anchor='w')
        update_description_label.grid(row=5, column=0, sticky='w', padx=5, pady=5)

        udpdate_descrip_frame = Frame(update_pw, bg=button_bg)
        update_description_input = Entry(udpdate_descrip_frame, font=font_3, fg=fg_color , bg='#F0F0F0' , width=68, relief=FLAT, insertbackground=fg_color)
        update_description_input.grid(row=0, column=0, sticky='w', padx=1, pady=1)
        update_description_input.insert(0, return_products[0][5])
        udpdate_descrip_frame.grid(row=6, column=0, columnspan=2, sticky='w', padx=5, pady=5)

        clear_update_entries =Button(update_pw, text="Clear Entries", fg=button_fg, bg=button_bg, relief=FLAT,font = font_5, width=30, anchor='w', command=clearupdate_entries,activebackground=activeBGC, activeforeground=activeFGC)
        clear_update_entries.grid(row=7, column=0, sticky='w',  padx=5, pady=4)

        save_update_entry =Button(update_pw, text="Update Product", relief=FLAT,fg=button_fg, bg=button_bg, font=font_5, width=30, anchor='w', command=update_product,activebackground=activeBGC, activeforeground=activeFGC)
        save_update_entry.grid(row=8, column=0, sticky='w', padx=5)

        

def delete_items():
    response = messagebox.askquestion(title="Warning" ,message="Are you sure you want to delete items")
    deleteid = 0
   
    if response == "yes":
        for index in reversed(inventory_list.curselection()):
            deleteid = cursordataid[int(index)]
            deleteitem = database_conn1.cursor()
            deleteitem.execute(f"DELETE FROM inventory  WHERE rowid = {deleteid}")
            inventory_list.delete(index)
            cursordataid.pop(index)
            database_conn1.commit()
            print("Done")
        

def searchFunction2(return_products):
    count = 0
    inventory_list.delete(0,END)
    for product_in in return_products:
        cursordataid.clear()
        cursordataid[count] = product_in[0]
        count += 1
        
        product_deatils = f"Product Name: {product_in[1]} /// Product Code{product_in[4]} /// Product Quantity:{product_in[2]} /// Product Unit Price:{product_in[3]} /// Product Description:{product_in[5]}"
        inventory_list.insert(int(product_in[0]), product_deatils) 
        print(cursordataid)

def  search_rec():
    filt1 = filter_by_entryI.get()
    filt2 = filt1.lower()
    searche = value_entry.get()
    

    if(len(filt2) < 1 or len(searche) < 1):
        messagebox.showwarning(title="Warning", message="Ensure both \"Filter By\" and \" Search Entry\" are not empty")
    
    else:
        if(filt2 == 'pc'):
            searchparam = int(searche)
            filters = database_conn1.cursor()
            filters.execute(f"SELECT rowid, * FROM inventory WHERE product_code LIKE '%{searchparam}%'")
            result = filters.fetchall()
            searchFunction2(result)
        elif(filt2 == "pn"):
            filters = database_conn1.cursor()
            filters.execute(f"SELECT rowid, * FROM inventory WHERE product_name LIKE '%{searche}%' ")
            result = filters.fetchall()
            searchFunction2(result)
        
        else:
            messagebox.showerror(title="Error", message="The only Filter by parameters allowed are \"Product Code(pc), Product Name(pn)")



def inventoryrecords():
    global information_frame
    global inventory_list
    information_frame.grid_forget()
    information_frame = Frame(main_frame, bg="white")
    header_frame = Frame(information_frame, bg="white")
    header_frame.grid(row=0, column=0, sticky='w', padx=5)
    
    header_text = Label(header_frame, text="Inventory",font = font_1, bg= "White",fg=fg_color, anchor='w')
    header_text.grid(row=0, column=0,sticky='w')

    filter_by = Label(header_frame, text="Filter By(pn,pc)", fg=fg_color, bg="white", font=font_4, anchor='w')
    filter_by.grid(row=1, column=0, sticky='w')
    
    value = Label(header_frame, text="Value", font=font_4, bg="white", fg=fg_color, anchor='w')
    value.grid(row=1, column=1, sticky='w')
    
    filter_by_entry_frame = Frame(header_frame, bg=button_bg)
    filter_by_entry = Entry(filter_by_entry_frame, width=20, font = font_4, relief=FLAT, bd=entry_bd, bg='#F0F0F0', fg=fg_color,  insertbackground=fg_color)
    filter_by_entry.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    filter_by_entry_frame.grid(row=2, column=0, sticky='w')
    
    value_entry_frame = Frame(header_frame, bg=button_bg)
    value_entry = Entry(value_entry_frame, width=20, font = font_4, relief=FLAT, bd=entry_bd, bg='#F0F0F0', fg=fg_color, insertbackground=fg_color)
    value_entry.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    value_entry_frame.grid(row=2, column=1, sticky='w', padx=2)

    search_button = Button(header_frame, text="Search Records", font=font_5, fg=button_fg, bg=button_bg, command=search_rec, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    search_button.grid(row=2, column=2)
    
    refresh_button = Button(header_frame, text="Refresh Records", font=font_5, fg=button_fg, bg=button_bg, command=listdisplay, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    refresh_button.grid(row=2, column=3, padx=1)
    
    inventory_update_buttons = Frame(header_frame)
    inventory_update_buttons.grid(row=3, column=0, columnspan=3, sticky='w', pady=1)
    
    enter_item = Button(inventory_update_buttons, text="Enter Item", bg=button_bg, fg=button_fg, width=20, font=font_5, command=enter_product, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    enter_item.grid(row=3, column=0)
    
    update_inventory = Button(inventory_update_buttons, text="Update Item", bg=button_bg, fg=button_fg, width=20, font=font_5, command=update_in, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    update_inventory.grid(row=3, column=1, padx=1)
    
    delete_item = Button(inventory_update_buttons, text="Delete Items", bg=button_bg, fg=button_fg, width=20, font=font_5, command=delete_items, relief=FLAT)
    delete_item.grid(row=3, column=2)
    


    inventory_data = Frame(information_frame, bg=button_bg)
    

    

    inventory_list = Listbox(inventory_data, width=116, height=20,  selectmode=MULTIPLE, font=font_5, fg=fg_color,  xscrollcommand = True, relief=FLAT)
    inventory_list.grid(row=0, column=0, padx=1, pady=1)

    listdisplay()
 

    

    
    inventory_data.grid(row=1, column=0, sticky='w', padx=5)

    information_frame.grid(row=0, column=1, rowspan=5)

def salesRecordList():
    saleListBox.delete(0,END)
    sellsDataId.clear()
    countSales = 0
    getSalesData = database_conn1.cursor()
    getSalesData.execute("SELECT rowid, * FROM sells ")
    salesData = getSalesData.fetchall()

    for item in salesData:
        sellsDataId[countSales] = item[0]
        displaySale = f"Product Name: {item[1]} /// Product Code: {item[2]} /// Product Unit Price: {item[3]} /// Quantity: {item[4]} /// Amount: {item[5]} /// Date Sold: {item[6]}"
        saleListBox.insert(int(countSales), displaySale)
        countSales += 1


def refreshSaleRecords():
    salesRecordList()

def searchFunction(resultList):
    saleListBox.delete(0,END)
    salesDataList.clear()
    countSales = 0
    for item in resultList:
        sellsDataId.clear()
        sellsDataId[countSales] = item[0]
        displaySale = f"Product Name: {item[1]} /// Product Code: {item[2]} /// Product Unit Price: {item[3]} /// Quantity: {item[4]} /// Amount: {item[5]} /// Date Sold: {item[6]}"
        saleListBox.insert(int(countSales), displaySale)
        countSales += 1


def searchSellsRecords():
    filt1 = filterByEntry.get()
    filt2 = filt1.lower()
    searche = searchByEntry.get()
    

    if(len(filt2) < 1 or len(searche) < 1):
        messagebox.showwarning(title="Warning", message="Ensure both \"Filter By\" and \" Search Entry\" are not empty")
    
    else:
        if(filt2 == 'pc'):
            searchparam = int(searche)
            filters = database_conn1.cursor()
            filters.execute(f"SELECT rowid, * FROM sells WHERE product_code LIKE '%{searchparam}%'")
            result = filters.fetchall()
            searchFunction(result)
        elif(filt2 == "pn"):
            filters = database_conn1.cursor()
            filters.execute(f"SELECT rowid, * FROM sells WHERE product_name LIKE '%{searche}%' ")
            result = filters.fetchall()
            searchFunction(result)
        elif(filt2 == "dos"):
            filters = database_conn1.cursor()
            filters.execute(f"SELECT rowid, * FROM sells WHERE dateof_sale LIKE '%{searche}%' ")
            result = filters.fetchall()
            searchFunction(result)
        else:
            messagebox.showerror(title="Error", message="The only Filter by parameters allowed are \"Product Code(pc), Product Name(pn) and Date Of Sell(dos)\"")

def deleteSaleRecords():
    items = saleListBox.curselection()
    if len(items) > 0:
        for index in reversed(saleListBox.curselection()):
            deleteSells = database_conn1.cursor()
            entryid = sellsDataId[index]
            deleteSells.execute(f"DELETE  FROM sells WHERE rowid = '{entryid}'")
            saleListBox.delete(index)
            sellsDataId.pop(index)
            database_conn1.commit()
    else:
        messagebox.showwarning(title="Warning", message="No items where selected for deletion")


def loadSellsData():
    entry_1 = dateFilterByE.get()
    entry_2 = dateFilterByE2.get()
    entry_3 = dateFilterByECode.get()
    inventoryList = []
    datecodes = []
    storedData = database_conn1.cursor()
    storedData.execute("SELECT rowid, * FROM sells")
    listData = storedData.fetchall()

    for code in listData:
        if code[2]  in inventoryList:
            pass
        else:
            inventoryList.append(code[2])
    
   
    

    if (len(entry_1) < 1 and len(entry_2) < 1 and len(entry_3) < 1):
        total = 0
        count = 0
        amountSold = 0
        listsData = 0
        saleListBox.delete(0,END)
        for code in inventoryList:
            codeData = database_conn1.cursor()
            codeData.execute(f"SELECT rowid, * FROM sells WHERE product_code = '{code}'")
            sellsData = codeData.fetchall()
            for amount in sellsData:
                total += amount[5]
                amountSold += amount[4]
                count += 1
            displaySale = f"Product Name: {amount[1]} /// Product Code: {amount[2]} /// Product Unit Price: {amount[3]} /// Quantity: {amountSold } /// Amount:{setCurrency}{total}"
            saleListBox.insert(int(listsData), displaySale) 
            listsData += 1
            total = 0
            count = 0
            amountSold = 0
    elif(len(entry_1) > 1):
        saleListBox.delete(0,END)
        if(len(entry_2) < 1 and len(entry_3) < 1):
            total = 0
            count = 0
            amountSold = 0
            listsData = 0
            filterDate = database_conn1.cursor()
            for code in inventoryList:
                filterDate.execute(f"SELECT rowid, * FROM sells WHERE product_code = '{code}' AND  dateof_sale = '{entry_1}'")
                dateData = filterDate.fetchall()
               
               
                if code not in datecodes and len(dateData)> 0:
                    datecodes.append(code)
                
                    for amount in dateData:
                        total += amount[5]
                        amountSold += amount[4]
                        count += 1
                    displaySale = f"Product Name: {amount[1]} /// Product Code: {amount[2]} /// Product Unit Price: {amount[3]} /// Quantity: {amountSold } /// Amount:{setCurrency}{total}"
                    saleListBox.insert(int(listsData), displaySale) 
                    listsData += 1
                    total = 0
                    count = 0
                    amountSold = 0
        elif len(entry_2)> 1 and len(entry_3) > 1:
            date_1 = datetime.datetime.strptime(entry_1, '%m/%d/%y')
            date_2 = datetime.datetime.strptime(entry_2, '%m/%d/%y')
            working_date = date_1 - date_2
            num_days = int(working_date.days)
            
            if int(entry_3) in inventoryList:
                for cday in range(num_days):
                    day = datetime.timedelta(days=cday)
                    result = date_2 + day 
                    thdate = result.strftime('%D')
                    num_days -= 1
                    thsells = database_conn1.cursor()
                    thsells.execute(f"SELECT * FROM sells WHERE product_code = '{entry_3}' AND  dateof_sale = '{str(thdate)}'")
                    sellsd = thsells.fetchall() 
                    if len(sellsd) > 0:
                        for itemdata in sellsd:
                            amount_sold = itemdata[3]
                            price = itemdata[4]
                            total += price
                            amountSold += amount_sold
                            
                        displaySale = f"Product Name: { itemdata[1]} /// Product Code: { itemdata[2]} /// Product Unit Price: { itemdata[3]} /// Quantity: {amountSold } /// Amount:{setCurrency}{total} /// Date: {itemdata[5]}"
                        saleListBox.insert(int(count), displaySale) 
                        
                        total = 0
                        amountSold = 0
                        count = + 1
                    total = 0
                    amountSold = 0
                    count = 0

            else:
                messagebox.showwarning(title="Warning", message=f"No product with item code \"{entry_3}\"")
            
            
            
            
            
        elif len(entry_2)<1 and len(entry_3)>1:
            total = 0
            count = 0
            amountSold = 0
            listsData = 0
            filterDate = database_conn1.cursor()
            filterDate.execute(f"SELECT rowid, * FROM sells WHERE product_code = '{entry_3}' AND  dateof_sale = '{entry_1}'")
            dateData = filterDate.fetchall()
            for items in dateData:
                total += items[5]
                amountSold += items[4]
                data = items
     
            displaySale = f"Product Name: {data[1]} /// Product Code: {data[2]} /// Product Unit Price: {data[3]} /// Quantity: {amountSold } /// Amount:{setCurrency}{total}"
            saleListBox.insert(int(listsData), displaySale) 
            total = 0
            amountSold = 0
        
        elif len(entry_2) > 1 and len(entry_3) <1:
            total = 0
            amountSold = 0
            count = + 1
            date_1 = datetime.datetime.strptime(entry_1, '%m/%d/%y')
            date_2 = datetime.datetime.strptime(entry_2, '%m/%d/%y')
            working_date = date_1 - date_2
            num_days = int(working_date.days)
            
            
            for cday in range(num_days):
                day = datetime.timedelta(days=cday)
                result = date_2 + day 
                thdate = result.strftime('%D')
                num_days -= 1
                for code in inventoryList:
                    thsells = database_conn1.cursor()
                    thsells.execute(f"SELECT * FROM sells WHERE product_code = '{code}' AND  dateof_sale = '{str(thdate)}'")
                    sellsd = thsells.fetchall() 
                    if len(sellsd) > 0:
                        for itemdata in sellsd:
                            amount_sold = itemdata[3]
                            price = itemdata[4]
                            total += price
                            amountSold += amount_sold
                            
                        displaySale = f"Product Name: { itemdata[0]} /// Product Code: { itemdata[1]} /// Product Unit Price: { itemdata[2]} /// Quantity: {amountSold } /// Amount:{setCurrency}{total} /// Date: {itemdata[5]}"
                        saleListBox.insert(int(count), displaySale) 
                        total = 0
                        amountSold = 0
                        count = + 1
                    total = 0
                    amountSold = 0
                    count = 0

               

def filterSells():
    global dateFilterByE
    global dateFilterByE2
    global dateFilterByECode
    filterSells = Toplevel()
    filterSells.title("Create New User")
    filterSells.wm_attributes("-topmost", 1)
    filterSells.focus_force()
    filterSells.geometry("400x270")
    windowWidth = filterSells.winfo_reqwidth()
    windowHeight = filterSells.winfo_reqheight()
    positionRight = int(filterSells.winfo_screenwidth()/2 - windowWidth * 1)
    positionDown = int(filterSells.winfo_screenheight()/2 - windowHeight *  1)
    filterSells.geometry("+{}+{}".format(positionRight, positionDown))
    filterSells.resizable(0,0)
    background_i = Label(filterSells, bg="white")
    background_i.place(x=0, y=0, relheight=1, relwidth=1)

    filterSell = Frame(filterSells, bg="white")
    filterSell.grid(row=0, column=0, padx=5)
    filterSellsH = Label(filterSell, text="Fillter Selss", font=font_2, fg=fg_color, anchor='w', bg="white")
    filterSellsH.grid(row=0, column=0, sticky='w')
    dateFilterBy = Label(filterSell, text="Filter by Time \"Point 1\" Date", font=font_5, fg=fg_color, anchor='w' , bg="white")
    dateFilterBy.grid(row=1, column=0, sticky='w', pady=2)

    sell1_frame = Frame(filterSell, bg=button_bg)
    dateFilterByE = Entry(sell1_frame, font=font_5, fg=fg_color, width=35, bg='#F0F0F0', insertbackground=fg_color, relief=FLAT)
    dateFilterByE.grid(row=0, column=0, sticky='w', pady=1, padx=1)
    sell1_frame.grid(row=2, column=0, sticky='w', pady=2)


    
    dateFilterBy2 = Label(filterSell, text="Filter by Time \"Point 2\" Date", font=font_5, fg=fg_color, anchor='w', bg="white" )
    dateFilterBy2.grid(row=3, column=0, sticky='w', pady=2)

    sell2_frame = Frame(filterSell, bg=button_bg)
    dateFilterByE2 = Entry(sell2_frame,font=font_5, fg=fg_color, width=35, bg='#F0F0F0', insertbackground=fg_color, relief=FLAT)
    dateFilterByE2.grid(row=0, column=0, sticky='w', pady=1, padx=1)
    sell2_frame.grid(row=4, column=0, sticky='w', pady=2)


    dateFilterByCode = Label(filterSell, text="Product Code", font=font_5, fg=fg_color, anchor='w', bg="white" )
    dateFilterByCode.grid(row=5, column=0, sticky='w', pady=2)

    sell3_frame = Frame(filterSell, bg=button_bg)
    dateFilterByECode = Entry(sell3_frame, font=font_5, fg=fg_color, width=35, bg='#F0F0F0', insertbackground=fg_color, relief=FLAT)
    dateFilterByECode.grid(row=0, column=0, sticky='w', pady=1, padx=1)
    sell3_frame.grid(row=6, column=0, sticky='w', pady=2)


    loadSells = Button(filterSell, text="Load Sells", relief=FLAT,fg=button_fg, bg=button_bg, anchor='w', command=loadSellsData, font=font_6)
    loadSells.grid(row=7, column=0, sticky='w', pady=2)


def salesrecord(): 
    global information_frame
    global saleListBox
    global filterByEntry
    global searchByEntry
    information_frame.grid_forget()
    
    information_frame = Frame(main_frame, bg='white')
    information_frame.grid(row=0, column=1, rowspan=5, padx=5)
    
    salesRecordLabel = Label(information_frame, text="Sales Records", bg='white', font=font_1,anchor='w', fg=fg_color)
    salesRecordLabel.grid(row=0, column=0, columnspan=1, sticky='w')

    salesInformationFrame = Frame(information_frame, bg='white')
    salesInformationFrame.grid(row=1, column=0, sticky='w', columnspan=1)

    filterByLable = Label(salesInformationFrame, text="Filter By (pc, pn, dos)", fg=fg_color, font=font_4, anchor='w', bg='white')
    filterByLable.grid(row=0, column=0, sticky='w', columnspan=2)

    f1_frame = Frame(salesInformationFrame, bg=button_bg)
    filterByEntry = Entry(f1_frame, width = 20,font = font_4, relief=FLAT,  bg='#F0F0F0', fg=fg_color, insertbackground=fg_color)
    filterByEntry.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    f1_frame.grid(row=1, column=0, sticky='w')

    searchByLable = Label (salesInformationFrame, text="Search Entry", fg=fg_color, font=font_4, anchor='w', bg='white')
    searchByLable.grid(row=0, column=1, sticky='w')

    f2_frame = Frame(salesInformationFrame, bg=button_bg)
    searchByEntry = Entry(f2_frame, width = 20,font = font_4, relief=FLAT,  bg='#F0F0F0', fg=fg_color, insertbackground=fg_color)
    searchByEntry.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    f2_frame.grid(row=1, column=1, sticky='w', padx=2)

    searchByButton = Button (salesInformationFrame, text ="Search Records", font=font_5, fg=button_fg, bg=button_bg,command=searchSellsRecords, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    searchByButton.grid(row=1, column=2, sticky='w')

    refreshRecButton = Button (salesInformationFrame, text ="Refresh Records", font=font_5, fg=button_fg, bg=button_bg, command=salesRecordList, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    refreshRecButton.grid(row=1, column=3, sticky='w', padx=1)

    deleteRecButton = Button (salesInformationFrame, text ="Delete Items", font=font_5, fg=button_fg, bg=button_bg,command=deleteSaleRecords, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    deleteRecButton.grid(row=1, column=4, sticky='w')
    filterSalesFrame = Frame(salesInformationFrame, bg="white")
    totalDailySells = Button(filterSalesFrame , text ="Filter Sells", font=font_5, fg=button_fg, bg=button_bg,command=filterSells, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    totalDailySells.grid(row=0, column=0, sticky='w')
    
    
    filterSalesFrame.grid(row=3, column=0, sticky='w', columnspan=4, pady=1)
    salesList = Frame(information_frame, bg=button_bg)
    salesList.grid(row=2, column=0,  sticky='w')

    saleListBox = Listbox(salesList, width=116, height=20,  selectmode=MULTIPLE, font=font_5, fg=fg_color,  xscrollcommand = True, relief=FLAT)
    saleListBox.grid(row=0, column=0, sticky='w',  pady=1, padx=1)

    salesRecordList()

def createUserFun():
    createUser.wm_attributes("-topmost", 0)
    def saveUserFun(uname, upassword, auth):
        
        passworden = encryptPassword(upassword)
        data = [uname, passworden, auth] 
        string = "INSERT INTO userdata(user_name, user_password, user_auth) VALUES(?,?,?)"
        saveUser = database_conn2.cursor()
        saveUser.execute(string, data)
        database_conn2.commit()
        showUserData(1)

    
    name =  userNameEntry.get()
    password =  userPasswordOneEntry.get()
    confirm =  userPasswordConfirmEntry.get()
    auth =  x.get()
    
    if len(name) < 1 or len(password) < 1:
        messagebox.showwarning(title="Warning", message="Ensure both \"User Name\" and \"Password\" fields are not empty")
        createUser.focus_force()
        createUser.wm_attributes("-topmost", 1)
    else:
        if str(password) != str(confirm):
            messagebox.showerror(title="Error", message="Password and Confirm Password  do not match")
            createUser.focus_force()
            createUser.wm_attributes("-topmost", 1)
        else:
            if auth == 1:
                saveUserFun(name, password, 1)
                
            else:
                saveUserFun(name, password, 0)


def updateUserFun():
    
    user = currentUserList.curselection()
    prP = previousPasswordE.get()
    upN = updateNameEntry.get()
    upP1 = updatePasswordOneEntry.get()
    upP2 = updatePasswordConfirmEntry.get()
    auth  = up.get()
    toUse = userUpdataData[user[0]]
    print(toUse)
    print(userUpdataData)
    updateUser.wm_attributes("-topmost", 0)
    
    
    def save(name, password, auth, ids):
        
        passw = encryptPassword(password)
        updateUser = database_conn2.cursor()
        updateUser.execute(f"DELETE FROM userdata WHERE rowid = {ids}")
        database_conn2.commit()
        data = [name , passw, auth]
        string = "INSERT INTO userdata (user_name, user_password, user_auth) VALUES(?,?,?)"
        updateUser.execute(string, data)
        database_conn2.commit()
        showUserData(2)
        
    getUser = database_conn2.cursor()
    getUser.execute(f"SELECT * FROM userdata WHERE rowid  = '{toUse}'")
    getUserD = getUser.fetchall()
    
    decodeP = getUserD[0][1]
   
    
    passworden = decrypt_password(decodeP)
    

    check = [prP, upN, upP1, upP2]
    for i in check:
        if len(i) < 1:
            messagebox.showwarning(title="Warning", message="Ensure all fileds are occupied")
            updateUser.focus_force()
            updateUser.wm_attributes("-topmost", 0)
            break
        else:
            if passworden != prP:
                messagebox.showerror(title="Error", message="Previous password is incorrect")
                updateUser.focus_force()
                updateUser.wm_attributes("-topmost", 0)
                break
            else:
                if upP1 != upP2:
                    messagebox.showwarning(title="Warning", message="New password and  Confirm password do not match")
                    updateUser.focus_force()
                    updateUser.wm_attributes("-topmost", 0)
                    break
                else:
                    if auth == 1:
                        save(upN, upP1, auth, toUse)
                    else:
                        save(upN,upP1, auth,toUse)

    
def deleteUserFun():
    createUser.wm_attributes("-topmost", 0)
    selected = currentUserListA.curselection()
    if len(selected) < 1:
        messagebox.showerror(title="Error", message="No items selected for deletion")
        createUser.focus_force()
        createUser.wm_attributes("-topmost", 1)
    else:
        deleteUser = database_conn2.cursor()
        for i in reversed(currentUserListA.curselection()):
            userId = userUserData[i]
            deleteUser.execute(f"DELETE  FROM userdata WHERE rowid = '{userId}'")
            database_conn2.commit()
            showUserData(1)
        
   

def showUserUpdata():
    user = currentUserList.curselection()
    if len(user) < 1:
        messagebox.showwarning(title="Warning", message="No user data selected to update")
    else:
        toUse = userUpdataData[user[0]]
        getUser = database_conn2.cursor()
        getUser.execute(f"SELECT * FROM userdata WHERE rowid = '{toUse}'")
        data = getUser.fetchall()
        auth = data[0][2]
        updateNameEntry.insert(0, data[0][0])
        if auth == 1:
            updateadminConfirm.select()
        

        
def showUserData(user):
    count = 0
   
    userUpdataData.clear()
    userUserData.clear()
    usersData = database_conn2.cursor()
    usersData.execute("SELECT rowid, * FROM userdata")
    userInfor = usersData.fetchall()

    if user == 2:
        currentUserList.delete(0, END)
    elif user == 1:
        currentUserListA.delete(0,END)

    for infor in userInfor:
        auth = ""
        if infor[3] == 1: 
            auth = "Administrator"
        else:
            auth = "Limited"
        userdata = f"User Name: {infor[1]} /// User Auth: {auth}"
        if user == 2:
            
            currentUserList.insert(int(count), userdata)
            userUpdataData[count] = int(infor[0])
            
            count += 1
            
        elif user == 1:
            currentUserListA.insert(int(count), userdata)
            userUserData[count] = int(infor[0])
            count += 1
   

    # currentUserList

# SETTINGS FUNCTIONS START

def createUserData():
    global userNameEntry
    global userPasswordOneEntry
    global userPasswordConfirmEntry
    global adminConfirm
    global x
    global currentUserListA
    global createUser
    createUser = Toplevel()
    createUser.wm_attributes("-topmost", 1)
    createUser.focus_force()
    createUser.title("Create New User")
    createUser.geometry("630x500")
    windowWidth = createUser.winfo_reqwidth()
    windowHeight = createUser.winfo_reqheight()
    positionRight = int(createUser.winfo_screenwidth()/2 - windowWidth * 1.5)
    positionDown = int(createUser.winfo_screenheight()/2 - windowHeight *  1.4)
    createUser.geometry("+{}+{}".format(positionRight, positionDown))
    createUser.resizable(0,0)
    x = IntVar(0)

    background_i = Label(createUser, bg="white")
    background_i.place(x=0, y=0, relheight=1, relwidth=1)

    userCreateTitle = Label(createUser, text="Create User", font=font_4, fg=fg_color, bg="white", anchor='w')
    userCreateTitle.grid(row=0, column=0, sticky='w', padx=5)

    userNameLabel = Label(createUser, text="User Name", font=font_3, fg=fg_color, bg="white", anchor='w')
    userNameLabel.grid(row=1, column=0, sticky='w', padx=5)

    f1_frame = Frame(createUser, bg=button_bg)
    userNameEntry = Entry(f1_frame,  font=font_3, width=35, fg=fg_color, relief=FLAT, bg='#F0F0F0', insertbackground=fg_color)
    userNameEntry.grid(row=0, column=0, padx=1, pady=1)
    f1_frame.grid(row=1, column=1, padx=5, pady=5)

    userPasswordOneLabel = Label(createUser, text="Password", fg=fg_color, bg="white", font=font_3, anchor='w')
    userPasswordOneLabel.grid(row=2, column=0, sticky='w', padx=5, pady=5)

    f2_frame = Frame(createUser, bg=button_bg)
    userPasswordOneEntry = Entry(f2_frame, width=35, font=font_3, show="*", fg=fg_color, relief=FLAT,bg='#F0F0F0', insertbackground=fg_color)
    userPasswordOneEntry.grid(row=0, column=0, padx=1, pady=1)
    f2_frame.grid(row=2, column=1, padx=5, pady=5)

    userPasswordConfirmLabel = Label(createUser, text="Confirm Password", fg=fg_color, bg="white", font=font_3, anchor='w')
    userPasswordConfirmLabel.grid(row=3, column=0, sticky='w', padx=5, pady=5)

    f3_frame = Frame(createUser, bg=button_bg)
    userPasswordConfirmEntry = Entry(f3_frame, width=35, font=font_3, show="*", fg=fg_color, relief=FLAT,bg='#F0F0F0', insertbackground=fg_color)
    userPasswordConfirmEntry.grid(row=0, column=0, padx=1, pady=1)
    f3_frame.grid(row=3, column=1, padx=5, pady=5)


    adminConfirmLabel = Label(createUser, text="Admin",fg=fg_color, bg="white", font=font_3, anchor='w')
    adminConfirmLabel.grid(row=4, column=0, sticky='w', padx=5, pady=5)
    adminConfirm = Checkbutton(createUser, bg="white",variable= x,onvalue= 1, offvalue=0, fg=fg_color)
    adminConfirm.grid(row=4, column = 1, sticky='w', padx=5, pady=5)

    submitUserData = Button(createUser, text = "Save", fg=button_fg, bg=button_bg, width=20, anchor='w', font=font_5, command=createUserFun, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    submitUserData.grid(row=5, column=0, sticky='w', padx=5, pady=5)

    submitUserData = Button(createUser, text = "Delete User", fg=button_fg, bg=button_bg, width=20, anchor='w', font=font_5, command=deleteUserFun, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    submitUserData.grid(row=5, column=1, sticky='w', padx=5, pady=5)


    currentUserData = Label(createUser, text = "User Data", fg=fg_color, bg="white", font=font_4, anchor='w')
    currentUserData.grid(row=6, column=0, sticky='w', padx=5)

    f4_frame = Frame(createUser, bg=button_bg)
    currentUserListA = Listbox(f4_frame,  width=68, height=13, fg=fg_color, font=font_5, selectmode=MULTIPLE, relief=FLAT)
    currentUserListA.grid(row=0, column=0,  padx=1, pady=1)
    f4_frame.grid(row=7, column=0, columnspan=2, padx=5)
    showUserData(1)




def updateUserData():
    global previousPasswordE
    global updateNameEntry
    global updatePasswordOneEntry
    global updatePasswordConfirmEntry
    global currentUserList
    global updateadminConfirm
    global up
    global updateUser
    updateUser = Toplevel()
    updateUser.wm_attributes("-topmost", 1)
    updateUser.focus_force()
    updateUser.title("Create New User")
    updateUser.geometry("630x500")
    windowWidth = updateUser.winfo_reqwidth()
    windowHeight = updateUser.winfo_reqheight()
    positionRight = int(updateUser.winfo_screenwidth()/2 - windowWidth * 1.5)
    positionDown = int(updateUser.winfo_screenheight()/2 - windowHeight *  1.4)
    updateUser.geometry("+{}+{}".format(positionRight, positionDown))
    updateUser.resizable(0,0)

    background_i = Label(updateUser, bg="white")
    background_i.place(x=0, y=0, relheight=1, relwidth=1)

    updateCreateTitle = Label(updateUser, text="Update User", font=font_4, fg=fg_color, bg="white", anchor='w')
    updateCreateTitle.grid(row=0, column=0, sticky='w', padx=5)

    updateNameLabel = Label(updateUser, text="User Name", font=font_3, fg=fg_color, bg="white", anchor='w')
    updateNameLabel.grid(row=1, column=0, sticky='w', padx=5)

    f1_frame = Frame(updateUser, bg=button_bg)
    updateNameEntry = Entry(f1_frame,  font=font_3, width=35, fg=fg_color, bg='#F0F0F0', insertbackground=fg_color, relief=FLAT)
    updateNameEntry.grid(row=0, column=0, padx=1, pady=1)
    f1_frame.grid(row=1, column=1, padx=5, pady=5)

    previousPasswordL = Label(updateUser, text="Enter old password", fg=fg_color, bg="white", font=font_3, anchor='w')
    previousPasswordL.grid(row=2, column=0, sticky='w', padx=5, pady=5)

    f2_frame = Frame(updateUser, bg=button_bg)
    previousPasswordE = Entry(f2_frame, width=35, font=font_3, fg=fg_color, show="*", bg='#F0F0F0', insertbackground=fg_color, relief=FLAT)
    previousPasswordE.grid(row=0, column=0, padx=1, pady=1)
    f2_frame.grid(row=2, column=1, padx=5, pady=5)

    updatePasswordOneLabel = Label(updateUser, text="New password", fg=fg_color, bg="white", font=font_3, anchor='w')
    updatePasswordOneLabel.grid(row=3, column=0, sticky='w', padx=5, pady=5)

    f3_frame = Frame(updateUser, bg=button_bg)
    updatePasswordOneEntry = Entry(f3_frame, width=35, font=font_3, fg=fg_color, show="*", bg='#F0F0F0', insertbackground=fg_color, relief=FLAT)
    updatePasswordOneEntry.grid(row=0, column=0, padx=1, pady=1)
    f3_frame.grid(row=3, column=1, padx=5, pady=5)

    updatePasswordConfirmLabel = Label(updateUser, text="Confirm Password", fg=fg_color, bg="white", font=font_3, anchor='w')
    updatePasswordConfirmLabel.grid(row=4, column=0, sticky='w', padx=5, pady=5)

    f4_frame = Frame(updateUser, bg=button_bg)
    updatePasswordConfirmEntry = Entry(f4_frame, width=35, font=font_3, fg=fg_color, show="*", bg='#F0F0F0', insertbackground=fg_color, relief=FLAT)
    updatePasswordConfirmEntry.grid(row=0, column=0, padx=1, pady=1)
    f4_frame.grid(row=4, column=1, padx=5, pady=5)

    adminConfirmLabel = Label(updateUser, text="Admin",fg=fg_color, bg="white", font=font_3, anchor='w')
    adminConfirmLabel.grid(row=5, column=0, sticky='w', padx=5, pady=5)

    up = IntVar(0)
    updateadminConfirm = Checkbutton(updateUser, bg="white", variable = up, onvalue = 1,offvalue=0 , fg=fg_color)
    updateadminConfirm.grid(row=5, column = 1, sticky='w', padx=5, pady=5)
    updateUserData = Button(updateUser, text = "Save", fg=button_fg, relief=FLAT,bg=button_bg, width=20, anchor='w', font=font_5, command=updateUserFun)
    updateUserData.grid(row=6, column=0, sticky='w', padx=5, pady=5)
    currentUserData = Label(updateUser, text = "User Data", fg=fg_color, bg="white", font=font_4, anchor='w')
    currentUserData.grid(row=7, column=0, sticky='w', padx=5)

    f5_frame = Frame(updateUser, bg=button_bg)
    currentUserList = Listbox(f5_frame, width=68, height=9, fg=fg_color, font=font_5, relief=FLAT)
    currentUserList.grid(row=0, column=0, padx=1, pady=1)
    f5_frame.grid(row=8, column=0, columnspan=2, padx=5)
    updateUserSelector = Button(updateUser, text = "Update Selected User", fg=button_fg, bg=button_bg, font=font_5, anchor='w', command=showUserUpdata, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    updateUserSelector.grid(row=9, column=0, sticky='w', padx=5,pady=5)
    showUserData(2)




    
def storeDataFun():
    global setCurrency
    global storeName
    storename = changeStoreEntry.get()
    currency = currencyE.get()
    check = database_conn2.cursor()
    if len(storename) < 1 and len(currency) < 1:
        messagebox.showwarning(title="Warning", message="Ensure \" Store Name\" and \"Currency\" fields are not empty")


    elif len(storename) < 1 and len(currency) > 1:
        check.execute(f"UPDATE storedata SET  set_currency = '{currency}'")
        database_conn2.commit()
        setCurrency = currency
        currencyE.delete(0, END)
    
    elif len(storename) > 1 and len(currency) < 1:
        check.execute(f"UPDATE storedata SET store_name = '{storename}'")
        database_conn2.commit()
        storeName = storename
        changeStoreEntry.delete(0, END)
        


    else:
        check.execute(f"UPDATE storedata SET store_name = '{storename}', set_currency = '{currency}'")
        database_conn2.commit()
        storeName = storename
        setCurrency = currency
        changeStoreEntry.delete(0, END)
        currencyE.delete(0, END)
        
    

        

# SETTINGS FUNCTIONS END




def settings():
    def allowdelete():
        global deleteAuth
        deleteA = y.get()
        deleteA = int(deleteA)
        updateda = database_conn3.cursor()
        updateda.execute(f"UPDATE settingd SET settings_value = '{deleteA}' WHERE rowid = 1")

        database_conn3.commit()
        deleteAuth = deleteA
    check_delete_auth = database_conn3.cursor()
    check_delete_auth.execute("SELECT * FROM settingd WHERE rowid = 1")
    result = check_delete_auth.fetchall()
    CDA = result[0][1]


    global information_frame
    global currencyE
    global changeStoreEntry
    information_frame.grid_forget()
    information_frame = Frame(main_frame, bg='white')
    information_frame.grid(row=0, column=1, rowspan=5, padx=5)
    y = IntVar(0)
    settingsLableFrame = Frame(information_frame, bg="white")
    settingsLableFrame.grid(row=0, column=0, sticky='w', ipadx=473 )
    salesRecordLabel = Label(settingsLableFrame, text="Settings", bg='white', font=font_1,anchor='w', fg=fg_color)
    salesRecordLabel.grid(row=0, column=0, columnspan=1, sticky='w')


    settingsFrame = Frame(information_frame, bg='white')
    settingsFrame.grid(row=1, column=0, sticky='w', columnspan=3, ipady=99)
    changeStoreName = Label(settingsFrame, text="Store Settings", fg=fg_color, bg="white", font=font_5, anchor='w')
    changeStoreName.grid(row=0, column=0, sticky='w')
    changeStoreName = Label(settingsFrame, text="Enter Store Name", fg=fg_color, bg="white", font=font_5, anchor='w')
    changeStoreName.grid(row=1, column=0, sticky='w')

    f1_frame =Frame(settingsFrame, bg=button_bg)
    changeStoreEntry = Entry(f1_frame, fg=fg_color, bg='#F0F0F0', font=font_4, width=35, relief=FLAT, insertbackground=fg_color)
    changeStoreEntry.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    f1_frame.grid(row=2, column=0, sticky='w')


    currencyL = Label(settingsFrame, text="Enter Currency", fg=fg_color, bg="white", font=font_5, anchor='w')
    currencyL.grid(row=3, column=0, sticky='w')

    f2_frame = Frame(settingsFrame, bg=button_bg)
    currencyE = Entry(f2_frame, fg=fg_color, bg='#F0F0F0', font=font_4, width=35, relief=FLAT, insertbackground=fg_color)
    currencyE.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    f2_frame.grid(row=4, column=0, sticky='w')

    changeStoreButton = Button(settingsFrame, text="Save", font=font_5, bg=button_bg, fg=button_fg, command=storeDataFun, anchor='w', relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    changeStoreButton.grid(row=5, column=0, sticky='w', pady=1)
   
    allow_delete = Checkbutton(settingsFrame, text="Allow delete of sells in register", variable=y, onvalue=1, offvalue=0,  fg=fg_color, bg="white", font=font_5, anchor='w',  activebackground='white' ,command=allowdelete, activeforeground=fg_color)
    allow_delete.grid(row=6, column=0, sticky='w')
    if CDA == 1:
        allow_delete.select()
    
    changeStoreName = Label(settingsFrame, text="User Settings", fg=fg_color, bg="white", font=font_5, anchor='w')
    changeStoreName.grid(row=7, column=0, sticky='w')

    createNewUser = Button(settingsFrame, text="Users", font=font_5, bg=button_bg, fg=button_fg, width=20, command=createUserData, anchor='w', relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    createNewUser.grid(row=8, column=0, sticky='w', pady=1)

    updateUser = Button(settingsFrame, text="Update User Data", font=font_5, bg=button_bg, fg=button_fg, width=20, command=updateUserData, anchor='w', relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    updateUser.grid(row=9, column=0, sticky='w', pady=1)

   
    


    
# ADMIN FUNCTIONS END
# 
# 
# 
# 

#ADMIN GUI START
def admin_window():
    global admin_main
    global inventory_list
    global information_frame
    global main_frame
    global filter_by_entryI
    global value_entry
    admin_main = Tk()
    admin_main.title("Easy POS")
    admin_main.state('zoomed')
    width = admin_main.winfo_screenwidth()
    height = admin_main.winfo_screenwidth()

    admin_main.geometry("%dx%d" % (width, height))
    
    icon_image = PhotoImage(file ="images/user.png") 
    # images
    background_image = PhotoImage(file = "images/bg_image2.png")
    
    # Code
    label = Label(admin_main, image=background_image, bg="white")
    label.place(x=0, y=0, relwidth=1, relheight=1)
    # STORE NAME FRAME
    store_name_frame = Frame(admin_main, padx=10, bg="white")
    store_name_frame.pack(anchor='w')
    store_name = Label(store_name_frame, text=storeName, font=storeName_font, bg="white", fg=fg_color)
    store_name.pack(side=LEFT)
    # USER LOGED IN DATA FRAME
    user_logged= Frame(admin_main, bg="white", padx=10, pady=10)
    user_logged.pack(anchor='w')
    user_name =  Label(user_logged, text=loggedUser, font=font_1, bg="white", fg=fg_color)
    user_name.grid(row=0, column=0, sticky='w')
    date_time = Label(user_logged, text=f"Date: {dateTime}", bg="white", font = font_2, fg=fg_color)
    date_time.grid(row=1, column=0, sticky='w')
    return_image = PhotoImage(file="images/landing_small.png")
    return_label = Label(user_logged, image=return_image )
    return_label.grid(row=2, column=0, sticky='w')
    return_label.bind("<Button-1>", return_directorad)
    main_frame = Frame(admin_main, bg="white")
    main_frame.pack(anchor='w')



    # DIRECTORY FRAME
    directory_frame = Frame(main_frame, bg='white')
    inventory_button = Button(directory_frame, text="Inventory Records", font = font_5, bg=button_bg, fg=button_fg, width=20, anchor='w', command=inventoryrecords, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    inventory_button.grid(row=0, column=0, sticky='w', ipadx=30)
    sales_button = Button(directory_frame, text="Sales Records", font = font_5, fg=button_fg, bg=button_bg, width=20, anchor='w', command=salesrecord, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    sales_button.grid(row=1, column=0, sticky='w', ipadx=30, pady=1)
    settings_button = Button(directory_frame, text="Settings", font = font_5, fg=button_fg, bg=button_bg, width=20,anchor='w', command = settings, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    settings_button.grid(row=2, column=0, sticky='w', ipadx=30)
    directory_frame.grid(row=0, column=0, sticky='w', padx=10, pady=2)

    # INFORMATION FRAME
    information_frame = Frame(main_frame, bg="white")
    header_frame = Frame(information_frame, bg="white")
    header_frame.grid(row=0, column=0, sticky='w', padx=5)
    
    header_text = Label(header_frame, text="Inventory",font = font_1, bg= "White",fg=fg_color, anchor='w')
    header_text.grid(row=0, column=0,sticky='w')

    filter_by = Label(header_frame, text="Filter By(pn,pc)", fg=fg_color, bg="white", font=font_4, anchor='w')
    filter_by.grid(row=1, column=0, sticky='w')
    
    value = Label(header_frame, text="Value", font=font_4, bg="white", fg=fg_color, anchor='w')
    value.grid(row=1, column=1, sticky='w')
    
    filter_by_entryI_frame = Frame(header_frame, bg=button_bg)
    filter_by_entryI = Entry(filter_by_entryI_frame, width=20, font = font_4, relief=FLAT, bd=entry_bd, bg='#F0F0F0', fg=fg_color, insertbackground=fg_color )
    filter_by_entryI.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    filter_by_entryI_frame.grid(row=2, column=0, sticky='w')
    
    value_entry_frame = Frame(header_frame, bg=button_bg)
    value_entry = Entry(value_entry_frame, width=20, font = font_4, relief=FLAT, bd=2, bg='#F0F0F0', fg=fg_color, insertbackground=fg_color)
    value_entry.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    value_entry_frame.grid(row=2, column=1, sticky='w', padx=2)

    search_button = Button(header_frame, text="Search Records", font=font_5, fg=button_fg, bg=button_bg, command=search_rec, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    search_button.grid(row=2, column=2)
    
    refresh_button = Button(header_frame, text="Refresh Records", font=font_5, fg=button_fg, bg=button_bg, command=listdisplay, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    refresh_button.grid(row=2, column=3, padx=1)
    
    inventory_update_buttons = Frame(header_frame)
    inventory_update_buttons.grid(row=3, column=0, columnspan=3, sticky='w', pady=1)
    
    enter_item = Button(inventory_update_buttons, text="Enter Item", bg=button_bg, fg=button_fg, width=20, font=font_5, command=enter_product, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    enter_item.grid(row=3, column=0)
    
    update_inventory = Button(inventory_update_buttons, text="Update Item", bg=button_bg, fg=button_fg, width=20, font=font_5, command=update_in, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    update_inventory.grid(row=3, column=1, padx=1)
    
    delete_item = Button(inventory_update_buttons, text="Delete Items", bg=button_bg, fg=button_fg, width=20, font=font_5, command=delete_items, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    delete_item.grid(row=3, column=2)
    


    inventory_data = Frame(information_frame, bg=button_bg)
    

    

    inventory_list = Listbox(inventory_data, width=116, height=20, bg='white',selectmode=MULTIPLE, font=font_5, fg=fg_color,  xscrollcommand = True, relief=FLAT)
    inventory_list.grid(row=0, column=0, pady=1, padx=1)

    listdisplay()
    
        

    

    
    inventory_data.grid(row=1, column=0, sticky='w', padx=5)

    information_frame.grid(row=0, column=1, rowspan=5)





    admin_main.mainloop()
# ADMIN WINDOW END
# 
# 
# 


# Selection Code
def enter_admin(event):
    if userAuth == 1:
        window.destroy()
        admin_window()
    else:
        messagebox.showwarning(title="Warning", message="You are not authorised to acces admin")
        

def enter_register(event):
    global register 
    global enter_register
    window.destroy()
    register_window()
   



def check_response():
    print("Working")
# Selector WindoW End

# Director Window


    
def verify_entry():
    
    global admin_auth
    global window
    admin_auth = True
    window = Tk()
    window.title("Easy POS")
    window.geometry("700x600")
    windowWidth = window.winfo_reqwidth()
    windowHeight = window.winfo_reqheight()
    positionRight = int(window.winfo_screenwidth()/2 - windowWidth * 1.7)
    positionDown = int(window.winfo_screenheight()/2 - windowHeight* 1.5)
    window.geometry("+{}+{}".format(positionRight, positionDown))
    window.resizable(0,0)
    icon_image = PhotoImage(file ="images/user.png") #Change later

    window.iconphoto(True, icon_image)

    # load background_image
    background_image = PhotoImage(file = "images/bg_image2_b.png")
    admin_image = PhotoImage(file="images/admin_small.png")
    register_image = PhotoImage(file="images/register_small.png")

    # Code
    default_font = ("Comic Sans", 17)
    label = Label(window, image=background_image)
    label.place(x=0, y=0, relwidth=1, relheight=1)
    frame_ad = Frame(window, bg="#0D3F7C")
    frame_ad.place(x=350, y=300, anchor="center")
    admin = Label(frame_ad, image=admin_image)
    admin.pack(side=LEFT, padx=20, pady=20)
    register = Label(frame_ad,  image=register_image)
    register.pack(side=LEFT, padx=20, pady=20)

    admin.bind("<Button-1>", enter_admin)
    register.bind("<Button-1>", enter_register)

    window.mainloop()
# Director Window End///   
    
 # REGISTER WINDOW
#Regiter Functions Start
def checkProduct(pCode, pQunatity):
    try:
        checkCodeVer =  database_conn1.cursor()
        checkCodeVer.execute(f"SELECT rowid, * FROM inventory WHERE product_code = '{pCode}'")
        result = checkCodeVer.fetchall()
        currentQ = result[0][3]
        
        
        if(currentQ < int(pQunatity)):
            messagebox.showerror(title="Error", message=f"No Enough Product With code \" {pCode}\" In Inventory ")
        else:
            return(result)

    except:
        messagebox.showerror(title="Error", message=f"No Product With code \" {pCode}\" ")
        
def saveSale(retItemData):
    print(retItemData)

   


def makeSell():
    global saleCount
    saleCount += 1
    itemCode =  str(item_name_entry.get())
    itemQunatity =  str(quantity_entry.get())
    checkInputList = [itemCode, itemQunatity]
    if len(itemCode) < 1 or len(itemQunatity) < 1:
        messagebox.askquestion(title="Warning!!", message="Ensure Both \"Item Name\\ Code\" and \"Item Quantity\" are not empty")
    
    else:
        retItem = checkProduct(itemCode, itemQunatity)
        calAmount = int(retItem[0][3]) * int(itemQunatity)
        itemDataString = f"Product Name: {retItem[0][1]} /// Product Quantity {itemQunatity} /// Product Price: {retItem[0][3]} /// Amount: {setCurrency}{calAmount}" 
        sale_list.insert(int(saleCount), itemDataString)
        productName = retItem[0][1]
        productPrice = retItem[0][3]
        productCode = retItem[0][4]
        productQuantity = int(itemQunatity)
        
        salesData = (productName, productCode,productPrice, productQuantity, calAmount)
        salesDataList.append(salesData)
        salesDataListAmount.append(calAmount)
        quantity_entry.delete(0, END)
        item_name_entry.delete(0, END)


def confirmDelete():
    user_name = userNameInput .get()
    user_password = userPasswordInput.get()
    getUserData = database_conn2.cursor()
    getUserData.execute("SELECT * FROM userdata")
    mydata = getUserData.fetchall()
    for user in mydata:
        password = decrypt_password(user[1])
        if user_name == user[0]:
            if user_password == password:
                if user[2] == 1:
                    for index in reversed(sale_list.curselection()):
                        sale_list.delete(index)
                        salesDataList.pop(index)
                        salesDataListAmount.pop(index)
                    
                    userAGet.destroy()
                    break
            else:
                messagebox.showwarning(title="Warning", message="Wrong Password")
                break 
    

def calChange():
    itemTotal =sum(salesDataListAmount)
    cash = cash_entry.get()
    
    if(len(cash) < 1):
        messagebox.showwarning(title="Warning", message="\"Enter Cash\" is empty")
    else:
        if(itemTotal > int(cash)):
            messagebox.showwarning(title="Not enough money")
        else:
            change = int(cash) - itemTotal
            changeAmountLabel.config(text = setCurrency + str(change))

def nextCustomer():
    if(len(salesDataList) > 0):
        
        for item in salesDataList:
            # delete from inventory
            
            productCode = item[1]
            pCode = int(productCode)

            productQuantity = item[3]
            pQuantity = int(productQuantity)
            
            productCode = item[0]
            getItemData = database_conn1.cursor()
            getItemData.execute(f"""SELECT * FROM inventory WHERE  product_code  = '{pCode}' """)
            result = getItemData.fetchall()
           
            productQuantity2 = result[0][1]
            pQuantity2 = int(productQuantity2)

            productDifference = pQuantity2 - pQuantity
           
            getItemData.execute(f"UPDATE inventory SET product_quantity = '{productDifference}'  WHERE product_code = '{pCode}'")

            
            pName = str(item[0])
            pCodes = int(item[1])
            pUnitep = int(item[2])
            pQuants = int(item[3])
            pAmounts = int(item[4])
            date = datetime.datetime.now(tz=pytz.UTC)
            dateOfSell = (date.strftime('%D'))
            insertSale =  [pName, pCodes, pUnitep, pQuants, pAmounts,dateOfSell]
            insertString = ''' INSERT INTO sells(
                                                            product_name ,
                                                            product_code ,
                                                            product_unit_price ,
                                                            product_quantity ,
                                                            product_amount ,
                                                            dateof_sale)
                                                            VALUES(?,?,?,?,?,?) '''
            saveSale = database_conn1.cursor()
            saveSale.execute(insertString, insertSale)
            
            database_conn1.commit()
            print("Sale Saved")



            
            # updateInventory = database_conn1.cursor()
            # updateInventory.execute("UPDATE inventory SET product_quantity = '{update_quantity}' WHERE product_code =")
            
        item_name_entry.delete(0,END)
        quantity_entry.delete(0,END)
        cash_entry.delete(0,END)
        sale_list.delete(0, END)
        total_value.config(text=0)
        changeAmountLabel.config(text=0)
        salesDataList.clear()
        salesDataListAmount.clear()

def salesTotal():
    if(len(salesDataListAmount) < 1):
        messagebox.showinfo(title="Total", message="No itesm have been sold")
        total_value.config(text=0)
    
    else:
        total = sum(salesDataListAmount)
        total_value.config(text=setCurrency + str(total))
        print(sum(salesDataListAmount))
        print(salesDataList)


def deleteSale():
    global userNameInput 
    global userPasswordInput 
    global userAGet
    selectedItems = sale_list.curselection()
    if len(selectedItems) < 1:
        messagebox.showwarning(title="No Items", message="No items selected")
    
    else:
        checkToDelete = messagebox.askquestion(title="Delete from sale", message="Are you sure you want to delete items")

        if checkToDelete == "yes":
            result = deleteAuth
            if(result == 1):
                for index in reversed(sale_list.curselection()):
                    sale_list.delete(index)
                    salesDataList.pop(index)
                    salesDataListAmount.pop(index)

            else:
                userAGet = Toplevel()
                userAGet.title("Admin Authentication")
                userAGet.geometry("400x200")
                windowHeight = userAGet.winfo_reqheight()
                positionRight = int(userAGet.winfo_screenwidth()/2 - windowWidth + 12)
                positionDown = int(userAGet.winfo_screenheight()/2 - windowHeight *  1)
                userAGet.geometry("+{}+{}".format(positionRight, positionDown))
                userAGet.resizable(0,0)
                background_i = Label(userAGet, bg="white")
                background_i.place(x=0, y=0, relheight=1, relwidth=1)
                userName = Label(userAGet, text="User Name", font=font_4, fg=fg_color, bg="white", anchor='w')
                userName.grid(row=0, column=0, sticky='w', padx=5, pady=5)
                userNameInput = Entry(userAGet, font=font_5, width=25, fg="white", insertbackground="white", bg=button_bg)
                userNameInput.grid(row=1, column=0, padx=5, pady=5)
                userPasswordLabel = Label(userAGet, text="Password", font=font_4, fg=fg_color, bg="white", anchor='w')
                userPasswordLabel.grid(row=2, column=0, sticky='w', padx=5, pady=5)
                userPasswordInput = Entry(userAGet, font=font_5, width=25, fg="white", show="*", bg=button_bg, insertbackground='white')
                userPasswordInput.grid(row=3, column=0, sticky='w', padx=5, pady=5)
                deleteButtonSales = Button(userAGet, text="Delete", font=font_5, bg=button_bg, fg=button_fg, width=15, anchor='w', command = confirmDelete, relief=FLAT)
                deleteButtonSales.grid(row=4, column=0, pady=5, padx=5, sticky='w' )
                


        # print(salesDataList)  
        # print(salesDataListAmount)  

        
        


#Register Functions End     
def register_window():
    global storeName
    global register_main
    global item_name_entry
    global quantity_entry
    global cash_entry
    global sale_list
    global total_value
    global changeAmountLabel
   
    
    register_main = Tk()
    register_main.title("Easy POS")
    register_main.state('zoomed')
    width = register_main.winfo_screenwidth()
    height = register_main.winfo_screenwidth()

    register_main.geometry("%dx%d" % (width, height))
    # register_main.attributes('-fullscreen', True)
    
    # register_main.geometry("1000x600")
    
  
    icon_image = PhotoImage(file ="images/user.png") 
    # images
    background_image = PhotoImage(file = "images/bg_image2.png")
    
    # Code
    label = Label(register_main, image=background_image, bg="white")
    label.place(x=0, y=0, relwidth=1, relheight=1)
    # STORE NAME FRAME
    store_name_frame = Frame(register_main, padx=10, bg="white")
    store_name_frame.pack(anchor='w')
    store_name = Label(store_name_frame, text=storeName, font=storeName_font, bg="white", fg=fg_color)
    store_name.pack(side=LEFT)
    # USER LOGED IN DATA FRAME
    user_logged= Frame(register_main, bg="white", padx=10, pady=10)
    user_logged.pack(anchor='w')
    user_name =  Label(user_logged, text=loggedUser, font=font_1, bg="white", fg=fg_color)
    user_name.grid(row=0, column=0, sticky='w')
    date_time = Label(user_logged, text=f"Date: {dateTime}", bg="white", font = font_2, fg=fg_color)
    date_time.grid(row=1, column=0, sticky='w')
    return_image = PhotoImage(file="images/landing_small.png")
    return_label = Label(user_logged, image=return_image )
    return_label.grid(row=2, column=0, sticky='w')
    return_label.bind("<Button-1>", return_director)

    
    # SALE INPUT 
    sales_frame = Frame(register_main, bg="white", padx=10)
    sales_frame.pack(anchor='w')

    item_name_label = Label(sales_frame, text="ITEM CODE",fg=fg_color, bg="white", font=font_3)
    item_name_label.grid(row=0, column=0, sticky='w')

    item_name_frame = Frame(sales_frame, bg=button_bg)
    item_name_entry = Entry(item_name_frame, font=font_4,  bg='#F0F0F0', fg=fg_color, relief=FLAT, insertbackground=fg_color)
    item_name_entry.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    item_name_frame.grid(row=1, column=0, sticky='w')

    quantity_label = Label(sales_frame, text="Quantity",fg=fg_color, bg="white", font=font_3)
    quantity_label.grid(row=0, column=1, sticky='w')
    
    quantity_frame = Frame(sales_frame, bg=button_bg)
    quantity_entry = Entry(quantity_frame, text="Quantity",font=font_4, relief=FLAT, bg='#F0F0F0', fg=fg_color, width=11,  insertbackground=fg_color)
    quantity_entry.grid(row=0, column=0, sticky='w', padx=1,pady=1)
    quantity_frame.grid(row=1, column=1, sticky='w', padx=1)

    cash_label = Label(sales_frame, text="Enter Cash",fg=fg_color, bg="white", font=font_3)
    cash_label.grid(row=0, column=2, sticky='w')
    cash_entry_frame = Frame(sales_frame, bg=button_bg)
    cash_entry = Entry(cash_entry_frame, font=font_4, bg='#F0F0F0', fg=fg_color, relief=FLAT,  insertbackground=fg_color)
    cash_entry.grid(row=0, column=0, sticky='w', padx=1, pady=1)
    cash_entry_frame.grid(row=1, column=2, sticky='w')
    # PROCESSING
    process_frame = Frame(register_main, bg="white")
    process_frame.pack(anchor='w', padx=10, pady=2)

    sales_button = Button(process_frame, text="SELL", width=button_width,  bg=button_bg, fg=button_fg, font=font_5, command = makeSell, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    sales_button.grid(row=0, column=0)
    
    total_button = Button(process_frame, text="TOTAL", width=button_width, bg=button_bg, fg=button_fg, font=font_5, command=salesTotal, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    total_button.grid(row=0, column=1,padx=2)

    delete_button = Button(process_frame, text="DELETE", width=button_width, bg=button_bg, fg=button_fg, font=font_5, command=deleteSale, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    delete_button.grid(row=0, column=2)

    change_button = Button(process_frame, text="CHANGE", width=button_width, bg=button_bg, fg=button_fg, font=font_5, command=calChange, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    change_button.grid(row=0, column=3, padx=2)
    nextCustomerButton = Button(process_frame, text="Next Customer",width=button_width, bg=button_bg, fg=button_fg, font=font_5, command=nextCustomer, relief=FLAT, activebackground=activeBGC, activeforeground=activeFGC)
    nextCustomerButton.grid(row=0, column=4, padx=2)

    data_frame = Frame(register_main, padx=10, bg='white')

    # SALES FRAME START
    
    sales_data = Frame(data_frame, bg='white')
    register_main.columnconfigure(0, weight=1)
    register_main.rowconfigure(0, weight=1)

    sales_label =Label(sales_data, text="Sells", fg=fg_color,font=font_4, bg='white')
    sales_label.grid(row=0, column=0, sticky='w')
    
    padFram1 = Frame(sales_data, bg=button_bg)
    sale_list = Listbox(padFram1, width=110, height=16, font=font_6, fg=fg_color,selectmode=MULTIPLE, relief=FLAT, bg='white')
    # sale_table.insert()
    # sx = Scrollbar(register_main, orient='horizontal', command=sale_table.xview)

 
    sale_list.grid(row=0, column=0,sticky='w',padx=1, pady=1)
    padFram1.grid(row=1, column=0,sticky='w')
    sales_data.grid(row=0, column=0, sticky='w',)
    # SALES FRAME END

    space_frame = Frame(data_frame, bg='white')
    label = Label(space_frame, width=3, bg='white').pack()
    space_frame.grid(row=0, column=1)

    # CODES  FRAME START
    codes_frame = Frame(data_frame, bg='white')
    code_label =Label(codes_frame, text="Item Codes",fg=fg_color, font=font_4, bg='white')
    code_label.grid(row=0, column=0, sticky='w')

    padframe2 = Frame(codes_frame, bg=button_bg)
    code_list = Listbox(padframe2, width = 50, height=16, font=font_6, fg=fg_color, relief=FLAT, bg='white')

    codes = database_conn1.cursor()
    codes.execute("SELECT rowid, * FROM inventory")
    codeList = codes.fetchall()

    codesCount = 0
    for codes in codeList:
        codesCount += 1
        codeListFormation = f"Product Code: {codes[4]} /// Product Name: {codes[1]}"
        code_list.insert(int(codesCount), codeListFormation)
    # sx = Scrollbar(register_main, orient='horizontal', command=code_table.xview)
    
    code_list.grid(row=1, column=0, sticky='w', padx=1, pady=1)
    padframe2.grid(row=1, column=0, sticky='w')
    codes_frame.grid(row=0, column=2, sticky='e')


    total_frame = Frame(data_frame)
    total_label = Label(total_frame, text="Total: ",fg=fg_color, font=font_4, bg='white', anchor='w')
    total_label.grid(row=0, column=0, sticky='w', ipadx=10)
    total_value =Label(total_frame, text=0, font=font_4, bg='#F0F0F0', anchor='c', fg=fg_color, width=10)
    total_value.grid(row=0, column=1, sticky='w', ipadx=10)
    changeAmount = Label(total_frame, fg=fg_color,text="Change: ", font=font_4, bg='white', anchor='w')
    changeAmount.grid(row=0, column=2, sticky='w', ipadx=10)
    changeAmountLabel = Label(total_frame, text=0, font=font_4, bg='#F0F0F0', anchor='c', fg=fg_color, width=10)
    changeAmountLabel.grid(row=0, column=3, sticky='w', ipadx=10)

    total_frame.grid(row=1, column=0, sticky='w')
    
    data_frame.pack(side=LEFT, padx=10)
    

    
    

    # code_frame = Frame(data_frame)
    # code_frame.grid(row=0, column=1)


    register_main.mainloop()
# Registor Window End 




# LOGIN WINDOW
login_window = Tk()
login_window.title("Easy POS")

# login_window.geometry("400x500")
windowWidth = login_window.winfo_reqwidth()
windowHeight = login_window.winfo_reqheight()
positionRight = int(login_window.winfo_screenwidth()/2 - windowWidth)
positionDown = int(login_window.winfo_screenheight()/2 - windowHeight)
login_window.geometry("+{}+{}".format(positionRight, positionDown))
login_window.resizable(0,0)
icon_image = PhotoImage(file ="images/user.png") #Change later
login_window.iconphoto(True, icon_image)

# load background_image
background_image = PhotoImage(file = "images/bg_image2_a.png")
my_canvas = Canvas(login_window, width=400, height=500)
my_canvas.pack(fill="both", expand=True)
my_canvas.create_image(0,0, image=background_image, anchor= "nw")

frame_loging =Frame(login_window, bg="#F0F0F0", pady=10)
frame_pack = my_canvas.create_window(200,250, anchor="center", window=frame_loging)

# Label
default_font = ("Comic Sans", 15)
default_font_buttons = ("Comic Sans", 12)
name_label = Label(frame_loging, text="Name",  width=20, anchor='w', bg="#F0F0F0",  fg=fg_color, font=font_5)
name_label.grid(row=0, column=0,sticky="w", padx=10)

name_frame = Frame(frame_loging, bg=button_bg)
name_entry = Entry(name_frame,  width=25, font=font_5, bg="#F0F0F0",fg=fg_color,insertbackground=fg_color, relief=FLAT)
name_entry.grid(row=0, column=0, padx=1, pady=1)
name_frame.grid(row=1, column=0, padx=10)

password_label = Label(frame_loging, text="Password", width=20, anchor='w', bg="#F0F0F0", fg=fg_color,font=font_5)
password_label.grid(row=2, column=0, sticky="w", padx=10)

password_frame = Frame(frame_loging, bg=button_bg)
password_entry = Entry(password_frame,  width=25, font=font_5, bg="#F0F0F0", fg=fg_color,relief=FLAT,insertbackground=fg_color, show="*")
password_entry.grid(row=1, column=0, padx=1, pady=1)
password_frame.grid(row=3, column=0, padx=10)

login_button = Button(frame_loging, text="Submit", font=font_5, width=15, bg=button_bg, fg="white", command=verify_entry_fun, activebackground=activeBGC, activeforeground=activeFGC, relief=FLAT)
login_button.grid(row=4, column=0,  padx=10, pady=10)



# Log in frame




if __name__ == '__main__':
    login_window.mainloop()