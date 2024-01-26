import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import ImageTk, Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import re
import random
import sqlite3
import os
import win32api
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import my_email

root = tk.Tk()

root.geometry('500x600')
root.title('Student Registration System')

bg_color = '#273b7a'
login_student_icon = tk.PhotoImage(file='images/login_student_img.png')
login_admin_icon = tk.PhotoImage(file='images/admin_img.png')
add_student_icon = tk.PhotoImage(file='images/add_student_img.png')
locked_icon = tk.PhotoImage(file='images/locked.png')
unlocked_icon = tk.PhotoImage(file='images/unlocked.png')
add_student_pic_icon = tk.PhotoImage(file='images/add_image.png')


def init_databse():
    if os.path.exists('students_accounts.db'):
        connection = sqlite3.connect('students_accounts.db')

        cursor = connection.cursor()

        cursor.execute("""
                SELECT * FROM data
                """)

        connection.commit()

        connection.close()
    else:
        connection = sqlite3.connect('students_accounts.db')

        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE data(
        id_number text,
        password text,
        name text,
        age text,
        gender text,
        phone_number text,
        class text,
        email text,
        image blob
        )
        """)

        connection.commit()
        connection.close()

def check_id_already_exists(id_number):
    connection = sqlite3.connect('students_accounts.db')

    cursor = connection.cursor()

    cursor.execute(f"""
    SELECT id_number FROM data WHERE id_number =='{id_number}'
    """)

    connection.commit()
    response = cursor.fetchall()
    connection.close()

    return response

def check_valid_password(id_number, password):
    connection = sqlite3.connect('students_accounts.db')

    cursor = connection.cursor()

    cursor.execute(f"""
    SELECT id_number, password FROM data WHERE id_number =='{id_number}' AND 
    password == '{password}'
    """)

    connection.commit()
    response = cursor.fetchall()
    connection.close()

    return response


def add_data(id_number, password, name, age, gender,phone_number,
             student_class, email, pic_data):
    connection = sqlite3.connect('students_accounts.db')

    cursor = connection.cursor()

    cursor.execute(f"""
            INSERT INTO data VALUES('{id_number}','{password}','{name}','{age}','{gender}',
            '{phone_number}','{student_class}','{email}',?)
            """, [pic_data])

    connection.commit()
    connection.close()

def message_box(message):
    message_box_fm = tk.Frame(root, highlightbackground=bg_color,
                                   highlightthickness=3)
    close_btn=tk.Button(message_box_fm, text='X', bd=0, font=('Bold',13),
                        fg=bg_color, command=lambda: message_box_fm.destroy())
    close_btn.place(x=290, y=5)

    message_lb=tk.Label(message_box_fm, text=message, font=('Bold', 15),)
    message_lb.place(x=15, y=70)

    message_box_fm.place(x=100, y=120, width=320, height=200)

def draw_student_card(student_pic_path, student_data):

    labels = """
