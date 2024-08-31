import json
import os
from datetime import datetime

FILE_PATH = 'rooms_example.json'
HISTORY_PATH = 'history_example.json'

if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, 'w') as file:
        json.dump({"rooms": []}, file)

if not os.path.exists(HISTORY_PATH):
    with open(HISTORY_PATH, 'w') as file:
        json.dump({"history": []}, file)


def load_rooms():
    with open(FILE_PATH, 'r') as file:
        data = json.load(file)
    return data["rooms"]


def save_rooms(rooms):
    with open(FILE_PATH, 'w') as file:
        json.dump({"rooms": rooms}, file)


def load_history():
    with open(HISTORY_PATH, 'r') as file:
        data = json.load(file)
    return data["history"]


def save_history(history):
    with open(HISTORY_PATH, 'w') as file:
        json.dump({"history": history}, file)


def add_room():
    room_number = input("Zimmer Nummer: ")
    max_guests = int(input("Maximale Gäste: "))
    size = float(input("Größe (in Quadratmetern): "))
    price_per_night = float(input("Preis pro Nacht: "))

    rooms = load_rooms()
    rooms.append({
        "room_number": room_number,
        "max_guests": max_guests,
        "size": size,
        "price_per_night": price_per_night,
        "available": True,
        "reserved": False,
        "booked": False,
        "guest_name": None,
        "guest_options": [],
        "additional_info": []
    })
    save_rooms(rooms)
    print("Zimmer erfolgreich hinzugefügt!")


def list_rooms():
    rooms = load_rooms()
    total_rooms = len(rooms)
    available_rooms = len([room for room in rooms if room["available"]])
    print(f"Gesamtanzahl Zimmer: {total_rooms}")
    print(f"Freie Zimmer: {available_rooms}")
    for room in rooms:
        print(f"\nZimmer Nummer: {room['room_number']}")
        print(f"  Maximale Gäste: {room['max_guests']}")
        print(f"  Größe: {room['size']} m²")
        print(f"  Preis pro Nacht: {room['price_per_night']}€")
        print(f"  Verfügbar: {'Ja' if room['available'] else 'Nein'}")
        print(f"  Reserviert: {'Ja' if room['reserved'] else 'Nein'}")
        print(f"  Gebucht: {'Ja' if room['booked'] else 'Nein'}")
        if room['guest_name']:
            print(f"  Gast: {room['guest_name']}")
        if room['guest_options']:
            print(f"  Gast Optionen: {', '.join(room['guest_options'])}")
        if room['additional_info']:
            print(f"  Weitere Informationen: {', '.join(room['additional_info'])}")


def room_info():
    room_number = input("Zimmer Nummer für Informationen: ")
    rooms = load_rooms()
    for room in rooms:
        if room["room_number"] == room_number:
            print(f"\nZimmer Nummer: {room['room_number']}")
            print(f"  Maximale Gäste: {room['max_guests']}")
            print(f"  Größe: {room['size']} m²")
            print(f"  Preis pro Nacht: {room['price_per_night']}€")
            print(f"  Verfügbar: {'Ja' if room['available'] else 'Nein'}")
            print(f"  Reserviert: {'Ja' if room['reserved'] else 'Nein'}")
            print(f"  Gebucht: {'Ja' if room['booked'] else 'Nein'}")
            if room['guest_name']:
                print(f"  Gast: {room['guest_name']}")
            if room['guest_options']:
                print(f"  Gast Optionen: {', '.join(room['guest_options'])}")
            if room['additional_info']:
                print(f"  Weitere Informationen: {', '.join(room['additional_info'])}")
            return
    print("Zimmer nicht gefunden!")


def reserve_room():
    room_number = input("Zimmer Nummer zum Reservieren: ")
    rooms = load_rooms()
    for room in rooms:
        if room["room_number"] == room_number and room["available"] and not room["reserved"]:
            room["reserved"] = True
            save_rooms(rooms)
            print("Zimmer erfolgreich reserviert!")
            return
    print("Zimmer nicht verfügbar oder bereits reserviert!")


