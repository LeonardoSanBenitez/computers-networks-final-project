bme280 = Bme280()
(chip_id, chip_version) = bme280.readBME280ID()
print("Sensor bme280 init OK")
print("Chip ID     :" + str(chip_id))
print("Version     :" + str(chip_version))

while(1):
    values = bme280.readBME280All()
    f = open("assets/log/log.txt", "w")
    f.write("Temp.: " + str(values['temperature']) + " C\n")
    f.write("Pressure: " + str(values['pressure']) + "hPa\n")
    f.write("Humidity : " + str(values['humidity']) + "%\n")
    f.close()
    print("Sensor log writed")