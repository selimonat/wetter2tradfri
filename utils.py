from pytradfri.util import load_json, save_json
import numpy as np
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.gateway import Gateway


def get_light(api,light_index):
    #returns light(s) selected by light_index 
    gateway = Gateway()
    devices_commands = api(gateway.get_devices())
    devices = api(devices_commands)
    lights = [dev for dev in devices if dev.has_light_control]
    #if many light  wanted 
    try:
        return [lights[l] for l in light_index]
    except:
        return lights[light_index]

def autenticate_api(host="192.168.2.167"):
    #returns an authenticated API object
    CONFIG_FILE = '/home/pi/code/python/pytradfri/tradfri_standalone_psk.conf'
    conf = load_json(CONFIG_FILE)
    identity = conf[host].get('identity')
    psk = conf[host].get('key')
    api_factory = APIFactory(host=host, psk_id=identity, psk=psk)
    return api_factory.request 

def cart2pol(x, y,white_point=(.3128,.329)):
    x = x - white_point[0]
    y = y - white_point[1]
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    print("radius is %f" % rho)
    print("angle is  %f" % phi)
    return(rho, phi)

def pol2cart(rho, phi,white_point=(.3128,.329)):
    x = (rho * np.cos(phi)+white_point[0])
    x = x.clip(max=65535,min=0)
    y = (rho * np.sin(phi)+white_point[1])
    y = y.clip(max=65535,min=0)
    print(type(x))
    print("x is %f" % x)
    print("y is %f" % y)
    return(int(x*65535), int(y*65535))
