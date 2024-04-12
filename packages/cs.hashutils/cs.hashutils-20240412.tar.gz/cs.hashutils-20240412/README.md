Convenience hashing facilities.

*Latest release 20240412*:
* BaseHashCode.hashclass(hashname): fall back to looking for blake3 from the blake3 module.
* BaseHashCode: new get_hashfunc(hashname) static method.

## Class `BaseHashCode(builtins.bytes)`

Base class for hashcodes, subclassed by `SHA1`, `SHA256` et al.

You can obtain the class for a particular hasher by name, example:

    SHA256 = BaseHashCode.hashclass('sha256')

*Method `BaseHashCode.__str__(self)`*:
Return `f'{self.hashname}:{self.hex()}'`.

*Method `BaseHashCode.from_buffer(bfr: cs.buffer.CornuCopyBuffer)`*:
Compute hashcode from the contents of the `CornuCopyBuffer` `bfr`.

*Method `BaseHashCode.from_data(bs)`*:
Compute hashcode from the data `bs`.

*Method `BaseHashCode.from_fspath(fspath, **kw)`*:
Compute hashcode from the contents of the file `fspath`.

*Method `BaseHashCode.from_hashbytes(hashbytes)`*:
Factory function returning a `BaseHashCode` object from the hash bytes.

*Method `BaseHashCode.from_hashbytes_hex(hashhex: str)`*:
Factory function returning a `BaseHashCode` object
from the hash bytes hex text.

*Method `BaseHashCode.from_named_hashbytes_hex(hashname, hashhex)`*:
Factory function to return a `HashCode` object
from the hash type name and the hash bytes hex text.

*Method `BaseHashCode.from_prefixed_hashbytes_hex(hashtext: str)`*:
Factory function returning a `BaseHashCode` object
from the hash bytes hex text prefixed by the hashname.
This is the reverse of `__str__`.

*Method `BaseHashCode.get_hashfunc(hashname: str)`*:
Fetch the hash function implied by `hashname`.

*Method `BaseHashCode.hashclass(hashname: str, hashfunc=None, **kw)`*:
Return the class for the hash function named `hashname`.

Parameters:
* `hashname`: the name of the hash function
* `hashfunc`: optional hash function for the class

*Property `BaseHashCode.hashname`*:
The hash code type name, derived from the class name.

*Method `BaseHashCode.hex(self) -> str`*:
Return the hashcode bytes transcribes as a hexadecimal ASCII `str`.

*Method `BaseHashCode.promote(obj)`*:
Promote to a `BaseHashCode` instance.

## Class `MD5(BaseHashCode)`

Hash class for the 'md5' algorithm.

*`MD5.hashfunc`*

## Class `SHA1(BaseHashCode)`

Hash class for the 'sha1' algorithm.

*`SHA1.hashfunc`*

## Class `SHA224(BaseHashCode)`

Hash class for the 'sha224' algorithm.

*`SHA224.hashfunc`*

## Class `SHA256(BaseHashCode)`

Hash class for the 'sha256' algorithm.

*`SHA256.hashfunc`*

## Class `SHA384(BaseHashCode)`

Hash class for the 'sha384' algorithm.

*`SHA384.hashfunc`*

## Class `SHA512(BaseHashCode)`

Hash class for the 'sha512' algorithm.

*`SHA512.hashfunc`*

# Release Log



*Release 20240412*:
* BaseHashCode.hashclass(hashname): fall back to looking for blake3 from the blake3 module.
* BaseHashCode: new get_hashfunc(hashname) static method.

*Release 20240316*:
Fixed release upload artifacts.

*Release 20240211*:
Initial PyPI release: BaseHashCode(bytes) and subclasses for various hash algorithms.
