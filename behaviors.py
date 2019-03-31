import time
SAMPLING_RATE = .1 #seconds
import wetter2tradfri.utils as utils
import wetter2tradfri.sequences as s
def randomize_brightness(light_index,smooth_window=20,mean=128,duration=100,sigma=60):
    #duration in econds
    
    number_of_samples  = duration/SAMPLING_RATE
    #autenticate api
    api = utils.autenticate_api()
    #get all lights and select one or some
    lights = utils.get_light(api,light_index)
    #get the light sequence
    brightness = s.dimmer_noisy(total_sample = number_of_samples ,mean=mean,
                                sigma=sigma,smooth_window=smooth_window)
    #brightness = s.dimmer_exponential(total_sample = number_of_samples ,
    #                                  scale=sigma,mean=mean)
    #set the light brightness
    counter = 0
    for b in brightness:
        for light in lights:
            #measure how long an api call lasts in second, and 
            #see how realistical it is to control many lamps and still
            #satisfy a given SAMPLING_RATE
            api(light.light_control.set_dimmer(b))
        #instead of sleeping given time, compute until when to sleep, because
        #api calls take also some time in these type of synchronous calls.
        time.sleep(SAMPLING_RATE)
        counter += 1
        print((counter,b))

def randomize_color(light_index,duration=100,sigma=.02):
    #duration in seconds
    
    number_of_samples  = duration/SAMPLING_RATE
    #autenticate api
    api = utils.autenticate_api()
    #get all lights and select one or some
    lights = utils.get_light(api,light_index)
    #get the light sequence
    xy  = s.xy_randomwalk(total_sample = number_of_samples,sigma=sigma)
    #set the light brightness
    counter = 0
    for x,y in xy:
        for light in lights:
            api(light.light_control.set_xy_color(int(x),int(y)))
        time.sleep(SAMPLING_RATE)
        counter += 1
        print(counter)
