
import re
import model
import os

keras_model = None
input_encoding = None
input_decoding = None
output_encoding = None
output_decoding = None

def load_default_model():
    trained_model_dir = os.path.join(os.path.dirname(__file__), '../trained_models')
    global keras_model, input_encoding, input_decoding, output_encoding, output_decoding
    keras_model, input_encoding, input_decoding, output_encoding, output_decoding = model.load(save_dir=trained_model_dir)

def to_katakana(text):

    if keras_model is None:
        load_default_model()

    return model.to_katakana(
        text=text.lower(),
        keras_model=keras_model,
        input_encoding=input_encoding,
        output_decoding=output_decoding)