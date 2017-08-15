
import re
import model

keras_model = None
input_encoding = None
input_decoding = None
output_encoding = None
output_decoding = None

def load_default_model():
    global keras_model, input_encoding, input_decoding, output_encoding, output_decoding
    keras_model, input_encoding, input_decoding, output_encoding, output_decoding = model.load()


def to_katakana(text):

    if keras_model is None:
        load_default_model()

    return model.to_katakana(
        text=text.lower(),
        keras_model=keras_model,
        input_encoding=input_encoding,
        output_decoding=output_decoding)