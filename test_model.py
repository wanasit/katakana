from __future__ import print_function

import pandas as pd

from katakana import model, encoding

# ===============================================================

print('Loading the model...')

testing_model, input_encoding, input_decoding, output_encoding, output_decoding = model.load()

# ===============================================================

print('Evaluating the model on random testing dataset...')

data = pd.read_csv('./dataset/data.csv')
data = data.sample(frac=1, random_state=11)

data_input = [s.lower() for s in data[0]]
data_output = [s.lower() for s in data[1]]

data_size = len(data)
test_split = int(data_size*10/100)

test_input  = data_input[:test_split]
test_output = data_output[:test_split]

encoded_testing_input = encoding.transform(input_encoding, test_input)
encoded_testing_output = encoding.transform(output_encoding, test_output)

test_encoder_input, test_decoder_input, test_decoder_output = \
    model.create_model_data(encoded_testing_input, encoded_testing_output, len(output_decoding) + 1)

testing_model.evaluate(x=[test_encoder_input, test_decoder_input], y=test_decoder_output)

# ===============================================================

print('Evaluating the model on random names...')


def to_katakan(english_text):
    return model.to_katakana(english_text, testing_model, input_encoding, output_decoding)


print(data_input[0], to_katakan(data_input[0]))
print(data_input[1], to_katakan(data_input[1]))
print(data_input[2], to_katakan(data_input[2]))

print('Hello World', to_katakan('Hello World'))
print('Banana', to_katakan('Banana'))
print('Test', to_katakan('Test'))