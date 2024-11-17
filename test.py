import tkinter as tk
from PIL import Image, ImageTk
from gtts import gTTS
import os
import requests
from io import BytesIO
from tkinter import messagebox
import webbrowser
import speech_recognition as sr
import json
from tkinter import ttk
import psutil
import socket
from tkinter import font
import subprocess  
import ftplib
import os
import sys
import urllib.request

class Lernprojekt:
    
    def __init__(self):
       # ...

   


        self.root = tk.Tk()
        self.root.title  ("Lernerforscher")
        self.root.geometry("1600x1900")
        self.root.configure(bg="orange")
        self.aufgaben = []  # Liste zum Speichern der Aufgaben
        self.aufgaben_datei = "aufgaben.json"  # Datei zum Speichern der Aufgaben
     
        
        self.benutzer = self.lade_benutzer()
        self.aktueller_benutzer = None
        self.admin_passwort = "admin123"  # Setzen Sie ein starkes Admin-Passwort
        
        self.Startseite()
    
        
        self.Startseite()
      
        
        self.einstellungen = {
            "ton_aktiviert": True,
            "schwierigkeitsgrad": "normal"
        }
        
        self.aufgaben = []
        self.aufgaben_datei = "aufgaben.json"
        
        #self.lade_aufgaben()
        self.lade_ergebnisse()
        
        self.anmeldebildschirm()

    def lade_benutzer(self):
        try:
            with open("benutzer.json", "r") as datei:
                return json.load(datei)
        except FileNotFoundError:
            return {}

    def speichere_benutzer(self):
        with open("benutzer.json", "w") as datei:
            json.dump(self.benutzer, datei)

    def anmeldebildschirm(self):
        self.loesche_aktuelles_frame()
        
        tk.Label(self.root, text="Benutzername:", bg="orange").pack()
        self.benutzername_eingabe = tk.Entry(self.root)
        self.benutzername_eingabe.pack()
        
        tk.Label(self.root, text="Passwort:", bg="orange").pack()
        self.passwort_eingabe = tk.Entry(self.root, show="*")
        self.passwort_eingabe.pack()
        
        tk.Button(self.root, text="Anmelden", command=self.anmelden).pack()
        tk.Button(self.root, text="Admin-Anmeldung", command=self.admin_anmeldung).pack()

    def anmelden(self):
        benutzername = self.benutzername_eingabe.get()
        passwort = self.passwort_eingabe.get()
        
        if benutzername in self.benutzer and self.benutzer[benutzername]["passwort"] == passwort:
            self.aktueller_benutzer = benutzername
            self.Startseite()
        else:
            messagebox.showerror("Fehler", "Ungültige Anmeldedaten")

    def admin_anmeldung(self):
        passwort = self.passwort_eingabe.get()
        if passwort == self.admin_passwort:
            self.aktueller_benutzer = "admin"
            self.admin_panel()
        else:
            messagebox.showerror("Fehler", "Ungültiges Admin-Passwort")

    def admin_panel(self):
        self.loesche_aktuelles_frame()
        
        tk.Button(self.root, text="Benutzer hinzufügen", command=self.benutzer_hinzufuegen).pack()
        tk.Button(self.root, text="Benutzer löschen", command=self.benutzer_loeschen).pack()
        tk.Button(self.root, text="Passwort zurücksetzen", command=self.passwort_zuruecksetzen).pack()
        tk.Button(self.root, text="Rechte verwalten", command=self.rechte_verwalten).pack()
        tk.Button(self.root, text="Überwachung", command=self.admin_ueberwachung).pack()
        tk.Button(self.root, text="Zurück", command=self.anmeldebildschirm).pack()

    def benutzer_hinzufuegen(self):
        self.loesche_aktuelles_frame()
        
        tk.Label(self.root, text="Neuer Benutzername:", bg="orange").pack()
        neuer_benutzername = tk.Entry(self.root)
        neuer_benutzername.pack()
        
        tk.Label(self.root, text="Neues Passwort:", bg="orange").pack()
        neues_passwort = tk.Entry(self.root, show="*")
        neues_passwort.pack()
        
        tk.Button(self.root, text="Hinzufügen", command=lambda: self.benutzer_hinzufuegen_aktion(neuer_benutzername.get(), neues_passwort.get())).pack()

    def benutzer_hinzufuegen_aktion(self, benutzername, passwort):
        if benutzername and passwort:
            if benutzername not in self.benutzer:
                self.benutzer[benutzername] = {"passwort": passwort, "rechte": []}
                self.speichere_benutzer()
                messagebox.showinfo("Erfolg", f"Benutzer {benutzername} wurde hinzugefügt.")
                self.admin_panel()
            else:
                messagebox.showerror("Fehler", "Benutzername existiert bereits.")
        else:
            messagebox.showerror("Fehler", "Benutzername und Passwort dürfen nicht leer sein.")

    def benutzer_loeschen(self):
        self.loesche_aktuelles_frame()
        
        tk.Label(self.root, text="Zu löschender Benutzername:", bg="orange").pack()
        zu_loeschender_benutzer = tk.Entry(self.root)
        zu_loeschender_benutzer.pack()
        
        tk.Button(self.root, text="Löschen", command=lambda: self.benutzer_loeschen_aktion(zu_loeschender_benutzer.get())).pack()

    def benutzer_loeschen_aktion(self, benutzername):
        if benutzername in self.benutzer:
            del self.benutzer[benutzername]
            self.speichere_benutzer()
            messagebox.showinfo("Erfolg", f"Benutzer {benutzername} wurde gelöscht.")
            self.admin_panel()
        else:
            messagebox.showerror("Fehler", "Benutzername nicht gefunden.")

    def passwort_zuruecksetzen(self):
        self.loesche_aktuelles_frame()
        
        tk.Label(self.root, text="Benutzername:", bg="orange").pack()
        benutzername = tk.Entry(self.root)
        benutzername.pack()
        
        tk.Label(self.root, text="Neues Passwort:", bg="orange").pack()
        neues_passwort = tk.Entry(self.root, show="*")
        neues_passwort.pack()
        
        tk.Button(self.root, text="Zurücksetzen", command=lambda: self.passwort_zuruecksetzen_aktion(benutzername.get(), neues_passwort.get())).pack()

    def passwort_zuruecksetzen_aktion(self, benutzername, neues_passwort):
        if benutzername in self.benutzer:
            self.benutzer[benutzername]["passwort"] = neues_passwort
            self.speichere_benutzer()
            messagebox.showinfo("Erfolg", f"Passwort für {benutzername} wurde zurückgesetzt.")
            self.admin_panel()
        else:
            messagebox.showerror("Fehler", "Benutzername nicht gefunden.")

    def rechte_verwalten(self):
        self.loesche_aktuelles_frame()
        
        tk.Label(self.root, text="Benutzername:", bg="orange").pack()
        benutzername = tk.Entry(self.root)
        benutzername.pack()
        
        rechte = ["aufgaben_erstellen", "nutzer_hinzufuegen"]
        rechte_vars = {}
        
        for recht in rechte:
            var = tk.BooleanVar()
            tk.Checkbutton(self.root, text=recht, variable=var).pack()
            rechte_vars[recht] = var
        
        tk.Button(self.root, text="Rechte aktualisieren", command=lambda: self.rechte_aktualisieren(benutzername.get(), rechte_vars)).pack()

    def rechte_aktualisieren(self, benutzername, rechte_vars):
        if benutzername in self.benutzer:
            neue_rechte = [recht for recht, var in rechte_vars.items() if var.get()]
            self.benutzer[benutzername]["rechte"] = neue_rechte
            self.speichere_benutzer()
            messagebox.showinfo("Erfolg", f"Rechte für {benutzername} wurden aktualisiert.")
            self.admin_panel()
        else:
            messagebox.showerror("Fehler", "Benutzername nicht gefunden.")

    def admin_ueberwachung(self):
        if self.aktueller_benutzer != "admin":
            messagebox.showerror("Fehler", "Nur der Admin hat Zugriff auf diese Funktion.")
            return
        
        self.loesche_aktuelles_frame()
        
        self.ueberwachung_label = tk.Label(self.root, text="Admin-Überwachung", bg="orange", font=("Arial", 22))
        self.ueberwachung_label.pack(anchor="center")
        
        for benutzer, ergebnisse in self.ergebnisse.items():
            benutzer_label = tk.Label(self.root, text=f"Benutzer: {benutzer}", bg="orange", font=("Arial", 18))
            benutzer_label.pack()
            
            for ergebnis in ergebnisse:
                ergebnis_label = tk.Label(self.root, text=f"{ergebnis['aufgabe']}: {ergebnis['ergebnis']}", bg="orange", font=("Arial", 14))
                ergebnis_label.pack()
            
            tk.Label(self.root, text="", bg="orange").pack()  # Leerzeile zwischen Benutzern
        
        self.zurueck_button = tk.Button(self.root, text="Zurück", font=("Arial", 18), command=self.admin_panel, width=20)
        self.zurueck_button.pack()

    def speichere_ergebnis(self, aufgabe, ergebnis):
        if not hasattr(self, 'ergebnisse'):
            self.ergebnisse = {}
        if self.aktueller_benutzer not in self.ergebnisse:
            self.ergebnisse[self.aktueller_benutzer] = []
        self.ergebnisse[self.aktueller_benutzer].append({"aufgabe": aufgabe, "ergebnis": ergebnis})
        self.speichere_ergebnisse()

    def speichere_ergebnisse(self):
        with open("ergebnisse.json", "w") as datei:
            json.dump(self.ergebnisse, datei)

    def lade_ergebnisse(self):
        try:
            with open("ergebnisse.json", "r") as datei:
                self.ergebnisse = json.load(datei)
        except FileNotFoundError:
            self.ergebnisse = {}

            
    def is_connected_to_wifi():
        try:
            # Überprüfen Sie die Verbindung zu einer öffentlichen Website
            socket.gethostbyname("www.google.com")
            return True
        except socket.error:
            return False
    
    # Speicherplatz überprüfen (mindestens 1 GB)
    def check_disk_space():
        disk_usage = psutil.disk_usage('/')
        return disk_usage.free >= 1 * 1024 * 1024 * 1024  # 1 GB in Bytes
    
    # Arbeitsspeicher überprüfen (mindestens 1 GB)
    def check_memory():
        memory = psutil.virtual_memory()
        return memory.available >= 1 * 1024 * 1024 *1024   # 1 GB in Bytes

    errors = []

    if not is_connected_to_wifi():
        errors.append("Kein WLAN verfügbar.")
    if not check_disk_space():
        errors.append("Nicht genügend Speicherplatz (mindestens 1 GB benötigt).")
    if not check_memory():
        errors.append("Nicht genügend Arbeitsspeicher (mindestens 1 GB benötigt).")

    if errors:
        messagebox.showerror("Fehler", "\n".join(errors))
    else:
        messagebox.showinfo("Überprüfung erfolgreich", "Alle Anforderungen sind erfüllt!")

