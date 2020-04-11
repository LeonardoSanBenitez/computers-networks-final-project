from bme280 import Bme280

bme280 = Bme280()
(chip_id, chip_version) = bme280.readBME280ID()
print("Sensor bme280 init OK")
print("Chip ID     :" + str(chip_id))
print("Version     :" + str(chip_version))

while(1):
    temperature,pressure,humidity = bme280.readBME280All()
    f = open("assets/log/log.txt", "w")
    f.write("Temp.: " + str(temperature) + " C\n")
    f.write("Pressure: " + str(pressure) + "hPa\n")
    f.write("Humidity : " + str(humidity) + "%\n")
    f.close()
    #print("Sensor log writed")