ID Number:
Name:
Age:
Gender:
Class:
Contacts:
Email:
    """

    student_card = Image.open('images/student_card_frame.png')
    pic = Image.open(student_pic_path).resize((100,100))

    student_card.paste(pic,(15,25))

    draw = ImageDraw.Draw(student_card)
    heading_font = ImageFont.truetype('bahnschrift', 18)
    labels_font = ImageFont.truetype('arial', 13)
    data_font = ImageFont.truetype('bahnschrift',13)

    draw.text(xy=(150,60), text='Student Card', fill=(0,0,0),
              font=heading_font)

    draw.multiline_text(xy=(15, 120), text=labels, fill=(0,0,0),
                        font=labels_font, spacing=6)

    draw.multiline_text(xy=(95,122), text=student_data, fill=(0,0,0),
                        font=data_font, spacing= 7)

    return student_card


def student_card_page(student_card_obj):

    def save_student_card():
        path = askdirectory()

        if path:


            student_card_obj.save(f'{path}/student_card.png')

    def print_student_card():
        path = askdirectory()

        if path:


            student_card_obj.save(f'{path}/student_card.png')

            win32api.ShellExecute(0, 'print', f'{path}/student_card.png',
                                  None, '.', 0)

    def close_page():
        student_card_page_fm.destroy()
        root.update()
        student_login_page()

    student_card_img = ImageTk.PhotoImage(student_card_obj)

    student_card_page_fm=tk.Frame(root,highlightbackground=bg_color,
                                  highlightthickness=3)

    heading_lb=tk.Label(student_card_page_fm, text='Student Card',
                        bg=bg_color, fg='white',font=('Bold',18))
    heading_lb.place(x=0, y=0, width=400)

    close_btn = tk.Button(student_card_page_fm, text='X', bg=bg_color,
                          fg='white', font=('Bold',13),bd=0,
                          command=close_page)
    close_btn.place(x=370, y=0)





    student_card_lb = tk.Label(student_card_page_fm, image=student_card_img)
    student_card_lb.place(x=50, y=50)

    student_card_lb.image = student_card_img

    save_student_card_btn = tk.Button(student_card_page_fm, text='Save Student Card',
                                      bg=bg_color,fg='white', font=('Bold', 15),
                                      bd=1, command=save_student_card)
    save_student_card_btn.place(x=80, y=375)

    print_student_card_btn = tk.Button(student_card_page_fm, text='🖨️',
                                      bg=bg_color, fg='white', font=('Bold', 18),
                                      bd=1, command=print_student_card)
    print_student_card_btn.place(x=270, y=370)

    student_card_page_fm.place(x=50, y=30, width=400, height=450)

def confirmation_box(message):
    answer = tk.BooleanVar()
    answer.set(False)

    def action(ans):
        answer.set(ans)
        confirmation_box_fm.destroy()

    confirmation_box_fm = tk.Frame(root, highlightbackground=bg_color,
                                   highlightthickness=3)

    message_lb = tk.Label(confirmation_box_fm, text=message, font=('Bold', 15))
    message_lb.pack(pady=20)

    cancel_btn = tk.Button(confirmation_box_fm, text='Cancel', font=('Bold', 15),
                           bd=0, bg=bg_color, fg='white',
                           command=lambda: action(False))
    cancel_btn.place(x=50, y=160)

    yes_btn = tk.Button(confirmation_box_fm, text='Yes', font=('Bold', 15),
                        bd=0, bg='red', fg='white',
                        command=lambda: action(True))
    yes_btn.place(x=190, y=160, width=80)

    confirmation_box_fm.place(x=100, y=120, width=320, height=220)

    root.wait_window(confirmation_box_fm)
    return answer.get()


# Welcome page function
def welcome_page():
    def forward_to_student_login_page():
        welcome_page_fm.destroy()
        root.update()
        student_login_page()

    def forward_to_admin_login_page():
        welcome_page_fm.destroy()
        root.update()
        admin_login_page()

    def forward_to_add_account_page():
        welcome_page_fm.destroy()
        root.update()
        add_account_page()

    welcome_page_fm = tk.Frame(root, highlightbackground=bg_color,
                               highlightthickness=3)  # background color

    heading_lb = tk.Label(welcome_page_fm,
                          text='Student Registration & \nManagement System',
                          bg=bg_color, fg='white', font=('Bold', 18))

    heading_lb.place(x=0, y=0, width=400)

    # login student button
    student_login_btn = tk.Button(welcome_page_fm, text='Login Student', bg=bg_color,
                                  fg='white', font=('Bold', 15), bd=0,
                                  command=forward_to_student_login_page)
    student_login_btn.place(x=120, y=125, width=200)

    student_login_img = tk.Button(welcome_page_fm, image=login_student_icon, bd=0,
                                  command=forward_to_student_login_page)
    student_login_img.place(x=60, y=100)

    # login admin button
    admin_login_btn = tk.Button(welcome_page_fm, text='Login Admin', bg=bg_color,
                                fg='white', font=('Bold', 15), bd=0,
                                command=forward_to_admin_login_page)
    admin_login_btn.place(x=120, y=225, width=200)

    admin_login_img = tk.Button(welcome_page_fm, image=login_admin_icon, bd=0,
                                command=forward_to_admin_login_page)
    admin_login_img.place(x=60, y=200)

    # create account button
    add_student_btn = tk.Button(welcome_page_fm, text='Create Account', bg=bg_color,
                                fg='white', font=('Bold', 15), bd=0, command=forward_to_add_account_page)
    add_student_btn.place(x=120, y=325, width=200)

    add_student_img = tk.Button(welcome_page_fm, image=login_student_icon, bd=0, command=forward_to_add_account_page)
    add_student_img.place(x=60, y=300)

    # frame define
    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=400, height=420)

#Send mail to student
def sendmail_to_student(email, message, subject):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    username = my_email.email_address
    password = my_email.password

    msg = MIMEMultipart()

    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = email

    msg.attach(MIMEText(_text=message, _subtype='html'))

    smtp_connection = smtplib.SMTP(host=smtp_server, port=smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(user=username, password=password)

    smtp_connection.sendmail(from_addr=username, to_addrs=email,
                             msg=msg.as_string())




#forget password function
def forget_password_page():

    def recover_password():
        if check_id_already_exists(id_number=student_id_ent.get()):


            connection = sqlite3.connect('students_accounts.db')
            cursor = connection.cursor()

            cursor.execute(f"""
            SELECT password FROM data WHERE id_number == '{student_id_ent.get()}'
            """)

            connection.commit()

            recovered_password = cursor.fetchall()[0][0]


            cursor.execute(f"""
            SELECT email FROM data WHERE id_number == '{student_id_ent.get()}'
            """)

            connection.commit()

            student_email = cursor.fetchall()[0][0]

            connection.close()

            confirmation = confirmation_box(message=f"""We will send \n Your Forget Password
