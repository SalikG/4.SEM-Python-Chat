import socket
import threading
import queue
import time
import pickle

clients = []
messages = queue.Queue()

host = "127.0.0.1"

port = 9000

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.bind((host, port))
connection.listen(5)

def acceptConnections():
    while True:
        conn, addr = connection.accept()
        client_dict = {"NICKNAME": "", "CONNECTION_TS": time.time(), "CLIENT": conn, "ROOM": ""}
        clients.append(client_dict)
        print("New Client Connected: ", addr)
        t = threading.Thread(target=client_thread, args=(conn,))
        t.start()


def broadcast_messages():
    while True:
        msg = messages.get()
        data = pickle.dumps(msg)
        for c in clients:
            if c["ROOM"] == msg["room"]:
                try:
                    c["CLIENT"].send(data)
                    print(msg)
                except:
                    c["CLIENT"].close()
                    if c in clients:
                        clients.remove(c)


def client_thread(conn):
    while True:
        try:
            data = conn.recv(1024)
            msg = pickle.loads(data)
            print("New message ", msg)

            if msg["action"] == "reg":
                file = open("users.txt", "a")
                file.write(msg["username"] + " " + msg["nickname"] + " " + msg["password"] + "\n")
                file.close()

                response_msg = {"action":"reg_success"}
                response_data= pickle.dumps(response_msg)
                conn.send(response_data)
            elif msg["action"] == "msg":
                messages.put(msg)
            elif msg["action"] == "join_room":              #if statement for at joine et rum
                for client_index in range(clients.__len__()):
                    if clients[client_index]["CLIENT"] == conn:
                        messages.put({"action": "leave_room", "room": clients[client_index]["ROOM"], "nickname": msg["nickname"]})
                        clients[client_index]["ROOM"] = msg["room"]
                        messages.put(msg)
            elif msg["action"] == "login":
                file = open("users.txt", "r")
                users = file.read().splitlines()
                login_success = False
                for line_index in  range(users.__len__()):
                    temp_user = users[line_index].split(" ")
                    if temp_user[0] == msg["username"] and temp_user[2] == msg["password"]:
                        login_msg = pickle.dumps({"action":"msg", "msg":temp_user[1] + " has joined Hackers Paradise"})
                        for client_index in range(clients.__len__()):
                            if clients[client_index]["CLIENT"] == conn:
                                clients[client_index]["ROOM"] = "Black Hats"
                                clients[client_index]["NICKNAME"] = temp_user[1]
                            else:
                                # besked til alle clients undtagen den som prøver at logge ind om at en ny client er logget in
                                if clients[client_index]["ROOM"] != "":
                                    clients[client_index]["CLIENT"].send(login_msg)
                        response_data = pickle.dumps({"action":"login_success", "nickname":temp_user[1]})
                        conn.send(response_data)
                        login_success = True

                if login_success == False:
                    response_data = pickle.dumps({"action": "login_failed"})
                    conn.send(response_data)
            elif msg["action"] == "logout":
                for client_index in range(clients.__len__()):
                    if clients[client_index]["CLIENT"] == conn:
                        clients[client_index]["ROOM"] = "Black Hats"
                        clients[client_index]["NICKNAME"] = ""
                messages.put(msg)
            print("New message ", msg)
        except:
            continue

threading.Thread(target=broadcast_messages).start()
acceptConnections()