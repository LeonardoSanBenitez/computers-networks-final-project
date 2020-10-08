# RemoteEXP

Complete docs on: https://docs.google.com/document/d/16KV8YbAj3a8sfPOGyVjEKWebncUCCB7gR_Yp_kgiS2w/edit?usp=sharing



## Communication MSP with raspberry

UART, 115200, no parity, 1 stopbit

Frame:

| Field    | Size | Description                                 |
| -------- | ---- | ------------------------------------------- |
| N_REQ    | 2    | sequencial ID of the request                |
| PAYLOAD  | 1    | See list of commands below                  |
| CHECKSUM | 1    | 8 bits checksum, $!(\sum \text{byte})\%256$ |

List of commands:

* `0x00`: read motor state; Expects 1 byte as answer
* `0x80`: go forth; expects ACK/NACK as answer
* `0x81`: turn left; expects ACK/NACK as answer
* `0x82`: turn right; expects ACK/NACK as answer
* `0x83`: stop; expects ACK/NACK as answer
* `0x84`: go back; expects ACK/NACK as answer



#  Enviroment configurations

## Local: Conda

* Used for development
* We should create the environment (if it don’t exist yet), activate, run jupyter
* The dependencies should be installed with `conda install`, if possible

```
 conda create -n devRaspberryCV \
 python=3.7.6 numpy=1.18.1 opencv=3.4.2 \
 matplotlib=3.1.3 seaborn=0.10.0 \
 pandas=1.0.1 tensorflow=2.1.0 keras=2.3.1 Pillow=7.0.0 \
 jupyter=1.0.0 nb_conda=2.2.1
 conda activate devRaspberryCV
```

* If you need to install something not available, in conda, use pip3:

```
 pip3 install -r requirements.txt    
```

## Embedded: venv

* Raspbian 9.11 stretch

* mainly just production

* To activate: `source .virtualenvs/cv/bin/activate`

* See instalation details in *Raspberry - OpenCV*

* **Requirements**

  * raspbian strech lite
  * openCV==3.3.0
  * Python==3.5 
  * picamera
  * Numpy==1.18.1

* **LCD requirements**

  * adafruit-blinka??
  * `pip3 install adafruit-circuitpython-charlcd`

* **Sensor requiremetns**

  * enable I2C

  * ```
     sudo apt-get install -y i2c-tools
     pip3 install smbus
    ```

* **Run project**

  * `python3 main.py`

  * or in background, `nohup python3 main.py &`

## Cloud: AWS

* Log in intro instance

* Install git, docker, docker-compose

* The mqtt subscribe script is running outside the container, so you also have to install pip and paho

```
sudo apt install python3-pip
pip3 install paho-mqtt
```

* Run forever:

```
nohup python3 mqtt_sub.py &
cd web_server 
docker-compose build
docker-compose up -d
```

* Right now it's running on 107.21.56.72