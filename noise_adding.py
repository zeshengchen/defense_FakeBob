# Noise-addding method
import numpy as np 

def add_noise(audios, noise_std):
	mean = 0
	noise = np.random.normal(mean, noise_std, size = len(audios))
	out_audios = audios + noise

	return out_audios
