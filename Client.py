import socket
import tkinter as tk
from tkinter import messagebox
from threading import Thread
import pickle


class Application():
    def __init__(self, master):
        self.master = master
        self.nickname = ""
        self.room = "Black Hats"
        # --------------------GUI_START-----------------------

        master.geometry("300x300")
        # LOGIN_start
        self.login_frame = tk.Frame(master)

        username_label = tk.Label(self.login_frame, text="Username")
        self.username = tk.StringVar()
        self.username.set("")
        username_input_field = tk.Entry(self.login_frame, textvariable=self.username)
        # Binder input field til 'enter' kommando fra keyboard og kalder 'send' metoden
        username_input_field.bind("<Return>", lambda e: self.send_login())

        password_label = tk.Label(self.login_frame, text="Password")
        self.password = tk.StringVar()
        self.password.set("")
        password_input_field = tk.Entry(self.login_frame, textvariable=self.password, show="*")
        # Binder input field til 'enter' kommando fra keyboard og kalder 'send' metoden
        password_input_field.bind("<Return>", lambda e: self.send_login())

        btn_login = tk.Button(self.login_frame, text="Login", bg="green", command = self.send_login)
        btn_register = tk.Button(self.login_frame, text="Register", bg="lightblue", command=lambda: self.raise_frame(self.register_frame))

        # PACKING_START
        username_label.pack(side=tk.TOP)
        username_input_field.pack(side=tk.TOP, fill=tk.X)
        password_label.pack(side=tk.TOP)
        password_input_field.pack(side=tk.TOP, fill=tk.X)
        btn_login.pack(side=tk.BOTTOM)
        btn_register.pack(side=tk.BOTTOM)

        self.login_frame.grid(row=0, column=0, sticky="NSEW", padx=40, pady=40)
        # PACKING_END
        # LOGIN_END

        # REGISTER_START
        self.register_frame = tk.Frame(master)

        # global register_username
        register_username_label = tk.Label(self.register_frame, text="Username")
        self.register_username = tk.StringVar()
        self.register_username.set("")
        register_username_input_field = tk.Entry(self.register_frame, textvariable=self.register_username)
        # Binder input field til 'enter' kommando fra keyboard og kalder 'send' metoden
        register_username_input_field.bind("<Return>", lambda e: self.send_register())

        # global register_nickname
        register_nickname_label = tk.Label(self.register_frame, text="Nickname")
        self.register_nickname = tk.StringVar()
        self.register_nickname.set("")
        register_nickname_input_field = tk.Entry(self.register_frame, textvariable=self.register_nickname)
        # Binder input field til 'enter' kommando fra keyboard og kalder 'send' metoden
        register_nickname_input_field.bind("<Return>", lambda e: self.send_register())

        # global register_password
        register_password_label = tk.Label(self.register_frame, text="Password")
        self.register_password = tk.StringVar()
        self.register_password.set("")
        register_password_input_field = tk.Entry(self.register_frame, textvariable=self.register_password)
        # Binder input field til 'enter' kommando fra keyboard og kalder 'send' metoden
        register_password_input_field.bind("<Return>", lambda e: self.send_register())

        btn_confirm_register = tk.Button(self.register_frame, text="Register", bg="green", command = self.send_register)
        btn_back_to_login = tk.Button(self.register_frame, text="Back", command=lambda: self.raise_frame(self.login_frame))

        # PACKING_START
        register_username_label.pack(side=tk.TOP)
        register_username_input_field.pack(side=tk.TOP, fill=tk.X)
        register_nickname_label.pack(side=tk.TOP)
        register_nickname_input_field.pack(side=tk.TOP, fill=tk.X)
        register_password_label.pack(side=tk.TOP)
        register_password_input_field.pack(side=tk.TOP, fill=tk.X)
        btn_confirm_register.pack(side=tk.BOTTOM)
        btn_back_to_login.pack(side=tk.BOTTOM)

        self.register_frame.grid(row=0, column=0, sticky="NSEW", padx=40, pady=40)
        # PACKING_END
        # REGISTER_END

        self.login_frame.tkraise()

    # bliver kaldt hvis server sender action: login_failed
    def login_failed(self):
        self.username.set("")
        self.password.set("")
        login_failed = tk.Label(self.login_frame, text="LOGIN FAILED", bg="red")
        login_failed.pack(side=tk.TOP)

    # Bliver kaldt når client er logget ind
    def chat_frame(self):
        self.login_frame.grid_remove()
        self.register_frame.grid_remove()
        msg_frame = tk.Frame(self.master)
        btn_room_frame = tk.Frame(self.master)

        scrollbar = tk.Scrollbar(msg_frame)
        global msg_list
        msg_list = tk.Listbox(msg_frame, height=30, width=60, yscrollcommand=scrollbar.set)

        global msg
        msg = tk.StringVar()
        msg.set("")
        msg_input_field = tk.Entry(msg_frame, textvariable=msg)
        # Binder input field til 'enter' kommando fra keyboard og kalder 'send' metoden
        msg_input_field.bind("<Return>", lambda e: self.send())
        btn_send = tk.Button(msg_frame, text="Send", bg="green", command=self.send)
        global lbl_room
        lbl_room = tk.Label(btn_room_frame, text=self.room, bg="yellow", fg="red", padx=2, pady=7)
        btn_room1 = tk.Button(btn_room_frame, text="Black Hats", bg="lightgreen", fg="black", command=lambda: self.send_room("Black Hats"))
        btn_room2 = tk.Button(btn_room_frame, text="White Hats", bg="lightgreen", fg="white",command=lambda: self.send_room("White Hats"))
        btn_room3 = tk.Button(btn_room_frame, text="Grey Hats", bg="lightgreen", fg="grey",command=lambda: self.send_room("Grey Hats"))

        # PACKING_START
        lbl_room.pack(side=tk.TOP)
        btn_room1.pack(side=tk.TOP)
        btn_room2.pack(side=tk.TOP)
        btn_room3.pack(side=tk.TOP)
        btn_send.pack(side=tk.BOTTOM)

        msg_input_field.pack(side=tk.BOTTOM, fill=tk.X)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.master.geometry("400x540")
        btn_room_frame.grid(row=0, column=0)
        msg_frame.grid(row=0, column=1, padx=4, pady=4)
        # PACKING_END
        msg_frame.tkraise()

    # Bliver kaldt når et frame skal være øverst
    def raise_frame(self, frame=tk.Frame):
        frame.tkraise()

    def send_login(self):
        # tjekker om der er mellemrum i username password og nickname
        if self.reg_login_input_validation(self.username.get()) and self.reg_login_input_validation(self.password.get()):
            msg = {"action": "login", "username": self.username.get(), "password": self.password.get()}
            data = pickle.dumps(msg)
            mySocket.send(data)
        else:
            messagebox.showerror("Error", "There cant be 'Spaces' in the text!")

    def send(self):
        global msg
        message = {"action":"msg", "room": self.room, "msg":msg.get(), "nickname":self.nickname}
        print("Sending message:  ", message)
        msg.set("")
        data = pickle.dumps(message)
        mySocket.send(data)

    def send_register(self):
        # tjekker om der er mellemrum i username password og nickname
        if self.reg_login_input_validation(self.register_username.get()) == True and \
                self.reg_login_input_validation(self.register_nickname.get()) and \
                self.reg_login_input_validation(self.register_password.get()) == True:
            msg = {"action": "reg", "username": self.register_username.get(), "nickname": self.register_nickname.get(),
                   "password": self.register_password.get()}
            data = pickle.dumps(msg)
            mySocket.send(data)
        else:
            messagebox.showerror("Error", "There cant be 'Spaces' in the text!")

    def send_room(self, room):
        self.room = room
        global lbl_room
        lbl_room["text"] = room
        msg = {"action": "join_room", "room": room, "nickname": self.nickname}
        global msg_list
        msg_list.delete(0, tk.END)
        data = pickle.dumps(msg)
        mySocket.send(data)

    def reg_login_input_validation(self, inpt):
        if ' ' in inpt:
            return False
        else:
            return True

    def error_frame(self, error_msg):
        self.login_frame.grid_remove()
        self.register_frame.grid_remove()
        error_frame = tk.Frame(self.master)
        error_label = tk.Label(error_frame, text=error_msg, bg="red")
        error_label.pack(fill=tk.BOTH)
        error_frame.grid(row=0, column=0, padx=4, pady=4)
        error_frame.tkraise()

