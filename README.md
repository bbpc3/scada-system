# scada-system

## Pi Dokumentation

### Ports

| Port | Funktion    | Beschreibung                                            |
| ---- | ----------- | ------------------------------------------------------- |
| 8888 | LEDfx       | Webapp zur Steuerung der LEDs                           |
| 1881 | FUXA        | Scada/HMI Software zur Visualisierung                   |
| 1883 | MQTT-Broker | Zentrale stelle um mittels MQTT kommunizieren zu können |
| 8086 | InfluxDB2   | Timeseries Datenbank                                    |
| 9443 | Portainer   | Webapp um andere Dockercontainer zu verwalten           |
| 3005 | Chronograf  | Webapp um die InfluxDB zu verwalten                     |
| 3000 | Grafana     | Webapp um die InfluxDB zu verwalten                     |

---

### MQTT Dokumentation

#### Wärmepumpe

- `BasisTopic: /home/wp...`

| Beschreibung                 | Topic     | Payload - Einheit | Source     |
| ---------------------------- | --------- | ----------------- | ---------- |
| Zustandswerte der Wärmepumpe | /state    | JSON              | ESP8266-WP |
| Ändern des Ausleseintervalls | /interval | RAW - Sekunden    | FUXA       |

---

#### Solarsteuerung

- `BasisTopic: /home/solar...`

| Beschreibung                     | Topic     | Payload - Einheit | Source  |
| -------------------------------- | --------- | ----------------- | ------- |
| Zustandswerte der Solarsteuerung | /state    | JSON              | SD-Card |
| Ändern des Ausleseintervalls     | /interval | RAW - Sekunden    | FUXA    |

---

### Portainer Dokumentation

```
- User: admin
- Password: scada!system!123
```

---

### InfluxDB2 Dokumentation

```
- User: admin
- Password: scada!123
```

---

### Solarsteuerung

#### Verfügbare Env-Variablen

Variablen müssen im docker-compose file oder in Portainer gesetzt werden. Wird hier nichts gesetet, werden die angegebenen Standardwerte genutzt.

| Beschreibung                                                                  | Variablenname  | Default                      |
| ----------------------------------------------------------------------------- | -------------- | ---------------------------- |
| Mountpoint der genutzt wird um die SD-Karte zu mounten                        | mountpoint     | "/mnt/usb"                   |
| Befehl der genutzt wird, um die SSH-Verbindung zum Openwrtrouter herzustellen | sshcommand     | "ssh root@openwrt.fritz.box" |
| Transportart des MQTT-Clients                                                 | transport      | "tcp"                        |
| Hostname des MQTT-Brokers                                                     | brokerhostname | "raspberrypi.fritz.box"      |
| Port des MQTT-Services                                                        | mqttport       | "1883"                       |
| Topic für die Datenübertragung                                                | datatopic      | "/home/solar/state"          |
| Topic um geänderte Intervalle zu empfangen                                    | intervalTopic  | "/home/solar/interval"       |
| Die erste Zeile im .DAT file. (Sollte nicht geändert werden müssen)           | csvheader      | "...Sehr viel Text..."       |

---

### Wichtige Dateien

[comment]: <> (// @formatter:off)

<details>
<summary>docker-compose.yml</summary>

```yaml
version: "3"

services:
  fuxa:
    image: frangoteam/fuxa:latest
    container_name: fuxa
    ports:
      - 1881:1881
    restart: unless-stopped
    volumes:
      - ./folders/fuxa/appdata:/usr/src/app/FUXA/server/_appdata:rw
      - ./folders/fuxa/db:/usr/src/app/FUXA/server/_db:rw
      - ./folders/fuxa/logs:/usr/src/app/FUXA/server/_logs:rw
      - ./folders/fuxa/images:/usr/src/app/FUXA/server/_images:rw

  mosquitto:
    image: eclipse-mosquitto:latest
    container_name: mosquitto
    volumes:
      - ./folders/mosquitto/config:/mosquitto/config:rw
      - ./folders/mosquitto/data:/mosquitto/data:rw
      - ./folders/mosquitto/log:/mosquitto/log:rw

    ports:
      - 1883:1883
      - 9001:9001
    restart: always
  influxdb:
    image: influxdb:latest
    container_name: influxdb2
    volumes:
      - ./folders/influxdb/data:/var/lib/influxdb2:rw
    env_file: config.env
    ports:
      - 8086:8086
    restart: unless-stopped

  telegraf:
    image: telegraf:latest
    container_name: telegraf
    #    links:
    #      - influxdb
    volumes:
      #  Map Telegraf configuration file
      - ./folders/influxdb/telegraf.conf:/etc/telegraf/telegraf.conf:ro
      #  Map /tmp to permanent storage  (this includes /tmp/metrics.out)
      - ./folders/influxdb:/tmp:rw
    restart: unless-stopped
    depends_on:
      - influxdb
    links:
      - influxdb
  wireguard:
    image: lscr.io/linuxserver/wireguard:latest
    container_name: wireguard
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=Europe/London
      - SERVERURL=wireguard.domain.com #optional
      - SERVERPORT=51820 #optional
      - PEERS=1 #optional
      - PEERDNS=auto #optional
      - INTERNAL_SUBNET=10.13.13.0 #optional
      - ALLOWEDIPS=0.0.0.0/0 #optional
      - LOG_CONFS=true #optional
    volumes:
      - /path/to/appdata/config:/config
      - /lib/modules:/lib/modules
    ports:
      - 51820:51820/udp
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
    restart: unless-stopped
```

</details>

<details>
    <summary>ESP32 Sensorwerte</summary>

```python

sensornames = [
    (b'Einschaltdauer', 'str'),
    (b'T-Vorlauf', 'float'),
    (b'T-Heissgas', 'float'),
    (b'T-Aussen', 'float'),
    (b'T-Raum', 'float'),
    (b'T-Puffer', 'float'),
    (b'T-Boiler', 'float'),
    (b'T-Sauggas', 'float'),
    (b'T-WP2', 'float'),
    (b'T-Abtauung', 'float'),
    (b'T-Mischer', 'float'),
    (b'T-Raumsoll', 'float'),
    (b'T-Ruecklauf', 'float'),
    (b'Durchfluss', 'float'),
    (b'Pt1000 EVI', 'float'),
    (b'Steps EVI', 'float'),
    (b'Ueberhitz', 'float'),
    (b'Steps EEV', 'float'),
    (b'T-Verdampf', 'float'),
    (b'P-Sauggas', 'float'),
    (b'Solldrehz', 'float'),
    (b'MischPos', 'float'),
    (b'Mischer1', 'str')
]

```

</details>

[comment]: <> (// @formatter:on)
