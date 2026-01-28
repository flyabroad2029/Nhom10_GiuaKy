import socket
import threading

HOST = "127.0.0.1"
PORT = 1234
lock = threading.Lock()

choices = {}
connections = {}

def get_result(c1, c2):
    if c1 == c2:
        return "HOA"
    if (c1 == "ROCK" and c2 == "SCISSORS") or \
       (c1 == "PAPER" and c2 == "ROCK") or \
       (c1 == "SCISSORS" and c2 == "PAPER"):
        return "BAN THANG"
    return "BAN THUA"

def handle_client(conn):
    try:
        data = conn.recv(1024).decode()
        player, choice = data.split(":")

        with lock:
            choices[player] = choice
            connections[player] = conn

            if len(choices) == 2:
                p1 = choices.get("player1")
                p2 = choices.get("player2")

                r1 = get_result(p1, p2)
                r2 = get_result(p2, p1)

                if "player1" in connections:
                    connections["player1"].sendall(r1.encode())
                if "player2" in connections:
                    connections["player2"].sendall(r2.encode())

                choices.clear()
                connections.clear()
    except:
        pass

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Socket Game Server dang chay...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    main()