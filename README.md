# Base58Check
 [![Pypi Version](https://img.shields.io/pypi/v/base58check.svg)](https://pypi.python.org/pypi/base58check) [![Pypi License](https://img.shields.io/pypi/l/base58check.svg)](https://pypi.python.org/pypi/base58check) [![Pypi Wheel](https://img.shields.io/pypi/wheel/base58check.svg)](https://pypi.python.org/pypi/base58check) [![Pypi Versions](https://img.shields.io/pypi/pyversions/base58check.svg)](https://pypi.python.org/pypi/base58check)


## Maintainer
Nik Kuvshinov | <exceptionoff@gmail.com> | [github](https://github.com/exceptionoff)


## Introduction
A python implementation of the Base58Check encoding scheme.


The Base58Check encoding scheme is a modified Base 58 binary-to-text encoding.  More generically, Base58Check encoding is used for encoding byte arrays in Bitcoin into human-typable strings.


*PLEASE NOTE*: For consistency with encoding schemes in python, encode inputs must be bytes and will be enforced.  Use `.encode('ascii')` on text input to encode to bytes.

* ref: https://en.bitcoin.it/wiki/Base58Check_encoding


## Installation
```shell
pip3 install base58check
```


## Usage
```python
>>> import base58check
```

### encoding
```python
>>> base58check.b58encode(b'1BoatSLRHtKNngkdXEeobR76b53LETtpyT')
b'\x00v\x80\xad\xec\x8e\xab\xca\xba\xc6v\xbe\x9e\x83\x85J\xde\x0b\xd2,\xdb\x0b\xb9`\xde'
>>> base58check.b58check_encode(b'_&\x13y\x1b6\xf6g\xfd\xb8\xe9V\x08\xb5^=\xf4\xc5\xf9\xeb')
b'19g6oo8foQF5jfqK9gH2bLkFNwgCenRBPD'
```

### decoding (input can be text or bytes here)
```python
>>> base58check.b58decode('\x00v\x80\xad\xec\x8e\xab\xca\xba\xc6v\xbe\x9e\x83\x85J\xde\x0b\xd2,\xdb\x0b\xb9`\xde')
b'1BoatSLRHtKNngkdXEeobR76b53LETtpyT'
>>> base58check.b58check_decode(b'19g6oo8foQF5jfqK9gH2bLkFNwgCenRBPD')
b'_&\x13y\x1b6\xf6g\xfd\xb8\xe9V\x08\xb5^=\xf4\xc5\xf9\xeb'
```

### check address
```python
>>> base58check.b58check_address_is_valid(b'19g6oo8foQF5jfqK9gH2bLkFNwgCenRBPD')
True
```

## Changes
* [CHANGELOG](CHANGELOG.md)
