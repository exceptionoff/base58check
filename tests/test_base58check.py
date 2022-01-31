import pytest
from collections import namedtuple

import base58check

CaseData = namedtuple('case_data', 'raw encoded_base58 encoded_base58check')

TEST_DATA = [
    CaseData(b'\x00v\x80\xad\xec\x8e\xab\xca\xba\xc6v\xbe\x9e\x83\x85J\xde\x0b\xd2,\xdb\x0b\xb9`\xde',
             b'1BoatSLRHtKNngkdXEeobR76b53LETtpyT',
             b'112Dh9Vjc6BeqJNk7YRf4BZVreDP8yTp41i3Jd5Ny'),
    CaseData(b'\x05\xf8\x15\xb06\xd9\xbb\xbc\xe5\xe9\xf2\xa0\n\xbd\x1b\xf3\xdc\x91\xe9U\x10\xcd\x001\x07',
             b'3QJmV3qfvL9SuYo34YihAf3sRCW3qSinyC',
             b'1Gia9Vskkz2Q2b7pezDvmLjNTqVHYKKetkVc88s4'),
    CaseData(b'o;|F\xa5\xa6\x00\xb2\x98k\xd8\x04\x13|\xf9\x1d\xbbZE\xa2|\xa8\x00l+',
             b'mkwV3DZkgYwKaXkphBtcXAjsYQEqZ8aB3x',
             b'163suu9V6FpVHGRyzZX2wpWomHTUXDwPbnvqDirKG'),
    CaseData(b'o\xdf\x84\xed0\x95\xc6_\xddu\xf4j\xd8|3\xe0\xb1\xf4\x14\xff\xe6\xf8\t\x8f\xaa',
             b'n1tpDjEJw32qGwkdQKPfACpcTtCa6hDVBw',
             b'165ZmQX219niYtUrnmGFUvYbnMwaeN8NqrrZa3r8z'),
    CaseData(b'0\xd0\xa2\x07\xd1\x82\xa7\xe0]\x7fD\xb6\\5\xf9\xe1\xd1v\xeb\xde\xa7\xba\x08\x90\\',
             b'LeF6vC9k1qfFDEj6UGjM5e4fwHtiKsakTd',
             b'13DXoiasVcoBH7tuUoV91nQSPTBLQxzoHHJefCC7G'),
    CaseData(b'o\x96_\xfa\xccH\xe6\x87\xe0\xd3NJ\x8a\x86\x83*\x8dl\xfc\xf0{\xf1#\xb76',
             b'muE4dcYXagWA7WT8ZnCriiy65FELikhdUy',
             b'164p8e7XQoc11kQ7GfjbLF3T4sN5hDXDF3mqWDhV7')
]

CUSTOM_CHARSET = b'rpshnaf39wBUDNEGHJKLM4PQRST7VWXYZ2bcdeCg65jkm8oFqi1tuvAxyz'
CUSTOM_CHARSET_DATA = [
    CaseData(b'\x00\x88\xa5\xa5|\x82\x9f@\xf2^\xa83\x85\xbb\xdel=\x8bL\xa0\x82\xedC\x86A',
             b'rDTXLQ7ZKZVKz33zJbHjgVShjsBnqMBhmN',
             b'rrpQWAHDdmvPvLn3mbbAemwZJghBLNRCFCVQCt8tH')
]


