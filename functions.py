import tkinter as tk
root = tk.Tk()



bg_color='#273b7a'
login_student_icon=tk.PhotoImage(file='images/login_student_img.png')
login_admin_icon=tk.PhotoImage(file='images/admin_img.png')
add_student_icon=tk.PhotoImage(file='images/add_student_img.png')

def welcome_page():

    welcome_page_fm = tk.Frame(root,highlightbackground=bg_color,
                               highlightthickness=3) #background color

    heading_lb=tk.Label(welcome_page_fm,
                        text='Student Registration & \nManagement System',
                        bg=bg_color,fg='white',font=('Bold',18))

    heading_lb.place(x=0,y=0,width=400)

    student_login_btn= tk.Button(welcome_page_fm,text='Login Student',bg=bg_color,
                                 fg='white',font=('Bold',15),bd=0)
    student_login_btn.place(x=120,y=125,width=200)

    student_login_img= tk.Button(welcome_page_fm,image=login_student_icon,bd=0)
    student_login_img.place(x=60,y=100 )

    admin_login_btn= tk.Button(welcome_page_fm,text='Login Admin',bg=bg_color,
                                 fg='white',font=('Bold',15),bd=0)
    admin_login_btn.place(x=120,y=225,width=200)

    admin_login_img= tk.Button(welcome_page_fm,image=login_admin_icon,bd=0)
    admin_login_img.place(x=60,y=200 )

    add_student_btn= tk.Button(welcome_page_fm,text='Create Account',bg=bg_color,
                                 fg='white',font=('Bold',15),bd=0)
    add_student_btn.place(x=120,y=325,width=200)

    add_student_img= tk.Button(welcome_page_fm,image=login_student_icon,bd=0)
    add_student_img.place(x=60,y=300 )


    welcome_page_fm.pack(pady=30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width=400,height=420)
