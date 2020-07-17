import requests
import json

def main():
    print('Below you can type an address in Flanders to plot the corresponding 3D House')
    print('Example: Sint-janstraat 20, 3583 Beringen')
    address = str(input('-> Please provide an address: ')) # is standard str so I don't need to specify
    if (re.match("^([A-z-]+)\s(\d+),\s(\d+)\s([A-z]+)"), address):
        print("Valid address")
    else:
        print("This address was not in the valid format.") # Hier aan pitsen dat als niet n input dan weer adres ingeven

    # COORDS FROM ADDRESS
    from geopy.geocoders import Nominatim  # I need to explicitly import Nominatim as such
    # import folium
    from pyproj import Proj, transform

    # retrieve coordinates from address
    locator = Nominatim(user_agent="myGeocode")
    location = locator.geocode('22, sint-janstraat, Beringen, Belgium')
    print('Latitude = {}, Longitude = {}'.format(location.latitude, location.longitude))

    # convert above coordinates to Lambert coordinates
    inProj = Proj('epsg:4326')
    outProj = Proj('epsg:31370')
    la1, lo1 = location.latitude, location.longitude
    la2, lo2 = transform(inProj, outProj, la1, lo1)
    print(la2, lo2)

    req = requests.get(f"http://loc.geopunt.be/geolocation/location?q={address}&c=1", )
    x = req.json()['LocationResult'][0]['Location']['X_Lambert72']
    y = req.json()['LocationResult'][0]['Location']['Y_Lambert72']
    print("x= ", x, " y= ", y)

main()