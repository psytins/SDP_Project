#Load Balancer --------
import socket
import threading

SERVER_IP = '127.0.0.1' # ip of load balancer
PORT = 8887 # port of load balancer

# Define a list of servers
data_list_ip   = [ '127.0.0.1' , '127.0.0.1' ] # the indexes of ips and ports have to match!
data_list_port = [  8888       ,  8889       ] # add more servers if needed

current_index  = 0

def handle_client(client_socket): # send the server to redirect a client
    global current_index

    # Get the value from the list based on the current index
    port = data_list_port[current_index]
    ip = data_list_ip[current_index]

    data_to_send = f"{ip}:{port}"

    # Increment the index for the next connection
    current_index = (current_index + 1) % len(data_list_ip)

    # Send the value to the client
    client_socket.sendall(str(data_to_send).encode())
    print("Sent client to " + str(data_to_send))

    # Close the connection
    client_socket.close()

def start_server(ip, port): #ip is string
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((ip, port))

    # Listen for incoming connections
    server_socket.listen()
    print(f"Load balancing listening on address {ip}:{port}...")

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server(SERVER_IP, PORT)