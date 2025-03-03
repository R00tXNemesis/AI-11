import re
import requests
import sys
import time
from bs4 import BeautifulSoup

# Warna untuk efek terminal hacker
GREEN = "\033[92m"
RED = "\033[91m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Fungsi efek mengetik seperti di film hacker (DIPERBAIKI)
def type_effect(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)  # Mencetak satu karakter pada satu waktu
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Pindah ke baris baru setelah selesai

# Tampilan awal
banner = f"""{GREEN}
███╗   ██╗ ██████╗ ███████╗███╗   ██╗██╗  ██╗███████╗
████╗  ██║██╔═══██╗██╔════╝████╗  ██║██║  ██║██╔════╝
██╔██╗ ██║██║   ██║███████╗██╔██╗ ██║███████║███████╗
██║╚██╗██║██║   ██║╚════██║██║╚██╗██║██╔══██║╚════██║
██║ ╚████║╚██████╔╝███████║██║ ╚████║██║  ██║███████║
╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝
{RESET}
{RED}[!] Security Audit Tool - Termux Edition [!]{RESET}
"""
type_effect(banner)

# Autentikasi awal
password = input("\n" + BLUE + "[+] Masukkan password untuk mengakses alat: " + RESET)
if password != "admin234":
    print(RED + "[!] Password salah! Keluar..." + RESET)
    sys.exit()

print(GREEN + "[✓] Akses diberikan! Memulai pengecekan..." + RESET)
time.sleep(1)

# Meminta input URL
url = input("\n" + BLUE + "[+] Masukkan URL target (contoh: https://example.com): " + RESET)

# Fungsi untuk mengambil data dari website
def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        print(RED + "[!] Gagal mengakses website. Periksa URL dan koneksi internet." + RESET)
        sys.exit()

# Fungsi untuk memprediksi kemungkinan password
def predict_passwords(email):
    print(YELLOW + f"\n[~] Memprediksi kemungkinan password untuk {email}..." + RESET)
    common_passwords = [
        "123456", "password", "qwerty", "iloveyou", "admin123",
        email.split("@")[0] + "123", email.split("@")[0] + "2024"
    ]
    for pwd in common_passwords:
        print(RED + f"- {pwd}" + RESET)

# Scraping website
print(YELLOW + "[~] Mengambil data dari website..." + RESET)
html_content = scrape_website(url)

# Parsing HTML dengan BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")
text_content = soup.get_text()

# Mencari username, email, password, nomor telepon, dan alamat dengan regex
emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text_content)
phones = re.findall(r"\+?\d{1,4}[-.\s]?\d{2,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}", text_content)
passwords = re.findall(r"(password|passwd|pwd)\s*[:=]\s*([^\s]+)", text_content, re.IGNORECASE)
usernames = re.findall(r"(username|user|uname)\s*[:=]\s*([^\s]+)", text_content, re.IGNORECASE)
addresses = re.findall(r"(alamat|address|lokasi)\s*[:=]\s*([^\n,]+)", text_content, re.IGNORECASE)

# Menampilkan hasil dengan batasan agar tidak terlalu panjang
print("\n" + BLUE + "[+] Hasil Pengecekan:" + RESET)
print(GREEN + f"- Username: {(usernames[0][1] if usernames else 'Tidak ada kebocoran')}" + RESET)
print(GREEN + f"- Email: {(emails[0] if emails else 'Tidak ada kebocoran')}" + RESET)

if passwords:
    print(GREEN + f"- Password: {passwords[0][1]}" + RESET)
else:
    print(RED + "- Password: Tidak ditemukan!" + RESET)
    if emails:
        predict_passwords(emails[0])

print(GREEN + f"- No. Telepon: {(phones[0] if phones else 'Tidak ada kebocoran')}" + RESET)
print(GREEN + f"- Alamat: {(addresses[0][1] if addresses else 'Tidak ada kebocoran')}" + RESET)

print("\n" + BLUE + "[✓] Selesai! Pastikan data aman." + RESET)