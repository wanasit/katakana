from setuptools import setup

setup(
    name='katakana',
    version='0.1',
    description='English to Katakana with sequence-to-seqeucne learning',
    license='MIT',
    url='http://github.com/wanasit/katakana',
    author='wanasit',
    packages=['katakana'],
    install_requires=['keras', 'h5py', 'numpy'],
)
