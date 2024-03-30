"""
Extracffy's tests.
"""

import unittest
from api import Extracffy


class Test_A_ResourcePackExtraction(unittest.TestCase):
    def test_01_standard_extraction(self):
        extracffy = Extracffy("tests/ref_7-zip.zip")
        extracffy_idx = extracffy.cd_read()

        for idx in extracffy_idx:
            extracffy.extract(idx, True)

        extracffy.close()

    def test_02_pedantic_extraction(self):
        extracffy = Extracffy("tests/ps_0.4.0_pedantic.zip")
        extracffy_idx = extracffy.cd_read()

        for idx in extracffy_idx:
            extracffy.extract(idx, True)

        extracffy.close()

    def test_03_high_extraction(self):
        extracffy = Extracffy("tests/ps_0.4.0_high.zip")
        extracffy_idx = extracffy.cd_read()

        for idx in extracffy_idx:
            extracffy.extract(idx, True)

        extracffy.close()

    def test_04_balanced_extraction(self):
        extracffy = Extracffy("tests/ps_0.4.0_balanced.zip")
        extracffy_idx = extracffy.cd_read()

        for idx in extracffy_idx:
            extracffy.extract(idx, True)

        extracffy.close()

    def test_05_disregard_extraction(self):
        extracffy = Extracffy("tests/ps_0.4.0_disregard.zip")
        extracffy_idx = extracffy.cd_read()

        for idx in extracffy_idx:
            extracffy.extract(idx)

        extracffy.close()


if __name__ == '__main__':
    unittest.main()