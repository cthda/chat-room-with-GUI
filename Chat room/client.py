import socket
import tkinter as tk
from tkinter import messagebox as msgbox
import threading
import tkinter.scrolledtext as scrolledtxt




class MainWindow(tk.Tk):

    def __init__(self):

        super().__init__()

        self.wm_geometry("700x800")

        self.wm_minsize(670,740)

        self.wm_maxsize(1920,1080)

        self.wm_resizable(True,True)

        self.wm_title("Log in")

        self.username_input_entry = tk.StringVar()

        self.password_input_entry = tk.StringVar()

    def set_and_place_username_entry(self):

        def placeholder_for_username_field(event):

            self.username_entry_object["state"] = "normal"

            self.username_entry_object.delete(0,"end")

            self.username_entry_object.unbind("<Button-1>",placeholder_username_id)

        self.username_entry_object = tk.Entry(
        self,
        textvariable=self.username_input_entry,
        justify="left",
        bg="white",
        fg="black",
        font=(100)
        )

        self.username_entry_object.place_configure(relx=0.4,rely=0.3,relheight=0.04,relwidth=0.25)

        self.username_entry_object.insert(0,"Username")

        self.username_entry_object.configure(state="disabled",disabledbackground="white")

        placeholder_username_id = self.username_entry_object.bind("<Button-1>",placeholder_for_username_field)

    def set_and_place_info_label(self):

        def change_color_on_motion(event):

            self.info_label_object["fg"] = "orange"

        def move_out_mouse_from_area_of_label(event):

            self.info_label_object["fg"] = "black"

        def click_on_label(event):

            self.info_label_object.place_configure(relwidth=0.25)

            self.info_label_object["text"] = "The Username field will be shown\nas the nickname in the chat room"

            self.info_label_object.bind("<Button-1>",click_on_label_again)

        def click_on_label_again(event):

            self.info_label_object.place_configure(relwidth=0.05)

            self.info_label_object["text"] = "Info"

            self.info_label_object.bind("<Button-1>",click_on_label)

        self.info_label_object = tk.Label(
        self,
        bg="white",
        fg="black",
        text="Info",
        cursor="hand2"
        )

        self.info_label_object.place_configure(relx=0.4,rely=0.2656,relheight=0.032,relwidth=0.05)

        self.info_label_object.bind("<Motion>",change_color_on_motion)

        self.info_label_object.bind("<Leave>",move_out_mouse_from_area_of_label)

        self.info_label_object.bind("<Button-1>",click_on_label)

    def set_and_place_show_label(self):

        def change_color_on_motion(event):

            self.show_label_object["fg"] = "red"

        def move_out_mouse_from_area_of_label(event):

            self.show_label_object["fg"] = "black"

        def click_on_label(event):

            self.password_entry_object["show"] = ""

            self.show_label_object["text"] = "Hide"

            self.show_label_object.bind("<Button-1>",click_on_label_again)

        def click_on_label_again(event):

            self.password_entry_object["show"] = "*"

            self.show_label_object["text"] = "Show"

            self.show_label_object.bind("<Button-1>",click_on_label)

        self.show_label_object = tk.Label(
        self,
        bg="white",
        fg="black",
        text="Show",
        cursor="hand2",
        )

        self.show_label_object.place_configure(relx=0.6,rely=0.40,relheight=0.032,relwidth=0.05)

        self.show_label_object.bind("<Motion>",change_color_on_motion)

        self.show_label_object.bind("<Leave>",move_out_mouse_from_area_of_label)

        self.show_label_object.bind("<Button-1>",click_on_label)

    def set_and_place_password_entry(self):

        def placeholder_for_password_field(event):

            self.password_entry_object["state"] = "normal"

            self.password_entry_object.delete(0,"end")

            self.password_entry_object.unbind("<Button-1>",placeholder_password_id)

            self.password_entry_object["show"] = "*"

        self.password_entry_object = tk.Entry(
        self,
        textvariable=self.password_input_entry,
        justify="left",
        bg="white",
        fg="black",
        font=(100)
        )

        self.password_entry_object.place_configure(relx=0.4,rely=0.36,relheight=0.04,relwidth=0.25)

        self.password_entry_object.insert(0,"Password")

        self.password_entry_object.configure(state="disabled",disabledbackground="white")

        placeholder_password_id = self.password_entry_object.bind("<Button-1>",placeholder_for_password_field)

    def set_and_place_enter_button(self):

        self.enter_button_object = tk.Button(
        self,
        text="Enter",
        command=self.__open_the_chat_window,
        bg="white",
        fg="black",
        state="normal",
        activebackground="white",
        activeforeground="black",
        disabledforeground="black",
        cursor="hand2",
        font=(100)
        )

        self.enter_button_object.place_configure(relx=0.46,rely=0.47,relheight=0.05,relwidth=0.12)

    def __open_the_chat_window(self):  #This one actually starts the chat room

        try:

            client_connection = SocketConnection(socket.AF_INET,socket.SOCK_STREAM,"127.0.0.1",11111)

        except:

            msgbox.showerror("Error","Connection Error")

        else:

            username = self.username_input_entry.get()

            password = self.password_input_entry.get()

            try:

                client_connection.send(f"****UsErNamEToLOgin---PasSwORdToLOgin__?? {username} {password}".encode("utf-8"))  #sqlite has no server

            except:

                client_connection.close()

                msgbox.showerror("Error","Connection Error")

            else:

                try:

                    client_connection.settimeout(5.5)

                    message = client_connection.recv(1024).decode("utf-8")  #May raise error because of some cases

                    client_connection.settimeout(None)

                    if message == "FALSE":   #Wrong username or password

                        client_connection.close()

                        msgbox.showerror("Error","Wrong username or password")

                    elif message == "TRUE":     #If no problem for username and password while entering

                        chat_window = ChatWindow(self)  

                        user_input = chat_window.create_input_of_users_and_return_object()

                        send_button_object = chat_window.create_send_button_and_return_object()

                        text_screen = chat_window.create_text_widget_to_display_messages_and_return_object()

                        thread_to_get_message = threading.Thread(target=client_connection.recv_messages,args=(text_screen,),daemon=True)

                        thread_to_get_message.start()

                        send_button_object["command"] = lambda:client_connection.send_messages(user_input,username)

                except socket.timeout:

                    client_connection.close()

                    msgbox.showerror("Error","Connection timeout")

                except:

                    client_connection.close()

                    msgbox.showerror("Error","Connection has been shutted")

                else:

                    pass

    def set_and_place_signup_button(self):

        self.signup_button_object = tk.Button(
        self,
        text="Sign up",
        command=self.__after_click_signup_button,
        bg="white",
        fg="black",
        state="normal",
        activebackground="white",
        activeforeground="black",
        disabledforeground="black",
        cursor="hand2",
        font=(100)
        )

        self.signup_button_object.place_configure(relx=0.83,rely=0.09,relheight=0.05,relwidth=0.12)

    def __after_click_signup_button(self):

        def placeholder_for_username_field(event):

            self.username_entry_object["state"] = "normal"

            self.username_entry_object.delete(0,"end")

            self.username_entry_object.unbind("<Button-1>",placeholder_username_id)

        self.username_entry_object["state"] = "normal"

        self.username_entry_object.delete(0,"end")

        self.username_entry_object.insert(0,"Username")

        self.username_entry_object.configure(state="disabled",disabledbackground="white")

        placeholder_username_id = self.username_entry_object.bind("<Button-1>",placeholder_for_username_field)

        def placeholder_for_password_field(event):

            self.password_entry_object["state"] = "normal"

            self.password_entry_object.delete(0,"end")

            self.password_entry_object.unbind("<Button-1>",placeholder_password_id)

            self.password_entry_object["show"] = "*"

        self.password_entry_object.configure(show="",state="normal")

        self.password_entry_object.delete(0,"end")

        self.password_entry_object.insert(0,"Password")

        self.password_entry_object.configure(state="disabled",disabledbackground="white")

        placeholder_password_id = self.password_entry_object.bind("<Button-1>",placeholder_for_password_field)

        def sign_up_person():  #This one actually starts to sign up the person to the chat room

            try:

                client_connection_to_signup = SocketConnection(socket.AF_INET,socket.SOCK_STREAM,"127.0.0.1",11111)

            except:

                msgbox.showerror("Error","Connection Error")

            else:

                username_to_signup = self.username_input_entry.get()

                password_to_signup = self.password_input_entry.get()

                if (len(username_to_signup) >= 4 and len(password_to_signup) >= 4) and (username_to_signup != "Username" and password_to_signup != "Password"):

                    try:

                        client_connection_to_signup.send(f"****UsErNamE---PasSwORd__?? {username_to_signup} {password_to_signup}".encode("utf-8")) #sqlite has no server

                    except:

                        client_connection_to_signup.close()

                        msgbox.showerror("Error","Connection Error")

                    else:

                        try:

                            client_connection_to_signup.settimeout(5.5)

                            signup_message = client_connection_to_signup.recv(1024).decode("utf-8")  #May raise error because of some cases

                            client_connection_to_signup.settimeout(None)

                            if signup_message == "FALSE":

                                client_connection_to_signup.close()

                                msgbox.showwarning("Warning","Someone has the username")

                            elif signup_message == "TRUE":   #If no problem for username and password while signing up

                                msgbox.showinfo("Info","Signed up successfully")

                        except socket.timeout:

                            client_connection_to_signup.close()

                            msgbox.showerror("Error","Connection timeout")

                        except:

                            client_connection_to_signup.close()

                            msgbox.showerror("Error","Connection has been shutted")

                        else:

                            pass
                
                else:

                    client_connection_to_signup.close()

                    msgbox.showwarning("Warning","Username and Password must be at least 4 characters")

        self.signup_button_object.configure(text="Log in",command=self.__signup_window_widgets_after_click_login_button)

        self.enter_button_object.configure(text="Sign up",command=sign_up_person)

    def __signup_window_widgets_after_click_login_button(self):

        def placeholder_for_username_field(event):

            self.username_entry_object["state"] = "normal"

            self.username_entry_object.delete(0,"end")

            self.username_entry_object.unbind("<Button-1>",placeholder_username_id)

        self.username_entry_object["state"] = "normal"

        self.username_entry_object.delete(0,"end")

        self.username_entry_object.insert(0,"Username")

        self.username_entry_object.configure(state="disabled",disabledbackground="white")

        placeholder_username_id = self.username_entry_object.bind("<Button-1>",placeholder_for_username_field)

        def placeholder_for_password_field(event):

            self.password_entry_object["state"] = "normal"

            self.password_entry_object.delete(0,"end")

            self.password_entry_object.unbind("<Button-1>",placeholder_password_id)

            self.password_entry_object["show"] = "*"

        self.password_entry_object.configure(show="",state="normal")

        self.password_entry_object.delete(0,"end")

        self.password_entry_object.insert(0,"Password")

        self.password_entry_object.configure(state="disabled",disabledbackground="white")

        placeholder_password_id = self.password_entry_object.bind("<Button-1>",placeholder_for_password_field)




        self.signup_button_object.configure(text="Sign up",command=self.__after_click_signup_button)

        self.enter_button_object.configure(text="Enter",command=self.__open_the_chat_window)
    
        
            
