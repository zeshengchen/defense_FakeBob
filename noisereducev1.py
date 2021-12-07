# This file is downloaded and modified from
# https://github.com/timsainb/noisereduce/blob/master/noisereduce/noisereducev1.py
import scipy.signal
import numpy as np
import librosa
import copy


def _stft(y, n_fft, hop_length, win_length):
    return librosa.stft(
        y=y, n_fft=n_fft, hop_length=hop_length, win_length=win_length, center=True
    )


def _istft(y, n_fft, hop_length, win_length):
    return librosa.istft(y, hop_length, win_length)


def _amp_to_db(x):
    return librosa.core.amplitude_to_db(x, ref=1.0, amin=1e-20, top_db=80.0)


def update_pbar(pbar, message):
    """ writes to progress bar
    """
    if pbar is not None:
        pbar.set_description(message)
        pbar.update(1)


def _smoothing_filter(n_grad_freq, n_grad_time):
    """Generates a filter to smooth the mask for the spectrogram
        
    Arguments:
        n_grad_freq {[type]} -- [how many frequency channels to smooth over with the mask.]
        n_grad_time {[type]} -- [how many time channels to smooth over with the mask.]
    """

    smoothing_filter = np.outer(
        np.concatenate(
            [
                np.linspace(0, 1, n_grad_freq + 1, endpoint=False),
                np.linspace(1, 0, n_grad_freq + 2),
            ]
        )[1:-1],
        np.concatenate(
            [
                np.linspace(0, 1, n_grad_time + 1, endpoint=False),
                np.linspace(1, 0, n_grad_time + 2),
            ]
        )[1:-1],
    )
    smoothing_filter = smoothing_filter / np.sum(smoothing_filter)
    return smoothing_filter


def mask_signal(sig_stft, sig_mask):
    """ Reduces amplitude of time/frequency regions of a spectrogram based upon a mask 
        
    Arguments:
        sig_stft {[type]} -- spectrogram of signal
        sig_mask {[type]} -- mask to apply to signal
    
    Returns:
        sig_stft_amp [type] -- masked signal
    """
    sig_stft_amp = sig_stft * (1 - sig_mask)
    return sig_stft_amp


def convolve_gaussian(sig_mask, smoothing_filter):
    """ Convolves a gaussian filter with a mask (or any image)
    
    Arguments:
        sig_mask {[type]} -- The signal mask
        smoothing_filter {[type]} -- the filter to convolve
    
    """
    
    return scipy.signal.fftconvolve(sig_mask, smoothing_filter, mode="same")


def reduce_noise(
    audio_clip,
    noise_clip=None,
    n_grad_freq=2,
    n_grad_time=4,
    n_fft=2048,
    win_length=2048,
    hop_length=512,
    n_std_thresh=1.5,
    prop_decrease=1.0,
    pad_clipping=True,
):
    """Remove noise from audio based upon a clip containing only noise

    Args:
        audio_clip (array): Waveform of audio
        noise_clip (array): The second parameter.
        n_grad_freq (int): how many frequency channels to smooth over with the mask.
        n_grad_time (int): how many time channels to smooth over with the mask.
        n_fft (int): number audio of frames between STFT columns.
        win_length (int): Each frame of audio is windowed by `window()`. The window will be of length `win_length` and then padded with zeros to match `n_fft`..
        hop_length (int):number audio of frames between STFT columns.
        n_std_thresh (int): how many standard deviations louder than the mean dB of the noise (at each frequency level) to be considered signal
        prop_decrease (float): To what extent should you decrease noise (1 = all, 0 = none)
        pad_clipping (bool): Pad the signals with zeros to ensure that the reconstructed data is equal length to the data
        
    Returns:
        array: The recovered signal with noise subtracted

    """
    
    pbar = None

    # STFT over signal
    update_pbar(pbar, "STFT on signal")

    # pad signal with zeros to avoid extra frames being clipped if desired
    if pad_clipping:
        nsamp = len(audio_clip)
        audio_clip = np.pad(audio_clip, [0, hop_length], mode="constant")

    sig_stft = _stft(
        audio_clip, n_fft, hop_length, win_length
    )
    # spectrogram of signal in dB
    sig_stft_db = _amp_to_db(np.abs(sig_stft))

    update_pbar(pbar, "STFT on noise")
    # STFT over noise
    if noise_clip is None:
        noise_stft = copy.deepcopy(sig_stft)
        noise_stft_db = copy.deepcopy(sig_stft_db)
    else:
        noise_stft = _stft(
            noise_clip, n_fft, hop_length, win_length
        )
        noise_stft_db = _amp_to_db(np.abs(noise_stft))  # convert to dB
    # Calculate statistics over noise
    mean_freq_noise = np.mean(noise_stft_db, axis=1)
    std_freq_noise = np.std(noise_stft_db, axis=1)
    noise_thresh = mean_freq_noise + std_freq_noise * n_std_thresh

    update_pbar(pbar, "Generate mask")

    # calculate the threshold for each frequency/time bin
    db_thresh = np.repeat(
        np.reshape(noise_thresh, [1, len(mean_freq_noise)]),
        np.shape(sig_stft_db)[1],
        axis=0,
    ).T
    # mask if the signal is above the threshold
    sig_mask = sig_stft_db < db_thresh
    update_pbar(pbar, "Smooth mask")
    # Create a smoothing filter for the mask in time and frequency
    smoothing_filter = _smoothing_filter(n_grad_freq, n_grad_time)

    # convolve the mask with a smoothing filter
    sig_mask = convolve_gaussian(sig_mask, smoothing_filter)

    sig_mask = sig_mask * prop_decrease
    update_pbar(pbar, "Apply mask")
    # mask the signal

    sig_stft_amp = mask_signal(sig_stft, sig_mask)

    update_pbar(pbar, "Recover signal")
    # recover the signal
    recovered_signal = _istft(
        sig_stft_amp, n_fft, hop_length, win_length
    )
    # fix the recovered signal length if padding signal
    if pad_clipping:
        recovered_signal = librosa.util.fix_length(recovered_signal, nsamp)

    return recovered_signal
