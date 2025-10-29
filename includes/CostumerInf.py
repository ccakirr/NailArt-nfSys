class Costumer:
	def __init__(self, name, surname, mail, phone):
		self.__name = name
		self.__surname = surname
		self.__mail = mail
		self.__phone = phone
		self.reservation = []

	def getPersonalDetails(self):
		return {
			"name": self.__name, 
			"surname": self.__surname,
			"mail": self.__mail,
			"phone": self.__phone
			}

	def setReservation(self, day, hour, service):
		self.reservation.append({
			"day": day,
			"hour": hour,
			"service": service
			})

	def getReservation(self):
		return (self.reservation)
