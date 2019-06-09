import re
import os

from . import model

loaded_model = None
input_encoding = None
input_decoding = None
output_encoding = None
output_decoding = None


def load_default_model():
    global loaded_model, input_encoding, input_decoding, output_encoding, output_decoding

    trained_model_dir = os.path.join(os.path.dirname(__file__), '../trained_models')
    loaded_model, input_encoding, input_decoding, output_encoding, output_decoding = \
        model.load(save_dir=trained_model_dir)


def to_katakana(text):
    if loaded_model is None:
        load_default_model()

    return model.to_katakana(
        text=text.lower(),
        model=loaded_model,
        input_encoding=input_encoding,
        output_decoding=output_decoding)

