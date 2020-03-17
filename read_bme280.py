import bme280

(chip_id, chip_version) = bme280.readBME280ID()
#print("Chip ID     :" + str(chip_id))
#print("Version     :" + str(chip_version))

while(1):
  temperature,pressure,humidity = bme280.readBME280All()
  f = open("log.txt", "w")
  f.write("Temperature : " + str(temperature) + "C\n")
  f.write("Pressure: " + str(pressure) + "hPa\n")
  f.write("Humidity : " + str(humidity) + "%")
  f.close()
