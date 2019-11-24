from __future__ import print_function

import pandas as pd

from katakana import model, encoding

MAX_ENGLISH_INPUT_LENGTH = 20
MAX_KATAKANA_OUTPUT_LENGTH = 20

# Load and shuffle  ----------------------

data = pd.read_csv('./dataset/data.csv')
data = data.sample(frac=1, random_state=0)

data_input = [s.lower() for s in data[0]]
data_output = [s.lower() for s in data[1]]

data_size = len(data)

train_split_index = int(data_size*90/100)

training_input  = data_input[:train_split_index]
training_output = data_output[:train_split_index]
validation_input = data_input[train_split_index:]
validation_output = data_output[train_split_index:]

# Encoding the dataset ----------------------

input_encoding, input_decoding, input_dict_size = encoding.build_characters_encoding(data_input)
output_encoding, output_decoding, output_dict_size = encoding.build_characters_encoding(data_output)

encoded_training_input = encoding.transform(input_encoding, training_input, vector_size=MAX_ENGLISH_INPUT_LENGTH)
encoded_training_output = encoding.transform(output_encoding, training_output, vector_size=MAX_KATAKANA_OUTPUT_LENGTH)
encoded_validation_input = encoding.transform(input_encoding, validation_input, vector_size=MAX_ENGLISH_INPUT_LENGTH)
encoded_validation_output = encoding.transform(output_encoding, validation_output, vector_size=MAX_KATAKANA_OUTPUT_LENGTH)

# Building the model ----------------------

training_encoder_input, training_decoder_input, training_decoder_output = \
    model.create_model_data(encoded_training_input, encoded_training_output, output_dict_size)

validation_encoder_input, validation_decoder_input, validation_decoder_output = \
    model.create_model_data(encoded_validation_input, encoded_validation_output, output_dict_size)

# Building the model ----------------------

seq2seq_model = model.create_model(
    input_dict_size=input_dict_size,
    output_dict_size=output_dict_size,
    input_length=MAX_ENGLISH_INPUT_LENGTH,
    output_length=MAX_KATAKANA_OUTPUT_LENGTH)

seq2seq_model.fit(
    x=[training_encoder_input, training_decoder_input],
    y=[training_decoder_output],
    validation_data=(
        [validation_encoder_input, validation_decoder_input], [validation_decoder_output]),
    verbose=2,
    batch_size=64,
    epochs=30)

model.save(
    model=seq2seq_model,
    input_encoding=input_encoding,
    input_decoding=input_decoding,
    output_encoding=output_encoding,
    output_decoding=output_decoding)