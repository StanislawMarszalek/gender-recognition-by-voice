import numpy as np
from scipy.io import wavfile


def HPS_Single_Frame(frame:list, sample_rate:int, iterations:int)->int:

    spectrun = np.fft.fft(frame)
    spectrun = np.abs(spectrun)

    hps = spectrun.copy()
    n = len(spectrun)

    for harmonic in range(2, iterations+1):
        down = spectrun[::harmonic]              
        limit = min(len(down), len(hps)) 
        hps[:limit] *= down[:limit]

    
    hps = hps[:n//2]
    freqs = np.fft.fftfreq(n, 1/sample_rate)[:n//2]

    
    peak = np.argmax(hps[1:]) + 1
    f0 = freqs[peak]
    return f0


def Gender_Recognition(pathfile:str,frame_ms:int=150,hop_ms:int=30,iterations:int=3)->str:
    try:
        sr, data = wavfile.read(pathfile)

    except FileNotFoundError:
        return f"File '{pathfile}' not found"
    
    except IsADirectoryError:
        return f" '{pathfile}' is a direcotry not a file"
    
    except PermissionError:
        return f"Couldn't open '{pathfile}' permission denied"
    except OSError as e:
        if e.errno==22:
            return f"'{pathfile}' is not a valid file path'"
    except ValueError:
        return f"Wrong file format\nOnly 'RIFF', 'RIFX', and 'RF64' supported."

    if data.ndim > 1:
        data = data.mean(axis=1)

    data = data.astype(float)
    data = data - np.mean(data)
    if np.max(np.abs(data)) > 0:
        data = data / np.max(np.abs(data))

    frame_len = int(sr * frame_ms / 1000)
    hop = int(sr * hop_ms / 1000)

    labels = []

    for start in range(0, len(data)-frame_len, hop):
        frame = data[start:start+frame_len]
        frame = frame*np.hamming(len(frame))

        f0 = HPS_Single_Frame(frame, sr, iterations=iterations)
        if f0<85 or f0>260:
            continue
        labels.append('M') if abs(f0-165)<abs(f0-180) else labels.append('W')
                

    if len(labels) == 0:
        f0 = HPS_Single_Frame(data, sr, iterations)
        if f0 < 165:
            return 'M'
        else:
            return 'W'

    count_M = labels.count('M')
    count_W = labels.count('W')

    if count_W > count_M:
        return 'W'
    else:
        return 'M'
    