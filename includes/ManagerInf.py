from CostumerInf import CustomerInf
from PersonalInf import PersonalInf

class ManagerInf:
    def __init__(self):
		self.customers = []
		self.artists = []

    def add_customer(self, customer):
        if isinstance(customer, CustomerInf):
            self.customers.append(customer)
        else:
            raise TypeError("customer must be a CustomerInf instance")

    def add_artist(self, artist):
        if isinstance(artist, PersonalInf):
            self.artists.append(artist)
        else:
            raise TypeError("artist must be a PersonalInf instance")

    def list_customers(self):
        for c in self.customers:
            print(f"Customer: {c.name}, Phone: {c.phone}")

    def list_artists(self):
        for a in self.artists:
            print(f"Artist: {a.name}, Specialty: {a.specialty}")
