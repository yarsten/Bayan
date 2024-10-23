import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, TimeDistributed, Masking, RepeatVector
from tensorflow.keras.callbacks import EarlyStopping

def create_model(X_train_shape, max_len_text, vocab_size):
    model = Sequential()
    model.add(Masking(mask_value=0., input_shape=X_train_shape))
    model.add(LSTM(units=128))
    model.add(RepeatVector(max_len_text))
    model.add(LSTM(units=128, return_sequences=True))
    model.add(TimeDistributed(Dense(vocab_size, activation='softmax')))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train_model(model, X_train, y_train):
    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    history = model.fit(X_train, y_train, epochs=10, validation_split=0.2, batch_size=32, callbacks=[early_stopping])
    return history

def evaluate_model(model, X_test, y_test):
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')
