import tkinter as tk
from tkinter import ttk, messagebox
from includes.ResOps import load_reservations, add_reservation, delete_reservation
from tkcalendar import DateEntry
from datetime import datetime
from includes.ServiceOps import load_services


class CustomerPanel:
	def __init__(self, root, customers, artists):
		self.root = root
		self.root.title("Nail Art Information System - Customer Panel")
		self.root.geometry("900x600")
		self.root.config(bg="#fff")
		self.customers = customers
		self.customer = customers[0]
		self.artists = artists
		# Header
		header = tk.Label(root, text="💅 Nail Art Information System",
						font=("Helvetica", 18, "bold"),
						bg="#fcd6e2", fg="#444", pady=10)
		header.pack(fill="x")
		# Sidebar
		sidebar = tk.Frame(root, bg="#f7e6ed", width=200)
		sidebar.pack(side="left", fill="y")
		tk.Button(sidebar, text="Book Appointment", font=("Arial", 11, "bold"),
				bg="#f8b6c4", fg="white", command=self.book_appointment).pack(pady=20, fill="x")
		tk.Button(sidebar, text="My Appointments", font=("Arial", 11, "bold"),
				bg="#f8b6c4", fg="white", command=self.view_appointments).pack(pady=10, fill="x")
		tk.Button(sidebar, text="Logout", font=("Arial", 11, "bold"),
				bg="#f8b6c4", fg="white", command=self.root.quit).pack(side="bottom", fill="x", pady=10)
		# Main content
		self.content = tk.Frame(root, bg="white")
		self.content.pack(side="right", expand=True, fill="both")
		self.view_appointments()

	def clear_content(self):
		for widget in self.content.winfo_children():
			widget.destroy()

	# -------------------------------
	# BOOK APPOINTMENT
	# -------------------------------

	def book_appointment(self):
		self.clear_content()
		tk.Label(self.content, text="Book Appointment",
				font=("Helvetica", 16, "bold"), bg="white", fg="#444").pack(pady=15)
		tk.Label(self.content, text="Select Artist:", bg="white").pack()
		artist_names = [f"{a.getDetails()['name']} {a.getDetails()['surname']}" for a in self.artists]
		self.artist_combo = ttk.Combobox(self.content, values=artist_names)
		self.artist_combo.pack(pady=5)
		# --- Date picker ---
		tk.Label(self.content, text="Select Date:", bg="white").pack()
		self.date_picker = DateEntry(self.content, mindate=datetime.now().date(), date_pattern='dd/mm/yyyy')
		self.date_picker.pack(pady=5)
		# --- Time entry ---
		tk.Label(self.content, text="Hour (e.g. 14:30):", bg="white").pack()
		self.entry_hour = tk.Entry(self.content)
		self.entry_hour.pack(pady=5)
		# --- Services (checkbox list) ---
		tk.Label(self.content, text="Select Services:", bg="white").pack(pady=5)
		self.service_vars = []
		self.services = self.service_ops.load_services()
		# --- Services (checkbox list) ---
		tk.Label(self.content, text="Select Services:", bg="white").pack(pady=5)
		self.service_vars = []
		self.services = load_services()
		for s in self.services:nd((s, var))
		tk.Button(self.content, text="Confirm Booking",
				bg="#f8b6c4", fg="white", font=("Arial", 12, "bold"),
				command=self.confirm_booking).pack(pady=10)

	def confirm_booking(self):
		artist_index = self.artist_combo.current()
		if artist_index == -1:
			messagebox.showwarning("Error", "Please select an artist")
			return
		artist = self.artists[artist_index]
		details_c = self.customer.getDetails()
		details_a = artist.getDetails()
		day = self.date_picker.get_date().strftime("%d/%m/%Y")
		hour = self.entry_hour.get().strip()
		services_selected = [s for s, v in self.service_vars if v.get()]
		if not services_selected:
			messagebox.showwarning("Error", "Please select at least one service")
			return
		service = ", ".join(services_selected)
		if not day or not hour or not service:
			messagebox.showwarning("Error", "Please fill all fields")
			return
		reservation_data = {
			"customer_name": f"{details_c['name']} {details_c['surname']}",
			"customer_mail": details_c["mail"],
			"artist_name": f"{details_a['name']} {details_a['surname']}",
			"artist_mail": details_a["mail"],
			"day": day,
			"hour": hour,
			"service": service
		}
		add_reservation(reservation_data)
		messagebox.showinfo("Success", f"Appointment booked with {details_a['name']} on {day} at {hour}")
		self.view_appointments()
	# -------------------------------
	# VIEW / CANCEL APPOINTMENTS
	# -------------------------------
	def view_appointments(self):
		self.clear_content()
		tk.Label(self.content, text="My Appointments",
				font=("Helvetica", 16, "bold"), bg="white", fg="#444").pack(pady=10)
		reservations = load_reservations()
		details = self.customer.getDetails()
		my_res = [r for r in reservations if r["customer_mail"] == details["mail"]]
		if not my_res:
			tk.Label(self.content, text="No appointments found.", bg="white", fg="#777").pack(pady=20)
			return
		tree = ttk.Treeview(self.content, columns=("Artist", "Day", "Hour", "Service"), show="headings", height=10)
		for col in tree["columns"]:
			tree.heading(col, text=col)
		for r in my_res:
			tree.insert("", "end", values=(r["artist_name"], r["day"], r["hour"], r["service"]))
		tree.pack(pady=10)
		def cancel_selected():
			selected = tree.selection()
			if not selected:
				messagebox.showwarning("Error", "Select an appointment to cancel.")
				return
			values = tree.item(selected[0])["values"]
			artist, day, hour, service = values
			delete_reservation(details["mail"], day, hour)
			messagebox.showinfo("Cancelled", f"Appointment on {day} at {hour} has been cancelled.")
			self.view_appointments()
		tk.Button(self.content, text="Cancel Selected Appointment",
				bg="#f8b6c4", fg="white", font=("Arial", 12, "bold"),
				command=cancel_selected).pack(pady=10)