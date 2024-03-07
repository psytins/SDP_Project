# client.py - This module is responsible for client-side functionality.
from Application.network import *

def connect_to_server(host, port):
    client_socket = create_socket()
    client_socket.connect((host, port))
    return client_socket

def get_loadbalancer_addr(ip, port): #ip is string
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port)) # connect to load balancer

    # Receive data from the load balancer (this data is the info of the server that the LB is redirecting us)
    data_received = client_socket.recv(1024).decode() #this is a list
    print(f"Received data from Load Balancer: {data_received}\nPlease wait for incoming connections...")

    # Close the connection
    client_socket.close()

    result = data_received.split(":")
    result[1] = int(result[1]) #pass the port (that is string) to int

    return result

def send_name(client_socket, username, password, mode):
    payload = username + ":" + password + ":" + mode
    
    client_socket.sendall(payload.encode())

    res = client_socket.recv(1024)

    return res.decode()

def create_note(client_socket, note_title, note_content):
    client_socket.sendall(f"CREATE_NOTE:{note_title}:{note_content}".encode())
    print(f"\nNote created!\n")
    input("Press Enter to continue...")

def list_notes(client_socket):
    client_socket.sendall("LIST_NOTES".encode())
    data = client_socket.recv(1024)
    print(f"\nYour Notes:\n{data.decode()}\n")

    if(data.decode() == "No notes."):
        input("Press Enter to continue...")
        return -1
     
    return 0

def list_note(client_socket, note_id):
    client_socket.sendall(f"LIST_NOTE:{note_id}".encode())
    note = client_socket.recv(1024).decode()
    print(note)
    input("Press Enter to continue...")


def delete_note(client_socket, note_index):
    client_socket.sendall(f"DELETE_NOTE:{note_index}".encode())
    res = client_socket.recv(1024).decode()
    print(f"\n{res}\n")
    input("Press Enter to continue...")