import tkinter as tk
from tkinter import ttk, messagebox
from includes.Operations import save_user
from includes.ArtistInf import Artist
from includes.CostumerInf import Costumer
from includes.ServiceOps import load_services, add_service, delete_service

class ManagerPanel:
    def __init__(self, root, manager, users):
        self.root = root
        self.manager = manager
        self.users = users

        self.root.title("Nail Art Information System - Manager Panel")
        self.root.geometry("1100x700")
        self.root.config(bg="#fff")

        # Header
        header = tk.Label(root, text=f"💅 Nail Art Information System | Manager Dashboard",
                          font=("Helvetica", 18, "bold"), bg="#fcd6e2", fg="#333", pady=10)
        header.pack(fill="x")

        # Sidebar
        sidebar = tk.Frame(root, bg="#f7e6ed", width=240)
        sidebar.pack(side="left", fill="y")

        self.active_btn = None
        def add_button(text, command):
            btn = tk.Button(sidebar, text=text, font=("Arial", 11, "bold"),
                            bg="#f8b6c4", fg="white", relief="flat",
                            command=lambda: [self.activate(btn), command()])
            btn.pack(pady=15, fill="x")
            return btn

        self.btn_dash = add_button("Dashboard", self.dashboard)
        self.btn_users = add_button("Users", self.view_users)
        self.btn_add = add_button("Add User", self.add_user)
        self.btn_services = add_button("Services", self.manage_services)
        self.btn_logout = add_button("Logout", self.root.quit)

        # Main area
        self.content = tk.Frame(root, bg="white")
        self.content.pack(side="right", expand=True, fill="both")

        self.dashboard()

    # -----------------------------------------
    # Utility Functions
    # -----------------------------------------
    def activate(self, btn):
        if self.active_btn:
            self.active_btn.config(bg="#f8b6c4")
        btn.config(bg="#f47996")
        self.active_btn = btn

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # -----------------------------------------
    # DASHBOARD
    # -----------------------------------------
    def dashboard(self):
        self.clear_content()

        tk.Label(self.content, text="📊 Dashboard Overview", font=("Helvetica", 18, "bold"),
                 bg="white", fg="#444").pack(pady=20)

        artists = [u for u in self.users if u["type"] == "artist"]
        customers = [u for u in self.users if u["type"] == "customer"]
        total_earnings = sum([a["object"].getEarning() for a in artists])
        total_reservations = sum([len(a["object"].reservations) for a in artists])

        # Statistic cards
        cards = [
            ("Total Artists", len(artists)),
            ("Total Customers", len(customers)),
            ("Total Reservations", total_reservations),
            ("Total Earnings (₺)", total_earnings)
        ]

        card_frame = tk.Frame(self.content, bg="white")
        card_frame.pack(pady=20)

        for name, value in cards:
            c = tk.Frame(card_frame, bg="#fcd6e2", bd=1, relief="solid", width=200, height=100)
            c.pack(side="left", padx=20)
            c.pack_propagate(False)
            tk.Label(c, text=name, font=("Arial", 12, "bold"), bg="#fcd6e2", fg="#333").pack(pady=5)
            tk.Label(c, text=str(value), font=("Arial", 16, "bold"), bg="#fcd6e2", fg="#000").pack()

    # -----------------------------------------
    # VIEW USERS
    # -----------------------------------------
    def view_users(self):
        self.clear_content()
        tk.Label(self.content, text="👥 All Users", font=("Helvetica", 16, "bold"), bg="white", fg="#444").pack(pady=10)

        tree = ttk.Treeview(self.content, columns=("Type", "Username", "Name", "Mail"), show="headings", height=15)
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=200)

        for u in self.users:
            d = u["object"].getDetails()
            tree.insert("", "end", values=(u["type"], u["username"], f"{d['name']} {d['surname']}", d["mail"]))
        tree.pack(pady=20)

    # -----------------------------------------
    # ADD USER
    # -----------------------------------------
    def add_user(self):
        self.clear_content()
        tk.Label(self.content, text="➕ Create New User", font=("Helvetica", 16, "bold"),
                 bg="white", fg="#444").pack(pady=15)

        tk.Label(self.content, text="User Type:", bg="white").pack()
        self.user_type = ttk.Combobox(self.content, values=["artist", "customer"])
        self.user_type.pack(pady=5)

        fields = ["Username", "Password", "Name", "Surname", "Mail", "Phone", "OffDay"]
        self.entries = {}
        for field in fields:
            tk.Label(self.content, text=field + ":", bg="white").pack()
            e = tk.Entry(self.content)
            e.pack(pady=3)
            self.entries[field] = e

        def create_user():
            utype = self.user_type.get()
            if utype not in ["artist", "customer"]:
                messagebox.showerror("Error", "Select valid user type")
                return

            username = self.entries["Username"].get()
            password = self.entries["Password"].get()
            name = self.entries["Name"].get()
            surname = self.entries["Surname"].get()
            mail = self.entries["Mail"].get()
            phone = self.entries["Phone"].get()
            offday = self.entries["OffDay"].get()

            if not all([username, password, name, surname, mail, phone]):
                messagebox.showerror("Error", "Fill all fields")
                return

            if utype == "artist":
                obj = Artist(name, surname, mail, phone, offday or "Belirtilmedi", 0)
            else:
                obj = Costumer(name, surname, mail, phone)

            if save_user(utype, username, password, obj):
                self.users.append({
                    "type": utype,
                    "username": username,
                    "password": password,
                    "object": obj
                })
                messagebox.showinfo("Success", f"New {utype} created successfully!")
                self.view_users()
            else:
                messagebox.showerror("Error", "User could not be saved. Username may already exist.")

        tk.Button(self.content, text="Save User", bg="#f8b6c4", fg="white",
                  font=("Arial", 12, "bold"), command=create_user).pack(pady=10)

    # -----------------------------------------
    def manage_services(self):
        self.clear_content()
        tk.Label(self.content, text="💅 Manage Services", font=("Helvetica", 16, "bold"), bg="white", fg="#444").pack(pady=15)

        services = load_services()

        tree = ttk.Treeview(self.content, columns=("Service Name",), show="headings", height=10)
        tree.heading("Service Name", text="Service Name")
        for s in services:
            tree.insert("", "end", values=(s,))
        tree.pack(pady=10)

        entry = tk.Entry(self.content, width=30)
        entry.pack(pady=5)

        def add_new():
            name = entry.get().strip()
            if name:
                if add_service(name):
                    messagebox.showinfo("Added", f"'{name}' added successfully.")
                    self.manage_services()
                else:
                    messagebox.showwarning("Warning", f"'{name}' already exists.")

        def delete_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Error", "Select a service to delete.")
                return
            name = tree.item(sel[0])["values"][0]
            if delete_service(name):
                messagebox.showinfo("Deleted", f"'{name}' removed.")
                self.manage_services()
            else:
                messagebox.showerror("Error", "Service could not be deleted.")
            messagebox.showinfo("Deleted", f"'{name}' removed.")
            self.manage_services()

        tk.Button(self.content, text="Add Service", bg="#f8b6c4", fg="white",
                  font=("Arial", 12, "bold"), command=add_new).pack(pady=5)
        tk.Button(self.content, text="Delete Selected", bg="#f8b6c4", fg="white",
                  font=("Arial", 12, "bold"), command=delete_selected).pack(pady=5)
