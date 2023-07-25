# pi_lightsensor_webthing
An internet-connected digital light sensor that measures the intensity of ambient light on the Raspberry Pi.

This project provides a [webthing API](https://iot.mozilla.org/wot/) for a digital light sensor like [BH1750](https://learn.adafruit.com/adafruit-bh1750-ambient-light-sensor).
Please note that you need to enable [I2C](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c) on the Raspberry Pi.

The pi_lightsensor_webthing package provides an http webthing endpoint that supports ambient light intensity measurement over http. E.g. 
```
# webthing has been started on host 192.168.0.23

curl http://192.168.0.23:9122/properties 

{
   "brightness": 100
}
```

For building and wiring the RaspberryPi/Digital Light Sensor, please refer to the tutorials above.

To install this software, you can use the [Docker](https://phoenixnap.com/kb/docker-on-raspberry-pi) or [PIP](https://realpython.com/what-is-pip/) package manager as shown below.

**Docker approach**
```
sudo docker run --privileged -p 9122:9122 grro/pi_lightsensor_webthing
```

**PIP approach**
```
sudo pip install pi_lightsensor_webthing
```

After this installation you can start the webthing http endpoint in your Python code or from the command line with
```
sudo lightsensor --command listen --port 9122 
```
This will bind the webthing API to the local port 9122.

As an alternative to the *listen* command, you can also use the *register* command to register and start the webthing service as a systemd unit.
This way, the webthing service will be started automatically at boot time. Starting the server manually with the *listen* command is no longer necessary. 
```
sudo lightsensor --command register --port 9122
```  
