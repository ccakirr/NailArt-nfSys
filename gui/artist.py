import tkinter as tk
from tkinter import ttk, messagebox
from includes.ResOps import load_reservations, save_reservations
from includes.Operations import update_user_earnings
from datetime import datetime


class ArtistPanel:
	def __init__(self, root, artist):
		self.root = root
		self.artist = artist
		self.root.title("Nail Art Information System - Artist Panel")
		self.root.geometry("950x600")
		self.root.config(bg="#fff")
		header = tk.Label(root, text=f"🎨 Artist Panel - {artist.getDetails()['name']} {artist.getDetails()['surname']}",
						font=("Helvetica", 18, "bold"), bg="#fcd6e2", fg="#444", pady=10)
		header.pack(fill="x")
		sidebar = tk.Frame(root, bg="#f7e6ed", width=220)
		sidebar.pack(side="left", fill="y")
		tk.Button(sidebar, text="View My Reservations", font=("Arial", 11, "bold"),
				bg="#f8b6c4", fg="white", command=self.view_reservations).pack(pady=15, fill="x")
		tk.Button(sidebar, text="Delete Reservation", font=("Arial", 11, "bold"),
				bg="#f8b6c4", fg="white", command=self.delete_reservation).pack(pady=10, fill="x")
		tk.Button(sidebar, text="Update Earnings", font=("Arial", 11, "bold"),
				bg="#f8b6c4", fg="white", command=self.update_earnings).pack(pady=10, fill="x")
		tk.Button(sidebar, text="Logout", font=("Arial", 11, "bold"),
				bg="#f8b6c4", fg="white", command=self.root.quit).pack(side="bottom", fill="x", pady=10)
		self.content = tk.Frame(root, bg="white")
		self.content.pack(side="right", expand=True, fill="both")
		self.view_reservations()

	def clear_content(self):
		for widget in self.content.winfo_children():
			widget.destroy()

	def get_artist_reservations(self):
		all_res = load_reservations()
		my_mail = self.artist.getDetails()["mail"]
		today = datetime.now().date()

		my_res = []
		for r in all_res:
			if r["artist_mail"] == my_mail:
				try:
					res_date = datetime.strptime(r["day"], "%d/%m/%Y").date()
					if res_date >= today:
						my_res.append(r)
				except:
					my_res.append(r)  # tarih parse edilemezse yine ekle
		self.artist.reservations = my_res
		return my_res


	def view_reservations(self):
		self.clear_content()
		tk.Label(self.content, text="My Reservations", font=("Helvetica", 16, "bold"), bg="white", fg="#444").pack(pady=10)
		reservations = self.get_artist_reservations()
		if not reservations:
			tk.Label(self.content, text="No reservations yet.", bg="white", fg="#777").pack(pady=20)
			return
		self.tree = ttk.Treeview(self.content, columns=("Customer", "Day", "Hour", "Service"), show="headings", height=12)
		for col in self.tree["columns"]:
			self.tree.heading(col, text=col)
		for r in reservations:
			self.tree.insert("", "end", values=(r["customer_name"], r["day"], r["hour"], r["service"]))
		self.tree.pack(pady=15)
	
	def delete_reservation(self):
		self.clear_content()
		tk.Label(self.content, text="Delete Reservation", font=("Helvetica", 16, "bold"), bg="white", fg="#444").pack(pady=15)

		reservations = self.get_artist_reservations()
		if not reservations:
			tk.Label(self.content, text="No reservations available.", bg="white", fg="#777").pack(pady=20)
			return

		self.tree = ttk.Treeview(self.content, columns=("Customer", "Day", "Hour", "Service"), show="headings", height=12)
		for col in self.tree["columns"]:
			self.tree.heading(col, text=col)
		for r in reservations:
			self.tree.insert("", "end", values=(r["customer_name"], r["day"], r["hour"], r["service"]))
		self.tree.pack(pady=15)

		# ⚠️ delete_selected artık bu fonksiyonun içinde, bir tab içeride!
		def delete_selected():
			selected = self.tree.selection()
			if not selected:
				messagebox.showwarning("Error", "Select a reservation to delete.")
				return

			val = self.tree.item(selected[0])["values"]
			customer, day, hour, service = val
			all_res = load_reservations()
			updated = [r for r in all_res if not (
				r["artist_mail"] == self.artist.getDetails()["mail"]
				and r["day"] == day
				and r["hour"] == hour
			)]
			save_reservations(updated)
			messagebox.showinfo("Deleted", f"Reservation for {customer} on {day} at {hour} deleted.")
			self.view_reservations()

		tk.Button(self.content, text="Delete Selected", bg="#f8b6c4", fg="white",
				font=("Arial", 12, "bold"), command=delete_selected).pack(pady=10)

	
	def update_earnings(self):
		self.clear_content()
		tk.Label(self.content, text="Update Earnings", font=("Helvetica", 16, "bold"),
				bg="white", fg="#444").pack(pady=15)
		tk.Label(self.content, text=f"Current Earnings: {self.artist.getEarning()} ₺",
				bg="white", fg="#666", font=("Arial", 12, "italic")).pack(pady=10)
		tk.Label(self.content, text="New Amount:", bg="white").pack()
		entry = tk.Entry(self.content)
		entry.pack(pady=5)
		def save_earn():
			try:
				val = float(entry.get())
				self.artist.setEarning(val)
				# Veritabanını güncelle
				update_user_earnings(self.artist.getDetails()["mail"], val)
				messagebox.showinfo("Updated", f"Earnings updated to {val} ₺")
				self.update_earnings()
			except ValueError:
				messagebox.showerror("Error", "Please enter a valid number")
		tk.Button(self.content, text="Save", bg="#f8b6c4", fg="white",
				font=("Arial", 12, "bold"), command=save_earn).pack(pady=10)