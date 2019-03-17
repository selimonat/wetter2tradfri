import time
SAMPLING_RATE = .1 #seconds
import wetter2tradfri.utils as utils
import wetter2tradfri.sequences as s
def randomize_brightness(light_index,mean=128,duration=100,sigma=60):
    #duration in econds
    
    number_of_samples  = duration/SAMPLING_RATE
    #autenticate api
    api = utils.autenticate_api()
    #get all lights and select one or some
    lights = utils.get_light(api,light_index)
    #get the light sequence
    brightness = s.dimmer_noisy(total_sample = number_of_samples ,mean=mean, sigma=sigma)
    #brightness = s.dimmer_exponential(total_sample = number_of_samples ,
    #                                  scale=sigma,mean=mean)
    #set the light brightness
    counter = 0
    for b in brightness:
        for light in lights:
            api(light.light_control.set_dimmer(b[0]))
        time.sleep(SAMPLING_RATE)
        counter += 1