def receive():
    while True:
        try:
            data = mySocket.recv(1024)
            msg = pickle.loads(data)
            print("msg from server: ", msg)
            if msg["action"] == "msg":
                global msg_list
                if msg.get('nickname', None) == None:
                    msg_list.insert(tk.END, msg["msg"])
                    msg_list.see(tk.END)
                else:
                    msg_list.insert(tk.END, msg["nickname"] + ":  " + msg["msg"])
                    msg_list.see(tk.END)
            elif msg["action"] == "login_success":
                print("login was a success")
                app.username.set("")
                app.password.set("")
                app.nickname = msg["nickname"]
                app.chat_frame()
            elif msg["action"] == "join_room":
                msg_list.insert(tk.END, msg["nickname"] + " has join the " + app.room)
                msg_list.see(tk.END)
            elif msg["action"] == "login_failed":
                app.login_failed()
                print("login FAILED")
            elif msg["action"] == "reg_success":
                app.register_username.set("")
                app.register_nickname.set("")
                app.register_password.set("")
                app.raise_frame(app.login_frame)
                print("reg was a success")
            elif msg["action"] == "server_closing":
                app.error_frame("Server is down")
        except OSError:
            break



try:
    host = '127.0.0.1'
    port = 9000

    mySocket = socket.socket()
    mySocket.connect((host, port))
    reciever_thread = Thread(target=receive)
    reciever_thread.start()



except Exception:
    root = tk.Tk()

    app = Application(root)
    root.title("Hacker Paradise")

    app.error_frame("SERVER ERROR:  server is down or connection is lost")

    root.mainloop()
else:
    root = tk.Tk()
    app = Application(root)
    root.title("Hacker Paradise")

    root.mainloop()

    mySocket.close()




