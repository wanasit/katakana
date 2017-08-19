import json
import os
import shutil

import numpy as np
from keras.layers import Input, Embedding, LSTM, TimeDistributed, Dense
from keras.models import Model

import encoding


def load(save_dir='trained_models',
         input_length=20,
         output_length=20):

    input_encoding = json.load(open(save_dir + '/input_encoding.json'))
    input_decoding = json.load(open(save_dir + '/input_decoding.json'))
    input_decoding = {int(k): v for k, v in input_decoding.items()}

    output_encoding = json.load(open(save_dir + '/output_encoding.json'))
    output_decoding = json.load(open(save_dir + '/output_decoding.json'))
    output_decoding = {int(k): v for k, v in output_decoding.items()}

    output_dict_size = len(output_decoding) + 1
    input_dict_size = len(input_decoding) + 1

    model = create_keras_model(
        input_dict_size=input_dict_size,
        output_dict_size=output_dict_size,
        input_length=input_length,
        output_length=output_length)

    model.load_weights(save_dir + '/model_weight.h5')
    return model, input_encoding, input_decoding, output_encoding, output_decoding


def save(model, input_encoding, input_decoding, output_encoding, output_decoding,
         save_dir='trained_models'):

    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)

    os.mkdir(save_dir)
    json.dump(input_encoding, open(save_dir + '/input_encoding.json', 'w'))
    json.dump(input_decoding, open(save_dir + '/input_decoding.json', 'w'))
    json.dump(output_encoding, open(save_dir + '/output_encoding.json', 'w'))
    json.dump(output_decoding, open(save_dir + '/output_decoding.json', 'w'))
    model.save_weights(save_dir + '/model_weight.h5')
    with open(save_dir + '/model.json', 'w') as f:
        f.write(model.to_json())

def create_keras_model(
        input_dict_size,
        output_dict_size,
        input_length=20,
        output_length=20):

    encoder_input = Input(shape=(input_length,))
    decoder_input = Input(shape=(output_length,))

    encoder = Embedding(input_dict_size, 64, input_length=input_length, mask_zero=True)(encoder_input)
    encoder = LSTM(64, return_sequences=False)(encoder)

    decoder = Embedding(output_dict_size, 64, input_length=output_length, mask_zero=True)(decoder_input)
    decoder = LSTM(64, return_sequences=True)(decoder, initial_state=[encoder, encoder])
    decoder = TimeDistributed(Dense(output_dict_size, activation="softmax"))(decoder)

    model = Model(inputs=[encoder_input, decoder_input], outputs=[decoder])
    model.compile(optimizer='adam', loss='binary_crossentropy')

    return model

# =====================================================================


def to_katakana(text, keras_model, input_encoding, output_decoding,
                input_length=20,
                output_length=20):

    encoder_input = encoding.transform(input_encoding, [text.lower()], input_length)
    decoder_input = np.zeros(shape=(len(encoder_input), output_length))
    decoder_input[:, 0] = encoding.CHAR_CODE_START
    for i in range(1, output_length):
        output = keras_model.predict([encoder_input, decoder_input]).argmax(axis=2)
        decoder_input[:, i] = output[:, i]

    decoder_output = decoder_input
    return encoding.decode(output_decoding, decoder_output[0][1:])