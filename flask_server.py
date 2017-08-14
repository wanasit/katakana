from __future__ import print_function
from flask import Flask, jsonify, request, send_from_directory, redirect

from katakana import model

keras_model, input_encoding, input_decoding, output_encoding, output_decoding = model.load()

print('Loaded model')
print('Input dict size', len(input_encoding))
print('Output dict size', len(output_encoding))

print('test "hello world"', model.to_katakana('hello world', keras_model, input_encoding, output_decoding).encode('utf8'))
print('test "john doe"', model.to_katakana('john doe', keras_model, input_encoding, output_decoding).encode('utf8'))
print('test "john"', model.to_katakana('john', keras_model, input_encoding, output_decoding).encode('utf8'))
print('test "james"', model.to_katakana('james', keras_model, input_encoding, output_decoding).encode('utf8'))

app = Flask(__name__)

@app.route('/katakana')
def do_katakana():
    text = request.args['text']
    katakana = model.to_katakana(text, keras_model, input_encoding, output_decoding)
    return jsonify({
        'input': text,
        'katakana': katakana
    })

@app.route('/<path:path>')
def do_static(path):
    return send_from_directory('web', path)

@app.route('/')
def hello():
    return redirect("/index.html")

if __name__ == '__main__':
    app.run(debug=True)