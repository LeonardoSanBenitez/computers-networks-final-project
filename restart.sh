# Bote no cron:
# 30 * * * * /home/pi/computers-networks-final-project/restart.sh
#o 30 é o intervalo em minutos
#isso ai tu vai colocar no arquivo que vai abrir quando digitar o comando: `sudo crontab -e`
#Vai repetir pra sempre

kill `pidof python3`
python3 /home/pi/computers-networks-final-project/main.py