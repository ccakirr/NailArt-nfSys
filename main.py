import tkinter as tk
from tkinter import messagebox
from includes.Operations import load_users
from gui.customer import CustomerPanel
from gui.artist import ArtistPanel
from gui.manager import ManagerPanel
from database.db_manager import init_database

def start_gui(user_type, user_obj, all_users):
	root = tk.Tk()
	if user_type == "customer":
		CustomerPanel(root, [user_obj], [u["object"] for u in all_users if u["type"] == "artist"])
	elif user_type == "artist":
		ArtistPanel(root, user_obj)
	elif user_type == "manager":
		ManagerPanel(root, user_obj, all_users)
	root.mainloop()

def main():
	init_database()
	
	users = load_users()
	login = tk.Tk()
	login.title("Nail Art Information System - Login")
	login.geometry("400x350")
	login.config(bg="white")
	tk.Label(login, text="User Login", font=("Helvetica", 16, "bold"), bg="white").pack(pady=20)
	tk.Label(login, text="Username:", bg="white").pack()
	entry_user = tk.Entry(login)
	entry_user.pack(pady=5)
	tk.Label(login, text="Password:", bg="white").pack()
	entry_pass = tk.Entry(login, show="*")
	entry_pass.pack(pady=5)
	def login_user():
		username = entry_user.get().strip()
		password = entry_pass.get().strip()
		for u in users:
			if u["username"] == username and u["password"] == password:
				login.destroy()
				start_gui(u["type"], u["object"], users)
				return
		messagebox.showerror("Login Failed", "Invalid username or password")
	tk.Button(login, text="Login", bg="#f8b6c4", fg="white", font=("Arial", 12, "bold"),
			width=20, command=login_user).pack(pady=20)
	tk.Label(login, text="Default Admin: admin / 1234", bg="white", fg="#888").pack(pady=10)
	login.mainloop()


if __name__ == "__main__":
	main()