class ChatWindow(tk.Toplevel):

    def __init__(self,master_window:tk.Tk):

        super().__init__(master_window)

        self.master_window = master_window

        self.wm_geometry("700x800")

        self.wm_minsize(670,740)

        self.wm_maxsize(1920,1080)

        self.wm_resizable(True,True)

        self.wm_title("Chat")

        self.wm_protocol('WM_DELETE_WINDOW',self.master_window.destroy)

        self.master_window.wm_withdraw()

    def create_input_of_users_and_return_object(self):

        self.user_input_object = scrolledtxt.ScrolledText(
        self,
        )

        self.user_input_object.place_configure(relx=0.11,rely=0.8,relheight=0.14,relwidth=0.65)

        return self.user_input_object

    def create_text_widget_to_display_messages_and_return_object(self):

        self.displaying_messages_object = scrolledtxt.ScrolledText(
        self,
        state="disabled"
        )

        self.displaying_messages_object.place_configure(relx=0.11,rely=0.09,relheight=0.68,relwidth=0.65)

        return self.displaying_messages_object

    def create_send_button_and_return_object(self):

        self.send_button_object = tk.Button(
        self,
        text="Send",
        bg="white",
        fg="black",
        state="normal",
        activebackground="white",
        activeforeground="black",
        disabledforeground="black",
        cursor="hand2",
        font=(100)
        )

        self.send_button_object.place_configure(relx=0.83,rely=0.85,relheight=0.05,relwidth=0.12)

        return self.send_button_object

    
        

