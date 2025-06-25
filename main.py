import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

DATA_FILE = 'contacts.json'

def load_contacts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

def save_contacts():
    with open(DATA_FILE, 'w') as file:
        json.dump(contacts, file, indent=4)

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    address = address_entry.get()

    if not name or not phone:
        messagebox.showwarning("Input Error", "Name and phone are required.")
        return

    for contact in contacts:
        if contact['phone'] == phone:
            messagebox.showerror("Duplicate", "Contact with this phone already exists.")
            return

    contacts.append({'name': name, 'phone': phone, 'email': email, 'address': address})
    save_contacts()
    messagebox.showinfo("Success", "Contact added.")
    clear_entries()
    display_contacts()

def display_contacts():
    contact_listbox.delete(0, tk.END)
    for contact in contacts:
        contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

def search_contact():
    query = search_entry.get().lower()
    contact_listbox.delete(0, tk.END)
    for contact in contacts:
        if query in contact['name'].lower() or query in contact['phone']:
            contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

def delete_contact():
    selected = contact_listbox.curselection()
    if not selected:
        messagebox.showwarning("Select Contact", "Please select a contact to delete.")
        return
    index = selected[0]
    contact = contacts[index]
    if messagebox.askyesno("Confirm Delete", f"Delete {contact['name']}?"):
        contacts.pop(index)
        save_contacts()
        display_contacts()

def update_contact():
    selected = contact_listbox.curselection()
    if not selected:
        messagebox.showwarning("Select Contact", "Select a contact to update.")
        return
    index = selected[0]
    contact = contacts[index]

    name = simpledialog.askstring("Update Name", "Enter new name:", initialvalue=contact['name'])
    phone = simpledialog.askstring("Update Phone", "Enter new phone:", initialvalue=contact['phone'])
    email = simpledialog.askstring("Update Email", "Enter new email:", initialvalue=contact['email'])
    address = simpledialog.askstring("Update Address", "Enter new address:", initialvalue=contact['address'])

    if name and phone:
        contacts[index] = {'name': name, 'phone': phone, 'email': email, 'address': address}
        save_contacts()
        display_contacts()
    else:
        messagebox.showerror("Error", "Name and phone are required.")

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

contacts = load_contacts()
root = tk.Tk()
root.title("Contact Book")
root.geometry("600x550")

main_frame = tk.Frame(root)
main_frame.pack(expand=True)

tk.Label(main_frame, text="Name").grid(row=0, column=0, sticky='e', padx=5, pady=5)
name_entry = tk.Entry(main_frame, width=40)
name_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

tk.Label(main_frame, text="Phone").grid(row=1, column=0, sticky='e', padx=5, pady=5)
phone_entry = tk.Entry(main_frame, width=40)
phone_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

tk.Label(main_frame, text="Email").grid(row=2, column=0, sticky='e', padx=5, pady=5)
email_entry = tk.Entry(main_frame, width=40)
email_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

tk.Label(main_frame, text="Address").grid(row=3, column=0, sticky='e', padx=5, pady=5)
address_entry = tk.Entry(main_frame, width=40)
address_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

tk.Button(main_frame, text="Add Contact", width=15, command=add_contact).grid(row=4, column=1, pady=10)
tk.Button(main_frame, text="Update Selected", width=15, command=update_contact).grid(row=5, column=1)
tk.Button(main_frame, text="Delete Selected", width=15, command=delete_contact).grid(row=6, column=1)

tk.Label(main_frame, text="Search").grid(row=7, column=0, sticky='e', padx=5, pady=10)
search_entry = tk.Entry(main_frame, width=30)
search_entry.grid(row=7, column=1, sticky='w', pady=10)
tk.Button(main_frame, text="Search", command=search_contact).grid(row=7, column=2, padx=5)

contact_listbox = tk.Listbox(main_frame, width=60, height=12)
contact_listbox.grid(row=8, column=0, columnspan=3, pady=10)

display_contacts()

root.mainloop()