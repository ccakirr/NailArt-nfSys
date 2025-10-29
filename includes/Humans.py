class Humans:
	def __init__(self, name, surname, mail, phone):
		self.__name = name
		self.__surname = surname
		self.__mail = mail
		self.__phone = phone
	
	def getDetails(self):
		return {
			"name": self.__name,
			"surname": self.__surname,
			"mail": self.__mail,
			"phone": self.__phone
			}