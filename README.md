# pi_lightsensor_webthing
A web connected digital light sensor measuring the intensity of ambient light on Raspberry Pi

This project provides a [webthing API](https://iot.mozilla.org/wot/) to a digital light sensor such as mentioned in [Photo-resistor light sensor on Raspberry Pi](https://www.freva.com/2019/06/12/light-sensor-on-raspberry-pi/)  
running on a Raspberry Pi. As a webthing, the light sensor can be discovered and used by 
*home automation systems* or custom solutions supporting the webthing API.  

The pi_lightsensor_webthing package exposes an http webthing endpoint which supports measuring the intensity of ambient light via http. E.g. 
```
# webthing has been started on host 192.168.0.23

curl http://192.168.0.23:9122/properties 

{
   "bright": true
}
```

Regarding the RaspberryPi/digital light sensor hardware setup and wiring please refer tutorials mentioend above

To install this software you may use [PIP](https://realpython.com/what-is-pip/) package manager such as shown below
```
sudo pip install pi_lightsensor_webthing
```

After this installation you may start the webthing http endpoint inside your python code or via command line using
```
sudo lightsensor --command listen --port 9122 --gpio 131
```
Here, the webthing API will be bind to the local port 9122 and be connected to the light sensor digital pin using gpio 13

Alternatively to the *listen* command, you can use the *register* command to register and start the webthing service as systemd unit. 
By doing this the webthing service will be started automatically on boot. Starting the server manually using the *listen* command is no longer necessary. 
```
sudo lightsensor --command register --port 9122 --gpio 33
```  
