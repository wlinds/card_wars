# from https://medium.com/@maxel333/creating-a-name-generator-with-lstm-9aaa600aeacf

import pickle

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

from card_wars.import_cards import get_all_cards

# Define the list of names
names = []
cards = get_all_cards(minions=True, weapons=True, spells=True)
for card in cards:
    names.append(card.name)

with open("data/training_data/name_list.pkl", "rb") as f:
    names_list += pickle.load(f)

# Tokenize the names at character level
tokenizer = Tokenizer(char_level=True)
tokenizer.fit_on_texts(names)

# Convert characters to sequences
sequences = tokenizer.texts_to_sequences(names)

# Create input sequences and labels
X = []
y = []
for seq in sequences:
    for i in range(1, len(seq)):
        X.append(seq[:i])
        y.append(seq[i])

# Pad sequences for consistent input shape
max_seq_length = max([len(seq) for seq in X])
X = pad_sequences(X, maxlen=max_seq_length, padding="pre")

# One-hot encode labels
y = tf.keras.utils.to_categorical(y, num_classes=len(tokenizer.word_index) + 1)

#  Define the LSTM model
model = Sequential()
model.add(Embedding(len(tokenizer.word_index) + 1, 32, input_length=max_seq_length))
model.add(LSTM(64))
model.add(Dense(len(tokenizer.word_index) + 1, activation="softmax"))

# Compile the model
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])


# Define a custom callback to store training progress
class TrainingProgressCallback(Callback):
    def on_train_begin(self, logs=None):
        self.epochs = []
        self.accuracies = []
        self.losses = []

    def on_epoch_end(self, epoch, logs=None):
        accuracy_percentage = logs.get("accuracy") * 100
        loss_percentage = logs.get("loss") * 100
        self.epochs.append(epoch + 1)
        self.accuracies.append(accuracy_percentage)
        self.losses.append(loss_percentage)


# Train the model with the progress callback
progress_callback = TrainingProgressCallback()
model.fit(X, y, epochs=100, verbose=0, callbacks=[progress_callback])


# Display training progress in a table
df = pd.DataFrame(
    {
        "Epoch": progress_callback.epochs,
        "Accuracy (%)": progress_callback.accuracies,
        "Loss (%)": progress_callback.losses,
    }
)
print(df)


# Function to generate a new name
def generate_name(model, tokenizer, max_seq_length):
    seed_text = ""
    generated_text = ""

    while True:
        sequence = tokenizer.texts_to_sequences([seed_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_seq_length, padding="pre")

        predicted_probabilities = model.predict(sequence)[0]
        predicted_id = np.argmax(predicted_probabilities)


if __name__ == "__main__":
    generate_name(model, tokenizer, max_seq_length)
