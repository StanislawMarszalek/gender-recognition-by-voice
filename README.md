## Python gender recognition from .wav files

The algorithm is based on:

* HPS (Harmonic Product Spectrum)
* framing
* majority voting.

### Brief description of the program

The program reads the data and performs simple pre-processing. It then takes a single frame of length `frame_ms` in milliseconds, multiplies it by a Hamming window, computes the FFT for that frame, and applies the Harmonic Product Spectrum (downsampling the given signal `iterations` times) to the frame. \
Frames with a fundamental frequency outside the range 85–260 Hz are ignored.
If the frame's frequency is closer to 165 it is labeled as **M (man)**, otherwise it is labeled as **W (woman)** (`labels.append('M') if abs(f0-165) < abs(f0-180) else labels.append('W')`). \
Then the next frame is taken with a step of length `hop_ms` in milliseconds. After processing all frames, the labels are counted. If the number of votes for W is greater than the number of votes for M, the result is W, otherwise it is M. If no valid frames are detected, the HPS is computed on the entire signal. \
The output is in the format `Result: predicted_gender` or an error message.

### Datasets

I used the "ST-AEDS-20180100_1, Free ST American English Corpus" dataset and the "Gender Recognition by Voice (original)" dataset to evaluate the performance of my algorithm. \
The datasets can be found here: 
* [SLR45](https://www.openslr.org/45/) 
* [Gender Recognition by Voice](https://www.kaggle.com/datasets/murtadhanajim/gender-recognition-by-voiceoriginal)

### Usage

Type ```py gender_recognition.py [FILE] [OPTION]``` \
Type ```py gender_recognition.py -h``` or ```py gender_recognition.py --help``` for more information.

### Performance

The parameter values used during testing the algorithm's performance:

* ```frame_ms=150```
* ```hop_ms=30```
* ```iterations=3```

#### SLR45

|              | Prediction M | Prediction W |
| :----------: | :----------: | :----------: |
| **Actual M** |     1656     |       0      |
| **Actual W** |      278     |     1908     |

$\displaystyle Accuracy=\frac{1656 + 1908}{1656 + 1908 + 278 + 0}\approx 92.76\\%$  </br></br>  $\displaystyle Precision=\frac{1656}{1656 + 278}\approx 85.63\\%$ </br></br> $\displaystyle Recall=\frac{1656}{1656 + 0}=100\\%$

#### Gender Recognition by Voice

|              | Prediction M | Prediction W |
| :----------: | :----------: | :----------: |
| **Actual M** |     10197    |      183     |
| **Actual W** |      375     |     5393     |

$\displaystyle Accuracy=\frac{10197 + 5393}{10197 + 5393 + 183 + 375}\approx 96.54\\%$  </br></br> $\displaystyle Precision=\frac{10197}{10197 + 375}\approx 96.45\\%$ </br></br> $\displaystyle Recall=\frac{10197}{10197 + 183}\approx 98.24\\%$ 
