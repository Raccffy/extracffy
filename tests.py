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

    def test_06_dir_obfs_extraction(self):
        extracffy = Extracffy("tests/ps_20240404_8ea2917_dir_obfs.zip")
        extracffy_idx = extracffy.cd_read()

        for idx in extracffy_idx:
            extracffy.extract(idx)

        extracffy.close()


class Test_B_OggDeobfs(unittest.TestCase):
    def test_01_ref(self):
        extracffy = Extracffy("tests/ref_ogg_obfs.zip")
        extracffy_idx = extracffy.cd_read()

        for idx in extracffy_idx:
            extracffy.extract(idx, True)

        extracffy.close()

    def test_02_deobfs(self):
        """
        Currently there's no Vorbis autocorrection in Extracffy. Ogg files
        are not readable due to corrupted codec magic number, which leads
        to the "End of file" error.
        """

        extracffy = Extracffy("tests/ps_20240404_8ea2917_ogg_obfs.zip")
        extracffy_idx = extracffy.cd_read()

        for idx in extracffy_idx:
            extracffy.extract(idx, True)

        extracffy.close()


if __name__ == '__main__':
    unittest.main()
