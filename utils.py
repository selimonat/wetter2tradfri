PYTRADFRI_PATH = '/home/pi/code/python/pytradfri/'
import sys;sys.path.append(PYTRADFRI_PATH )
from pytradfri.util import load_json, save_json
from pytradfri.api.libcoap_api import APIFactory
from pytradfri.gateway import Gateway

from colormath.color_objects import XYZColor, sRGBColor
from colormath.color_conversions import convert_color

import numpy as np

CONFIG_FILE = '/home/pi/code/python/pytradfri/tradfri_standalone_psk.conf'
BRIDGE_IP = "192.168.2.167"

def run_command(command):
    try:
        api = authenticate_api()
        return api(command)
    except:
        print('timeout')

def rgb_2_xy(r,g,b):
    rgb = sRGBColor(r,g,b)
    xyz = convert_color(rgb, XYZColor, target_illuminant='d65')
    xy = int(xyz.xyz_x), int(xyz.xyz_y)
    return xy

def set_light_color(light_index,rgb):
    light = get_light(light_index)
    xy    = rgb_2_xy(rgb[0],rgb[1],rgb[2])
    print(xy)
    command = light[0].light_control.set_xy_color(min(xy[0],65535),
                                                  min(xy[1],65535))
    run_command(command)

def set_light_dimmer(light_index,value):
    for i in light_index:
        l=get_light(i);
        run_command(l.light_control.set_dimmer(value))

def list_all_lights():
    lights = get_light(slice(None))
    
    for i,l in enumerate(lights):
        print("{}: Light {}:\n\tState: {}, Value: {}".format(i,l,
                                                            l.light_control.lights[0].state,
                                                            l.light_control.lights[0].dimmer))
    from pprint import pprint
    return lights

def get_light(light_index):
    #returns light(s) selected by light_index 
    gateway = Gateway()
    devices_commands = run_command(gateway.get_devices())
    devices = run_command(devices_commands)
    lights = [dev for dev in devices if dev.has_light_control]
    #if many light  wanted 
    try:
        return [lights[l] for l in light_index]
    except:
        return lights[light_index]

def authenticate_api(host=BRIDGE_IP):
    #returns an authenticated API object
    conf = load_json(CONFIG_FILE)
    identity = conf[host].get('identity')
    psk = conf[host].get('key')
    api_factory = APIFactory(host=host, psk_id=identity, psk=psk,timeout=1)
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

if __name__ == '__main__':
    list_all_lights()
