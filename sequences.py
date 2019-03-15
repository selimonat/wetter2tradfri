from numpy import random as R

def dimmer_noisy(total_sample=100,mean=128,sigma=60):
    #Returns an unsigned 8bit integer generator with a specific 
    #(approximate) mean and standard deviation with sample length of
    #total_sample
    current = 0
    MAXIMUM_VALUE = 254
    while current < total_sample:
        current += 1 
        value = R.randn(1)*sigma+mean
        brightness =  value.clip(max = MAXIMUM_VALUE ) #clip to 254
        yield brightness.astype('uint8').tolist()
        