# Button zur Überprüfung




    def zeige_info(self):
        # Zeigt eine Messagebox mit Informationen über das Programm an
        messagebox.showinfo("Über", "Deutsch Erforscher\nVersion 1.0\nEin Lernprojekt.")

    def loesche_aktuelles_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def Startseite(self):
       pass       
    def loesche_aktuelles_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

   

    def Startseite(self):
        
        self.loesche_aktuelles_frame()
        # Menüleiste erstellen
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        font_settings = font.Font(size=14)  # Schriftgröße hier einstellen

        # Menü "Datei" hinzufügen
        datei_menu = tk.Menu(self.menu_bar, tearoff=0, font=font_settings)
        # Menü "Datei" hinzufügen
         
        self.menu_bar.add_cascade(label="Datei", menu=datei_menu)
        datei_menu.add_command(label="Startseite", command=self.Startseite)


        datei_menu.add_separator()
        datei_menu.add_command(label="Übungen",command=self.menü)

        datei_menu.add_separator()
        datei_menu.add_command(label="Beenden", command=self.root.quit)

        datei_menu.add_separator()
        datei_menu.add_command(label="Admin",command=self.admin)
        datei_menu.add_separator()
        datei_menu.add_command(label="Update", command=self.Update) 
    

        #2 LEISTE----------------------------------------------------------------------

        font_settings = font.Font(size=14)  # Schriftgröße hier einstellen

        # Menü "Datei" hinzufügen
        datei_menu = tk.Menu(self.menu_bar, tearoff=0, font=font_settings)

        self.menu_bar.add_cascade(label="Aufgaben", menu=datei_menu)
        datei_menu.add_command(label="Aufgaben erstellen", command=self.aufgaben_erstellen)
        
        datei_menu.add_separator()
        datei_menu.add_command(label="Importieren",command=self.importieren)
        

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.willkommen = tk.Label(self.root, text="Willkommen  im Deutschkurs", bg="orange",font=("Arial", 30,))
        self.willkommen.pack(anchor="center")
        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()


        self.Startseite_unterschrift = tk.Label(self.root, text="Viel spaß beim lernen",fg="black",bg="orange", font=("Arial", 25,"italic"))
        self.Startseite_unterschrift.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()


        

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        #self.coin_shop=tk.Button(self.root,text="Shop",font=("Arial",18),command=self.shop,width=18)
       # self.coin_shop.pack(anchor="center")
     

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.der_die_das=tk.Button(self.root,text="Der/Die/Das",font=("Arial",18),command=self.satzartikel,width=18)
        self.der_die_das.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.Neues_lernen=tk.Button(self.root,text="Deutschtest",font=("Arial",18),command=self.Deutschtest,width=18) 
        self.Neues_lernen.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.aufgaben_neu=tk.Button(self.root,text="Neue aufgaben",font=("Arial",18),command=self.aufgaben_loesen,width=18)
        self.aufgaben_neu.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.neue_funktion_ueberschrifft=tk.Button(self.root,text="Was ist neu!!",fg="red",font=("fett",18),command=self.neue_funktion,width=18)
        self.neue_funktion_ueberschrifft.pack(anchor="center")

        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
    

        # Erstelle einen Button zum Öffnen des E-Mail-Programms
        self.email_button = tk.Button(self.root, text="Fehler melden",font=("Arial",18), command=self.open_email_program,width=18)
        self.email_button.pack(anchor="center")

        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        

        self.Sprachuebungen = tk.Button(self.root, text="Start ->", font=("Arial", 20), command=self.alphabet_a_z,width=22)
        self.Sprachuebungen.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()


   




    def satzartikel(self):
        self.loesche_aktuelles_frame()

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Menü "Datei" hinzufügen
        font_settings = font.Font(size=14)  # Schriftgröße hier einstellen

        # Menü "Datei" hinzufügen
        datei_menu = tk.Menu(self.menu_bar, tearoff=0, font=font_settings)
        

        self.menu_bar.add_cascade(label="Datei", menu=datei_menu)
        datei_menu.add_command(label="Startseite", command=self.Startseite)
        
        
        datei_menu.add_separator()
        datei_menu.add_command(label="Menü", command=self.menü)


        self.überschrifft_der_die_das=tk.Label(self.root,text="Der/Die/Das",bg="orange",font=("Arial",22))
        self.überschrifft_der_die_das.pack(anchor="center")
        
        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        
        self.Hund_LABEL=tk.Label(self.root,text="Hund",bg="red",font=("Arial",20))
        self.Hund_LABEL.pack(anchor="center")

        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.Hund_Button=tk.Button(text="Der",font=("Arial",17),command=self.Der_Hund,width=20)
        self.Hund_Button.pack(anchor="center")
       
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.Hund_Button_die=tk.Button(text="Die",font=("Arial",17),command=self.Falsche_Antwort,width=20)
        self.Hund_Button_die.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        

        self.Hund_Button_das=tk.Button(text="Das",font=("Arial",17),command=self.Falsche_Antwort,width=20)
        self.Hund_Button_das.pack(anchor="center")



    def Der_Hund(self):
        messagebox.showinfo("Antwort","Richtig")
        self.Die_Katze()
    def Falsche_Antwort(self):

      messagebox.showinfo("Antwort","Deine Antwort war Falsch")
      self.satzartikel()
        
    def Die_Katze(self):
        self.loesche_aktuelles_frame()

        self.Katze_Label=tk.Label(text="Katze",bg="red",font=("Arial",17))
        self.Katze_Label.pack(anchor="center") #
        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.der_Katze=tk.Button(text="Der",font=("Arial",17),command=self.Falsche_Antwort,width=17)
        self.der_Katze.pack(anchor="center") #

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.die_Katze=tk.Button(text="Die",font=("Arial",17),command=self.Maus,width=17)
        self.die_Katze.pack(anchor="center")



    def open_email_program(self):
        # Öffne das Standard-E-Mail-Programm mit der E-Mail-Adresse als Empfänger
        email_address = "swinters1996@gmail.com"
        webbrowser.open(f"mailto:{email_address}")


        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        
    def lesen(self):
        self.loesche_aktuelles_frame()
        self.lesen_aufgabe=tk.Label(self.root,text="Verfolständige den Satz",bg="orange",font=("Arial",20))
        self.lesen_aufgabe.pack(anchor="center")

        self.lesen_aufgabe1=tk.Label(self.root,text="Ich bin --- Auto",font=("Arial",20),bg="orange")
        self.lesen_aufgabe1.pack(anchor="center")

        self.absatz=tk.Label(text="",bg="orange")
        self.absatz.pack()


        self.eingabe_lesen=tk.Entry(font=("Arial",16))
        self.eingabe_lesen.pack(anchor="center")

        self.absatz=tk.Label(text="",bg="orange")
        self.absatz.pack()
        
        self.absatz=tk.Label(text="",bg="orange")
        self.absatz.pack()

        self.lesen_aufgabe1_button=tk.Button(self.root,text="überprüfen",command=self.lesen_logik,width=20)
        self.lesen_aufgabe1_button.pack(anchor="center")

        #Weiterleittung geht noch nicht ------------------------------------------------------------------------------------------------------------------------

    def lesen_logik(self):
        eingabe = self.eingabe_lesen.get()


            
        if eingabe == "Ich bin ein Auto":
            self.sätze_verfolständigen
        elif eingabe == "":
            messagebox.showerror("Fehler", "Bitte eine Antwort angeben")
        else:
            self.falsch_antwort()
    
    def sätze_verfolständigen(self):
        self.loesche_aktuelles_frame()
        self.sätze_aufgaben_überschrifft=tk.Label(self.root,text="Vervolständige den satz",font=("Arial",20))
        self.sätze_aufgaben_überschrifft.pack(anchor="center")
        
        self.absatz=tk.Label()
        self.absatz.pack()
        
        self.sätze_aufgabe1=tk.Label(self.root,text="Meine Katze---Fröhlich")
        self.sätze_aufgabe1.pack(anchor="center")

        self.sätze_aufgabe1_eingabefeld=tk.Entry(self.root,text="")
        self.sätze_aufgabe1_eingabefeld.pack(anchor="center")

        self.sätze_aufgabe1_Button=tk.Button(self.root,text="Überprüfen",command=self.sätze_aufgabe1_logik,width=22)
        self.sätze_aufgabe1_Button.pack(anchor="center")
    def sätze_aufgabe1_logik (self):
        eingabe= self.sätze_aufgabe1_eingabefeld.get()
        if eingabe == "Mein Katze ist Fröhlich":
            messagebox.showinfo("Antwort","Richtig")
            self.Sätze_aufgabe2
        elif eingabe=="":
            messagebox.showerror("Warnung","Eingabe Fehlt")
        else:
            messagebox.showinfo("Antwort","Leider Falsch")
    def Sätze_aufgabe2(self):
        pass
    #ENDE-------------------------------------------------------------------------------------------------------------------------------------------------

  
        
        self.neue_funktion_ueberschrifft=tk.Button(self.root,text="Was ist neu",fg="red",font=("Arial",16),command=self.neue_funktion,width=22)
        self.neue_funktion_ueberschrifft.pack(anchor="se")


        self.Sprachuebungen = tk.Button(self.root, text="Start ->",fg="red", font=("Arial", 20), width=25, command=self.Lerne_das_a)
        self.Sprachuebungen.pack(anchor="center")

    def Deutschtest(self):
        self.loesche_aktuelles_frame()
        


        text = "Kamel"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.aufgabe1_deutschtest=tk.Label(text="Schreibe was du Gehört hasst",bg="orange",font=("Arial",22))
        self.aufgabe1_deutschtest.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()


        self.aufgabe1_deutschtest_button=tk.Button(self.root,text="Kamel",font=("Arial",22),command=self.deutschtest_aufgabe2,width=17)
        self.aufgabe1_deutschtest_button.pack()

        self.aufgabe1_deutschtest_button2=tk.Button(self.root,text="Esel",font=("Arial",22),command=self.Falsche_antwort,width=17)
        self.aufgabe1_deutschtest_button2.pack(anchor="center")
  

    def deutschtest_aufgabe2(self):
        self.loesche_aktuelles_frame()
        self.aufgabe2_deutschtest_überschrifft=tk.Label(text="Welches Wort fehlt",bg="orange",font=("Arial",22))
        self.aufgabe2_deutschtest_überschrifft.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.aufgabe1_deutschtest=tk.Label(text="Ich nach Hause",bg="orange",font=("Arial",20))
        self.aufgabe1_deutschtest.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        
       
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        
        self.aufgabe1_deutschtest_button=tk.Button(self.root,text="Möchte",font=("Arial",18),command=self.aufgabe2_deutschtest,width=17)
        self.aufgabe1_deutschtest_button.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        
        self.falsch_antwort=tk.Button(self.root,text="Bringe",font=("Arial",18),command=self.Falsche_antwort,width=17)
        self.falsch_antwort.pack(anchor="center")



    def aufgabe2_deutschtest(self):
        self.loesche_aktuelles_frame()
        
        self.aufgabe2_deutschtest_überschrifft=tk.Label(text="Welches wort ist Falsch geschrieben?",font=("Arial",20))
        self.aufgabe2_deutschtest_überschrifft.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.aufgabe3_deutschtest=tk.Button(self.root,text="Halo",font=("Arial",17),command=self.aufgabe4_deutschtest,width=17)
        self.aufgabe3_deutschtest.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.aufgabe3_deutschtest_falsche_antwort=tk.Button(self.root,text="Hallo",font=("Arial",17),command=self.Falsche_antwort,width=17)
        self.aufgabe3_deutschtest_falsche_antwort.pack(anchor="center")


    def aufgabe4_deutschtest(self):
        self.loesche_aktuelles_frame()

        self.aufgabe4_deutschtest_überschrifft=tk.Label(self.root,text="Was ist hier Falsch",bg="orange",font=("Arial",20))
        self.aufgabe4_deutschtest_überschrifft.pack(anchor="center")

        self.aufgabe4=tk.Label(text="Ich habe heute Geburtsag",font=("Arial",20),bg="orange")# das t fehlt
        self.aufgabe4.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.richtige_antwort_aufgabe4=tk.Button(self.root,text="Das T fehlt",font=("Arial",20),command=self.aufgabe5_deutschtest,width=17)
        self.richtige_antwort_aufgabe4.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        
        self.Falsche_antwort_aufgabe4=tk.Button(self.root,text="Das S fehlt",font=("Arial",20),command=self.Falsche_antwort,width=17)
        self.Falsche_antwort_aufgabe4.pack(anchor="center")

    def aufgabe5_deutschtest(self):
        self.loesche_aktuelles_frame()
        self.aufgabe5=tk.Label(text="Nehme dir jetzt ein Stifft und ein stück Papier und schreibe auf ein Zette was du Hörst",font=("Arial",20),bg="orange")
        self.aufgabe5.pack(anchor="center")
        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.aufgabe5_ok=tk.Button(self.root,text="Ok",font=("Arial",20),command=self.Ampel,width=22)
        self.aufgabe5_ok.pack(anchor="center")

    def Ampel(self):
        self.loesche_aktuelles_frame()

        text = "Tier"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.überschrifft_hören=tk.Label(text="Was hasst du Gehört",bg="orange",font=("Arial",22))
        self.überschrifft_hören.pack(anchor="center")

        self.Nächste_frage=tk.Button(self.root,text="Nächste aufgabe",font=("Arial",17),command=self.aufgabe6)
        self.Nächste_frage.pack(anchor="center")

    def aufgabe6(self):
        self.loesche_aktuelles_frame()
        
        self.überschrifft_hören_aufgabe6=tk.Label(text="Weitere aufgaben folgen",bg="orange",font=("Arial",22))
        self.überschrifft_hören_aufgabe6.pack(anchor="center")

        text ="Hallo"
        tts = gTTS(text,lang='de')
        tts.save("output.mp3")
        os.system("start output.mp3")

        self.Nächste_frage=tk.Button(self.root,text="Ende ",font=("Arial",17),command=self.ende,width=22)
        self.Nächste_frage.pack(anchor="center")

        self.Wiederholen_deutschtest=tk.Button(self.root,text="Wiederholen",font=("Arial",17),command=self.Deutschtest,width=15)
        self.Wiederholen_deutschtest.pack(anchor="center")
    def admin(self):
        self.loesche_aktuelles_frame()

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Menü "Datei" hinzufügen
        font_settings = font.Font(size=14)  # Schriftgröße hier einstellen

        # Menü "Datei" hinzufügen
        datei_menu = tk.Menu(self.menu_bar, tearoff=0, font=font_settings)
        

        self.menu_bar.add_cascade(label="Datei", menu=datei_menu)
        datei_menu.add_command(label="Aufgaben erstellen", command=self.aufgaben_erstellen)
        datei_menu.add_command(label="Importieren", command=self.importieren)
        datei_menu.add_separator()
        datei_menu.add_command(label="Startseite", command=self.Startseite)
        datei_menu.add_separator()
        datei_menu.add_command(label="Beenden", command=self.root.quit)


    


        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.einstellungen_überschrifft=tk.Label(self.root,text="Was möchtest du an Einstellungen vornehmen?",font=("Arial",12))
        self.einstellungen_überschrifft.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.einstellungen = tk.Button(self.root, text="Aufgabe erstellen", font=("Arial", 17), command=self.aufgaben_erstellen, width=22)
        self.einstellungen.pack(anchor="center")

        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.nutzer_hinzufügen=tk.Button(self.root,text="Nutzer hinzufügen",font=("Arial",17),command=self.anmeldebildschirm,width=22)
        self.nutzer_hinzufügen.pack(anchor="center")

             
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack(anchor="center")


    def nutzer(self):
        pass

    def aufgaben_erstellen(self):
        self.loesche_aktuelles_frame()

    

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        font_settings = font.Font(size=14)  # Schriftgröße hier einstellen

        # Menü "Datei" hinzufügen
        datei_menu = tk.Menu(self.menu_bar, tearoff=0, font=font_settings)
        

        self.menu_bar.add_cascade(label="Datei", menu=datei_menu)

        datei_menu.add_separator()
        datei_menu.add_command(label="Startseite", command=self.Startseite)

        datei_menu.add_command(label="Importieren", command=self.importieren)
        datei_menu.add_separator()

        datei_menu.add_command(label="Beenden", command=self.root.quit)

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()


        self.frage_label = tk.Label(self.root, text="Frage:", font=("Arial", 16))
        self.frage_label.pack()
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.frage_entry = tk.Entry(self.root, font=("Arial", 16))
        self.frage_entry.pack()
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.antwort_label = tk.Label(self.root, text="Antwort:", font=("Arial", 16))
        self.antwort_label.pack()
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.antwort_entry = tk.Entry(self.root, font=("Arial", 16))
        self.antwort_entry.pack()

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.fertig_button = tk.Button(self.root, text="Fertig",font=("Arial",16) ,command=self.speichern_aufgabe,width=16)
        self.fertig_button.pack()

    def speichern_aufgabe(self):
        frage = self.frage_entry.get()
        antwort = self.antwort_entry.get()

        if frage and antwort:
            aufgabe = {"frage": frage, "antwort": antwort}
            self.aufgaben.append(aufgabe)
            messagebox.showinfo("Erfolg", "Aufgabe gespeichert!")
            self.frage_entry.delete(0, tk.END)
            self.antwort_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warnung", "Bitte beide Felder ausfüllen.")
            
    def importieren(self):
    # Erstelle ein neues Fenster für den Ladebalken
     ladefenster = tk.Toplevel(self.root)
     ladefenster.title("Importieren")
    
    # Konfiguriere das Fenster für den Ladebalken
     ladefenster.geometry("300x100")
     ladefenster.transient(self.root)  # Fenster bleibt im Vordergrund

    # Ladebalken-Label
     label = tk.Label(ladefenster, text="Aufgaben werden importiert...")
     label.pack(pady=10)

    # Erstelle den Ladebalken
     progress_bar = ttk.Progressbar(ladefenster, orient="horizontal", mode="determinate", length=250)
     progress_bar.pack(pady=10)
     progress_bar["maximum"] = 100  # Maximalwert für den Ladebalken (100%)

    # Starte die Aktualisierung des Ladebalkens
     self.root.update_idletasks()
     for i in range(101):
        progress_bar["value"] = i  # Aktualisiere den Ladebalken
        self.root.update_idletasks()  # Aktualisiere das GUI-Layout
        self.root.after(15)  # Warte kurz, um den Fortschritt sichtbar zu machen

    # Aufgaben importieren, wenn der Ladebalken vollständig geladen ist
     if self.aufgaben:
        with open(self.aufgaben_datei, 'w') as f:
            json.dump(self.aufgaben, f)
        messagebox.showinfo("Importieren", "Aufgaben importiert!")
     else:
        messagebox.showwarning("Warnung", "Keine weiteren Aufgaben zum Importieren.")
        
    
    # Ladefenster schließen
     ladefenster.destroy()

    def loesche_aktuelles_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def aufgaben_loesen(self):
        self.loesche_aktuelles_frame()
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        font_settings = font.Font(size=14)  # Schriftgröße hier einstellen

        # Menü "Datei" hinzufügen
        datei_menu = tk.Menu(self.menu_bar, tearoff=0, font=font_settings)
        

        self.menu_bar.add_cascade(label="Datei", menu=datei_menu)
        datei_menu.add_command(label="Startseite", command=self.Startseite)
        datei_menu.add_command(label="Importieren", command=self.importieren)
        datei_menu.add_separator()
        datei_menu.add_command(label="Beenden", command=self.root.quit)
        
        if not self.aufgaben:
            messagebox.showwarning("Warnung", "Keine Aufgaben zum Lösen verfügbar.")
        
            return
           
        self.aktuelle_aufgabe_index = 0
        self.zeige_aufgabe()


    def zeige_aufgabe(self):
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        datei_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Datei", menu=datei_menu)
        datei_menu.add_command(label="Startseite", command=self.Startseite)
        datei_menu.add_command(label="Importieren", command=self.importieren)
        datei_menu.add_separator()
        datei_menu.add_command(label="Beenden", command=self.root.quit)
        

        if self.aktuelle_aufgabe_index < len(self.aufgaben):
            aufgabe = self.aufgaben[self.aktuelle_aufgabe_index]

            
            label = tk.Label(self.root, text="", bg="orange")
            label.pack()


            self.frage_label = tk.Label(self.root, text=aufgabe["frage"], font=("Arial", 20))
            self.frage_label.pack()

            label = tk.Label(self.root, text="", bg="orange")
            label.pack()

            self.antwort_entry = tk.Entry(self.root, font=("Arial", 18))
            self.antwort_entry.pack()
            
            label = tk.Label(self.root, text="", bg="orange")
            label.pack()
            label = tk.Label(self.root, text="", bg="orange")
            label.pack()

            self.pruefen_button = tk.Button(self.root, text="Antwort prüfen",font=("Arial",17), command=self.pruefen_antwort,width=20)
            self.pruefen_button.pack()
        else:
            self.frage_label = tk.Label(self.root, text="Keine weiteren Aufgaben!", font=("Arial", 16))
            self.frage_label.pack()
            

    def pruefen_antwort(self):
        user_antwort = self.antwort_entry.get()
        richtige_antwort = self.aufgaben[self.aktuelle_aufgabe_index]["antwort"]

        if user_antwort == richtige_antwort:
            messagebox.showinfo("Erfolg", "Richtige Antwort!")
        else:
            messagebox.showwarning("Falsch", f"Falsche Antwort! Die richtige Antwort ist: {richtige_antwort}")

        self.aktuelle_aufgabe_index += 1
        self.loesche_aktuelles_frame()
        self.zeige_aufgabe()

    def loesche_aktuelles_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def Fehlercode(self):
        self.loesche_aktuelles_frame()

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Menü "Datei" hinzufügen
        font_settings = font.Font(size=14)  # Schriftgröße hier einstellen

        # Menü "Datei" hinzufügen
        datei_menu = tk.Menu(self.menu_bar, tearoff=0, font=font_settings)
        

        self.menu_bar.add_cascade(label="Datei", menu=datei_menu)
        datei_menu.add_command(label="Startseite", command=self.Startseite)

        datei_menu.add_separator()
        datei_menu.add_command(label="Übungen",command=self.menü)

        datei_menu.add_separator()
        datei_menu.add_command(label="Beenden", command=self.root.quit)

        datei_menu.add_separator()
        datei_menu.add_command(label="Admin",command=self.admin)

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
    
        self.Fehlercode_text=tk.Label(text="Fehlercode: Netzwerk error ",font=("Arial",17))
        self.Fehlercode_text.pack(anchor="n")
 




    def Falsche_antwort(self):
        messagebox.showinfo("Warnug","Deine Antwort war falsch")
       


        


        

    def Lerne_das_a(self):

      
      
        #self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(A) Wie Ampel.jpeg")
        self.background_image_url = "https://i.ibb.co/Khf6vx5/A-Wie-Ampel.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

       

        # Hintergrundbild anzeigen
        
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.background_label.configure(bg="orange")


        text = "A Wie Ampel"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_ = tk.Button(self.root, text="weiter ->", font=("Arial", 24), command=self.lerne_das_a_seit2)
        self.button_.pack(anchor="se")
        
       

    def lerne_das_a_seit2(self):
        self.background_label.configure(bg="orange")

        self.loesche_aktuelles_frame()
        self.root.configure(bg="orange")
        
        #self.zurueck=tk.Button(self.root,text="Zurück",font=("Arial,14"),command=self.eingabefeld_lerne_das_a)
        #self.zurueck.pack(anchor="se")
        self.ueberschrifft2_lerne_das_a_seites=tk.Label(self.root,text="Frage1",bg="orange",font=("Arial",25))
        self.ueberschrifft2_lerne_das_a_seites.pack(anchor="center")
        
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
         


        self.ueberschrifft_lerne_das_a_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 18))
        self.ueberschrifft_lerne_das_a_seites.pack(anchor="center")

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()


        self.eingabefeld_lerne_das_a = tk.Entry(self.root, text="", font=("Arial", 20))
        self.eingabefeld_lerne_das_a.pack(anchor="center")

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_a_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

    def lerne_das_a_antwor_ueberpruefen(self):
        user_answer = self.eingabefeld_lerne_das_a.get()
    
        if user_answer == "A":
            self.lerne_das_b_seite1()
        elif messagebox.showerror("Warnung", "Versuch es erneut"):
                pass
        else:
            self.zeige_falsche_antwort_meldung3()

    def lerne_das_b_seite1(self):
       