class SocketConnection(socket.socket):

    def __init__(self,ip_version,socket_type,*server_ip_and_port):

        super().__init__(ip_version,socket_type)

        self.connect(server_ip_and_port)

    def recv_messages(self,show_incoming_messages_on_screen:scrolledtxt.ScrolledText): #Thread will be handling

        while True:

            try:

                incoming_messages = self.recv(1024).decode("utf-8")

            except:

                pass

            else:

                show_incoming_messages_on_screen["state"] = "normal"

                show_incoming_messages_on_screen.insert(tk.END,incoming_messages)

                show_incoming_messages_on_screen.see(tk.END)

                show_incoming_messages_on_screen["state"] = "disabled"

    def send_messages(self,messages_in_user_input_scrolledtext:scrolledtxt.ScrolledText,username):

        messages_to_be_sent = messages_in_user_input_scrolledtext.get("1.0",tk.END)

        messages_in_user_input_scrolledtext.delete("1.0","end")

        if messages_to_be_sent.isspace() == False:

            try:

                self.send(f"{username}:{messages_to_be_sent}".encode("utf-8"))

            except:

                pass

main_window = MainWindow()

main_window.set_and_place_enter_button()

main_window.set_and_place_password_entry()

main_window.set_and_place_signup_button()

main_window.set_and_place_username_entry()

main_window.set_and_place_show_label()

main_window.set_and_place_info_label()

main_window.mainloop()