Via Your Email Address: 
{student_email}
Do You Want to Continue?
            """)
            if confirmation:
                sendmail_to_student(student_email,
                                    message=f"Your Account Pasword is {recovered_password}",
                                    subject='Password Recovery')
            else:
                pass

        else:

            message_box('Invalid ID')

    forget_password_page_fm = tk.Frame(root, highlightbackground=bg_color,
                                       highlightthickness=3)

    heading_lb = tk.Label(forget_password_page_fm, text='Forgetting Password',
                          font=('Bold', 15), bg=bg_color, fg='white')
    heading_lb.place(x=0, y=0, width=350)

    close_btn = tk.Button(forget_password_page_fm, text='X',
                          font=('Bold',13), bg=bg_color, fg='white',
                          bd=0, command= lambda: forget_password_page_fm.destroy())
    close_btn.place(x=320, y=0)

    student_id_lb = tk.Label(forget_password_page_fm, text='Enter Student ID No',
                          font=('Bold', 13))

    student_id_lb.place(x=90, y=40)

    student_id_ent = tk.Entry(forget_password_page_fm,
                              font=('Bold', 15), justify=tk.CENTER)
    student_id_ent.place(x=90, y=80, width= 140)

    info_lb = tk.Label(forget_password_page_fm,
                       text="""Via Your Email Address
We will send you
Your Forgot Password.""", justify=tk.CENTER)

    info_lb.place(x=100, y=110)

    next_btn = tk.Button(forget_password_page_fm, text='Next',
                         font=('Bold',13), bg=bg_color,
                         fg='white', command=recover_password)
    next_btn.place(x=130, y=200, width=80)

    forget_password_page_fm.place(x=75, y=120, width=350, height=250)


#fetching data dashboard
def fetch_student_data(query):
    connection = sqlite3.connect('students_accounts.db')
    cursor = connection.cursor()

    cursor.execute(query)

    connection.commit()
    response = cursor.fetchall()
    connection.close()

    return response

#student Dashboard
def student_dashboard(student_id):

    get_student_details = fetch_student_data(f"""
    SELECT name, age, gender, class, phone_number, email FROM data WHERE id_number =='{student_id}'
    """)

    get_student_pic = fetch_student_data(f"""
    SELECT image FROM data WHERE id_number == '{student_id}'
    """)

    student_pic = BytesIO(get_student_pic[0][0])




    def switch(indicator, page):

        home_btn_indicator.config(bg=bg_color)
        student_card_btn_indicator.config(bg=bg_color)
        security_btn_indicator.config(bg=bg_color)
        edit_data_card_btn_indicator.config(bg=bg_color)
        delete_account_btn_indicator.config(bg=bg_color)

        indicator.config(bg='white')

        for child in pages_fm.winfo_children():
            child.destroy()
            root.update()

        page()


    dashboard_fm = tk.Frame(root, highlightbackground=bg_color,
                            highlightthickness=3)

    options_fm = tk.Frame(dashboard_fm,bg=bg_color,
                            highlightthickness=0)


    home_btn = tk.Button(options_fm, text='Home',
                         font=('Bold', 15), fg='white',
                         bd=0, bg=bg_color, command=lambda:
                                 switch(indicator=home_btn_indicator,
                                        page=home_page))
    home_btn.place(x=10, y=80)

    home_btn_indicator = tk.Label(options_fm, bg='white')
    home_btn_indicator.place(x=5, y=76.5, width=3, height=40)

    student_card_btn = tk.Button(options_fm, text='Student\nCard',
                         font=('Bold', 15), fg='white',
                         bd=0, bg=bg_color, justify=tk.LEFT,
                                 command=lambda:
                                 switch(indicator=student_card_btn_indicator,
                                        page=dashboard_student_card_page))
    student_card_btn.place(x=10, y=130)

    student_card_btn_indicator = tk.Label(options_fm, bg=bg_color)
    student_card_btn_indicator.place(x=5, y=138.5, width=3, height=40)

    security_btn = tk.Button(options_fm, text='Security',
                         font=('Bold', 15), fg='white',
                         bd=0, bg=bg_color, command=lambda:
                                 switch(indicator=security_btn_indicator,
                                        page=security_page))
    security_btn.place(x=10, y=200)

    security_btn_indicator = tk.Label(options_fm, bg=bg_color)
    security_btn_indicator.place(x=5, y=198, width=3, height=40)

    edit_data_card_btn = tk.Button(options_fm, text='Edit Data',
                                 font=('Bold', 15), fg='white',
                                 bd=0, bg=bg_color, command=lambda:
                                 switch(indicator=edit_data_card_btn_indicator,
                                        page=edit_data_card_page))
    edit_data_card_btn.place(x=10, y=250)

    edit_data_card_btn_indicator = tk.Label(options_fm, bg=bg_color)
    edit_data_card_btn_indicator.place(x=5, y=246.5, width=3, height=40)

    delete_account_btn = tk.Button(options_fm, text='Delete\nAccount',
                         font=('Bold', 15), fg='white',
                         bd=0, bg=bg_color, justify=tk.LEFT, command=lambda:
                                 switch(indicator=delete_account_btn_indicator,
                                        page=delete_account_page))
    delete_account_btn.place(x=10, y=300)

    delete_account_btn_indicator = tk.Label(options_fm, bg=bg_color)
    delete_account_btn_indicator.place(x=5, y=307.5, width=3, height=40)

    logout_btn = tk.Button(options_fm, text='Logout',
                                 font=('Bold', 15), fg='white',
                                 bd=0, bg=bg_color)
    logout_btn.place(x=0,y=520, width=120)

    options_fm.place(x=0, width=120, height=575)

    #homepage
    def home_page():

        #User profile
        student_pic_img_obj = Image.open(student_pic)
        size = 100
        mask = Image.new(mode='L', size=(size,size))

        draw_circle  = ImageDraw.Draw(im=mask)
        draw_circle.ellipse(xy=(0, 0, size, size), fill=255, outline=True)

        output = ImageOps.fit(image=student_pic_img_obj, size=mask.size,
                              centering=(1,1))

        output.putalpha(mask)

        student_picture = ImageTk.PhotoImage(output)

        home_page_fm = tk.Frame(pages_fm, bg='white')

        student_pic_lb = tk.Label(home_page_fm, image=student_picture, bg='white')
        student_pic_lb.image = student_picture
        student_pic_lb.place(x=10, y=10)


        #Labels
        hi_lb = tk.Label(home_page_fm, text=f'Hi! {get_student_details[0][0]}'.upper(),
                         bg='white', font=('Bold', 15))

        hi_lb.place(x=130, y=50)

        student_details = f"""
