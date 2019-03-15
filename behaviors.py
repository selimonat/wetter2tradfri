import time
SAMPLING_RATE = .5 #seconds
import wetter2tradfri.utils as utils
import wetter2tradfri.sequences as s
def randomize_brightness(light_index,duration=100,sigma=60):
    #duration in econds
    
    number_of_samples  = duration/SAMPLING_RATE
    #autenticate api
    api = utils.autenticate_api()
    #get all lights and select one or some
    light = utils.get_light(api,light_index)
    #get the light sequence
    brightness = s.dimmer_noisy(total_sample = number_of_samples , sigma=sigma)
    #set the light brightness
    counter = 0
    for b in brightness:
        api(light.light_control.set_dimmer(b[0]))
        time.sleep(SAMPLING_RATE)
        counter += 1
        print(counter)
