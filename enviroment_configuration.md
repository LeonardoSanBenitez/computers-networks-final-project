

# Enviroment configurations

## Local: Conda
* Used for development
* We should create the enviroment (if it don’t exist yet), activate, run jupyter
* The dependencies shuld be installed with `conda install`, if possible

```
conda create -n devRaspberryCV python=3.6.9 numpy=1.18.1 pandas=0.25.1 matplotlib=3.1.1 opencv=3.4.2 tensorflow=1.14.0 keras=2.2.4 seaborn=0.9.0 Pillow jupyter nb_conda

conda activate devRaspberryCV
```

* If you need to install something not available, in conda, use pip3:

```
pip3 install -r requirements.txt	
```



conda create -n devRaspberryCV python=3.5 numpy=1.18.1 opencv=3.4.2 \
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

## Cloud: ?