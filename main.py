from includes.ArtistInf import Artist


artist = Artist("caner", "Çakır", "canercakir6134@gmail.com", "xxxxxxxxx", "Monday", 50)
artistDetails = artist.getDetails()
print(artistDetails["mail"])