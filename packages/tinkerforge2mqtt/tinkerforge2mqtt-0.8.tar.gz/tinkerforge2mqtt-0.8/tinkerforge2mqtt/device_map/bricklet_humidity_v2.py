import logging

from ha_services.mqtt4homeassistant.components.sensor import Sensor
from tinkerforge.bricklet_humidity_v2 import BrickletHumidityV2

from tinkerforge2mqtt.device_map import register_map_class
from tinkerforge2mqtt.device_map_utils.base import DeviceMapBase, print_exception_decorator


logger = logging.getLogger(__name__)


@register_map_class()
class BrickletHumidityV2Mapper(DeviceMapBase):
    # https://www.tinkerforge.com/de/doc/Software/Bricklets/HumidityV2_Bricklet_Python.html

    device_identifier = BrickletHumidityV2.DEVICE_IDENTIFIER

    def __init__(self, *, device: BrickletHumidityV2, **kwargs):
        self.device: BrickletHumidityV2 = device
        super().__init__(device=device, **kwargs)

    @print_exception_decorator
    def setup_sensors(self):
        super().setup_sensors()

        self.humidity = Sensor(
            device=self.mqtt_device,
            name='Humidity',
            uid='humidity',
            device_class='humidity',
            state_class='measurement',
            unit_of_measurement='%',
            suggested_display_precision=2,
        )
        self.temperature = Sensor(
            device=self.mqtt_device,
            name='Temperature',
            uid='temperature',
            device_class='temperature',
            state_class='measurement',
            unit_of_measurement='°C',
            suggested_display_precision=2,
        )

    @print_exception_decorator
    def setup_callbacks(self):
        super().setup_callbacks()
        self.device.set_temperature_callback_configuration(
            period=self.user_settings.callback_period * 1000,
            value_has_to_change=False,
            option=self.device.THRESHOLD_OPTION_OFF,
            min=0,
            max=0,
        )
        self.device.register_callback(self.device.CALLBACK_TEMPERATURE, self.callback_temperature)

        self.device.set_humidity_callback_configuration(
            period=self.user_settings.callback_period * 1000,
            value_has_to_change=False,
            option=self.device.THRESHOLD_OPTION_OFF,
            min=0,
            max=0,
        )
        self.device.register_callback(self.device.CALLBACK_HUMIDITY, self.callback_humidity)

    @print_exception_decorator
    def callback_temperature(self, value):
        temperature = value / 100
        logger.info(f'Temperature callback: {temperature}°C (UID: {self.device.uid_string})')
        self.temperature.set_state(temperature)
        self.temperature.publish(self.mqtt_client)

    @print_exception_decorator
    def callback_humidity(self, value):
        humidity = value / 100
        logger.info(f'Temperature callback: {humidity}°C (UID: {self.device.uid_string})')
        self.humidity.set_state(humidity)
        self.humidity.publish(self.mqtt_client)
