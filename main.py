from includes.ArtistInf import Artist
from includes.CostumerInf import Costumer
from includes.ManagerInf import Manager


manager = Manager("Caner", "Çakır", "caner@mail.com", "555", "Sunday")
artists = [Artist("Ayşe", "Yılmaz", "ayse@mail.com", "444", "Monday", 500)]
customers = [Costumer("Ali", "Kaya", "ali@mail.com", "333")]

print(manager.getDetails())
print(manager.viewAllArtists(artists))
print(manager.viewAllCustomers(customers))