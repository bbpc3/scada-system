import os

mountpoint=os.getenv('mountpoint', '/mnt/usb')
basepath=f'{mountpoint}/LOGFILES/'

sshcommand=os.getenv('sshcommand', 'ssh -o "StrictHostKeyChecking=no" root@openwrt.fritz.box')
csvheader = os.getenv('csvheader', 'Time	TS1 [°C]	TS2 [°C]	TS3 [°C]	TS4 [°C]	TS5 [°C]	TS6 [°C]	UI1 [°C]	RO1 [%]	RO2 [%]	REL [%]	RO1 Safety	RO2 Safety	REL Safety	Vol. flow	Vol. flow 3	Vol. flow 4	Heat quantity	Heat quantity 1	Heat quantity 2	Heat quantity 3	Heat quantity 4	CO2 Savings	Errors')


# MQTT Settings
transport = os.getenv('transport', 'tcp') # or 'tcp'
broker = os.getenv('brokerhostname','raspberrypi.fritz.box') # eg. choosen-name-xxxx.cedalo.cloud
myport = os.getenv('mqttport', 1883)
dataTopic = os.getenv('datatopic', '/home/wp/state')

