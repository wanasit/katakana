from __future__ import print_function

import numpy as np
import pandas as pd

from katakana import model, encoding

MAX_ENGLISH_INPUT_LENGTH = 20
MAX_KATAKANA_OUTPUT_LENGTH = 20

# Load and shuffle  ----------------------

data = pd.read_csv('./data/joined_titles.csv', header=None)
data = data.sample(frac=1, random_state=0)

data_input = [s.decode('utf-8').lower() for s in data[0]]
data_output = [s.decode('utf-8') for s in data[1]]

data_size = len(data)

training_input  = data_input[data_size*0/100:data_size*90/100]
training_output = data_output[data_size*0/100:data_size*90/100]

validation_input = data_input[data_size*90/100:data_size*100/100]
validation_output = data_output[data_size*90/100:data_size*100/100]

# Encoding the data ----------------------

input_encoding, input_decoding, input_dict_size = encoding.build_characters_encoding(data_input)
output_encoding, output_decoding, output_dict_size = encoding.build_characters_encoding(data_output)

encoded_training_input = encoding.transform(input_encoding, training_input, vector_size=MAX_ENGLISH_INPUT_LENGTH)
encoded_training_output = encoding.transform(output_encoding, training_output, vector_size=MAX_KATAKANA_OUTPUT_LENGTH)
encoded_validation_input = encoding.transform(input_encoding, validation_input, vector_size=MAX_ENGLISH_INPUT_LENGTH)
encoded_validation_output = encoding.transform(output_encoding, validation_output, vector_size=MAX_KATAKANA_OUTPUT_LENGTH)

# Building the model ----------------------

training_encoder_input = encoded_training_input

training_decoder_input = np.zeros_like(encoded_training_output)
training_decoder_input[:, 1:] = encoded_training_output[:,:-1]
training_decoder_input[:, 0] = encoding.CHAR_CODE_START
training_decoder_output = np.eye(output_dict_size)[encoded_training_output.astype('int')]

validation_encoder_input = encoded_validation_input
validation_decoder_input = np.zeros_like(encoded_validation_output)
validation_decoder_input[:, 1:] = encoded_validation_output[:,:-1]
validation_decoder_input[:, 0] = encoding.CHAR_CODE_START
validation_decoder_output = np.eye(output_dict_size)[encoded_validation_output.astype('int')]

# Building the model ----------------------

keras_model = model.create_keras_model(
    input_dict_size=input_dict_size,
    output_dict_size=output_dict_size,
    input_length=MAX_ENGLISH_INPUT_LENGTH,
    output_length=MAX_KATAKANA_OUTPUT_LENGTH)

keras_model.fit(
    x=[training_encoder_input, training_decoder_input],
    y=[training_decoder_output],
    validation_data=(
        [validation_encoder_input, validation_decoder_input], [validation_decoder_output]),
    verbose=2,
    batch_size=64,
    epochs=100)

model.save(
    model=keras_model,
    input_encoding=input_encoding,
    input_decoding=input_decoding,
    output_encoding=output_encoding,
    output_decoding=output_decoding)