# Beispielbild laden
        #self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(B) Wie Ball.jpeg")
        self.background_image_url = "https://i.ibb.co/v3zzBXC/B-Wie-Ball.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        text = "B Wie ball"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_b_seit2)
        self.button_lerne_das_b.pack(anchor="se")
        self.background_label.configure(bg="orange")

        self.root.configure(bg="orange")

    


    def lerne_das_b_seit2(self):

        self.loesche_aktuelles_frame()
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
        self.ueberschrifft_lerne_das_b_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange" ,font=("Arial", 18))
        self.ueberschrifft_lerne_das_b_seites.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
        self.eingabefeld_lerne_das_b = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_b.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 18),command=self.lerne_das_b_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
        

    def lerne_das_b_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_b.get()

        if user_answer == "B":
            self.lerne_das_c_seite_1()
        else:
            self.zeige_falsche_antwort_meldung3()

    def lerne_das_c_seite_1(self):
            
        #self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(C) Wie Camelion.jpeg")

        self.background_image_url = "https://i.ibb.co/9b8jgtF/C-Wie-Camelion.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "C wie Camelion"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_c = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_c_seit2)
        self.button_lerne_das_c.pack(anchor="se")
        self.background_label.configure(bg="orange")

        self.root.configure(bg="orange")
    def lerne_das_c_seit2(self):
        self.loesche_aktuelles_frame()

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
    
        self.ueberschrifft_lerne_das_c_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 18))
        self.ueberschrifft_lerne_das_c_seites.pack(anchor="center")  # Korrigierter Name hier

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.eingabefeld_lerne_das_c = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_c.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14), command=self.lerne_das_c_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
    

    def lerne_das_c_antwor_ueberpruefen(self):


        user_answer = self.eingabefeld_lerne_das_c.get()

        if user_answer == "C":
            self.lerne_das_d_seite1()
        else:
            self.zeige_falsche_antwort_meldung3()

    def lerne_das_d_seite1(self):

