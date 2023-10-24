import numpy as np
from keras.layers import BatchNormalization
from tensorflow import keras

from card_wars.import_cards import get_all_cards


def build_model_and_train(X, y, maxlen, chars):
    """
    Build and train a simple LSTM model.

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

    # Compile the model
    model.compile(
        loss="categorical_crossentropy", optimizer="adam"
    )  # Try different loss functions and optimization algorithms.

    # Train the model, you might need more data for better results
    model.fit(
        X, y, batch_size=64, epochs=160
    )  # Implement learning rate scheduling and batch normalization for better convergence.

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


def generate_names_from_list(names):
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

    model = build_model_and_train(X, y, maxlen, chars)

    # Generate new names
    generated_names = []
    for i in range(10):
        generated_names.append(
            generate_name(
                model,
                "Gob",
                maxlen,
                chars,
                char_indices,
                indices_char,
                temperature=1.0,
                generated_length=4,
            )
        )

    for i in range(10):
        generated_names.append(
            generate_name(
                model,
                "Dem",
                maxlen,
                chars,
                char_indices,
                indices_char,
                temperature=1.0,
                generated_length=4,
            )
        )

    return generated_names


names_list = []
cards = get_all_cards(minions=True, weapons=True, spells=True)
for card in cards:
    names_list.append(card.name)


names_list += [
    "Aldric",
    "Althaea",
    "Aradia",
    "Azazel",
    "Belladonna",
    "Bellerophon",
    "Caspian",
    "Celestia",
    "Cressida",
    "Draven",
    "Eowyn",
    "Evelina",
    "Fabian",
    "Faelan",
    "Gaia",
    "Galadriel",
    "Gideon",
    "Hadrian",
    "Ignatius",
    "Isolde",
    "Jareth",
    "Kieran",
    "Lavinia",
    "Leander",
    "Lilith",
    "Lucius",
    "Lyra",
    "Maia",
    "Malachi",
    "Melisandre",
    "Nerys",
    "Oberon",
    "Ophelia",
    "Orion",
    "Persephone",
    "Phineas",
    "Quinlan",
    "Rhiannon",
    "Ronan",
    "Rosalind",
    "Seraphina",
    "Silas",
    "Soren",
    "Tamsin",
    "Thaddeus",
    "Theodora",
    "Uriel",
    "Valerian",
    "Vesper",
    "Xanthe",
    "Xerxes",
    "Yseult",
    "Zephyr",
    "Zora",
    "Astra",
    "Aurelius",
    "Baelor",
    "Calista",
    "Caius",
    "Darius",
    "Delphine",
    "Elowen",
    "Emrys",
    "Evander",
    "Faustus",
    "Ginevra",
    "Griffin",
    "Heloise",
    "Icarus",
    "Isabeau",
    "Jericho",
    "Kaius",
    "Kallista",
    "Lysander",
    "Morrigan",
    "Myrcella",
    "Narcissa",
    "Nicasia",
    "Octavian",
    "Odessa",
    "Pandora",
    "Percival",
    "Ravenna",
    "Rowena",
    "Sable",
    "Severus",
    "Theodosia",
    "Ulysses",
    "Valencia",
    "Vespera",
    "Wolfgang",
    "Xena",
    "Yvaine",
    "Zephyrine",
]
names_list += [
    "Gnarltooth",
    "Scabgob",
    "Mucksnare",
    "Stinkfinger",
    "Rotbelly",
    "Biletoe",
    "Ratfink",
    "Moldclaw",
    "Slimegut",
    "Fungusface",
    "Pusmaw",
    "Grimefoot",
    "Miregrub",
    "Rancidtoe",
    "Fetidnose",
    "Snotbelch",
    "Wartfinger",
    "Grimewart",
    "Sludgesnout",
    "Pustule",
    "Bilescum",
    "Maggotgrin",
    "Wartnail",
    "Fungusnail",
    "Gunknuckle",
    "Stenchtooth",
    "Squallbelly",
    "Pusfist",
    "Moldsnout",
    "Mirefist",
    "Wartfist",
    "Grimeslime",
    "Snotmaw",
    "Goblintooth",
    "Ratgrub",
    "Squallfist",
    "Snotgrin",
    "Maggotsnout",
    "Rotgob",
    "Muckfist",
    "Pusbelly",
    "Gnarlslime",
    "Sludgegrin",
    "Muckbelch",
    "Wartscum",
    "Maggotclaw",
    "Grimemaw",
    "Ratmaw",
    "Scumtooth",
    "Fungustoe",
    "Stenchscum",
    "Rotsnout",
    "Gunknail",
    "Fungusgrin",
    "Sludgenose",
    "Snotfist",
    "Grimebelch",
    "Pusgrub",
    "Gunknose",
    "Stenchgut",
    "Muckscum",
    "Ratgut",
    "Gnarlclaw",
    "Squallgut",
    "Fungusmaw",
    "Rotnail",
    "Slimegob",
    "Maggotnail",
    "Grimenail",
    "Miremaw",
    "Bilegut",
    "Snotscum",
    "Wartbelly",
    "Stinkgrin",
    "Pusmaw",
    "Slimebelly",
    "Gunknose",
    "Maggotbelch",
    "Squallnose",
    "Fungusgrub",
    "Rotfist",
    "Mirebelch",
    "Biletooth",
    "Snotgob",
    "Wartgut",
    "Stenchmaw",
    "Pusnail",
    "Slimegut",
    "Muckmaw",
    "Ratfist",
    "Gnarlgrub",
    "Squalltoe",
    "Fungusnail",
    "Rottongue",
]
names_list += [
    "Alabaster",
    "Bilbron",
    "Cobble",
    "Dabbledob",
    "Eldon",
    "Fiddlestrom",
    "Glimmerglam",
    "Hobblesprocket",
    "Ivory",
    "Jinglepocket",
    "Kipperwick",
    "Luminatus",
    "Muddlefoot",
    "Nimblefingers",
    "Oxworth",
    "Pipperwhistle",
    "Quiddle",
    "Riddlewrench",
    "Sprocket",
    "Tinkerdome",
    "Umbledown",
    "Vexwicket",
    "Wobblestock",
    "Xizzle",
    "Yanzen",
    "Zephyrus",
    "Almondar",
    "Bristlewick",
    "Coppernick",
    "Dewblossom",
    "Eldritch",
    "Fizzlebang",
    "Gimble",
    "Hobblestock",
    "Irongrip",
    "Jacket",
    "Knottington",
    "Lugwrench",
    "Mimbleton",
    "Noblecog",
    "Oakenbough",
    "Pippernott",
    "Quibble",
    "Rumbletoss",
    "Snickersneeze",
    "Tallowtoes",
    "Underbough",
    "Vittle",
    "Wigglefizz",
    "Zapfizz",
    "Alderwhistle",
    "Bumblebucket",
    "Cogspring",
    "Dingle",
    "Elderspring",
    "Fizzlesprocket",
    "Glimmerwhistle",
    "Hickory",
    "Inkwell",
    "Jumble",
    "Knickknack",
    "Lumbersprocket",
    "Muddlewick",
    "Nimblecog",
    "Oatsworth",
    "Peeper",
    "Quill",
    "Rustle",
    "Springel",
    "Tweedle",
    "Underfoot",
    "Vickers",
    "Whittle",
    "Zigzag",
    "Alabasterson",
    "Bilbangle",
    "Copperdome",
    "Dewwidget",
    "Elderberry",
    "Fizzlebottom",
    "Glimmerwick",
    "Hickoryswitch",
    "Inkle",
    "Jumbletoss",
    "Kipperwink",
    "Lumberspring",
    "Muddlesprocket",
    "Nimblewhistle",
    "Oakenthorn",
    "Pipperknot",
    "Quibblefidget",
    "Rustlesprocket",
    "Springle",
    "Twizzle",
]
names_list += [
    "Azazel",
    "Balerion",
    "Crimson",
    "Drakon",
    "Ember",
    "Fafnir",
    "Gargouille",
    "Haku",
    "Ignatius",
    "Jabberwock",
    "Kaida",
    "Ladon",
    "Mordremoth",
    "Nidhogg",
    "Ouroboros",
    "Pyra",
    "Quetzalcoatl",
    "Ryujin",
    "Saphira",
    "Tiamat",
    "Umbra",
    "Vermithrax",
    "Wyvern",
    "Xiang",
    "Y Ddraig Goch",
    "Zmey",
    "Alduin",
    "Bahamut",
    "Charizard",
    "Drogon",
    "Ebonhorn",
    "Firnen",
    "Godzilla",
    "Haku",
    "Indigo",
    "Jormungandr",
    "Kohaku",
    "Lorelai",
    "Mushu",
    "Níðhöggr",
    "Ormr",
    "Puff",
    "Querim",
    "Ryūjin",
    "Smaug",
    "Tatsu",
    "Uther",
    "Viserion",
    "Wyrm",
    "Xiuhcoatl",
    "Yazi",
    "Zephyr",
    "Aether",
    "Baleroc",
    "Cinder",
    "Draco",
    "Eclipse",
    "Fang",
    "Ghidorah",
    "Hydra",
    "Inferno",
    "Jade",
    "Kaiju",
    "Lava",
    "Midgardsormr",
    "Níðhöggur",
    "Obsidian",
    "Puff the Magic Dragon",
    "Quetzalli",
    "Ragnarok",
    "Saphire",
    "Tiamtu",
    "Umber",
    "Vermithrax Pejorative",
    "Wyrmheart",
    "Xíng",
    "Yamata no Orochi",
    "Zircon",
    "Achlys",
    "Boreas",
    "Chrysophylax",
    "Drakaina",
    "Eldur",
    "Firaxas",
    "Goreclaw",
    "Hephaestus",
    "Igneel",
    "Jormungand",
    "Kaida",
    "Ladon",
    "Mushu",
    "Nidhögg",
    "Ormarr",
]
print(names_list)

generated_names = generate_names_from_list(names_list)
for name in generated_names:
    print(name)
