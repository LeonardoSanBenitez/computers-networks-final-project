import bme280

(chip_id, chip_version) = readBME280ID()
temperature,pressure,humidity = readBME280All()
print("Chip ID     :" + str(chip_id))
print("Version     :" + str(chip_version))
while(1):
    f = open("log.txt", "w")
    f.write("Temperature : ", temperature, "C\n")
    f.write("Pressure: ", pressure, "hPa\n")
    f.write("Humidity : ", humidity, "%")
    f.close()