# Beispielbild laden
        #self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(D) Wie Dose.jpeg")
         
        self.background_image_url = "https://i.ibb.co/4StcpLX/D-Wie-Dose.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "D wie Dose"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_D_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")


    def lerne_das_D_seit2 (self):

        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()

        
        self.ueberschrifft_lerne_das_d_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 18))
        self.ueberschrifft_lerne_das_d_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_d = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_d.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_d_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

    def lerne_das_d_antwor_ueberpruefen(self):


        user_answer = self.eingabefeld_lerne_das_d.get()

        if user_answer == "D":
            self.lerne_das_e_seite1()
        else:
            self.zeige_falsche_antwort_meldung3()

#Elefant---------------------------------------------------------------------------------------------
    def lerne_das_e_seite1(self):

        self.background_image_url = "https://i.ibb.co/hmSFYWs/E-Wie-Elefant.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "E wie Elefant"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_E_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")

    def lerne_das_E_seit2(self):

        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_E_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")


    def lerne_das_E_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "E":
            self.zwischen_abfrage()
        else:
            self.zeige_falsche_antwort_meldung3()
#ende Elefant----------------------------------------------------------------------------------
#Zwischenabfrage A-E-------------------------------------------------------------------------------------------
    def zwischen_abfrage(self):
        self.loesche_aktuelles_frame()
        self.root.configure(bg="orange") 
        self.zwischen_abfrage_label=tk.Label(self.root,text="Gebe (A) (B) (C) (D) (E) ein",bg="orange",font=("Arial",20))
        self.zwischen_abfrage_label.pack(anchor="center")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()
        self.zwischen_abfrage_eingabefeld=tk.Entry(self.root,text="",font=("Arial",17))
        self.zwischen_abfrage_eingabefeld.pack(anchor="center")
        self.zwischen_abfrage_button=tk.Button(self.root,text="->",font=("Arial",20),command=self.zwischen_abfrage_eingabe)
        self.zwischen_abfrage_button.pack(anchor="center")

    def zwischen_abfrage_eingabe(self):

        
        user_answer = self. zwischen_abfrage_eingabefeld.get()

        if user_answer == "A B C D E":
            self.eingabefeld_lerne_das_F()
        else:
            self.zeige_falsche_antwort_meldung3()
#<ENDE ZWISCHENABFRAGE >

#FISCH---------------------------------------------------------------------------------------

    def eingabefeld_lerne_das_F(self):
        self.background_image_url = "https://i.ibb.co/2tHQWFc/F-Wie-Fisch.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        
        #self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(F) Wie Fisch.jpeg")

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "F wie Fisch"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_F_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")

    def lerne_das_F_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_F_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

    def lerne_das_F_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "F":
            self.eingabefeld_lerne_das_G()
        else:
            self.zeige_falsche_antwort_meldung3()

#ende Fisch -----------------------------------------------------------------------------------------------------
    def eingabefeld_lerne_das_G(self):

        self.background_image_url = "https://i.ibb.co/vdhrQV9/G-Wie-Giraffe.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        
        #self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(G) Wie Giraffe.jpeg")

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "G wie Giraffe"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_G_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")

    def lerne_das_G_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_G_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

    def lerne_das_G_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "G":
            self.eingabefeld_lerne_das_H()
        else:
            self.zeige_falsche_antwort_meldung3()

            #ende giraffe


            #Hund-----------------------------------------------------------------------------------------------------
    def eingabefeld_lerne_das_H(self):

        self.background_image_url = "https://i.ibb.co/gtcnmnp/H-Wie-hund.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        #self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(H) Wie Hund.jpeg")

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "H wie Hund"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_c = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_h_seit2)
        self.button_lerne_das_c.pack(anchor="se")
        self.background_label.configure(bg="orange")

        self.root.configure(bg="orange")
    def lerne_das_h_seit2(self):
        self.loesche_aktuelles_frame()

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
    
        self.ueberschrifft_lerne_das_c_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_c_seites.pack(anchor="center")  # Korrigierter Name hier

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.eingabefeld_lerne_das_c = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_c.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14), command=self.lerne_das_h_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
    

    def lerne_das_h_antwor_ueberpruefen(self):



        user_answer = self.eingabefeld_lerne_das_c.get()

        if user_answer == "H":
            self.eingabefeld_lerne_das_I()
        else:
            self.zeige_falsche_antwort_meldung3()

        #ende HUND

