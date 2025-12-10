from Humans import Humans

class Manager(Humans):
	def __init__(self, name, surname, mail, phone, offDay):
		super().__init__(name, surname, mail, phone)
		self.__offDay = offDay

	def setOffDay(self, day):
		self.__offDay = day

	def getOffDay(self):
		return (self.__offDay)

	def getDetails(self):
		details = super().getDetails()
		details.update({
			"offDay": self.__offDay
		})
		return (details)

	def viewAllArtists(self, artistList):
		return [artist.getDetails() for artist in artistList]

	def viewAllCustomers(self, customerList):
		return [customer.getDetails() for customer in customerList]