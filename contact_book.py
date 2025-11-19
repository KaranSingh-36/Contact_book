# Simple Contact Book Application
# Features: add, list, search, update, delete, export/import JSON, simple logging

import csv
import json
import os
from datetime import datetime

CSV_FILE = "contacts.csv"
JSON_FILE = "contacts.json"
LOG_FILE = "error_log.txt"
FIELDNAMES = ["Name", "Phone", "Email"]

def write_log(level, msg):
    """Append a simple timestamped log line."""
    try:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] [{level}] {msg}\n")
    except Exception:
        pass  # don't crash if logging fails

def ensure_csv_exists():
    """Create CSV with header if it does not exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def read_contacts():
    """Return a list of contacts (each is a dict)."""
    ensure_csv_exists()
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_contacts(contacts):
    """Overwrite CSV with the given list of contact dicts."""
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(contacts)

def add_contact():
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    email = input("Email: ").strip()
    if not name or not phone or not email:
        print("All fields are required.")
        return
    contacts = read_contacts()
    contacts.append({"Name": name, "Phone": phone, "Email": email})
    write_contacts(contacts)
    write_log("INFO", f"Added contact: {name}")
    print("Contact added.")

def list_contacts():
    contacts = read_contacts()
    if not contacts:
        print("No contacts found.")
        return
    print(f"\n{'Name':30} {'Phone':20} {'Email':30}")
    print("-" * 80)
    for c in contacts:
        print(f"{c['Name'][:29]:30} {c['Phone'][:19]:20} {c['Email'][:29]:30}")
    print(f"\nTotal: {len(contacts)}")

def search_contact():
    term = input("Enter name to search: ").strip().lower()
    found = [c for c in read_contacts() if term in c["Name"].lower()]
    if not found:
        print("No matches.")
        return
    for c in found:
        print(f"\nName: {c['Name']}\nPhone: {c['Phone']}\nEmail: {c['Email']}")

def update_contact():
    name = input("Enter exact name to update: ").strip()
    contacts = read_contacts()
    for c in contacts:
        if c["Name"].lower() == name.lower():
            print(f"Current phone: {c['Phone']}")
            new_phone = input("New phone (leave blank to keep): ").strip()
            if new_phone:
                c["Phone"] = new_phone
            new_email = input("New email (leave blank to keep): ").strip()
            if new_email:
                c["Email"] = new_email
            write_contacts(contacts)
            write_log("INFO", f"Updated contact: {name}")
            print("Contact updated.")
            return
    print("Contact not found.")

def delete_contact():
    name = input("Enter exact name to delete: ").strip()
    contacts = read_contacts()
    new_contacts = [c for c in contacts if c["Name"].lower() != name.lower()]
    if len(new_contacts) == len(contacts):
        print("Contact not found.")
        return
    write_contacts(new_contacts)
    write_log("INFO", f"Deleted contact: {name}")
    print("Contact deleted.")

def export_json():
    contacts = read_contacts()
    if not contacts:
        print("No contacts to export.")
        return
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2)
    write_log("INFO", f"Exported {len(contacts)} contacts to JSON.")
    print(f"Exported {len(contacts)} contacts to {JSON_FILE}.")

def import_json():
    if not os.path.exists(JSON_FILE):
        print("JSON file not found.")
        return
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            contacts = json.load(f)
            if not isinstance(contacts, list):
                raise ValueError("JSON must be a list of objects.")
            # Keep only required fields and write to CSV
            cleaned = []
            for c in contacts:
                cleaned.append({
                    "Name": str(c.get("Name", "")).strip(),
                    "Phone": str(c.get("Phone", "")).strip(),
                    "Email": str(c.get("Email", "")).strip()
                })
            write_contacts(cleaned)
            write_log("INFO", f"Imported {len(cleaned)} contacts from JSON.")
            print(f"Imported {len(cleaned)} contacts from {JSON_FILE}.")
        except Exception as e:
            print("Failed to import JSON:", e)
            write_log("ERROR", f"Import JSON failed: {e}")

def menu():
    while True:
        print("\nContact Book")
        print("1) Add  2) List  3) Search  4) Update  5) Delete  6) Export JSON  7) Import JSON  8) Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            add_contact()
        elif choice == "2":
            list_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            export_json()
        elif choice == "7":
            import_json()
        elif choice == "8":
            print("Goodbye.")
            write_log("INFO", "Program exited")
            break
        else:
            print("Invalid choice. Enter a number 1-8.")

if __name__ == "__main__":
    ensure_csv_exists()
    write_log("INFO", "Program started")
    menu()