#Igel----------------------------------------------------------------------------------------------------------------------
    def eingabefeld_lerne_das_I(self):

        self.background_image_url = "https://i.ibb.co/Pt9sm8r/I-Wie-Igel.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        
        #self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(I) Wie Igel.jpeg")

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "I wie Igel"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_I_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")

    def lerne_das_I_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_I_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

    def lerne_das_I_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "I":
            self.eingabefeld_lerne_das_J()
        else:
            self.zeige_falsche_antwort_meldung3()
#ENDE IGEL

#Anfang Jäger ----------------------------------------------------------------------------------------------------------------------------

    def eingabefeld_lerne_das_J(self):


        self.background_image_url = "https://i.ibb.co/VWgvHGY/J-Wie-j-ger.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        
       # self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(J) Wie Jäger.jpeg")

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "J wie Jäger"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_J_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")

    def lerne_das_J_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")
        
        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_J_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

    def lerne_das_J_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "J":
            self.eingabefeld_lerne_das_K()
        else:
            self.zeige_falsche_antwort_meldung3()
        #ENDE JÄGER

#ANFANG Kamel -----------------------------------------------------------------------------------------------------
    def eingabefeld_lerne_das_K(self):
        self.background_image_url = "https://i.ibb.co/cJ5pQRx/K-Wie-kamel.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        #self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(K) Wie Kamel.jpeg")

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "K wie Kamel"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_K_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")

    def lerne_das_K_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_K_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

    def lerne_das_K_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "K":
            self.eingabefeld_lerne_das_L()
        else:
            self.zeige_falsche_antwort_meldung3()
#ENDE KAMEL
#----------------------------------------------------------------------------------------------------------------------------

#Anfang Löwe

    def eingabefeld_lerne_das_L(self):

        self.background_image_url = "https://i.ibb.co/jzkPwRF/L-Wie-L-we.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        
        #self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(L) Wie Löwe.jpeg")

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "L wie Löwe"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_L_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")

    def lerne_das_L_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_L_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

    def lerne_das_L_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "L":
            self.eingabefeld_lerne_das_M()
        else:
            self.zeige_falsche_antwort_meldung3()
#HIER MUSS ERNEUT DAS M EINGEFÜGT WERDEN 

    
    def eingabefeld_lerne_das_M(self):

        self.background_image_url = "https://i.ibb.co/XVSh963/M-Wie-M-we.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "M wie Möwe"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_M = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_M_seit2)
        self.button_lerne_das_M.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")
            #ende löwe

            #Anfang Möwe--------------------------------------


                

    def lerne_das_M_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_M_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

        
    def lerne_das_M_antwor_ueberpruefen(self):
            user_answer = self.eingabefeld_lerne_das_E.get()
            if user_answer == "M":
                self.joker1()
            else:
                self.zeige_falsche_antwort_meldung3()

    def joker1(self):
    
            self.ueberschrifft = tk.Label(self.root, text="Super, du hast jetzt die Hälfte geschafft. Ab jetzt kannst du dir tipps anzeigen lassen", font=("Arial", 20))
            self.ueberschrifft.pack(anchor="center")

            self.leertaste = tk.Label(self.root, bg="orange")
            self.leertaste.pack()

            self.leertaste = tk.Label(self.root, bg="orange")
            self.leertaste.pack()

            self.leertaste = tk.Label(self.root, bg="orange")
            self.leertaste.pack()

            self.button_weiter_zu_n = tk.Button(self.root, text="Weiter ->", font=("Arial", 14), command=self.eingabefeld_lerne_das_N)
            self.button_weiter_zu_n.pack(anchor="center")
           
            #Ende Möwe

    

    def eingabefeld_lerne_das_N(self):


        self.background_image_url = "https://i.ibb.co/xDxf8DG/N-Wie-Nashorn.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "N wie Nashorn"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_N_seit2)
        self.button_lerne_das_b.pack(anchor="se")
        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")



    def lerne_das_N_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_N_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
       

    def lerne_das_N_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "N":
            self.eingabefeld_lerne_das_o()
        else:
            self.zeige_falsche_antwort_meldung3()

#anfang Ohr--------------------------------------------------------------------------------------
    def eingabefeld_lerne_das_o(self):
        
        self.background_image_url = "https://i.ibb.co/hK8TTC2/O-Wie-Ohr.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "O wie Ohr"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_c = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_o_seit2)
        self.button_lerne_das_c.pack(anchor="se")
        self.background_label.configure(bg="orange")

        self.root.configure(bg="orange")
    def lerne_das_o_seit2(self):
        self.loesche_aktuelles_frame()

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
    
        self.ueberschrifft_lerne_das_c_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_c_seites.pack(anchor="center")  # Korrigierter Name hier

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.eingabefeld_lerne_das_c = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_c.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14), command=self.lerne_das_o_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
    

    def lerne_das_o_antwor_ueberpruefen(self):


        user_answer = self.eingabefeld_lerne_das_c.get()

        if user_answer == "O":
            self.zwischen_abfrage_D_H()
        else:
            self.zeige_falsche_antwort_meldung3()

#Zwischenabfrage A-E-------------------------------------------------------------------------------------------
    def zwischen_abfrage_D_H(self):
        self.loesche_aktuelles_frame()
        self.root.configure(bg="orange") 
        self.zwischen_abfrage_label=tk.Label(self.root,text="Gebe (D) (E) (F) (G) (H) ein",bg="orange",font=("Arial",20))
        self.zwischen_abfrage_label.pack(anchor="center")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()
        self.zwischen_abfrage_eingabefeld=tk.Entry(self.root,text="",font=("Arial",17))
        self.zwischen_abfrage_eingabefeld.pack(anchor="center")
        self.zwischen_abfrage_button=tk.Button(self.root,text="->",font=("Arial",20),command=self.zwischen_eingabe_D_H)
        self.zwischen_abfrage_button.pack(anchor="center")

    def zwischen_eingabe_D_H(self):

        
        user_answer = self. zwischen_abfrage_eingabefeld.get()

        if user_answer == "D E F G H":
            self.eingabefeld_lerne_das_P()
        else:
            self.zeige_falsche_antwort_meldung3()
#<ENDE ZWISCHENABFRAGE >

#Ohr---------------------------------------------------------------------------------------

   

#Ende Ohr--------------------------------------------------------------------------


