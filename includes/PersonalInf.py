#dateOfReservation must be a dict and key must be day value must be a list of hours
class PersonalInfos():
	def __init__(self, name, daysToWork, reservations, grossPerReservation):
		self.name = name
		self.daysToWork = daysToWork
		self.reservations = reservations
		self.grossPerReservation = grossPerReservation
		self.dateOfReservations = {}
		for day in daysToWork:
			self.dateOfReservations[day] = []

	def howMuchEarns(self):
		money = (self.reservations) * (self.grossPerReservation)
		return (money)

	def addReservation(self, day, hour):
		if (day not in self.daysToWork):
			print(self.name + ", " + day + " gününde izinli.")
			return
		if (day not in self.dateOfReservations):
			self.dateOfReservations[day] = []
		if (hour in self.dateOfReservations[day]):
			print(self.name + ", " + day + " günü" + hour + " saatinde dolu.")
			return
		self.dateOfReservations[day].append(hour)
		self.reservations += 1
		print(self.name + "için, " + day + " günü " + hour + "saatine randevu eklendi.")

	def cancelReservation(self, day, hour):
		if ((day in self.dateOfReservations) and (hour in self.dateOfReservations[day])):
			self.dateOfReservations[day].remove(hour)
			self.reservations -= 1
			print(f"{day} günü {hour} rezervasyonu iptal edildi.")
		else:
			print("İptal edilecek rezervasyon bulunamadı.")

	def showSchedule(self):
		print(self.name + " Rezervasyonları:")
		for day, hours in self.dateOfReservations.items():
			if hours:
				print(f"{day}: {', '.join(hours)}")
			else:
				print(f"{day}: Boş")
