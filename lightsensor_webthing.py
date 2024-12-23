import sys
import logging
import tornado.ioloop
from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
from lightsensor import LightSensor


class LightSensorThing(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, light_sensor: LightSensor):
        Thing.__init__(
            self,
            'urn:dev:ops:illuminanceSensor-1',
            'Illuminance Sensor',
            ['MultiLevelSensor'],
            "light sensor"
        )

        self.ioloop = tornado.ioloop.IOLoop.current()

        self.light_sensor = light_sensor
        light_sensor.listen(self.on_measured)

        self.bright = Value(0)
        self.add_property(
            Property(self,
                     'brightness',
                     self.bright,
                     metadata={
                         'title': 'Brightness',
                         "type": "integer",
                         'unit': 'lux',
                         'description': '"The brightness level in lux',
                         'readOnly': True,
                     }))

        self.smoothing_window = Value(light_sensor.smoothing_window_sec, light_sensor.update_smoothing_window)
        self.add_property(
            Property(self,
                     'smoothing_window',
                     self.smoothing_window,
                     metadata={
                         'title': 'smoothing window',
                         "type": "integer",
                         'unit': 'second',
                         'description': '"The smoothing window',
                         'readOnly': False,
                     }))

        self.sampling_rate = Value(light_sensor.sampling_rate_sec, light_sensor.update_sampling_rate)
        self.add_property(
            Property(self,
                     'sampling_rate',
                     self.sampling_rate,
                     metadata={
                         'title': 'sampling rate',
                         "type": "integer",
                         'unit': 'second',
                         'description': '"The sampling rate',
                         'readOnly': False,
                     }))

        self.refreshing_rate = Value(light_sensor.refreshing_rate_sec, light_sensor.update_refreshing_rate)
        self.add_property(
            Property(self,
                     'refreshing_rate',
                     self.refreshing_rate,
                     metadata={
                         'title': 'refreshing rate',
                         "type": "integer",
                         'unit': 'second',
                         'description': '"The refreshing rate',
                         'readOnly': False,
                     }))

        self.measures = Value("")
        self.add_property(
            Property(self,
                     'measures',
                     self.measures,
                     metadata={
                         'title': 'measures',
                         "type": "string",
                         'description': '"The measures',
                         'readOnly': True,
                     }))

    def on_measured(self, brightness: int):
        self.ioloop.add_callback(self.__update_brightness, brightness)
        self.ioloop.add_callback(self.__update_measures, ",".join([str(int(measure)) for measure in self.light_sensor.measures]))

    def __update_brightness(self, brightness: int):
        self.bright.notify_of_external_update(brightness)

    def __update_measures(self, measures):
        self.measures.notify_of_external_update(measures)


def run_server(port: int, sampling_rate_sec: int = 5, smoothing_window_sec: int = 10, refreshing_rate_sec:int = 3):
    light_sensor = LightSensorThing(LightSensor(sampling_rate_sec, smoothing_window_sec, refreshing_rate_sec))
    server = WebThingServer(SingleThing(light_sensor), port=port, disable_host_validation=True)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')


if __name__ == '__main__':
    try:
        logging.basicConfig(format='%(asctime)s %(name)-20s: %(levelname)-8s %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
        logging.getLogger('tornado.access').setLevel(logging.ERROR)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)
        run_server(int(sys.argv[1]))
    except Exception as e:
        logging.error(str(e))
        raise e
