# Denoising method
import numpy as np 
from noisereducev1 import reduce_noise 

def denoise(audios, noise_std):
	mean = 0
	noise = np.random.normal(mean, noise_std, size = len(audios))
	
	out_audios = reduce_noise(audios,
							  noise,
							  n_fft = 512,
							  win_length = 400,
							  hop_length = 160
							 )

	return out_audios
