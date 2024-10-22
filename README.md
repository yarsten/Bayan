![Bayan Logo](https://media.discordapp.net/attachments/1295421459975376916/1297875599590821969/Bayan_Interface_tp.png?ex=6718d5d8&is=67178458&hm=ad8d4966549a59496977334d6b78309d5f9c067b900371fbc0caae5ad36f19a0&=&format=webp&quality=lossless&width=881&height=140)

## Overview
Bayan is a platform that converts spoken Arabic into clear, readable text. It aims to enhance communication by providing accurate transcription across various Arabic dialects. The name "Bayan" means clarity, reflecting the project's goal of making communication more accessible and understandable for Arabic speakers.

reflecting the project’s goal of bringing clarity to communication by transcribing Arabic speech in a way that’s accurate and easy to understand, no matter the dialect or context.


## Dataset Description
We have collected the data we will be working with from several different sources, namely: Mozilla Common Voice 11.0, OpenSLR (MediaSpeech), SADA (Echo) 2022 on Kaggle.

| Dataset                | Duration   | Link |
|------------------------|------------|------|
| Mozilla Common Voice    | 117 Hours  | [Link](https://huggingface.co/datasets/mozilla-foundation/common_voice_11_0/viewer/ar) |
| OpenSLR (MediaSpeech)   | 10 Hours   | [Link](https://openslr.org/108/) |
| SADA (صدى)              | 667 Hours  | [Link](https://www.kaggle.com/datasets/sdaiancai/sada2022) |

## Demo
You can access the demo of the Bayan platform [Here](#)

**Note: we need to specify the steps more later**

- **Step 1:** Upload an Arabic audio file or record your voice.
- **Step 2:** The model will transcribe your speech into text.
- **Step 3:** View and download the transcription in multiple formats.

Here’s a preview of the platform:

**Note: Here we need to upload an image for the interface, plz don't forget**


## Model Selection
We implemented two main models: **Whisper** and **LSTM**.

**Whisper** was chosen for its strength in handling noisy environments and its ability to process different Arabic dialects.

**LSTM** was selected for its ability to manage sequential data, making it a strong choice for continuous speech transcription.

Both models were trained and evaluated independently using the datasets mentioned above.


## Data Preprocessing
### Text Preprocessing
We implemented various preprocessing steps tailored for the Arabic language in the text transcriptions to ready them for model training, including:

- Normalization.
- Removing non Arabic text, numbers, urls, punctuations, etc..
- Tokenization and Padding
- Tokenization: Tokenize the Arabic text into words or subwords.
- Padding: Ensure all sequences are of the same length by padding shorter sequences.
  
### Audio Preprocessing
Before feeding the audio data into the models, we applied several audio preprocessing steps to ensure consistency and improve model performance:

- Resampling: All audio files were resampled to a standard frequency of 16kHz to maintain uniformity.
- MFCC Conversion: Converted each audio file into a Mel Frequency Cepstral Coefficients (MFCCs), which is commonly used for audio tasks.
- Padding: Calculated the maximum number of time steps across all the audio files then padded all the extracted feature arrays to the same length by appending zeros at the end.

## Model Overview
The LSTM model is designed for converting Arabic speech into Arabic text, architecture incorporates masking, TimeDistributed layers, and a RepeatVector layer to handle variable-length sequences.


## Model Performance
We used **Word Error Rate (WER)** to evaluate the performance of each model since it measures the accuracy of the transcribed text by comparing it to the reference text and calculating the proportion of errors

Model	Word Error Rate (WER)
Whisper-tiny	100
LSTM	94

| Model      | Word Error Rate (WER)   |
|------------------|------------|
| Whisper-tiny  |  100 |
| LSTM     | 94  |

## Challenges
During the implementation of this project, we encountered numerous challenges primarily stemming from the scarcity of machine learning and deep learning resources in the Arabic language domain. The task was further complicated by the necessity to train the model on Arabic language sounds, which presented its own set of difficulties.

Despite these obstacles, we persevered and managed to overcome several hurdles, eventually reaching a satisfactory level of performance. Through dedication and effort, we successfully trained the model on Arabic language sounds and achieved commendable accuracy. This journey, though arduous, has equipped us with valuable insights and strengthened our resolve to tackle complex problems in the future.


## Next Step
- Fine-tuning Whisper and LSTM models to further reduce the Word Error Rate (WER).
- Experimenting with variety of models to improve the performance of Arabic speech-to-text tasks.
- Trying to make the models lightweight for deployment on devices with lower processing power.

## Authors

 [@Roaa Mansour](https://github.com/RoaaAljedaani)
