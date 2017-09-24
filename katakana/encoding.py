import numpy as np

CHAR_CODE_START = 1
CHAR_CODE_PADDING = 0


def build_characters_encoding(names):
    """
    :param names: list of strings
    :return: (encoding, decoding, count)
    """
    count = 2
    encoding = {}
    decoding = {1: 'START'}
    for c in set([c for name in names for c in name]):
        encoding[c] = count
        decoding[count] = c
        count += 1
    return encoding, decoding, count


def transform(encoding, data, vector_size=20):
    """
    :param encoding: encoding dict built by build_characters_encoding()
    :param data: list of strings
    :param vector_size: size of each encoded vector
    """
    transformed_data = np.zeros(shape=(len(data), vector_size))
    for i in range(len(data)):
        for j in range(min(len(data[i]), vector_size)):
            transformed_data[i][j] = encoding[data[i][j]]
    return transformed_data


def decode(decoding, vector):
    """
    :param decoding: decoding dict built by build_characters_encoding()
    :param vector: an encoded vector
    """
    text = ''
    for i in vector:
        if i == 0:
            break
        text += decoding[i]
    return text
