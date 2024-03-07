# run_client.py
import sys
import Application.utilities as utils
from Application.client import *

APP_TITLE = "Note Taking"

SERVER_IP = '127.0.0.1' # ip of load balancer
PORT = 8887 # port of load balancer

# Define a list of servers (in case load balancer is down)
data_list_ip   = [ '127.0.0.1' , '127.0.0.1' ] # the indexes of ips and ports have to match!
data_list_port = [  8888       ,  8889       ] # add more servers if needed

def show_unauthenticated_menu():
    utils.clear_console()
    print(f"\n--- Menu - {APP_TITLE} ---\n")
    print("1. Authenticate")
    print("2. Register")
    print("0. Exit")

def auth(mode, client_socket):
    utils.clear_console()
    print(f"\nWelcome to {APP_TITLE}!\n")
    print(f"--- Please {mode}. ---")

    username = input("Username: ")
    password = input("Password: ")

    res = send_name(client_socket, username, password, mode)

    return res

def show_authenticated_menu(username):
    utils.clear_console()
    print(f"\n--- Menu - {APP_TITLE} - Welcome {username} ---\n")
    print("1. Create a new note")
    print("2. My notes")
    print("3. Delete note")
    print("0. Exit")

def restart_connection(client_socket):
    #Restart connection
    client_socket.close()
    main()

def direct_connect():
    connection_token = False # to check the connection
    idx = 0
    while not connection_token:
        try:
            print(f"Trying server {idx + 1}...")
            client_socket = connect_to_server(data_list_ip[idx], data_list_port[idx])
            connection_token = True
        except:            
            print(f"Something went wrong with the connection. Trying next server...")

            idx += 1
            
            if(idx >= len(data_list_ip)):
                print(f"\n{APP_TITLE} is currently down.\t\nGoodbye!\n")
                sys.exit()

    return client_socket


def main():
    # ----- Connection Process ---------
    connection_token = False # to check the connection
    timeout = 0 # after 5 tries connect directly to servers
    while not connection_token:
        try:
            server_addr = get_loadbalancer_addr(SERVER_IP, PORT) # get port and ip from the server that LB redirect us (list -> ['0.0.0.0', 0000])
            client_socket = connect_to_server(server_addr[0], server_addr[1])
            connection_token = True
        except:
            if(timeout < 5):
                print(f"Trying {timeout}... Something went wrong with the connection. Trying again...")
            else:
                print(f"Trying {timeout}... Something went wrong with the load balancer or the servers. Trying to connect to servers directly...")
                client_socket = direct_connect()
                connection_token = True

            timeout += 1
    #-----------------------------
            
    # ----- Authentication Process ---------
    while True:
        show_unauthenticated_menu()
        
        choice = input("\nPlease choose an option: ")

        if(choice == "1"):
            res = auth("authenticate", client_socket)

            if(res == "AUTH_FAILED"):
                print("\nAuthetication failed. Please try again.")
                input("Press Enter to continue...")
                restart_connection(client_socket)
            else:
                break

        elif(choice == "2"):
            res = auth("register", client_socket)

            if(res == "AUTH_FAILED"):
                print("\nRegistration failed. Please try another username.")
                input("Press Enter to continue...")
                restart_connection(client_socket)
            else:
                break

        elif(choice == "0"):
            utils.clear_console()
            print(f"\nClosing client.\nThank you for using {APP_TITLE}!\n")
            client_socket.close()
            break
        else:
            print("\nWrong option. Please try again.\n")
            input("Press Enter to continue...")

    #-----------------------------
            
    # NOTE: server commands only work with the client authenticated 
    # Main loop (enters loop with client already authenticated)
            
    while True:
        show_authenticated_menu(res)

        choice = input("\nPlease choose an option: ")

        if choice == "1": #Create note
            utils.clear_console()
            note_title = input("\nInsert a title: ")
            note_content = input("\nStart writing: \n")
            create_note(client_socket, note_title, note_content)

        elif choice == "2": #List all notes of the authenticated user
            utils.clear_console()
            if(list_notes(client_socket) == 0): # check for no notes
                lock = 0
                while lock == 0:
                    utils.clear_console()
                    list_notes(client_socket)
                    try:
                        sub_choice = int(input("\nSelect a note by index to view - or - 0 to exit: "))
                    except:
                        print("Please, input only a number.")

                    if(sub_choice == 0):
                        lock = 1
                    else:
                        utils.clear_console()
                        list_note(client_socket, sub_choice)

        elif choice == "3": #Delete a note according an given index
            utils.clear_console()
            list_notes(client_socket)
            note_index = input("\nIndex of note to be erased: ")
            delete_note(client_socket, note_index)

        elif choice == "0": #Close connection and exit application
            utils.clear_console()
            print(F"\nClosing client.\n Thank you for using {APP_TITLE}!\n")
            client_socket.close()
            break

        else: # Wrong input
            print("\nWrong option. Please try again.\n")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Forced exit. Goodbye!")
    finally:
        sys.exit()