# SPDX-License-Identifier: CC0-1.0

import binascii
import hashlib
import hmac
from abc import ABC, abstractmethod
from typing import ClassVar


class QRGenerator(ABC):
    B32TABLE: ClassVar[bytes] = b"GN5BH8QJSAC0MFR6P4VET1O7K9U2LD3I"

    @property
    @abstractmethod
    def type_len(self) -> int:
        ...

    @property
    @abstractmethod
    def var_len(self) -> int:
        ...

    @property
    @abstractmethod
    def keys(self) -> list[bytes]:
        ...

    @classmethod
    def modB32_encode(cls, in_buf: bytes) -> bytes:
        in_table = b"0123456789abcdefghijklmnopqrstuv"
        in_buf = bytes([in_table.index(x) for x in binascii.b2a_hex(in_buf).lower()])
        out_buf = bytearray()
        bit_pos = 0
        buf_pos = 0

        out_bit = 5
        in_bit = 4

        while buf_pos < len(in_buf):
            a = in_buf[buf_pos] << (32 - in_bit)
            if buf_pos + 1 < len(in_buf):
                a |= in_buf[buf_pos + 1] << (32 - in_bit * 2)

            a >>= 32 - out_bit - bit_pos
            a &= 2**out_bit - 1

            if buf_pos + 1 >= len(in_buf):
                a >>= 2

            out_buf.append(cls.B32TABLE[a])
            bit_pos += out_bit
            while bit_pos >= in_bit:
                bit_pos -= in_bit
                buf_pos += 1
        return out_buf

    def gen(self, pattern: str) -> str:
        if len(pattern) != self.type_len + self.var_len:
            raise ValueError(
                "Pattern must be %d characters long" % (self.type_len + self.var_len)
            )

        if not pattern.isalnum():
            raise ValueError("Pattern can only contain alnum characters")

        pattern = pattern.upper()
        hash_ = self.calc_hash(pattern.encode())
        return pattern + hash_.decode()

    def calc_hash(self, code: bytes) -> bytes:
        for key in self.keys:
            h = hmac.new(key, msg=code, digestmod=hashlib.md5)
            code = h.hexdigest().lower().encode()
        return self.modB32_encode(h.digest())


class V1QRGenerator(QRGenerator):
    @property
    def type_len(self) -> int:
        return 2

    @property
    def var_len(self) -> int:
        return 4

    @property
    def keys(self) -> list[bytes]:
        return [b"A14+BDM71D", b"QK35+NI8WV"]


class V2QRGenerator(QRGenerator):
    @property
    def type_len(self) -> int:
        return 3

    @property
    def var_len(self) -> int:
        return 4

    @property
    def keys(self) -> list[bytes]:
        return [b"OYD78+MIP3", b"N+Q09V7LI5"]


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--variant", choices=["v1", "v2"], default="v2")
    parser.add_argument("pattern", type=str)
    args = parser.parse_args()

    generator: QRGenerator

    if args.variant == "v1":
        generator = V1QRGenerator()
    else:
        generator = V2QRGenerator()

    print("/" + generator.gen(args.pattern))

    sys.exit(0)
