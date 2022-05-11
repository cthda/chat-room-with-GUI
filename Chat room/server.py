import socket                                                 #SMALL CHAT ROOM
import sqlite3                                                #Cannot modify data on the database from clients if do not send messages via network
import threading                                              #because sqlite has no server

#VERSION:3.9.7          #The person number can be increased using the mysql database and also clients can access the mysql database easily without manually sending messages via network
                        #and listen() parameter can be increased
class SqliteDatabase:

    __all_online_clients = set()  #This is defined here because it is like a temporary database

    def start_sql_connection_and_set_username_password(self,username,password):
        """                                         
        if you want to use sql or modify something on the database,
        you have to use this method first.Otherwise it raises error. 
        """

        self.username = username

        self.password = password
                                                        
        self.conn = sqlite3.connect("chat_room_app.db")

        self.cursor = self.conn.cursor()

        self.__create_table()

    def __create_table(self):

        self.cursor.execute("CREATE TABLE IF NOT EXISTS Persons(Id INTEGER PRIMARY KEY,Username TEXT UNIQUE,Password TEXT NOT NULL)")

    def add_person_into_database(self):

        self.cursor.execute("SELECT Id FROM Persons")    #for dynamic Id in sql

        id_number_list = self.cursor.fetchall()

        id_number = len(id_number_list)

        id_number += 1
        
        self.cursor.execute(f"INSERT INTO Persons VALUES({self.id_number},'{self.username}','{self.password}')")

    def has_username(self,control_username):

        self.cursor.execute(f"SELECT Username FROM Persons WHERE Username = '{control_username}'")

        result = self.cursor.fetchone()

        if result == None:

            return True

        else:

            return False

    def login(self,username_to_login,password_to_login):

        self.cursor.execute(f"SELECT Username,Password FROM Persons WHERE Username = '{username_to_login}' AND Password = '{password_to_login}'")

        result = self.cursor.fetchone()

        if result == None:

            return False

        else:

            return True

    def close_sql_connection_and_commit(self):

        self.conn.commit()

        self.conn.close()

    @classmethod
    def online_clients_in_chatroom_for_broadcast_message(cls)-> set[socket.socket]:

        return cls.__all_online_clients

    @classmethod
    def add_client_that_entered_chatroom_for_broadcast_message(cls,conn):

        cls.__all_online_clients.add(conn)

    @classmethod
    def delete_client_that_left_chatroom_for_broadcast_message(cls,conn):

        cls.__all_online_clients.remove(conn)

class SocketConnection(socket.socket):

    def __init__(self,ip_version,socket_type,server_ip,server_port):

        super().__init__(ip_version,socket_type)

        self.server_ip = server_ip

        self.server_port = server_port

    def __bind_ip_to_port(self):

        self.bind((self.server_ip,self.server_port))

    def start_connection(self):

        self.__bind_ip_to_port()

        self.listen(15)

    def _wait_for_messages_and_send(self,conn_obj:socket.socket):

        while True:

            self.conn_obj = conn_obj

            try:

                message = self.conn_obj.recv(1024)

            except:

                break

            else:

                if message.decode("utf-8").startswith("****UsErNamE---PasSwORd__??") == True:

                    username_password_list = message.decode("utf-8")[28:].split(" ")

                    database_object.start_sql_connection_and_set_username_password(username_password_list[0],username_password_list[1])

                    check_username = database_object.has_username(username_password_list[0])

                    if check_username == False:

                        try:

                            self.conn_obj.send("FALSE".encode("utf-8"))  #Someone has the username

                        except:

                            pass

                        database_object.close_sql_connection_and_commit()

                    else:

                        try:

                            self.conn_obj.send("TRUE".encode("utf-8"))

                        except:

                            pass

                        lock.acquire()
                        
                        database_object.add_person_into_database()

                        database_object.close_sql_connection_and_commit()

                        lock.release()

                elif message.decode("utf-8").startswith("****UsErNamEToLOgin---PasSwORdToLOgin__??"):

                    username_password_list_to_login = message.decode("utf-8")[42:].split(" ")

                    database_object.start_sql_connection_and_set_username_password(username_password_list_to_login[0],username_password_list_to_login[1])

                    check_username_and_password = database_object.login(username_password_list_to_login[0],username_password_list_to_login[1])

                    if check_username_and_password == False:

                        try:

                            self.conn_obj.send("FALSE".encode("utf-8"))  #Wrong username or password

                        except:

                            pass

                        database_object.close_sql_connection_and_commit()

                    else:

                        try:

                            self.conn_obj.send("TRUE".encode("utf-8"))

                        except:

                            pass

                        SqliteDatabase.add_client_that_entered_chatroom_for_broadcast_message(self.conn_obj)

                        database_object.close_sql_connection_and_commit()

                elif message.decode("utf-8") == "":     #if any client closes the connection,server side connection that linked the client's connection shuts too.

                    break

                else: #broadcast message

                    for conns in SqliteDatabase.online_clients_in_chatroom_for_broadcast_message():

                                                       #The client sends itself the message too while broadcasting.
                                                       #In the client side script,if the message does not display on the chat screen,it means the client has network problems.
                        try:

                            conns.send(message)

                        except:

                            pass

        if self.conn_obj in SqliteDatabase.online_clients_in_chatroom_for_broadcast_message():

            SqliteDatabase.delete_client_that_left_chatroom_for_broadcast_message(self.conn_obj)

        self.conn_obj.close()

database_object = SqliteDatabase()

lock = threading.Lock()  #Thread lock mechanism for persons who will be added into the database with Id

chatroom_connection = SocketConnection(socket.AF_INET,socket.SOCK_STREAM,"127.0.0.1",11111)  #İPv4,TCP,LOCAL MACHİNE

chatroom_connection.start_connection()

while True:

    conn,addr = chatroom_connection.accept()

    thread_to_get_message = threading.Thread(target=chatroom_connection._wait_for_messages_and_send,args=(conn,))

    thread_to_get_message.start()


            