def book_room():
    room_number = input("Zimmer Nummer zum Einchecken: ")
    guest_name = input("Name des Gastes: ")
    rooms = load_rooms()
    for room in rooms:
        if room["room_number"] == room_number and room["reserved"]:
            room["booked"] = True
            room["available"] = False
            room["guest_name"] = guest_name
            save_rooms(rooms)
            history = load_history()
            history.append({
                "room_number": room_number,
                "guest_name": guest_name,
                "check_in": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "check_out": None
            })
            save_history(history)
            print("Zimmer erfolgreich gebucht!")
            return
    print("Zimmer nicht verfügbar oder nicht reserviert!")


def add_guest_options():
    room_number = input("Zimmer Nummer: ")
    rooms = load_rooms()
    for room in rooms:
        if room["room_number"] == room_number and room["booked"]:
            option = input("Option hinzufügen (z.B. Frühstück, Wellnessbereich, Allergien): ")
            if option.lower() in ['frühstück', 'wellnessbereich']:
                room["price_per_night"] += 20.0
                print(f"Preis pro Nacht erhöht um 20.0€, neuer Preis: {room['price_per_night']}€")
            elif option.lower() == 'allergien':
                allergy = input("Bitte geben Sie die Allergie(n) ein: ")
                room["additional_info"].append(f"Allergien: {allergy}")
                print(f"Allergie '{allergy}' erfolgreich hinzugefügt!")
                continue
            room["guest_options"].append(option)
            save_rooms(rooms)
            print(f"Option '{option}' erfolgreich hinzugefügt!")
            return
    print("Zimmer nicht verfügbar oder nicht gebucht!")


def checkout_room():
    room_number = input("Zimmer Nummer zum Auschecken: ")
    rooms = load_rooms()
    for room in rooms:
        if room["room_number"] == room_number and room["booked"]:
            print(f"Gesamtpreis: {room['price_per_night']}€")
            room["available"] = True
            room["reserved"] = False
            room["booked"] = False
            room["guest_name"] = None
            room["guest_options"] = []
            room["additional_info"] = []
            save_rooms(rooms)
            history = load_history()
            for record in history:
                if record["room_number"] == room_number and record["check_out"] is None:
                    record["check_out"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            save_history(history)
            print("Zimmer erfolgreich ausgecheckt und freigegeben!")
            return
    print("Zimmer nicht verfügbar oder nicht gebucht!")

def view_history():
    history = load_history()
    if not history:
        print("Kein Verlauf vorhanden.")
        return

    print("\nVerlauf durchsuchen")
    print("1. Nach Zimmernummer suchen")
    print("2. Nach Gastname suchen")
    choice = input("Wähle eine Option: ")

    if choice == '1':
        room_number = input("Gib die Zimmernummer ein: ")
        filtered_history = [record for record in history if record['room_number'] == room_number]
    elif choice == '2':
        guest_name = input("Gib den Gastnamen ein: ")
        filtered_history = [record for record in history if record['guest_name'].lower() == guest_name.lower()]
    else:
        print("Ungültige Auswahl!")
        return

    if not filtered_history:
        print("Keine Einträge gefunden.")
        return

    for record in filtered_history:
        print(f"\nZimmer Nummer: {record['room_number']}")
        print(f"  Gast Name: {record['guest_name']}")
        print(f"  Check-in: {record['check_in']}")
        print(f"  Check-out: {record['check_out'] if record['check_out'] else 'Noch nicht ausgecheckt'}")


# Hauptmenü
def main_menu():
    while True:
        print("\nHotel Buchungssystem")
        print("1. Zimmer Liste")
        print("2. Zimmer hinzufügen")
        print("3. Zimmer reservieren")
        print("4. Zimmer einchecken")
        print("5. Optionen auf Zimmer schreiben")
        print("6. Gast Optionen (z.B. Frühstück, Wellnessbereich)")
        print("7. Zimmer auschecken")
        print("8. Zimmer Informationen anzeigen")
        print("9. Verlauf anzeigen")
        print("10. Beenden")

        choice = input("Wähle eine Option: ")

        if choice == '1':
            list_rooms()
        elif choice == '2':
            add_room()
        elif choice == '3':
            reserve_room()
        elif choice == '4':
            book_room()
        elif choice == '5' or choice == '6':
            add_guest_options()
        elif choice == '7':
            checkout_room()
        elif choice == '8':
            room_info()
        elif choice == '9':
            view_history()
        elif choice == '10':
            break
        else:
            print("Ungültige Option, bitte erneut versuchen!")


if __name__ == "__main__":
    main_menu()