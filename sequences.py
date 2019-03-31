import numpy as np
MAXIMUM_VALUE = 254
from wetter2tradfri import utils as u

def dimmer_noisy(total_sample=100,smooth_window = 1, mean=128,sigma=60):
    #Returns an unsigned 8bit integer generator with a specific 
    #(approximate) mean and standard deviation with sample length of
    #total_sample
    value   = np.random.randn(smooth_window)
    current = 0
    while current < total_sample-smooth_window+1:
        current += 1 
        #shift and append a random value
        last_value = np.random.randn(1)*sigma+mean
        value = np.append(value[1:],last_value)
        #average the window
        output = np.mean(value)
        brightness =  output.clip(max = MAXIMUM_VALUE ) #clip to 254
        yield brightness.astype('uint8').tolist()
        
def dimmer_exponential(total_sample=100,mean=128,scale=20):
    
    current = 0
    while current < total_sample:
        current += 1
        sign  = np.random.choice([-1, 1],1)
        value = mean+np.random.exponential(scale,1)*sign
        brightness =  value.clip(max = MAXIMUM_VALUE ) #clip to 254
        yield brightness.astype('uint8').tolist()

def xy_randomwalk(total_sample=100,start_hue=0,start_intensity=.4,sigma=.1):
    current = 0
    while current < total_sample:
        current += 1 
        start_hue = start_hue + np.random.randn(1)*sigma
        yield u.pol2cart(start_hue,start_intensity)
 
