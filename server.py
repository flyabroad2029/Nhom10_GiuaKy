import socket
import threading

# ================== CẤU HÌNH SERVER ==================
HOST = "127.0.0.1"   # Địa chỉ localhost
PORT = 1234          # Cổng server

# ================== BIẾN TOÀN CỤC ==================
choices = {}        # Lưu lựa chọn của từng người chơi
connections = {}    # Lưu socket kết nối của từng người chơi
lock = threading.Lock()  # Khóa để tránh xung đột luồng

# ================== HÀM XÁC ĐỊNH KẾT QUẢ ==================
def get_result(c1, c2):
    """
    Xác định kết quả Oẳn Tù Tì
    c1: lựa chọn người chơi 1
    c2: lựa chọn người chơi 2
    """
    if c1 == c2:
        return "HOA"

    # Luật thắng:
    # ĐÁ thắng KÉO
    # GIẤY thắng ĐÁ
    # KÉO thắng GIẤY
    if (c1 == "ROCK" and c2 == "SCISSORS") or \
       (c1 == "PAPER" and c2 == "ROCK") or \
       (c1 == "SCISSORS" and c2 == "PAPER"):
        return "BAN THANG"

    return "BAN THUA"

# ================== XỬ LÝ MỖI CLIENT ==================
def handle_client(conn):
    try:
        # Nhận dữ liệu từ client (định dạng: player:choice)
        data = conn.recv(1024).decode()

        # Kiểm tra dữ liệu hợp lệ
        if ":" not in data:
            conn.sendall("DU LIEU KHONG HOP LE".encode())
            conn.close()
            return

        player, choice = data.split(":")

        # Khóa luồng để tránh ghi đè dữ liệu
        with lock:
            choices[player] = choice
            connections[player] = conn

            # Khi đã có đủ 2 người chơi
            if len(choices) == 2:
                players = list(choices.keys())
                p1, p2 = players[0], players[1]

                # Tính kết quả cho từng người
                result_p1 = get_result(choices[p1], choices[p2])
                result_p2 = get_result(choices[p2], choices[p1])

                # Gửi kết quả về client
                connections[p1].sendall(result_p1.encode())
                connections[p2].sendall(result_p2.encode())

                # Đóng kết nối
                connections[p1].close()
                connections[p2].close()

                # Reset dữ liệu cho lượt chơi mới
                choices.clear()
                connections.clear()

    except Exception as e:
        print("Lỗi xử lý client:", e)

# ================== HÀM MAIN ==================
def main():
    # Tạo socket TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Socket Game Server đang chạy tại", HOST, ":", PORT)

    # Luôn chờ client kết nối
    while True:
        conn, addr = server.accept()
        print("Client kết nối từ:", addr)

        # Tạo luồng mới cho mỗi client
        threading.Thread(
            target=handle_client,
            args=(conn,),
            daemon=True
        ).start()

# ================== CHẠY SERVER ==================
if __name__ == "__main__":
    main()
