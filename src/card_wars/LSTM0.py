import pickle

import numpy as np
from keras.layers import BatchNormalization
from tensorflow import keras
from tensorflow.keras.models import load_model

from card_wars.import_cards import get_all_cards


def train_model(X, y, maxlen, chars, save_model=True):
    """
    Args:
    X (ndarray): Input data for training.
    y (ndarray): Target data for training.
    maxlen (int): Length of the input sequences.
    chars (int): Number of unique characters in the dataset.

    Returns:
    model: Trained LSTM model.
    """

    model = keras.Sequential()
    model.add(keras.layers.LSTM(64, input_shape=(maxlen, len(chars))))

    # model.add(BatchNormalization())
    model.add(keras.layers.Dense(len(chars), activation="hard_sigmoid"))
    #  TODO Experiment with different activation functions
    #  https://www.tensorflow.org/api_docs/python/tf/keras/activations

    model.compile(
        loss="categorical_crossentropy", optimizer="adam"
    )  #  TODO Try different loss functions and optimization algorithms.

    model.fit(
        X, y, batch_size=64, epochs=160
    )  #  TODO Implement learning rate scheduling and batch normalization for better convergence.

    if save_model:
        model.save("trained_models/lstm/model_keras_lstm_00.keras")

    return model


def sample(preds, temperature=1):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def generate_name(
    model, seed, maxlen, chars, char_indices, indices_char, temperature=1, generated_length=7
):
    generated = seed
    for i in range(generated_length):
        x_pred = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(seed):
            x_pred[0, t, char_indices[char]] = 1.0
        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, temperature)
        next_char = indices_char[next_index]
        generated += next_char
        seed = seed[1:] + next_char
    return generated


def generate_names_from_list(names, seed_texts, model=None):
    """If model is None, a new one will be trained."""

    corpus = " ".join(names)
    chars = sorted(list(set(corpus)))

    # Dictionary mapping unique characters to indices
    char_indices = {
        c: i for i, c in enumerate(chars)
    }  # Mapping characters to their respective indices
    indices_char = {
        i: c for i, c in enumerate(chars)
    }  # Mapping indices to their respective characters

    print(char_indices)
    print(indices_char)

    maxlen = 4

    # Extract sequences of characters from the input names
    sentences = []
    next_chars = []
    for name in names:
        for i in range(len(name) - maxlen):
            sentences.append(name[i : i + maxlen])
            next_chars.append(name[i + maxlen])

    print(sentences[0])
    print(next_chars[0:10])

    # Vectorizing the sentences
    X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool_)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool_)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            X[i, t, char_indices[char]] = 1  #  One-hot encoding for input sequences
        y[i, char_indices[next_chars[i]]] = 1  #  One-hot encoding for next characters

    if model == None:
        model = train_model(X, y, maxlen, chars)

    generated_names = []
    for seed in seed_texts:
        for i in range(10):
            generated_names.append(
                generate_name(
                    model,
                    seed,
                    maxlen,
                    chars,
                    char_indices,
                    indices_char,
                    temperature=1.0,
                    generated_length=4,
                )
            )

    return generated_names


if __name__ == "__main__":
    names_list = []
    cards = get_all_cards(minions=True, weapons=True, spells=True)
    for card in cards:
        names_list.append(card.name)

    with open("data/training_data/name_list.pkl", "rb") as f:
        names_list += pickle.load(f)

    seed_texts = ["Gob", "Dem"]

    # Train model:
    # generated_names = generate_names_from_list(names_list)

    generated_names = generate_names_from_list(
        names_list, seed_texts, model=load_model("trained_models/lstm/model_keras_lstm_00.keras")
    )

    for name in generated_names:
        print(name)
