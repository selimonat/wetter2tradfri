from pytradfri.util import load_json, save_json

from pytradfri.api.libcoap_api import APIFactory
from pytradfri.gateway import Gateway
def get_light(api,light_index):
    #returns light(s) selected by light_index 
    gateway = Gateway()
    devices_commands = api(gateway.get_devices())
    devices = api(devices_commands)
    lights = [dev for dev in devices if dev.has_light_control]
    #if many light  wanted 
    if isinstance(light_index,list):
        return [lights for l in light_index]
    #if a single light
    return lights[light_index]

def autenticate_api(host="192.168.2.167"):
    #returns an authenticated API object
    CONFIG_FILE = '/home/pi/code/python/pytradfri/tradfri_standalone_psk.conf'
    conf = load_json(CONFIG_FILE)
    identity = conf[host].get('identity')
    psk = conf[host].get('key')
    api_factory = APIFactory(host=host, psk_id=identity, psk=psk)
    return api_factory.request 
