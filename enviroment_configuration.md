

# Enviroment configurations

## Local: Conda

* Used for development
* We should create the environment (if it don’t exist yet), activate, run jupyter
* The dependencies should be installed with `conda install`, if possible

```bash
conda create -n devRaspberryCV \
python=3.7.6 numpy=1.18.1 opencv=3.4.2 \
matplotlib=3.1.3 seaborn=0.10.0 \
pandas=1.0.1 tensorflow=2.1.0 keras=2.3.1 Pillow=7.0.0 \
jupyter=1.0.0 nb_conda=2.2.1
```
```bash
conda activate devRaspberryCV
```

* If you need to install something not available, in conda, use pip3:

```bash
pip3 install -r requirements.txt	
```




matplotlib seaborn \
pandas   tensorflow keras \
Pillow jupyter nb_conda

## Embedded: venv
* mainly just production

* To activate: `source .virtualenvs/cv/bin/activate`

* See instalation datails in *Raspberry - OpenCV*

* **Requirements**
  * raspbian strech lite
  * openCV==3.3.0
  * Python==3.5 
  * picamera
  * Numpy==1.18.1
  * ==something to TCP-IP socket?==	
  
* LCD requirements

  * adafruit-blinka
  * adafruit-circuitpython-charlcd

* Sensor requiremetns

  * enable I2C

  * ```
    sudo apt-get install -y python-smbus i2c-tools
    ```

## Cloud: ?







## External libs

* Pillow
  * free library for the Python programming language that adds support for opening, manipulating, and saving many different image file formats