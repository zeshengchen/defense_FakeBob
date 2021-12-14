# defense_FakeBob
Source code for the paper "Defending Against FakeBob Adversarial Attacks in Speaker Verification Systems With Noise-Adding"

## Main content
Jupyter notebook code used to gnerate Figures 3 and 5 in the paper. Moreover, the source code of denoising and noise-adding methods is provided.

## File structure
- **./Demo.ipuynb**: Jupyter notebook code used to gnerate Figures 3 and 5 in the paper. Contain the code that shows an audio in time domain and mel spectrogram.
- **./noise_adding.py**: python code for the noise-adding method. 
- **./denoising.py**: python code for the denoising method. It calls the method in "**./noisereducev1.py**" file.
- **./noisereducev1.py**: This file is downloaded and modified from [Noise reduction in python using spectral gating by Tim Sainburg](https://github.com/timsainb/noisereduce/blob/master/noisereduce/noisereducev1.py).
- **./237-126133-0017-att-org.wav**: Original clean audio that was used to generate an adversarial audio.
- **./237-126133-0017-att-adv.wav**: Adversarial audio.
- **./237-126133-0017-att-denoised.wav**: Denoised adversarial audio.
- **./237-126133-0017-att-noise-added.wav**: Noise-added adversarial audio.

Before running "**Demo.ipynb**", please make sure to create a "**./figs/**" folder that will contain generated figures.

### If you have any questions, please feel free to comment or contact.