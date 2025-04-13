import socket
import threading
import secrets
import subprocess

def generate_secret():
    return secrets.token_hex(16)

def handle_client(client_socket, target_host, target_port):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.connect((target_host, target_port))
    while True:
        try:
            request = client_socket.recv(4096)
            if not request:
                break
            proxy_socket.sendall(request)
            response = proxy_socket.recv(4096)
            client_socket.sendall(response)
        except:
            break
    client_socket.close()
    proxy_socket.close()

def start_proxy(listen_port, target_host, target_port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', listen_port))
    server.listen(10)
    print(f"[+] پروکسی راه‌اندازی شد روی پورت {listen_port}")
    while True:
        client_socket, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, target_host, target_port))
        thread.start()

if __name__ == "__main__":
    print(">>> شروع ساخت پروکسی ساده ...")
    secret = generate_secret()
    port = 8888
    tg_ip = "149.154.167.50"  # یکی از سرورهای تلگرام
    tg_port = 443
    threading.Thread(target=start_proxy, args=(port, tg_ip, tg_port)).start()

    ip = subprocess.getoutput("curl -s https://ipinfo.io/ip")
    tg_link = f"tg://proxy?server={ip}&port={port}&secret=ee{secret}"
    print(f"\n[+] لینک اتصال تلگرام:\n{tg_link}")
