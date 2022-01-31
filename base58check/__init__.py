"""
:mod:`base58check`
~~~~~~~~~~~

A python implementation of the Base58Check encoding scheme.

The Base58Check encoding scheme is a modified Base 58 binary-to-text encoding.
More generically, Base58Check encoding is used for encoding byte arrays in
Bitcoin into human-typable strings.

ref: `<https://en.bitcoin.it/wiki/Base58Check_encoding>`_

.. note::
    For consistency with encoding schemes in python, encode inputs must be
    bytes and will be enforced.  Use `.encode('ascii')` on text input to
    encode to bytes.

Usage::

    >>> import base58check
    >>> base58check.b58encode(b'1BoatSLRHtKNngkdXEeobR76b53LETtpyT')
    b'\x00v\x80\xad\xec\x8e\xab\xca\xba\xc6v\xbe\x9e\x83\x85J\xde\x0b\xd2,\xdb\x0b\xb9`\xde'

    >>> base58check.b58decode('\x00v\x80\xad\xec\x8e\xab\xca\xba\xc6v\xbe\x9e'
    ...                       '\x83\x85J\xde\x0b\xd2,\xdb\x0b\xb9`\xde')
    b'1BoatSLRHtKNngkdXEeobR76b53LETtpyT'

:copyright: (c) 2018 by Nik Kuvhinov.
:license: MIT, see LICENSE for more details.
"""

__version__ = '2.0.0'


from hashlib import sha256
from collections import deque


DEFAULT_CHARSET = b'123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
# BASE = len(CHARSET)


def b58encode(val, charset=DEFAULT_CHARSET):
    """Encode input to base58 encoding.

    :param bytes val: The value to base58 encode.
    :param bytes charset: (optional) The character set to use for encoding.
    :return: the encoded bytestring.
    :rtype: bytes
    :raises: TypeError: if `val` is not bytes.

    Usage::

      >>> import base58check
      >>> base58check.b58encode(b'1BoatSLRHtKNngkdXEeobR76b53LETtpyT')
      b'\x00v\x80\xad\xec\x8e\xab\xca\xba\xc6v\xbe\x9e\x83\x85J\xde\x0b\xd2,\xdb\x0b\xb9`\xde'
    """

    def _b58encode_int(int_, default=bytes([charset[0]])):
        if not int_ and default:
            return default
        output = b''
        while int_:
            int_, idx = divmod(int_, base)
            output = charset[idx:idx+1] + output
        return output

    if not isinstance(val, bytes):
        raise TypeError(
            "a bytes-like object is required, not '%s', "
            "use .encode('ascii') to encode unicode strings" %
            type(val).__name__)

    if isinstance(charset, str):
        charset = charset.encode('ascii')

    base = len(charset)

    if not base == 58:
        raise ValueError('charset base must be 58, not %s' % base)

    pad_len = len(val)
    val = val.lstrip(b'\0')
    pad_len -= len(val)

    p, acc = 1, 0
    for char in deque(reversed(val)):
        acc += p * char
        p = p << 8

    result = _b58encode_int(acc, default=False)
    prefix = bytes([charset[0]]) * pad_len
    return prefix + result


def b58decode(val, charset=DEFAULT_CHARSET):
    """Decode base58 encoded input to original raw bytes.

    :param bytes val: The value to base58 decode.
    :param bytes charset: (optional) The character set to use for decoding.
    :return: the decoded bytes.
    :rtype: bytes

    Usage::

      >>> import base58check
      >>> base58check.b58decode('\x00v\x80\xad\xec\x8e\xab\xca\xba\xc6v\xbe'
      ...                       '\x9e\x83\x85J\xde\x0b\xd2,\xdb\x0b\xb9`\xde')
      b'1BoatSLRHtKNngkdXEeobR76b53LETtpyT'
    """

    def _b58decode_int(val):
        output = 0
        for char in val:
            output = output * base + charset.index(char)
        return output

    if isinstance(val, str):
        val = val.encode()

    if isinstance(charset, str):
        charset = charset.encode()

    base = len(charset)

    if not base == 58:
        raise ValueError('charset base must be 58, not %s' % base)

    pad_len = len(val)
    val = val.lstrip(bytes([charset[0]]))
    pad_len -= len(val)

    acc = _b58decode_int(val)

    result = deque()
    while acc > 0:
        acc, mod = divmod(acc, 256)
        result.appendleft(mod)

    prefix = b'\0' * pad_len
    return prefix + bytes(result)


def b58check_encode(val: bytes, address_version=0, charset=DEFAULT_CHARSET):
    """Encode input to base58check encoding.

        :param bytes val: The value to base58check encode.
        :param address_version: Address version
        :param bytes charset: (optional) The character set to use for encoding.
        :return: the encoded bytestring.
        :rtype: bytes
        :raises: TypeError: if `val` is not bytes.

        Usage::

          >>> import base58check
          >>> base58check.b58check_encode(b'_&\x13y\x1b6\xf6g\xfd\xb8\xe9V\x08\xb5^=\xf4\xc5\xf9\xeb')
          b'19g6oo8foQF5jfqK9gH2bLkFNwgCenRBPD'
        """
    v_addr = hex(address_version).removeprefix('0x')
    if len(v_addr) == 1:
        v_addr = '0' + v_addr
    v_addr = bytes.fromhex(v_addr)
    chk_sum = sha256(sha256(v_addr + val).digest()).digest()[:4]

    return b58encode(v_addr + val + chk_sum, charset=charset)


def b58check_address_is_valid(val: bytes, charset=DEFAULT_CHARSET):
    """Base58check address validation.

            :param bytes val: The value for the base58check address.
            :param bytes charset: (optional) The character set to use for decoding.
            :return: address is correct?
            :rtype: bool

            Usage::

              >>> import base58check
              >>> base58check.b58check_address_is_valid(b'19g6oo8foQF5jfqK9gH2bLkFNwgCenRBPD')
              True
            """
    b58check_address_bytes = b58decode(val, charset=charset)

    expected_chk_sum = b58check_address_bytes[-4:]
    actual_chk_sum = sha256(sha256(b58check_address_bytes[:-4]).digest()).digest()[:4]

    if expected_chk_sum != actual_chk_sum:
        return False

    return True


def b58check_decode(val: bytes, charset=DEFAULT_CHARSET):
    """Decode base58check encoded input to original raw bytes.

        :param bytes val: The value to base58check decode.
        :param bytes charset: (optional) The character set to use for decoding.
        :return: the decoded bytes.
        :rtype: bytes
        :raises: IncorrectAddress: if `val` is incorrect address.

        Usage::

          >>> import base58check
          >>> base58check.b58check_decode(b'19g6oo8foQF5jfqK9gH2bLkFNwgCenRBPD')
          b'_&\x13y\x1b6\xf6g\xfd\xb8\xe9V\x08\xb5^=\xf4\xc5\xf9\xeb'

        """
    if not b58check_address_is_valid(val, charset=charset):
        raise IncorrectAddress

    return b58decode(val, charset=charset)[1:-4]


class IncorrectAddress(Exception):
    pass
