import utils
from pytradfri.util import load_json, save_json   
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.gateway import Gateway
from pprint import pprint as pp

class Register():

    def __init__(self):
        self.config_file = '/home/pi/code/python/pytradfri/tradfri_standalone_psk.conf'
        self.host  = "192.168.2.167"
        self.api  = self.authenticate_api()
        self.gateway = Gateway()
        self._devices = self.get_devices()
        self._lights  = self.get_lights()
        self._groups  = self.get_groups()
        self.clusters = None
    
    @property
    def groups(self):
        pp(self._groups)

    @property
    def lights(self):
        pp(self._lights)

    @property
    def devices(self):
        pp(self._devices)

    def get_groups(self):
        commands_to_get_groups = self.run_command(self.gateway.get_groups())
        return self.run_command(commands_to_get_groups)

    def get_devices(self):
        commands_to_get_devices = self.run_command(self.gateway.get_devices())
        return self.run_command(commands_to_get_devices)

    def get_lights(self):
        return [dev for dev in self._devices if dev.has_light_control]

    def run_command(self,command):
        return self.api(command)
    
    def authenticate_api(self):
        #returns an authenticated API object
        conf = load_json(self.config_file)
        identity = conf[self.host].get('identity')
        psk = conf[self.host].get('key')
        api_factory = APIFactory(host=self.host, psk_id=identity, psk=psk)
        return api_factory.request 

class Actuators():

    def __init__(self,Register):
        self.duration  = None
        self.time_step = 100
        self.register  = Register

    def set_luminance(self,lights,luminance):
        for i in lights:
            run_command(l.light_control.set_dimmer(value))

    def set_color(self,lights,color):
        pass

    def time_engine(self,frequency,duration,min_value,amplitude):
        pass

    def timecourse_random_colors(self,lights,frequency,duration,colors=None):
        pass

    def timecourse_oscillate_luminance(self,lights,luminance,frequency,duration):
        pass

    def rgb_2_xy():
        pass