#anfang Papagei--------------------------------------------------------------------------------------
    def eingabefeld_lerne_das_P(self):
        
             
        self.background_image_url = "https://i.ibb.co/z8tsSH7/P-Wie-Papagei.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        #self.background_image = Image.open(r"C:\Users\steve\Desktop\Python Projekte\(P) Wie Papagei.jpeg")

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "P wie Papagei"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_P_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.setze_weissen_hintergrund(self.leertaste)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")

        #Ende Papagei----------------------------------------------------------------------------------

    def lerne_das_P_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_P_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

    def lerne_das_P_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "P":
            self.eingabefeld_lerne_das_Q()
        else:
            self.zeige_falsche_antwort_meldung3()

            #anfang Ohr--------------------------------------------------------------------------------------
    def eingabefeld_lerne_das_Q(self):
        
             
        self.background_image_url = "https://i.ibb.co/j6pmXw2/Q-Wie-Qualle.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))     
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "Q wie Qualle"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_Q_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")

    def lerne_das_Q_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_Q_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

    def lerne_das_Q_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "Q":
            self.eingabefeld_lerne_das_R()
        else:
            self.zeige_falsche_antwort_meldung3()

            #anfang Robbe--------------------------------------------------------------------------------------
    def eingabefeld_lerne_das_R(self):
        
        self.background_image_url = "https://i.ibb.co/NyPQBBr/R-Wie-Robbe.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))     
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "R wie Robbe"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_R_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")

    def lerne_das_R_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_R_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")

    def lerne_das_R_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "R":
            self.eingabefeld_lerne_das_S()
        else:
            self.zeige_falsche_antwort_meldung3()
            #Ende Robbe

    def eingabefeld_lerne_das_S(self):
        
        self.background_image_url = "https://i.ibb.co/QMXdGxt/S-Wie-Sonne.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "S wie Sonne"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_b = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_S_seit2)
        self.button_lerne_das_b.pack(anchor="se")

        

        self.leertaste = tk.Label(self.root)
        self.leertaste.pack()
        self.background_label.configure(bg="orange")
    def lerne_das_S_seit2(self):
 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


        self.loesche_aktuelles_frame()
        
        self.ueberschrifft_lerne_das_E_seites2 = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_E_seites2.pack(anchor="center")

        self.eingabefeld_lerne_das_E = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_E.pack(anchor="center")

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14),command=self.lerne_das_S_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
    def lerne_das_S_antwor_ueberpruefen(self):

        user_answer = self.eingabefeld_lerne_das_E.get()

        if user_answer == "S":
            self.lerne_das_t_seite_1()
        else:
            self.zeige_falsche_antwort_meldung3()

    def lerne_das_t_seite_1(self):
        
        self.background_image_url = "https://i.ibb.co/Xjg6jWb/T-Wie-Tiger.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "T wie Tiger"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_c = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_t_seit2)
        self.button_lerne_das_c.pack(anchor="se")
        self.background_label.configure(bg="orange")

        self.root.configure(bg="orange")
    def lerne_das_t_seit2(self):
        self.loesche_aktuelles_frame()

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
    
        self.ueberschrifft_lerne_das_c_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_c_seites.pack(anchor="center")  

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.eingabefeld_lerne_das_c = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_c.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14), command=self.lerne_das_T_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
    def lerne_das_T_antwor_ueberpruefen(self):


        user_answer = self.eingabefeld_lerne_das_c.get()

        if user_answer == "T":
            self.lerne_das_u_seite_1()
        else:
            self.zeige_falsche_antwort_meldung3()
     
    def lerne_das_u_seite_1(self):
        
        self.background_image_url = "https://i.ibb.co/Y2GxXXm/U-Wie-Uhr.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "U wie Uhr"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_c = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_u_seit2)
        self.button_lerne_das_c.pack(anchor="se")
        self.background_label.configure(bg="orange")

        self.root.configure(bg="orange")
    def lerne_das_u_seit2(self):
        self.loesche_aktuelles_frame()

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
    
        self.ueberschrifft_lerne_das_c_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_c_seites.pack(anchor="center")  # Korrigierter Name hier

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.eingabefeld_lerne_das_c = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_c.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14), command=self.lerne_das_u_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
    def lerne_das_u_antwor_ueberpruefen(self):


        user_answer = self.eingabefeld_lerne_das_c.get()

        if user_answer == "U":
            self.lerne_das_v_seite_1()
        else:
            self.zeige_falsche_antwort_meldung3()

            self.zeige_falsche_antwort_meldung3()
    def lerne_das_v_seite_1(self):
            
        self.background_image_url = "https://i.ibb.co/bF1h1ky/V-Wie-Vogel.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "V wie Vogel"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_c = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_v_seit2)
        self.button_lerne_das_c.pack(anchor="se")
        self.background_label.configure(bg="orange")

        self.root.configure(bg="orange")
    def lerne_das_v_seit2(self):

        self.loesche_aktuelles_frame()

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
    
        self.ueberschrifft_lerne_das_c_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_c_seites.pack(anchor="center")  # Korrigierter Name hier

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.eingabefeld_lerne_das_c = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_c.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14), command=self.lerne_das_v_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
    def lerne_das_v_antwor_ueberpruefen(self):


        user_answer = self.eingabefeld_lerne_das_c.get()

        if user_answer == "V":
            self.lerne_das_w_seite_1()
        else:
            self.zeige_falsche_antwort_meldung3()
    def lerne_das_w_seite_1(self):
            
        self.background_image_url = "https://i.ibb.co/JkTDJFb/W-Wie-Wal.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "W wie Wal"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")
        
        self.button_lerne_das_c = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_w_seit2)
        self.button_lerne_das_c.pack(anchor="se")
        self.background_label.configure(bg="orange")

        self.root.configure(bg="orange")
    def lerne_das_w_seit2(self):

        self.loesche_aktuelles_frame()

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
    
        self.ueberschrifft_lerne_das_c_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_c_seites.pack(anchor="center")  # Korrigierter Name hier

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.eingabefeld_lerne_das_c = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_c.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14), command=self.lerne_das_w_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
    def lerne_das_w_antwor_ueberpruefen(self):


        user_answer = self.eingabefeld_lerne_das_c.get()

        if user_answer == "W":
            self.lerne_das_x_seite1()
        else:
            self.zeige_falsche_antwort_meldung3()
   
    def lerne_das_x_seite1(self):
            
        self.background_image_url = "https://i.ibb.co/hyttJ11/X-Wie-Xylophon.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "x wie Xylophon"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_c = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_x_seit2)
        self.button_lerne_das_c.pack(anchor="se")
        self.background_label.configure(bg="orange")

        self.root.configure(bg="orange")
    def lerne_das_x_seit2(self):

        self.loesche_aktuelles_frame()

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
    
        self.ueberschrifft_lerne_das_c_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_c_seites.pack(anchor="center")  # Korrigierter Name hier

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.eingabefeld_lerne_das_c = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_c.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14), command=self.lerne_das_x_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
    def lerne_das_x_antwor_ueberpruefen(self):


        user_answer = self.eingabefeld_lerne_das_c.get()

        if user_answer == "X":
            self.lerne_das_y_seite1()
        else:
            self.zeige_falsche_antwort_meldung3()
   
    def lerne_das_y_seite1(self):
            
        self.background_image_url = "https://i.ibb.co/pxFK8CR/Y-Wie-Yoga.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "y wie Yoga"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_c = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_y_seit2)
        self.button_lerne_das_c.pack(anchor="se")
        self.background_label.configure(bg="orange")

        self.root.configure(bg="orange")
    def lerne_das_y_seit2(self):

        self.loesche_aktuelles_frame()

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
    
        self.ueberschrifft_lerne_das_c_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_c_seites.pack(anchor="center")  # Korrigierter Name hier

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.eingabefeld_lerne_das_c = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_c.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14), command=self.lerne_das_y_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")   
    def lerne_das_y_antwor_ueberpruefen(self):


        user_answer = self.eingabefeld_lerne_das_c.get()

        if user_answer == "Y":
            self.lerne_das_z_seite_1()
        else:
            self.zeige_falsche_antwort_meldung3()
       
    def lerne_das_z_seite_1(self):

            
        self.background_image_url = "https://i.ibb.co/WcHTKQ4/Z-Wie-Zebra.jpg"
        self.background_image = Image.open(BytesIO(requests.get(self.background_image_url).content))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Hintergrundbild anzeigen
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        text = "Z wie Zebra"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.button_lerne_das_c = tk.Button(self.root, text="weiter", font=("Arial", 24), command=self.lerne_das_z_seit2)
        self.button_lerne_das_c.pack(anchor="se")
        self.background_label.configure(bg="orange")

        self.root.configure(bg="orange")
    def lerne_das_z_seit2(self):

        self.loesche_aktuelles_frame()

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()
    
        self.ueberschrifft_lerne_das_c_seites = tk.Label(self.root, text="Gebe den Buchstaben ein den du Gehört hasst",bg="orange", font=("Arial", 20))
        self.ueberschrifft_lerne_das_c_seites.pack(anchor="center")  # Korrigierter Name hier

        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.eingabefeld_lerne_das_c = tk.Entry(self.root,text="",font=("Arial",20))
        self.eingabefeld_lerne_das_c.pack(anchor="center")
        label = tk.Label(self.root, text="", bg="orange")
        label.pack()

        self.button_eingabefeld = tk.Button(self.root, text="Überprüfen", font=("Arial", 14), command=self.lerne_das_z_antwor_ueberpruefen)
        self.button_eingabefeld.pack(anchor="center")
    
        
    def lerne_das_z_antwor_ueberpruefen(self):


        user_answer = self.eingabefeld_lerne_das_c.get()

        if user_answer == "Z":
           self.silben_lesen_aufgabe(self)
        else:
            self.zeige_falsche_antwort_meldung3()

    

       
    def menü(self):
        self.loesche_aktuelles_frame()
        

        self.zurueck = tk.Button(self.root, text="Zurück", font=("Arial", 15), command=self.Startseite,width=22)
        self.zurueck.pack(anchor="ne")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()
     
        self.menue_ueberschrifft = tk.Label(self.root, text="Willkommen im Menü, was möchtest du machen", bg="orange",fg="blue", font=("fett",22,"italic"))
        self.menue_ueberschrifft.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()
     
        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()


        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.deutsch = tk.Button(self.root, text="Lernen", fg="black", font=("Arial", 17), command=self.silben_lesen_aufgabe,width=22)
        self.deutsch.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()


        self.au_eu_au=tk.Button(self.root,text="Umlaute",font=("Arial",17),fg="black",command=self.Umlaute,width=22)
        self.au_eu_au.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.deutsch_teil3 = tk.Button(self.root,text="Punkt und Komma", fg="black", font=("Arial", 17), command=self.Punkt_und_komma,width=22)
        self.deutsch_teil3.pack(anchor="center")


        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.alphabet=tk.Button(self.root,text="Alphabet: A-Z",font=("Arial",17),command=self.alphabet_a_z,width=22)
        self.alphabet.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.Anleitung=tk.Button(self.root,text="Fehlerbeheben",fg="red",font=("Arial",17),command=self.Anleitung_fehlerbeheben,width=22)
        self.Anleitung.pack(anchor="center")

        
        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()
        
      


    def Umlaute(self):
        self.loesche_aktuelles_frame()

        self.zurueck=tk.Button(self.root,text="zurück",command=self.menü,width=16)
        self.zurueck.pack(anchor="ne")
        self.Umlaute_überschrifft=tk.Label(self.root,text="Trage das passende Umlaut ein",font=("Arial",22),bg="orange")
        self.Umlaute_überschrifft.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()



        self.aufgabe1_umlaute = tk.Label(self.root,text="L..fer",bg="orange",font=("Arial",22))
        self.aufgabe1_umlaute.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()


        self.Antwort_umlaute_aufgabe1=tk.Button(self.root,text="ÄU",font=("Arial",15),command=self.Umlaute_aufgabe2,width=15)
        self.Antwort_umlaute_aufgabe1.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.Antwort_umlaute_aufgabe1_Falsch=tk.Button(self.root,text="Sch",font=("Arial",15),command=self.Falsche_antwort,width=15)
        self.Antwort_umlaute_aufgabe1_Falsch.pack(anchor="center")
    
        
      
     

    def Umlaute_aufgabe2(self):
        
        
        self.loesche_aktuelles_frame()

        self.zurueck=tk.Button(self.root,text="zurück",command=self.menü,width=16)
        self.zurueck.pack(anchor="ne")
        self.Umlaute_überschrifft=tk.Label(self.root,text="Trage das passende Umlaut ein",font=("Arial",22),bg="orange")
        self.Umlaute_überschrifft.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.Umlaute_überschrifft_aufgabe2=tk.Label(self.root,text="Pfel",font=("Arial",22),bg="orange")
        self.Umlaute_überschrifft_aufgabe2.pack(anchor="center")


    
        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

     

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()


        self.Antwort_umlaute_aufgabe2_richtig=tk.Button(self.root,text="Ä",font=("Arial",15),command=self.lückentext_aufgabe1,width=15)
        self.Antwort_umlaute_aufgabe2_richtig.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.Antwort_umlaute_aufgabe2_Falsch=tk.Button(self.root,text="ö",font=("Arial",15),command=self.Falsche_antwort,width=15)
        self.Antwort_umlaute_aufgabe2_Falsch.pack(anchor="center")
    