class TestBase58:
    def test_base(self):
        """Assert that BASE is equal to 58"""
        assert len(base58check.DEFAULT_CHARSET) == 58

    def test_encoding_text_raises_typeerror(self):
        """Assert encoding text (nonbinary) raises TypeError"""
        with pytest.raises(TypeError):
            base58check.b58encode('test text')

    @pytest.mark.parametrize('raw,encoded,_', TEST_DATA)
    def test_encoding(self, raw, encoded, _):
        """Assert correct encoding and return type"""
        result = base58check.b58encode(raw)
        assert result == encoded
        assert isinstance(result, bytes)

    @pytest.mark.parametrize('raw,encoded,_', TEST_DATA)
    def test_decoding(self, raw, encoded, _):
        """Assert correct decoding and return type from bytes"""
        result = base58check.b58decode(encoded)
        assert result == raw
        assert isinstance(result, bytes)

    @pytest.mark.parametrize('raw,encoded,_', TEST_DATA)
    def test_decoding_from_unicode(self, raw, encoded, _):
        """Assert correct decoding and return type from text"""
        result = base58check.b58decode(encoded.decode())
        assert result == raw
        assert isinstance(result, bytes)

    @pytest.mark.parametrize('raw,encoded,_', CUSTOM_CHARSET_DATA)
    def test_custom_charset_encoding(self, raw, encoded, _):
        """Assert correct encoding and return type for custom character set"""
        result = base58check.b58encode(raw, charset=CUSTOM_CHARSET)
        assert result == encoded
        assert isinstance(result, bytes)

    @pytest.mark.parametrize('raw,encoded,_', CUSTOM_CHARSET_DATA)
    def test_custom_charset_decoding(self, raw, encoded, _):
        """Assert correct decoding and return type for custom character set"""
        result = base58check.b58decode(encoded, charset=CUSTOM_CHARSET)
        assert result == raw
        assert isinstance(result, bytes)


class TestBase58Check:

    @pytest.mark.parametrize('_,__,encoded', TEST_DATA)
    def test_decoding_invalid_address_raises_incorrectaddress(self, _, __, encoded):
        """Assert encoding incorrect address raises IncorrectAddress"""
        with pytest.raises(base58check.IncorrectAddress):
            defective_encoded = encoded[-10:] + encoded[:-10]
            base58check.b58check_decode(defective_encoded)

    @pytest.mark.parametrize('_,__,encoded', TEST_DATA)
    def test_valid_address(self, _, __, encoded):
        """Assert correct address"""
        assert base58check.b58check_address_is_valid(encoded)

    @pytest.mark.parametrize('_,__,encoded', TEST_DATA)
    def test_invalid_address(self, _, __, encoded):
        """Assert incorrect address"""
        defective_encoded = encoded[-10:] + encoded[:-10]
        assert not base58check.b58check_address_is_valid(defective_encoded)

    @pytest.mark.parametrize('raw,_,encoded', TEST_DATA)
    def test_encoding(self, raw, _, encoded):
        """Assert correct encoding and return type"""
        result = base58check.b58check_encode(raw)
        assert result == encoded
        assert isinstance(result, bytes)

    @pytest.mark.parametrize('raw,_,encoded', TEST_DATA)
    def test_decoding(self, raw, _, encoded):
        """Assert correct decoding and return type from bytes"""
        result = base58check.b58check_decode(encoded)
        assert result == raw
        assert isinstance(result, bytes)

    @pytest.mark.parametrize('raw,_,encoded', TEST_DATA)
    def test_decoding_from_unicode(self, raw, _, encoded):
        """Assert correct decoding and return type from text"""
        result = base58check.b58check_decode(encoded.decode())
        assert result == raw
        assert isinstance(result, bytes)

    @pytest.mark.parametrize('raw,_,encoded', CUSTOM_CHARSET_DATA)
    def test_custom_charset_encoding(self, raw, _, encoded):
        """Assert correct encoding and return type for custom character set"""
        result = base58check.b58check_encode(raw, charset=CUSTOM_CHARSET)
        assert result == encoded
        assert isinstance(result, bytes)

    @pytest.mark.parametrize('raw,_,encoded', CUSTOM_CHARSET_DATA)
    def test_custom_charset_decoding(self, raw, _, encoded):
        """Assert correct decoding and return type for custom character set"""
        result = base58check.b58check_decode(encoded, charset=CUSTOM_CHARSET)
        assert result == raw
        assert isinstance(result, bytes)

