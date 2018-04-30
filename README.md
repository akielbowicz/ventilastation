# ventilastation

Desarrollo del ventilastation en el PyCamp 2018


Instalar screen

```
screen /dev/ttyUSB0 115200
```


Si no se puede comunicar hay que agregar el usuario al grupo


```
sudo usermod -a -G dialout usr_name

newgrp dialout
```

Una vez logeado en el grupo, correr nuevamente la conexion

Y te devuelve la repl de micropython de la ESP8266

ampy --port /dev/ttyUSB0 --baud 115200 put send_data.py 
