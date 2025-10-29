from includes.Humans import Humans

class Costumer(Humans):
	def __init__(self, name, surname, mail, phone):
		super().__init__(name, surname, mail, phone)
		self.reservation = []

	def setReservation(self, day, hour, service):
		self.reservation.append({
			"day": day,
			"hour": hour,
			"service": service
			})

	def getReservation(self):
		return (self.reservation)