Student ID: {student_id}\n
Name: {get_student_details[0][0]}\n
Age: {get_student_details[0][1]}\n
Gender: {get_student_details[0][2]}\n
Class: {get_student_details[0][3]}\n
Contact: {get_student_details[0][4]}\n
Email: {get_student_details[0][5]}\n
"""

        student_details_lb = tk.Label(home_page_fm,text=student_details,
                                      bg='white', justify=tk.LEFT,
                                      font=('Bold', 12))
        student_details_lb.place(x=30, y=160)

        home_page_fm.pack(fill=tk.BOTH, expand=True)

    # Student Card page
    def dashboard_student_card_page():
        student_details = f"""
{student_id}
{get_student_details[0][0]}
{get_student_details[0][1]}
{get_student_details[0][2]}
{get_student_details[0][3]}
{get_student_details[0][4]}
{get_student_details[0][5]}
"""

        student_card_image_obj = draw_student_card(student_pic_path=student_pic,
                                                   student_data=student_details)

        def save_student_card():
            path = askdirectory()

            if path:
                student_card_image_obj.save(f'{path}/student_card.png')

        def print_student_card():
            path = askdirectory()

            if path:
                student_card_image_obj.save(f'{path}/student_card.png')

                win32api.ShellExecute(0, 'print', f'{path}/student_card.png',
                                      None, '.', 0)

        student_card_img = ImageTk.PhotoImage(student_card_image_obj)

        dashboard_student_card_page_fm = tk.Frame(pages_fm, bg='white')

        card_lb = tk.Label(dashboard_student_card_page_fm, image=student_card_img, bg='white')
        card_lb.image = student_card_img
        card_lb.place(x=20, y=50)

        save_student_card_page_btn = tk.Button(dashboard_student_card_page_fm,
                                              text='Save Student Card',
                                              font=('Bold',15), bd=0, fg='white',
                                              bg=bg_color,
                                               command=save_student_card)
        save_student_card_page_btn.place(x=40, y=400)

        print_student_card_page_btn = tk.Button(dashboard_student_card_page_fm,
                                              text=f'     🖨️',
                                              font=('Bold', 15), bd=0, fg='white',
                                              bg=bg_color,
                                                command=print_student_card)
        print_student_card_page_btn.place(x=240, y=400)

        dashboard_student_card_page_fm.pack(fill=tk.BOTH, expand=True)

    # Security page
    def security_page():

        # show/hide function
        def show_hide_password():
            if current_password_ent['show'] == '*':
                current_password_ent.config(show='')
                show_hide_btn.config(image=unlocked_icon)
            else:
                current_password_ent.config(show='*')
                show_hide_btn.config(image=locked_icon)


        #change password
        def set_password():
            if new_password_ent.get() !='':
                confirm = confirmation_box(message='Do You Want to Change\n The Current Passowrd?')
                if confirm:
                    connection = sqlite3.connect('students_accounts.db')

                    cursor = connection.cursor()
                    cursor.execute(f"""UPDATE data SET password = '{new_password_ent.get()}' 
                                    WHERE id_number =='{student_id}'""")

                    connection.commit()
                    connection.close()

                    message_box(message='Password Changed Succesfully!')

                    current_password_ent.config(state=tk.NORMAL)
                    current_password_ent.delete(0, tk.END)
                    current_password_ent.insert(0, new_password_ent.get())
                    current_password_ent.config(state='readonly')

                    new_password_ent.delete(0, tk.END)
                else:
                    pass

            else:
                message_box(message='Enter New Password')




        security_page_fm = tk.Frame(pages_fm, bg='white')

        current_password_lb = tk.Label(security_page_fm, text='Your Current Password',
                                        font=('Bold', 12), bg='white')
        current_password_lb.place(x=90, y=30)

        current_password_ent = tk.Entry(security_page_fm, font=('Bold',15),
                                        justify=tk.CENTER, show='*',
                                        highlightcolor=bg_color, highlightthickness=3,
                                        highlightbackground=bg_color, bg='white')
        current_password_ent.place(x=50, y=80)

        student_current_password = fetch_student_data(f"""SELECT password FROM data WHERE id_number =='{student_id}'""")

        current_password_ent.insert(tk.END, student_current_password[0][0])
        current_password_ent.config(state='readonly')


        # show/hide password button
        show_hide_btn = tk.Button(security_page_fm, image=locked_icon, bd=0,
                                  command=show_hide_password, bg='white')
        show_hide_btn.place(x=290, y=74)


        #change password
        change_password_lb = tk.Label(security_page_fm, text='Change Password',
                                      font=('Bold',15), fg='white', bg='red')
        change_password_lb.place(x=30, y=200, width= 300)

        new_password_lb = tk.Label(security_page_fm, text='Set New Password',
                                      font=('Bold', 12), bg='white')
        new_password_lb.place(x=25, y=270, width=300)

        new_password_ent = tk.Entry(security_page_fm, font=('Bold', 15),
                                        justify=tk.CENTER, show='*',
                                        highlightcolor=bg_color, highlightthickness=3,
                                        highlightbackground=bg_color, bg='white')
        new_password_ent.place(x=60, y=350)


        set_password_btn = tk.Button(security_page_fm, text='SET Password',
                                     bg=bg_color, font=('Bold',12), fg='white',
                                     command=set_password)
        set_password_btn.place(x=120, y=450)

        security_page_fm.pack(fill=tk.BOTH, expand=True)

    # Edit Data Card page
    def edit_data_card_page():

        pic_path = tk.StringVar()
        pic_path.set('')

        def open_pic():
            path = askopenfilename()

            if path:
                img = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
                pic_path.set(path)

                add_pic_button.config(image=img)
                add_pic_button.image = img

        edit_data_card_page_fm = tk.Frame(pages_fm, bg='white')

        # ADD PICTURE
        add_pic_section_fm = tk.Frame(edit_data_card_page_fm, highlightbackground=bg_color,
                                      highlightthickness=2)
        add_pic_section_fm.place(x=5, y=5, width=105, height=105)

        add_pic_button = tk.Button(add_pic_section_fm, image=add_student_pic_icon,
                                   command=open_pic, bd=0, bg='white')
        add_pic_button.pack()

        edit_data_card_page_fm.pack(fill=tk.BOTH, expand=True)

        # Student full name entry
        student_name_lb = tk.Label(edit_data_card_page_fm, text='Enter Student Full Name',
                                   font=('Bold', 12), bg='white')
        student_name_lb.place(x=5, y=130)

        student_name_ent = tk.Entry(edit_data_card_page_fm, font=('Bold', 15),
                                    highlightcolor=bg_color, highlightbackground='grey',
                                    highlightthickness=2)
        student_name_ent.place(x=5, y=160, width=180)

        # Student Age entry
        student_age_lb = tk.Label(edit_data_card_page_fm, text='Enter Student Age',
                                  font=('Bold', 12), bg='white')
        student_age_lb.place(x=5, y=205)

        student_age_ent = tk.Entry(edit_data_card_page_fm, font=('Bold', 15),
                                   highlightcolor=bg_color, highlightbackground='grey',
                                   highlightthickness=2)
        student_age_ent.place(x=5, y=245, width=180)


    # Delete account page
    def delete_account_page():
        delete_account_page_fm = tk.Frame(pages_fm, bg='white')

        delete_account_page_lb = tk.Label(delete_account_page_fm, text='Delete Account Page',
                                          font=('Bold', 15))
        delete_account_page_lb.place(x=100, y=200)

        delete_account_page_fm.pack(fill=tk.BOTH, expand=True)


    #pages frame creating
    pages_fm = tk.Frame(dashboard_fm, bg='white')
    pages_fm.place(x=120, y=0, width=354, height=574)

    home_page()

    dashboard_fm.pack(pady=5)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.configure(width=480, height=580)


# student login page function
def student_login_page():
    # show/hide function
    def show_hide_password():
        if password_ent['show'] == '*':
            password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            password_ent.config(show='*')
            show_hide_btn.config(image=locked_icon)

    # forward to homepage function
    def forward_to_welcome_page():
        student_login_page_fm.destroy()
        root.update()
        welcome_page()

    def forward_to_forget_password_page():
        forget_password_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground'] !='grey':
            if entry.get() !='':
                entry.config(highlightcolor=bg_color,
                             highlightbackground='grey')


    def login_account():
        verify_id_number = check_id_already_exists(id_number=id_number_ent.get())

        if verify_id_number:


            verify_password = check_valid_password(id_number=id_number_ent.get(),
                                                   password=password_ent.get())

            if verify_password:
                id_number = id_number_ent.get()
                student_login_page_fm.destroy()
                student_dashboard(student_id=id_number)
                root.update()


            else:


                password_ent.config(highlightcolor='red',
                                     highlightbackground='red')

                message_box(message='Incorrect Password')


        else:


            id_number_ent.config(highlightcolor='red',
                         highlightbackground='red')

            message_box(message='Please Enter Valid Student ID')


    student_login_page_fm = tk.Frame(root, highlightbackground=bg_color,
                                     highlightthickness=3)

    heading_lb = tk.Label(student_login_page_fm, text='Student Login Page', bg=bg_color,
                          fg='white', font=('bold', 18))
    heading_lb.place(x=0, y=0, width=400)

    # back button
    back_btn = tk.Button(student_login_page_fm, text='←', font=('Bold', 20),
                         fg=bg_color, bd=0,
                         command=forward_to_welcome_page)
    back_btn.place(x=5, y=35)

    #####
    stud_icon_lb = tk.Label(student_login_page_fm, image=login_student_icon)
    stud_icon_lb.place(x=150, y=40)

    # username enter
    id_number_lb = tk.Label(student_login_page_fm, text='Enter Student ID No',
                            font=('Bold', 15), fg=bg_color)
    id_number_lb.place(x=90, y=140)

    id_number_ent = tk.Entry(student_login_page_fm, font=('Bold', 15),
                             justify=tk.CENTER, highlightcolor=bg_color,
                             highlightbackground='grey', highlightthickness=2)
    id_number_ent.place(x=80, y=180)
    id_number_ent.bind('<KeyRelease>',
                       lambda e: remove_highlight_warning(entry=id_number_ent))

    # password entry
    password_lb = tk.Label(student_login_page_fm, text='Enter Your Password',
                           font=('Bold', 15), fg=bg_color)
    password_lb.place(x=90, y=240)

    password_ent = tk.Entry(student_login_page_fm, font=('Bold', 15),
                            justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='grey', highlightthickness=2, show='*')
    password_ent.place(x=80, y=280)
    password_ent.bind('<KeyRelease>',
                       lambda e: remove_highlight_warning(entry=password_ent))

    # show/hide password button
    show_hide_btn = tk.Button(student_login_page_fm, image=locked_icon, bd=0,
                              command=show_hide_password)
    show_hide_btn.place(x=310, y=270)

    # login Button
    login_btn = tk.Button(student_login_page_fm, text='Login',
                          font=('Bold', 15), bg=bg_color, fg='white',
                          command=login_account)
    login_btn.place(x=95, y=340, width=200, height=40)

    # forget password button
    forget_password_btn = tk.Button(student_login_page_fm, text='⚠️\nForget Password',
                                    fg=bg_color, bd=0, command=lambda: forward_to_forget_password_page())
    forget_password_btn.place(x=150, y=390)

    student_login_page_fm.pack(pady=30)
    student_login_page_fm.pack_propagate(False)
    student_login_page_fm.configure(width=400, height=450)


# Admin login page

def admin_login_page():
    # show/hide function
    def show_hide_password():
        if password_ent['show'] == '*':
            password_ent.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            password_ent.config(show='*')
            show_hide_btn.config(image=locked_icon)

    # forward to homepage function
    def forward_to_welcome_page():
        admin_login_page_fm.destroy()
        root.update()
        welcome_page()

    admin_login_page_fm = tk.Frame(root, highlightbackground=bg_color,
                                   highlightthickness=3)

    heading_lb = tk.Label(admin_login_page_fm, text='Admin Login Page', bg=bg_color,
                          fg='white', font=('bold', 18))
    heading_lb.place(x=0, y=0, width=400)

    # back button
    back_btn = tk.Button(admin_login_page_fm, text='←', font=('Bold', 20),
                         fg=bg_color, bd=0,
                         command=forward_to_welcome_page)
    back_btn.place(x=5, y=35)

    admin_icon_lb = tk.Label(admin_login_page_fm, image=login_admin_icon)
    admin_icon_lb.place(x=150, y=40)

    # username enter
    id_number_lb = tk.Label(admin_login_page_fm, text='Enter Admin ID No',
                            font=('Bold', 15), fg=bg_color)
    id_number_lb.place(x=90, y=140)

    id_number_ent = tk.Entry(admin_login_page_fm, font=('Bold', 15),
                             justify=tk.CENTER, highlightcolor=bg_color,
                             highlightbackground='grey', highlightthickness=2)
    id_number_ent.place(x=80, y=180)

    # password entry
    password_lb = tk.Label(admin_login_page_fm, text='Enter Your Password',
                           font=('Bold', 15), fg=bg_color)
    password_lb.place(x=90, y=240)

    password_ent = tk.Entry(admin_login_page_fm, font=('Bold', 15),
                            justify=tk.CENTER, highlightcolor=bg_color,
                            highlightbackground='grey', highlightthickness=2, show='*')
    password_ent.place(x=80, y=280)

    # show/hide password button
    show_hide_btn = tk.Button(admin_login_page_fm, image=locked_icon, bd=0,
                              command=show_hide_password)
    show_hide_btn.place(x=310, y=270)

    # login Button
    login_btn = tk.Button(admin_login_page_fm, text='Login',
                          font=('Bold', 15), bg=bg_color, fg='white')
    login_btn.place(x=95, y=340, width=200, height=40)

    # forget password button
    forget_password_btn = tk.Button(admin_login_page_fm, text='⚠️\nForget Password',
                                    fg=bg_color, bd=0)
    forget_password_btn.place(x=150, y=390)

    admin_login_page_fm.pack(pady=30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width=400, height=450)


# create account page

def add_account_page():

    pic_path=tk.StringVar()
    pic_path.set('')

    def open_pic():
        path = askopenfilename()

        if path:
            img = ImageTk.PhotoImage(Image.open(path).resize((100,100)))
            pic_path.set(path)

            add_pic_button.config(image=img)
            add_pic_button.image=img

    def forward_to_welcome_page():

        ans = confirmation_box('Do You Want to Leave \n Registration Form?')
        if ans:
            add_account_page_fm.destroy()
            root.update()
            welcome_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground'] !='grey':
            if entry.get() !='':
                entry.config(highlightcolor=bg_color,
                             highlightbackground='grey')

    def check_input_validation():
        if student_name_ent.get() =='':
            student_name_ent.config(highlightcolor='red',
                                    highlightbackground='red')
            student_name_ent.focus()
            message_box('Student Full Name is Required')
        elif student_age_ent.get() =='':
            student_age_ent.config(highlightcolor='red',
                                    highlightbackground='red')
            student_age_ent.focus()
            message_box('Student Age is Required')

        elif student_contact_ent.get() =='':
            student_contact_ent.config(highlightcolor='red',
                                    highlightbackground='red')
            student_contact_ent.focus()
            message_box('Student Contact No is Required')

        elif student_email_ent.get() =='':
            student_email_ent.config(highlightcolor='red',
                                    highlightbackground='red')
            student_email_ent.focus()
            message_box('Student Email is Required')

        elif not check_invalid_email(email=student_email_ent.get().lower()):
            student_email_ent.config(highlightcolor='red',
                                     highlightbackground='red')
            student_email_ent.focus()
            message_box('Enter Valid Email Address')

        elif account_password_ent.get() =='':
            account_password_ent.config(highlightcolor='red',
                                    highlightbackground='red')
            account_password_ent.focus()
            message_box('Account Password is Required')

        else:
            pic_data = b''

            if pic_path.get() !='':
                resize_pic = Image.open(pic_path.get()).resize((100,100))
                resize_pic.save('temp_pic.png')

                read_data = open('temp_pic.png','rb')
                pic_data = read_data.read()
                read_data.close()
            else:
                read_data = open('images/add_image.png', 'rb')
                pic_data = read_data.read()
                read_data.close()
                pic_path.set('images/add_image.png')



            add_data(id_number=student_id.get(),
                     password=account_password_ent.get(),
                     name=student_name_ent.get(),
                     age=student_age_ent.get(),
                     gender=student_gender.get(),
                     phone_number=student_contact_ent.get(),
                     student_class=select_class_button.get(),
                     email=student_email_ent.get(),
                     pic_data=pic_data)



            data = f"""
{student_id.get()}
{student_name_ent.get()}
{student_gender.get()}
{student_age_ent.get()}
{select_class_button.get()}
{student_email_ent.get()}
"""

            get_student_card = draw_student_card(student_pic_path=pic_path.get(),
                              student_data=data)

            student_card_page(student_card_obj=get_student_card)

            add_account_page_fm.destroy()
            root.update()

            message_box('Account Successfully Created!')

    def check_invalid_email(email):
        pattern="^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$"
        match=re.match(pattern=pattern, string=email)
        return match

    def generate_id_number():
        generated_id=''

        for r in range(6):
            generated_id += str(random.randint(0,9))

        if not check_id_already_exists(id_number=generated_id):


            student_id.config(state=tk.NORMAL)
            student_id.delete(0,tk.END)
            student_id.insert(tk.END,generated_id)
            student_id.config(state='readonly')

        else:
            generate_id_number()


    student_gender = tk.StringVar()
    class_list = ['5th', '6th', '7th', '8th']


    add_account_page_fm = tk.Frame(root, highlightbackground=bg_color,
                                   highlightthickness=3)

    # ADD PICTURE
    add_pic_section_fm = tk.Frame(add_account_page_fm, highlightbackground=bg_color,
                                  highlightthickness=2)
    add_pic_section_fm.place(x=5, y=5, width=105, height=105)

    add_pic_button = tk.Button(add_pic_section_fm, image=add_student_pic_icon,
                               command=open_pic)
    add_pic_button.pack()

    # Student full name entry
    student_name_lb = tk.Label(add_account_page_fm, text='Enter Student Full Name',
                               font=('Bold', 12))
    student_name_lb.place(x=5, y=130)

    student_name_ent = tk.Entry(add_account_page_fm, font=('Bold', 15),
                                highlightcolor=bg_color, highlightbackground='grey',
                                highlightthickness=2)
    student_name_ent.place(x=5, y=160, width=180)
    student_name_ent.bind('<KeyRelease>',
                          lambda e:remove_highlight_warning(entry=student_name_ent))

    # Gender Selection
    student_gender_lb = tk.Label(add_account_page_fm, text='Select Student Gender',
                                 font=('Bold', 12))
    student_gender_lb.place(x=5, y=210)

    male_gender_btn = tk.Radiobutton(add_account_page_fm, text='Male',
                                     font=('Bold', 12), variable=student_gender,
                                     value='male')
    male_gender_btn.place(x=5, y=235)

    female_gender_btn = tk.Radiobutton(add_account_page_fm, text='Female',
                                       font=('Bold', 12), variable=student_gender,
                                       value='female')
    female_gender_btn.place(x=80, y=235)

    student_gender.set('male')

    # Student Age entry
    student_age_lb = tk.Label(add_account_page_fm, text='Enter Student Age',
                              font=('Bold', 12))
    student_age_lb.place(x=5, y=275)

    student_age_ent = tk.Entry(add_account_page_fm, font=('Bold', 15),
                               highlightcolor=bg_color, highlightbackground='grey',
                               highlightthickness=2)
    student_age_ent.place(x=5, y=305, width=180)
    student_age_ent.bind('<KeyRelease>',
                          lambda e:remove_highlight_warning(entry=student_age_ent))

    # Student Contact No entry
    student_contact_lb = tk.Label(add_account_page_fm, text='Enter Student Contact No',
                                  font=('Bold', 12))
    student_contact_lb.place(x=5, y=340)

    student_contact_ent = tk.Entry(add_account_page_fm, font=('Bold', 15),
                                   highlightcolor=bg_color, highlightbackground='grey',
                                   highlightthickness=2)
    student_contact_ent.place(x=5, y=370, width=180)
    student_contact_ent.bind('<KeyRelease>',
                          lambda e:remove_highlight_warning(entry=student_contact_ent))

    # Student Class entry
    student_class_lb = tk.Label(add_account_page_fm, text='Select Student Class',
                                font=('Bold', 12))
    student_class_lb.place(x=5, y=420)

    select_class_button = Combobox(add_account_page_fm, font=('Bold', 15),
                                   state='readonly', values=class_list)
    select_class_button.place(x=5, y=445, height=30, width=180)

    # Student ID section
    student_id_lb = tk.Label(add_account_page_fm, text='Student ID No: ',
                             font=('Bold', 12))
    student_id_lb.place(x=240, y=35)

    student_id = tk.Entry(add_account_page_fm, font=('Bold', 18), bd=0)
    student_id.place(x=380, y=33, width=80)


    generate_id_number()

    id_info_lb = tk.Label(add_account_page_fm, text="Automatically Generated ID Number", justify=tk.LEFT)
    id_info_lb.place(x=240, y=65)

    # Student Email entry
    student_email_lb = tk.Label(add_account_page_fm, text='Enter Student Email',
                                font=('Bold', 12))
    student_email_lb.place(x=240, y=130)

    student_email_ent = tk.Entry(add_account_page_fm, font=('Bold', 15),
                                 highlightcolor=bg_color, highlightbackground='grey',
                                 highlightthickness=2)
    student_email_ent.place(x=240, y=160, width=180)
    student_email_ent.bind('<KeyRelease>',
                          lambda e:remove_highlight_warning(entry=student_email_ent))

    email_info_lb = tk.Label(add_account_page_fm, text="""Via Email Address Student
