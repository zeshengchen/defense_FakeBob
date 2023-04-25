# defense_FakeBob
Source code for the paper "Defending Against FakeBob Adversarial Attacks in Speaker Verification Systems With Noise-Adding"
```
@Article{a15080293,
AUTHOR = {Chen, Zesheng and Chang, Li-Chi and Chen, Chao and Wang, Guoping and Bi, Zhuming},
TITLE = {Defending against FakeBob Adversarial Attacks in Speaker Verification Systems with Noise-Adding},
JOURNAL = {Algorithms},
VOLUME = {15},
YEAR = {2022},
NUMBER = {8},
ARTICLE-NUMBER = {293},
URL = {https://www.mdpi.com/1999-4893/15/8/293},
ISSN = {1999-4893},
ABSTRACT = {Speaker verification systems use human voices as an important biometric to identify legitimate users, thus adding a security layer to voice-controlled Internet-of-things smart homes against illegal access. Recent studies have demonstrated that speaker verification systems are vulnerable to adversarial attacks such as FakeBob. The goal of this work is to design and implement a simple and light-weight defense system that is effective against FakeBob. We specifically study two opposite pre-processing operations on input audios in speak verification systems: denoising that attempts to remove or reduce perturbations and noise-adding that adds small noise to an input audio. Through experiments, we demonstrate that both methods are able to weaken the ability of FakeBob attacks significantly, with noise-adding achieving even better performance than denoising. Specifically, with denoising, the targeted attack success rate of FakeBob attacks can be reduced from 100% to 56.05% in GMM speaker verification systems, and from 95% to only 38.63% in i-vector speaker verification systems, respectively. With noise adding, those numbers can be further lowered down to 5.20% and 0.50%, respectively. As a proactive measure, we study several possible adaptive FakeBob attacks against the noise-adding method. Experiment results demonstrate that noise-adding can still provide a considerable level of protection against these countermeasures.},
DOI = {10.3390/a15080293}
}
```

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