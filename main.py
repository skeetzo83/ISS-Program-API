import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 7.059697  # Your latitude
MY_LONG = 125.606192  # Your longitude
my_email = "XXX@gmail.com"
my_password = "yourpassword"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])
time_now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")


def compare_location():
    long_diff = abs(iss_longitude - MY_LONG)
    lat_diff = abs(iss_latitude - MY_LAT)

    if lat_diff <= 5 and long_diff <= 5:
        return True
    else:
        return False


response_sunset = requests.get(url="https://api.sunrisesunset.io/json?lat=7.059697&lng=125.606192")
response_sunset.raise_for_status()
data_sunset = response_sunset.json
sunset_time = data_sunset()["results"]["sunset"]

not_now = True
while not_now:
    time.sleep(60)
    if time_now >= sunset_time and compare_location() == True:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=my_email, to_addrs=my_email, msg="Subject:ISS Program\n\nLook up!"
                                                                           " The ISS satellite is above you!")