Can Recover Account
! In Case Forgetting Password and also
Student will get Future Notifications""", justify=tk.LEFT)
    email_info_lb.place(x=240, y=200)

    # Account password entry
    account_password_lb = tk.Label(add_account_page_fm, text='Create Password',
                                   font=('Bold', 12))
    account_password_lb.place(x=240, y=275)

    account_password_ent = tk.Entry(add_account_page_fm, font=('Bold', 15),
                                    highlightcolor=bg_color, highlightbackground='grey',
                                    highlightthickness=2)
    account_password_ent.place(x=240, y=305, width=180)
    account_password_ent.bind('<KeyRelease>',
                          lambda e:remove_highlight_warning(entry=account_password_ent))

    account_password_info_lb = tk.Label(add_account_page_fm, text="""Via Student Created Password
And Provided Student ID Number
Student Can Login Account""", justify=tk.LEFT)

    account_password_info_lb.place(x=240, y=345)

    # Home & Submit buttons
    home_btn = tk.Button(add_account_page_fm, text='Home', font=('Bold', 15),
                         bg='red', fg='white', bd=0, command=forward_to_welcome_page)
    home_btn.place(x=240, y=440)

    submit_btn = tk.Button(add_account_page_fm, text='Submit', font=('Bold', 15),
                           bg=bg_color, fg='white', bd=0,
                           command=check_input_validation)
    submit_btn.place(x=350, y=440)

    add_account_page_fm.pack(pady=5)
    add_account_page_fm.pack_propagate(False)
    add_account_page_fm.configure(width=490, height=580)


#student_card_page()
init_databse()
# add_account_page()
#draw_student_card()
# forget_password_page()

student_dashboard(student_id=173352)

root.mainloop()