#funktion noch nicht im betrieb


    def lückentext_aufgabe1(self):
        self.loesche_aktuelles_frame()
        self.lueckentext_aufgabe1=tk.Label(self.root,text="Mein .... ist Romy",bg="orange",font=("Arial",20))
        self.lueckentext_aufgabe1.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.lueckentext_aufgabe1_eingabefelfd=tk.Entry(self.root,text="",font=("Arial",16))
        self.lueckentext_aufgabe1_eingabefelfd.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.lueckentext_aufgabe1_button=tk.Button(self.root,text="Überprüfen",font=("",16),command=self.ende)
        self.lueckentext_aufgabe1_button.pack(anchor="center")
 

    def Anleitung_fehlerbeheben(self):
        self.loesche_aktuelles_frame()
        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.Anleitung_ueberschrifft=tk.Label(self.root,text="Fehlermeldungen",bg="orange",font=("Arial",20))
        self.Anleitung_ueberschrifft.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()      

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.Fehlerbehen=tk.Label(self.root,text="Programm reagiert nicht (Neustart vom Programm)",bg="orange",font=("Arial",17))
        self.Fehlerbehen.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.Fehlerbehen1=tk.Label(self.root,text="Problen: Das Spiel zeigt eine falsche Antwort an  ----- Lösung: Zurück zur Startseite und nochmal beginnen  ",bg="orange",font=("Arial",17))
        self.Fehlerbehen1.pack(anchor="center")

        self.Fehlermeldung=tk.Label(self.root,text="Weitere Fehlermeldungen kommen",bg="Orange",font=("Arial",17))
        self.Fehlermeldung.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()
        self.Fehlerbehen1=tk.Label(self.root,text="Problem: Button reagieren nicht  ----- Lösung: Neustart Programm  ",bg="orange",font=("Arial",17))
        self.Fehlerbehen1.pack(anchor="center")

        
        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()


    def neue_funktion(self):
        self.loesche_aktuelles_frame()
        self.root.configure(bg="orange") 
        self.startseite=tk.Button(self.root,text="Startseite",font=("Arial",12),command=self.Startseite,width=22)
        self.startseite.pack(anchor="se")

        self.ueberschrifft_neue_funktion=tk.Label(self.root,text="Was ist neu?",bg="orange",font=("Arial",20))
        self.ueberschrifft_neue_funktion.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()
        
        self.funktion1=tk.Label(self.root,text="Fehler wurden behoben",fg="red",bg="orange",font=("fett",25))
        self.funktion1.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.funktion3=tk.Label(self.root,text="Notizen zum Speichern",bg="orange",font=("Arial",17))
        self.funktion3.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()
        
        self.funktion4=tk.Label(self.root,text="neue aufgaben",bg="orange",font=("Arial",17))
        self.funktion4.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

           
        self.funktion5=tk.Label(self.root,text="",bg="orange",font=("Arial",17))
        self.funktion5.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.fehler_wurde_behoben=tk.Label(self.root,text="Design wurde angepasst",bg="orange",font=("Arial",17))
        self.fehler_wurde_behoben.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

       # self.funktion2=tk.Label(self.root,text="",bg="orange",font=("fett",17))
       # self.funktion2.pack(anchor="center")

        #self.leertaste=tk.Label(self.root,bg="orange")
       # self.leertaste.pack()

        
        self.funktion2=tk.Label(self.root,text="Deutschtest wurde angepasst Wurde erweitert",bg="orange",font=("fett",17))
        self.funktion2.pack(anchor="center")



        #ENDE

    def alphabet_a_z(self):

        self.loesche_aktuelles_frame()

        self.zurueck=tk.Button(self.root,text="Zurück",font=("Arial",15),command=self.Startseite,width=14)
        self.zurueck.pack(anchor="ne")

        self.alphabet_label=tk.Label(self.root,text="Wiederhole das ABC",bg="orange",font=("Arial",30))
        self.alphabet_label.pack(anchor="center")
        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()
        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()


        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.alphabet_a_z_durchgang=tk.Button(self.root,text="Alphabet: A-Z",font=("Arial",20),command=self.Lerne_das_a,width=22)
        self.alphabet_a_z_durchgang.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()


        self.alphabet_a_e=tk.Button(self.root,text="Alphabet: A-G",font=("Arial",20),command=self.Lerne_das_a,width=22)
        self.alphabet_a_e.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        
        self.alphabet_H_I=tk.Button(self.root,text="Alphabet: H-P",font=("Arial",20),command=self.lerne_das_h_seite1,width=22)
        self.alphabet_H_I.pack(anchor="center")

        
        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.alphabet_J_O=tk.Button(self.root,text="Alphabet. Q-Z",font=("Arial",20),command=self.eingabefeld_lerne_das_Q,width=22)
        self.alphabet_J_O.pack(anchor="center")

        self.leertaste = tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        


   
        self.root.configure(bg="orange") 

    def lerne_das_h_seite1 (self):

        self.alphabet_h_p_ueberschrifft=tk.Button(self.root,text="Wiederhoung H-P",bg="orange",font=("Arial",20),command=self.eingabefeld_lerne_das_H)
        self.alphabet_h_p_ueberschrifft.pack(anchor="center")
#

#++++++++++++++++++++++++++++++++++++

    def silben_lesen_aufgabe(self):
        
        self.loesche_aktuelles_frame()
        self.root.configure(bg="orange")
        self.zurueck = tk.Button(self.root, text="Zurück", font=("Arial", 16), command=self.Startseite)
        self.zurueck.pack(anchor="se")
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()
 
        self.überschrifft_lernen=tk.Label(text="Was willst du machen",bg="orange",font=("Arial",20,"italic"))
        self.überschrifft_lernen.pack(anchor="center")

        
        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()


     

        self.button_silben_lernen=tk.Button(self.root,text="Silben Lernen",font=("Arial",16),command=self.silben_aufgabe_auswahl,width=22)
        self.button_silben_lernen.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.button_wörter_lernen=tk.Button(self.root,text="Wörter Lernen",font=("Arial",16),command=self.wörter_lernen,width=22)
        self.button_wörter_lernen.pack(anchor="center")

    def silben_aufgabe_auswahl(self):

        self.loesche_aktuelles_frame()

        self.leertaste=tk.Label(self.root,text="",bg="orange")
        self.leertaste.pack()

        self.deutsch_ueberschrift_aufgaben = tk.Label(self.root, text="Wie Viele Silben hat Mama",bg="orange", font=("Arial", 25),width=22)
        self.deutsch_ueberschrift_aufgaben.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_aufgabe=tk.Label(self.root,text="MA+ma",fg="blue", bg="orange",font=("Arial",20,"bold"))
        self.silben_aufgabe.pack(anchor="center")
    
    

    
        
        self.button1_silben_aufgabe=tk.Button(self.root,text="1",font=("Arial",16),command=self.zeige_falsche_antwort_meldung3,width=22)
        self.button1_silben_aufgabe.pack(anchor="center")

    
        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()
        

        self.silben_button=tk.Button(self.root,text="2",font=("Arial",16),command=self.silben_lernen_aufgabe2,width=22)
        self.silben_button.pack(anchor="center")

        
        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_button=tk.Button(self.root,text="3",font=("Arial",16),command=self.zeige_falsche_antwort_meldung3,width=22)
        self.silben_button.pack(anchor="center")

        
    def wörter_lernen(self):

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.loesche_aktuelles_frame()
        
        self.haus=tk.Label(self.root,text="Welches wort hasst du gehört?",bg="orange",font=("Arial",20))
        self.haus.pack(anchor="center")


        text = "Haus"

        # Erzeuge ein gTTS-Objekt
        tts = gTTS(text, lang='de')
        # Speichere den Ton in einer Datei
        tts.save("output.mp3")

        # Spiele den Ton ab
        os.system("start output.mp3")

        self.haus_eingabefeld=tk.Entry(self.root,text="",font=("arial",17))
        self.haus_eingabefeld.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.haus_Button=tk.Button(self.root,text="Überprüfen",font=("arial",17),command=self.haus_ueberprüfen)
        self.haus_Button.pack(anchor="center")

    def haus_ueberprüfen(self):
       
        user_answer = self.haus_eingabefeld.get()

        if user_answer == "Haus":
           self.lückentext_aufgabe1(self)
        else:
            self.zeige_falsche_antwort_meldung3()
        

#                  TEXT HINTERGRUND ORANGE 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()
        #ENDE
        
   


    def silben_lernen_aufgabe2(self):
        
        self.loesche_aktuelles_frame()
        self.root.configure(bg="orange") 
        self.zurueck = tk.Button(self.root, text="Zurück", font=("Arial", 12), command=self.Startseite,width=22)
        self.zurueck.pack(anchor="nw")

        self.deutsch_ueberschrift_aufgaben = tk.Label(self.root, text="Elefant",bg="orange", font=("Arial", 25))
        #self.setze_weissen_hintergrund(self.deutsch_ueberschrift_aufgaben)
        self.deutsch_ueberschrift_aufgaben.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
       # self.setze_weissen_hintergrund(self.leertaste)
        self.leertaste.pack()

        self.silben_aufgabe=tk.Label(self.root,text="E+le+fant",fg="red", bg="orange",font=("Arial",25))
        self.silben_aufgabe.pack(anchor="center")
    
        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()
 
        self.silben_lesen_aufgabe2_button=tk.Button(self.root,text="1",font=("Arial",14),command=self.zeige_falsche_antwort_meldung3,width=25)
        self.silben_lesen_aufgabe2_button.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        
        self.silben_lesen_aufgabe2_button2=tk.Button(self.root,text="2",font=("Arial",14),command=self.zeige_falsche_antwort_meldung3,width=25)
        self.silben_lesen_aufgabe2_button2.pack(anchor="center")

        
        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        
        self.silben_lesen_aufgabe2_button3=tk.Button(self.root,text="3",font=("Arial",14),command=self.silben_aufgabe3,width=25)
        self.silben_lesen_aufgabe2_button3.pack(anchor="center")


