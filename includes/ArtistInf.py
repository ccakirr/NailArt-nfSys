from includes.Humans import Humans

class Artist(Humans):
	def __init__(self, name, surname, mail, phone, offDay, earnings):
		super().__init__(name, surname, mail, phone)
		self.__offDay = offDay
		self.__earnings = earnings
		self.reservations = []

	def getDetails(self):
		details = super().getDetails()
		details.update({
			"offDay": self.__offDay,
			"earnings": self.__earnings,
			"totalReservations": len(self.reservations)
		})
		return (details)

	def setOffDay(self, day):
		self.__offDay = day

	def getOffDay(self):
		return (self._offDay)

	def setEarning(self, earning):
		self.__earnings = earning

	def getEarning(self):
		return (self.__earnings)

	def setReservation(self, costumerDetails, day, hour, service):
		self.reservations.append({
			"name": costumerDetails.name,
			"surname": costumerDetails.surname,
			"mail": costumerDetails.mail,
			"phone": costumerDetails.phone,
			"day": day,
			"hour": hour,
			"service": service
		})