from flask import Flask, render_template, request
import socket

app = Flask(__name__)

def send_choice(player, choice):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 1234))
    s.sendall(f"{player}:{choice}".encode())
    result = s.recv(1024).decode()
    s.close()
    return result

@app.route("/player1", methods=["GET", "POST"])
def player1():
    result = ""
    if request.method == "POST":
        result = send_choice("player1", request.form["choice"])
    return render_template("play.html", player="Player 1", result=result)

@app.route("/player2", methods=["GET", "POST"])
def player2():
    result = ""
    if request.method == "POST":
        result = send_choice("player2", request.form["choice"])
    return render_template("play.html", player="Player 2", result=result)

if __name__ == "__main__":
    app.run()