#                  TEXT HINTERGRUND ORANGE 
        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()
        #ENDE
        

    def silben_aufgabe3(self):
        self.loesche_aktuelles_frame()

        self.leertaste = tk.Label(self.root,bg="orange")
       # self.setze_weissen_hintergrund(self.leertaste)
        self.leertaste.pack()
        self.ueberschrifft_silbenlernen_aufgabe4=tk.Label(self.root,text="Wie viele silben hat Haus" ,bg="orange",font=("Arial",20))
        self.ueberschrifft_silbenlernen_aufgabe4.pack(anchor="center")
        self.aufgabe3_silben_lernen=tk.Label(self.root,text="Haus", bg="orange",fg="red",font=("Arial",20))
        self.aufgabe3_silben_lernen.pack(anchor="center")

        

        self.leertaste = tk.Label(self.root,bg="orange")
       # self.setze_weissen_hintergrund(self.leertaste)
        self.leertaste.pack()

        self.silben_lesen_aufgabe3_button2=tk.Button(self.root,text="1",font=("Arial",14),command=self.silben_aufgabe4,width=25)
        self.silben_lesen_aufgabe3_button2.pack(anchor="center")

        
        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_lesen_aufgabe3_button2=tk.Button(self.root,text="2",font=("Arial",14),command=self.zeige_falsche_antwort_meldung3,width=25)
        self.silben_lesen_aufgabe3_button2.pack(anchor="center")

        
        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_lesen_aufgabe3_button2=tk.Button(self.root,text="3",font=("Arial",14),command=self.zeige_falsche_antwort_meldung3,width=25)
        self.silben_lesen_aufgabe3_button2.pack(anchor="center")

        self.background_label.configure(bg="orange")
        label=tk.Label(self.root,text="",bg="orange")
        label.pack()


    def silben_aufgabe4(self):
        self.loesche_aktuelles_frame()
        
        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_lesen_aufgabe4=tk.Label(self.root,text="Wie viele Silben hat",bg="orange",font=("Arial",18))
        self.silben_lesen_aufgabe4.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_lesen_aufgabe4_text=tk.Label(self.root,text="Bahnhof",bg="orange",fg="red",font=("Arial",16))
        self.silben_lesen_aufgabe4_text.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_lesen_aufgabe4_button=tk.Button(self.root,text="1",font=("Arial",14),command=self.zeige_falsche_antwort_meldung3,width=25)
        self.silben_lesen_aufgabe4_button.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()
        
        self.silben_aufgabe4_button2=tk.Button(self.root,text="2",font=("Arial",14),command=self.silben_aufgabe5,width=25)
        self.silben_aufgabe4_button2.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_aufgabe4_button3=tk.Button(self.root,text="3",font=("Arial",14),command=self.zeige_falsche_antwort_meldung3,width=25)
        self.silben_aufgabe4_button3.pack(anchor="center")

    def silben_aufgabe5(self):
        

    
        self.loesche_aktuelles_frame()
        
        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_lesen_aufgabe4=tk.Label(self.root,text="Wie viele Silben hat",bg="orange",font=("Arial",18))
        self.silben_lesen_aufgabe4.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_lesen_aufgabe4_text=tk.Label(self.root,text="Rakete",bg="orange",fg="red",font=("Arial",16))
        self.silben_lesen_aufgabe4_text.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_lesen_aufgabe4_button=tk.Button(self.root,text="1",font=("Arial",14),command=self.zeige_falsche_antwort_meldung3,width=25)
        self.silben_lesen_aufgabe4_button.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()
        
        self.silben_aufgabe4_button2=tk.Button(self.root,text="2",font=("Arial",14),command=self.zeige_falsche_antwort_meldung3,width=25)
        self.silben_aufgabe4_button2.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_aufgabe4_button3=tk.Button(self.root,text="3",font=("Arial",14),command=self.silben_ende,width=25)
        self.silben_aufgabe4_button3.pack(anchor="center")





    def silben_ende(self):
        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.button_silben_ende=tk.Label(self.root,text="super du hasst alle silben richtig beantworter willst du Weitermachen?",font=("Arial",16))
        self.button_silben_ende.pack(anchor="center")

        self.leertaste = tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.button_silben_ja=tk.Button(self.root,text="Ja",fg="red",font=("Arial",16),command=self.silben_lernen_teil2,width=22)
        self.button_silben_ja.pack(anchor="center")

        
        self.button_silben_nein=tk.Button(self.root,text="nein",fg="red",font=("Arial",16),command=self.Punkt_und_komma,width=22)
        self.button_silben_nein.pack(anchor="center")

        
    def silben_lernen_teil2(self):
        self.loesche_aktuelles_frame()
        
        self.silben_lesen_aufgabe5_text=tk.Label(self.root,text="Teil 2 (Namen)",bg="orange",fg="red",font=("Arial",16))
        self.silben_lesen_aufgabe5_text.pack(anchor="center")

        
        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.silben_lesen_aufgabe5=tk.Label(self.root,text="Hans",bg="orange",fg="red",font=("Arial",16))
        self.silben_lesen_aufgabe5.pack(anchor="center")

        self.silben_lesen_aufgabe5_richtige_antwort=tk.Button(self.root,text="1",fg="red",font=("Arial",16),command=self.silben_lernen_aufgabe6,width=25)
        self.silben_lesen_aufgabe5_richtige_antwort.pack(anchor="center")

        
        self.silben_lesen_aufgabe5_Falsche_Antwort_antwort=tk.Button(self.root,text="2",fg="red",font=("Arial",16),command=self.zeige_falsche_antwort_meldung3,width=25)
        self.silben_lesen_aufgabe5_Falsche_Antwort_antwort.pack(anchor="center")
  
    def silben_lernen_aufgabe6(self):
        self.loesche_aktuelles_frame()
        self.silben_lesen_aufgabe6_text=tk.Label(self.root,text="Ursula",bg="orange",fg="red",font=("Arial",16))
        self.silben_lesen_aufgabe6_text.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        
        self.silben_lesen_aufgabe6_falsche_antwort=tk.Button(self.root,text="1",fg="red",font=("Arial",16),command=self.zeige_falsche_antwort_meldung3,width=25)
        self.silben_lesen_aufgabe6_falsche_antwort.pack(anchor="center")

        
        self.silben_lesen_aufgabe6_richtige_antwort=tk.Button(self.root,text="3",fg="red",font=("Arial",16),command=self.ende,width=25)
        self.silben_lesen_aufgabe6_richtige_antwort.pack(anchor="center")
    def Punkt_und_komma(self):
        self.loesche_aktuelles_frame()
         
        self.zurueck=tk.Button(self.root,text="zurück",font=("Arial",16),command=self.Startseite)
        self.zurueck.pack(anchor="se")
        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()
 
        self.Ueberschrifft_punkt_und_komma=tk.Label(self.root,text="Wähle aus was du Lernen möchtest",font=("Arial",17))
        self.Ueberschrifft_punkt_und_komma.pack(anchor="center")


 
        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()



        self.lerne_punkt=tk.Button(self.root,text="Lerne Punkte setzen .",font=("Arial",15),command=self.lerne_Punkt_setzen,width=22)
        self.lerne_punkt.pack(anchor="center")


        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()


        self.start_button=tk.Button(self.root,text="Lerne Komma setzen ,",font=("Arial",15),command=self.lerne_komma_setzen,width=22)
        self.start_button.pack()

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()
        
        self.start_button=tk.Button(self.root,text="Lerne Ausrufezeichen !",font=("Arial",15),command=self.lerne_komma_setzen,width=22)
        self.start_button.pack()
        
        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()
        
        self.start_button=tk.Button(self.root,text="Lerne Fragezeichen ?",font=("Arial",15),command=self.lerne_komma_setzen,width=22)
        self.start_button.pack()

    def lerne_Punkt_setzen(self):
        self.loesche_aktuelles_frame()
        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.aufgabe1_punkt_und_komma_ueberschrifft=tk.Label(self.root,text="Aufgabe1",font=("Arial",20))
        self.aufgabe1_punkt_und_komma_ueberschrifft.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.aufgabe1_punkt_und_komma=tk.Label(self.root,text="Ich habe heute morgen gefrühstückt",font=("Arial",20))
        self.aufgabe1_punkt_und_komma.pack(anchor="center")

    
        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.aufgabe1_punkt_und_komma_eingabefelg=tk.Entry(self.root,text="/",font=("Arial",18))
        self.aufgabe1_punkt_und_komma_eingabefelg.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.aufgabe1_punkt_und_komma_button=tk.Button(self.root,text="Überprüfen",command=self.punkt_und_komma_ueberprufen,width=25)
        self.aufgabe1_punkt_und_komma_button.pack()


    def lerne_komma_setzen(self):
        pass


    def punkt_und_komma_ueberprufen(self):

        user_answer = self.aufgabe1_punkt_und_komma_eingabefelg.get()
        if user_answer == "Ich habe heute morgen gefrühstückt.":
            self.punkt_und_komma_aufgabe2()
        else:
            
            self.falsch_antwort=tk.Label(self.root,text="Leider falsch versuche es erneut",font=("arial",13))
            self.falsch_antwort.pack(anchor="center")
            
            
            self.leertaste=tk.Label(self.root,bg="orange")
            self.leertaste.pack()

            self.falsche_antwort_button=tk.Button(self.root,text="Versuche es erneut",font=("Arial",15),command=self.zeige_falsche_antwort_meldung3)
            self.falsche_antwort_button.pack(anchor="center")

    def punkt_und_komma_aufgabe2(self):
        self.loesche_aktuelles_frame()
        
        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.aufgabe2_punkt_und_komma_ueberschrifft=tk.Label(self.root,text="Ich mag Eis aber kein Schokoeis.",font=("Arial",18))
        self.aufgabe2_punkt_und_komma_ueberschrifft.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.aufgabe2_punkt_und_komma_eingabefeld=tk.Entry(self.root,text="/",font=("Arial",20))
        self.aufgabe2_punkt_und_komma_eingabefeld.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()
        
        self.aufgabe2_punkt_und_komma_button=tk.Button(self.root,text="Überprüfen",font=("Arial",15),command=self.ende)
        self.aufgabe2_punkt_und_komma_button.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()


    def ende(self):
        self.loesche_aktuelles_frame()
        self.ende_game=tk.Label(self.root,text="Super du hasst alle aufgaben richtig beantwortet",font=("Arial",15))
        self.ende_game.pack(anchor="center")

        self.leertaste=tk.Label(self.root,bg="orange")
        self.leertaste.pack()

        self.startseite_neubeginn=tk.Button(self.root,text="Zum Menü",font=("Arial",18),command=self.menü)
        self.startseite_neubeginn.pack(anchor="center")


    
    def zeige_falsche_antwort_meldung3(self):
        self.loesche_aktuelles_frame()

        messagebox.showinfo("Warnung","Falsche Antwort")

        self.Falsche_antwort_überschrifft=tk.Label(text="Deine Antwort war leider Falsch was möchtes du als nächstes machen?",bg="orange",font=("Fett",20))
        self.Falsche_antwort_überschrifft.pack(anchor="center")

        self.leertaste=tk.Label(text="",bg="orange")
        self.leertaste.pack()

        self.Aufgabe_wiederholen=tk.Button(self.root,text="Erneut versuchen",font=("Arial",18),command=self.alphabet_a_z,width=22)
        self.Aufgabe_wiederholen.pack(anchor="center")

        self.startseite=tk.Button(self.root,text="Zurück zur Startseite",font=("Arial",18),command=self.startseite,width=22)
        self.startseite.pack(anchor="center")
    def Update(self):
        """
        Diese Methode lädt die neueste Version des Programms herunter und ersetzt die lokale Datei.
        """
        try:
            UPDATE_URL = 'https://example.com/lernprogramm_romy_latest.py'
            LOCAL_FILENAME = 'Lernprogramm_Romy_version_5.py'
            response = requests.get(UPDATE_URL)

            if response.status_code == 200:
                with open(LOCAL_FILENAME, 'wb') as f:
                    f.write(response.content)
                messagebox.showinfo("Update", "Das Programm wurde erfolgreich aktualisiert.")
            else:
                messagebox.showerror("Fehler", "Server nicht erreichbar.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler: {e}")


if __name__ == "__main__":
    app = Lernprojekt()

    app.root.mainloop()


    # Hier müssen Sie die bestehenden Methoden wie Startseite(), aufgaben_loesen(), etc. anpassen,
    # um den aktuellen Benutzer anzuzeigen und Ergebnisse zu speichern.