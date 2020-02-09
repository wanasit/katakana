# Katakana

English to Katakana using a Sequence-to-Sequence model.

To learn more about how to train the model, checkout these resources:

* [English to Katakana using Sequence to Sequence in Tensorflow](https://medium.com/@wanasit/english-to-katakana-with-sequence-to-sequence-in-tensorflow-a03a16ac19be)
* [English to Katakana using Sequence to Sequence in Pytorch](https://medium.com/@wanasit/english-to-katakana-with-sequence-to-sequence-in-pytorch-24f18ab19296)

Please also feel free to download the English-Katakana dataset to train you own models [here](https://raw.githubusercontent.com/wanasit/katakana/master/dataset/data.csv)

## Use pre-trained model as a library

**Warning:** The pre-trained is a small network and not properly trained. It's not production ready 
and should be used just for demonstration propose. 

```
 pip install --upgrade git+https://github.com/wanasit/katakana.git
```

There is `to_katakana` function that takes English string as an input and return Katakana (unicode) as an output.
```python
from katakana import to_katakana 

to_katakana('katakana')
# u'\u30ab\u30bf\u30ab\u30ca' or カタカナ
```
