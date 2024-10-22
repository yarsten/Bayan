# Overview '#68bdb2'
Bayan is a platform that converts spoken Arabic into clear, readable text. 
Inspired by the idea of enhancing communication, Bayan aims to make interactions easier and more accessible for Arabic speakers. 
The name "Bayan" means clarity, 

reflecting the project’s goal of bringing clarity to communication by transcribing Arabic speech in a way that’s accurate and easy to understand, no matter the dialect or context.

<br>

# Challenges
During the implementation of this project, we encountered numerous challenges primarily stemming from the scarcity of machine learning and deep learning resources in the Arabic language domain. The task was further complicated by the necessity to train the model on Arabic language sounds, which presented its own set of difficulties.

Despite these obstacles, we persevered and managed to overcome several hurdles, eventually reaching a satisfactory level of performance. Through dedication and effort, we successfully trained the model on Arabic language sounds and achieved commendable accuracy. This journey, though arduous, has equipped us with valuable insights and strengthened our resolve to tackle complex problems in the future.

<br>

# Dataset Description

To note that we have collected the data we will be working with from several different sources, namely: Mozilla Common Voice 11.0, OpenSLR (MediaSpeech), SADA (Echo) 2022 on Kaggle, Arabic Speech Corpus

markdown


<p style="font-size: 12px;">1- Mozilla Common Voice 11.0 https://huggingface.co/datasets/mozilla-foundation/common_voice_11_0/viewer/ar
The Common Voice dataset consists of a unique MP3 file and a corresponding text file. Many of the 24,210 recorded hours in the dataset also include demographic metadata such as age, gender, and dialect that can help improve the accuracy of speech recognition engines.

The dataset currently consists of 16,413 recorded hours in 100 languages, but more voices and languages ​​are always being added.

In this case, we use *ar* as it is focused on Arabic </p>


<p style="font-size: 10px;">2- OpenSLR (MediaSpeech)
https://openslr.org/108/
MediaSpeech is a dataset of French, Arabic, Turkish and Spanish media speech built with the purpose of testing Automated Speech Recognition (ASR) systems performance. The dataset contains 10 hours of speech for each language provided.
The dataset consists of short speech segments automatically extracted from media videos available on YouTube and manually transcribed, with some pre- and post-processing.</p>


<p style="font-size: 10px;">3-SADA (صدى) 2022 on Kaggle
https://www.kaggle.com/datasets/sdaiancai/sada2022
The National Center for Artificial Intelligence at the Saudi Data and Artificial Intelligence Authority (SDAIA), in collaboration with the Saudi Broadcasting Authority (SBA), have published the “SADA” dataset, which stands for “Saudi Audio Dataset for Arabic”.

The published data exceeds 600 hours of Arabic audio recordings in various local Saudi dialects, sourced from more than 57 TV shows provided by the Saudi Broadcasting Authority. The National Center for Artificial Intelligence in SDAIA transcribed the data and prepared it for training and processing, together with providing 20 hours for development and testing.</p>


<p style="font-size: 12px;">4- Arabic Speech Corpus
https://en.arabicspeechcorpus.com/
This Speech corpus has been developed as part of PhD work carried out by Nawar Halabi at the University of Southampton. The corpus was recorded in south Levantine Arabic (Damascian accent) using a professional studio. Synthesized speech as an output using this corpus has produced a high quality, natural voice. </p>
