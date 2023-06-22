import sqlite3
import datetime
import time
import re

# Funktion zum Hinzufügen von Protokolleinträgen
def log_entry(log_message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('logs.txt', 'a') as log_file:
        log_file.write(f"{timestamp} - {log_message}\n")

log_entry("--- Starte den Authentifizierungsprozess ---")

fails = 0
erfolgreich = False

# Herstellen einer Verbindung zur SQLite-Datenbank
try:
    db_connection = sqlite3.connect('Benutzerdaten.sqlite')
    cursor = db_connection.cursor()

    while fails < 3:
        # Benutzernamen abfragen
        benutzername = input("Benutzername: ")

        # Überprüfen, ob der Benutzername mit einem Großbuchstaben beginnt
        if not re.match(r"^[A-Z]", benutzername):
            log_entry("Der Benutzername muss mit einem Großbuchstaben beginnen.")
            print("Der Benutzername muss mit einem Großbuchstaben beginnen.")
            fails += 1
            continue

        # SQL-Abfrage zum Überprüfen des Benutzernamens
        query = "SELECT * FROM Benutzer WHERE Benutzername = ?"
        cursor.execute(query, (benutzername,))
        result = cursor.fetchone()

        if result:
            # Passwort abfragen
            passwort = input("Passwort: ")

            # Überprüfen, ob das Passwort die Mindestlängenanforderung erfüllt
            if re.match(r"^.{8,}$", passwort):
                # Überprüfen, ob das Passwort mit dem Benutzernamen übereinstimmt
                if result[1] == passwort:
                    # Erfolgreicher Login
                    log_entry(f"Login erfolgreich für {benutzername}")
                    print(f"Willkommen in deinem Konto {benutzername}")
                    erfolgreich = True
                    break
                else:
                    # Falsches Passwort
                    log_entry(f"Falsches Passwort für {benutzername}")
                    print("Falsches Passwort")
            else:
                # Die Passwortlänge beträgt weniger als 8 Zeichen
                log_entry(f"Das Passwort muss mindestens 8 Zeichen lang sein.")
                print("Das Passwort muss mindestens 8 Zeichen lang sein.")
        else:
            # Benutzername existiert nicht
            log_entry(f"Der Benutzername {benutzername} existiert nicht")
            print("Der Benutzername existiert nicht")

        fails += 1

    if erfolgreich:
        # Gesamtzahl der aktuellen Benutzer abrufen
        query = "SELECT COUNT(*) FROM Benutzer"
        cursor.execute(query)
        total_users = cursor.fetchone()[0]
        print(f"Anzahl der aktuellen Benutzer: {total_users}")

    db_connection.close()

except sqlite3.Error as error:
    # Verbindungs- oder Abfragefehler
    log_entry(f"SQLite-Fehler: {error}")
    print("Es ist ein Fehler aufgetreten. Bitte versuche es erneut.")

if fails == 3:
    # Dritter fehlgeschlagener Versuch
    log_entry(f"Login wurde durch 3 fehlerhafte Versuche abgebrochen")
    print("Dritter fehlgeschlagener Versuch. Login wird abgebrochen.")
    print("Dieser Vorfall wird eingetragen und das Skript wird beendet.")
    for i in range(5, 0, -1):
        print(f"Warte {i} Sekunden...")
        time.sleep(1)
    print("Schließe das Skript.")
    exit(1)