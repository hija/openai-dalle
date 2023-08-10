from io import BytesIO
import shutil
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import requests
import openai
import os
from PIL import ImageTk, Image
import dotenv
import urllib3

dotenv.load_dotenv(dotenv.find_dotenv())
generate_image_url = None

def generate_image():
    global generate_image_url
    prompt = prompt_entry.get()

    # Setze deine OpenAI API-Zugriffstoken
    openai.api_key = os.environ.get('OPENAI_KEY', None)

    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024"
    )
    image_url = response['data'][0]['url']
    
    generate_image_url = image_url
    update_image(generate_image_url)

def update_image(url):
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((300, 300))  # Anpassen der Größe nach Bedarf
    photo = ImageTk.PhotoImage(img)
    image_label.configure(image=photo)
    image_label.image = photo

# Methode zum Speichern des Bildes
def download_image():   
    if generate_image_url is None:
        messagebox.showerror("Fehler", "Es wurde noch kein Bild generiert.")
        return

    try:
        # Bild von der URL herunterladen
        response = requests.get(generate_image_url, stream=True)
    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Herunterladen des Bildes: {e}")
        return
    
    # Auswählen des Speicherorts und Dateinamens mit Tkinter
    filepath = filedialog.asksaveasfilename(defaultextension=".jpg")
    if not filepath:
        messagebox.showerror("Fehler", "Es wurde kein Filepath ausgewählt")
        return
    
    try:
        # Bild in der ausgewählten Datei speichern
        with open(filepath, "wb") as f:
            shutil.copyfileobj(response.raw, f)

        messagebox.showinfo("Erfolgreich", "Bild wurde abgespeichert!")
    except Exception as e:
        print("Fehler beim Speichern des Bildes:", e)
        messagebox.showerror("Fehler", f"Fehler beim Speichern des Bildes: {e}")
    

# GUI erstellen
window = tk.Tk()
window.title("Bildgenerator")

# Eingabefeld
prompt_label = tk.Label(window, text="Prompt:")
prompt_label.pack()
prompt_entry = tk.Entry(window)
prompt_entry.pack()

# Button zum Generieren des Bildes
generate_button = tk.Button(window, text="Bild generieren", command=generate_image)
generate_button.pack()

# Button zum Speichern des Bildes
save_button = tk.Button(window, text="Bild speichern", command=download_image)
save_button.pack()

# Anzeige des generierten Bildes
image_label = tk.Label(window)
image_label.pack()

# GUI starten
window.mainloop()