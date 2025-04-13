import os
import subprocess
import secrets

def install_packages():
    os.system("pkg update -y && pkg upgrade -y")
    os.system("pkg install git curl make clang -y")

def download_mtproxy():
    if not os.path.exists("MTProxy"):
        os.system("git clone https://github.com/TelegramMessenger/MTProxy")
    os.chdir("MTProxy")
    os.system("make")

def generate_secret():
    return secrets.token_hex(16)

def run_proxy(port, secret):
    cmd = f"./objs/bin/mtproto-proxy -u nobody -p {port} -H {port} -S {secret} --aes-pwd proxy-secret proxy-multi.conf -M 1"
    print(f"\n[+] اجرای دستور:\n{cmd}\n")
    subprocess.Popen(cmd, shell=True)

def get_ip():
    return subprocess.getoutput("curl -s https://ipinfo.io/ip")

def main():
    print(">> نصب پیش‌نیازها ...")
    install_packages()

    print(">> دانلود و ساخت MTProxy ...")
    download_mtproxy()

    print(">> تولید secret ...")
    secret = generate_secret()
    
    port = input(">> پورت دلخواهت رو وارد کن (مثلاً 443): ").strip()

    print(">> اجرای پروکسی ...")
    run_proxy(port, secret)

    ip = get_ip()
    tg_link = f"tg://proxy?server={ip}&port={port}&secret=ee{secret}"
    print("\n[+] پروکسی ساخته شد!")
    print("[+] لینک اتصال تلگرام:")
    print(tg_link)

if __name__ == "__main__":
    main()
