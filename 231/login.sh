#!/bin/bash

# Setze Anfangswerte
benutzername=""
passwort=""
fails=0

# Funktion zum Hinzufügen von Logeinträgen
function log_entry {
    local log_message="$1"
    local timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "$timestamp - $log_message" >> logs.txt
}

log_entry "--- Starte den Authentifizierungsprozess ---"

while [ $fails -lt 3 ]; do
    # Benutzername abfragen
    read -p "Benutzername: " benutzername

    # Überprüfe, ob der Benutzername in daten.sh existiert
    if grep -q "^$benutzername:" daten.sh; then
        # Passwort abfragen
        read -s -p "Passwort: " passwort
        echo

        # Überprüfe, ob das Passwort zu dem Benutzernamen passt
        if grep -q "^$benutzername:$passwort$" daten.sh; then
            # Erfolgreicher Login
            log_entry "Login erfolgreich für $benutzername"
            echo "Willkommen in deinem Konto $benutzername"
            exit 0
        else
            # Falsches Passwort
            log_entry "Falsches Passwort für $benutzername"
            echo "Falsches Passwort"
            ((fails++))
        fi
    else
        # Benutzername existiert nicht
        log_entry "Der Benutzername $benutzername existiert nicht"
        echo "Der Benutzername existiert nicht"
        ((fails++))
    fi

    # Case construct for fails count
    case $fails in
        1)
            echo "Erster fehlgeschlagener Versuch. Bitte erneut versuchen."
            ;;
        2)
            echo "Zweiter fehlgeschlagener Versuch. Bitte erneut versuchen."
            ;;
        3)
            echo "Dritter fehlgeschlagener Versuch. Login wird abgebrochen."
            ;;
    esac
done

# Überprüfe die Anzahl der Fehlversuche
if [ $fails -eq 3 ]; then
    log_entry "Login wurde durch 3 fehlerhafte Versuche abgebrochen"
    echo "Login wurde durch 3 fehlerhafte Versuche abgebrochen"
    # For loop with break condition to count down before exit
    echo "Dieser Vorfall wird eingetragen und das Script wird beendet."
    for (( i=5; i>0; i-- ))
    do
        sleep 1
    done
    echo "Schliesse Script"
    exit 1
fi