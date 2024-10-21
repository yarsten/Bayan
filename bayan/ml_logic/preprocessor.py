import nltk
import re
import regex
import string
import pandas as pd
import os
import librosa
import numpy as np
import pyarabic.araby as araby

from nltk.stem.isri import ISRIStemmer
from nltk.stem.snowball import SnowballStemmer
from tashaphyne.stemming import ArabicLightStemmer
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split


# ============================
# 1. TEXT PREPROCESSING MODULE
# ============================

def remove_stop_words(text):
    Text = [i for i in str(text).split() if i not in arabic_stopwords]
    return " ".join(Text)

def ISRI_Stemmer(text):
    stemmer = ISRIStemmer()
    text = stemmer.stem(text)
    text = stemmer.pre32(text)
    text = stemmer.suf32(text)
    return text

def Snowball_stemmer(text):
    text = text.split()
    stemmer = SnowballStemmer("arabic")
    text = [stemmer.stem(y) for y in text]
    return " ".join(text)

def Arabic_Light_Stemmer(text):
    Arabic_Stemmer = ArabicLightStemmer()
    text = [Arabic_Stemmer.light_stem(y) for y in text.split()]
    return " ".join(text)

def normalizeArabic(text):
    text = text.strip()
    text = re.sub("ى", "ي", text)
    text = re.sub("ؤ", "ء", text)
    text = re.sub("ئ", "ء", text)
    text = re.sub("ة", "ه", text)
    text = re.sub("[إأٱآا]", "ا", text)
    text = text.replace('وو', 'و')
    text = text.replace('يي', 'ي')
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'(.)\1+', r"\1\1", text)
    text = araby.strip_tashkeel(text)
    text = araby.strip_diacritics(text)
    text = ''.join([i for i in text if not i.isdigit()])
    return text

def Removing_non_arabic(text):
    text = re.sub('[A-Za-z]+', ' ', text)
    return text

def Removing_numbers(text):
    text = ''.join([i for i in text if not i.isdigit()])
    return text

def Removing_punctuations(text):
    text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,،-./:;<=>؟?@[\]^_`{|}~"""), ' ', text)
    text = text.replace('؛', "")
    text = re.sub('\s+', ' ', text)
    return text.strip()

def Removing_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"
                           u"\U0001F300-\U0001F5FF"
                           u"\U0001F680-\U0001F6FF"
                           u"\U0001F1E0-\U0001F1FF"
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string).strip()

def remove_extra_Space(text):
    text = re.sub('\s+', ' ', text)
    return " ".join(text.split())

def remove_hashtages_and_mentions(text):
    text = re.sub("@[A-Za-z0-9_]+", "", text)
    text = re.sub("#[A-Za-z0-9_]+", "", text)
    return text

def preprocess_text(text):
    text = normalizeArabic(text)
    text = Removing_non_arabic(text)
    text = Removing_numbers(text)
    text = Removing_punctuations(text)
    text = Removing_urls(text)
    text = remove_hashtages_and_mentions(text)
    text = remove_extra_Space(text)
    return text

df_selected['Sentence'] = df_selected['Sentence'].apply(preprocess_text)


# ============================
# 2. AUDIO PROCESSING MODULE
# ============================

def load_audio_file(audio_path, sr=16000):
    """Loads an audio file and returns the audio time series and the sampling rate."""

    y, sr = librosa.load(audio_path, sr=sr)
    return y, sr


def add_noise(audio, noise_factor=0.005):
    """Adds random noise to the audio signal for data augmentation."""

    noise = np.random.randn(len(audio))
    augmented_audio = audio + noise_factor * noise
    return augmented_audio


# ============================
# 3. FEATURE EXTRACTION MODULE
# ============================

def extract_log_mel_features(audio_data, sr, n_mels=160):
    """Extracts log-mel spectrogram features from audio."""

    mel_spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sr, n_mels=n_mels)
    log_mel_spectrogram = librosa.power_to_db(mel_spectrogram)
    return log_mel_spectrogram


def pad_features(features, max_len):
    """Pads log-mel features to ensure they are of uniform length."""

    n_mels, time_steps = features.shape
    
    if time_steps < max_len:
        pad_width = max_len - time_steps
        padded_features = np.pad(features, ((0, 0), (0, pad_width)), mode='constant')
    else:
        padded_features = features[:, :max_len]
    
    return padded_features


# ============================
# 4. LSTM INPUT PREPARATION
# ============================

def prepare_lstm_input(padded_features):
    """Prepares the padded log-mel features for LSTM input."""
    return np.array(padded_features)
X_lstm_input = prepare_lstm_input(Final_df['padded_log_mel'].tolist())


# ============================
# 5. TEXT TOKENIZATION & PADDING
# ============================

tokenizer = Tokenizer(filters='', lower=False)  
tokenizer.fit_on_texts(Final_df['Sentence'])
sequences = tokenizer.texts_to_sequences(Final_df['Sentence'])
max_len_sentence = max(len(seq) for seq in sequences)
padded_sequences = pad_sequences(sequences, maxlen=max_len_sentence, padding='post')
Final_df['padded_sentences'] = padded_sequences.tolist()
y_lstm_target = np.array(padded_sequences)


def preprocess_data(df):

    Final_df['audio_data'] = Final_df['Audio Path'].apply(lambda x: load_audio_file(x))
    Final_df['noisy_audio'] = Final_df['audio_data'].apply(lambda x: (add_noise(x[0]), x[1]))
    Final_df['log_mel_features'] = Final_df['noisy_audio'].apply(lambda x: extract_log_mel_features(x[0], x[1]))
    max_audio_len = max([features.shape[1] for features in Final_df['log_mel_features']])
    Final_df['padded_log_mel'] = Final_df['log_mel_features'].apply(lambda f: pad_features(f, max_audio_len))
    return df


Final_df = preprocess_data(Final_df)


# ============================
# 6. DATA SPLITTING
# ============================

X_train, X_test, y_train, y_test = train_test_split(X_lstm_input, y_lstm_target, test_size=0.2, random_state=42)