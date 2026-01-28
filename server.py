import socket
import threading

HOST = "127.0.0.1"
PORT = 1234

waiting = []


lock = threading.Lock()



def handle_client(conn):
    try:
        data = conn.recv(1024).decode()   # player:choice
        player, choice = data.split(":")

        with lock:
            choices[player] = choice
            connections[player] = conn

    except:
        pass

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Socket Game Server dang chay...")

    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    main()
