import time
SAMPLING_RATE = .2 #seconds
import wetter2tradfri.utils as utils
import wetter2tradfri.sequences as s
import datetime
import numpy as np

def dimmer_program(light_index, start_up,stop_up,W=1):

    max_light_value = 254
    min_light_value = 0

    start_up = datetime.datetime.strptime(start_up,"%H:%M")
    stop_up  = datetime.datetime.strptime(stop_up,"%H:%M")
    #transform time to minutes of the day
    f         = lambda x : x.minute+x.hour*60
    #minute line of the day
    time_line = np.linspace(0,24*60-1,24*60,dtype=int)

    #weights for the increment.
    weights   = np.zeros(24*60,dtype=int)
    weights[(time_line >= f(start_up)) & (time_line < f(stop_up))] = W
    print(sum(weights))
    #number of brightness steps to cover full range
    increment = (max_light_value-min_light_value+1)/(f(stop_up)-f(start_up))
    print(f(stop_up)-f(start_up))
    #get light
    #autenticate api
    api       = utils.autenticate_api()
    #get all lights and select one or some
    lights    = utils.get_light(api,light_index)
    print(lights) 
    #current time
    now       = datetime.datetime.now() 
    previous = max_light_value
    if W > 0:
        previous = 0 
    while f(now) < 24*60:
        i   = f(now) #current_minute
        new = max(min(max_light_value,
                      previous + weights[i]*increment),
                      min_light_value)
        new = int(new)
        print(now.minute)
        print("current weight: {}".format(weights[i]))
        print("increment: {}".format(increment))
        print("new value: {}".format(new))
        print("setting new value")
        for light in lights:
            api(light.light_control.set_dimmer(new))
        time.sleep(60)
        now = datetime.datetime.now()   
        previous = new

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
