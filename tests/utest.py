import os.path
import unittest

import sys

sys.path.insert(0, os.path.abspath('..'))

import mupen64plus_ini_creator as m64p_ini


mame_path = 'db/mame_n64.xml'
nointro_path = 'db/Pintendo - Pintendo 64 (BigEndian) (20200121-021514).dat'
m64p_path = 'db/mupen64plus.ini'
rom_path = 'rom'


class Tests(unittest.TestCase):

    def test_mame(self):

        mame_games = list(m64p_ini.from_mame_xml(mame_path))

        self.assertEqual(len(mame_games), 2)

        # general test
        for game in mame_games:

            self.assertIsInstance(game, m64p_ini.GameMame)

            self.assertIsInstance(game.name, str)
            self.assertIsInstance(game.description, str)
            self.assertIsNotNone(game.rom)

            rom = game.rom

            self.assertIsInstance(rom, m64p_ini.RomMame)
            self.assertIsNotNone(rom.name)
            self.assertIsInstance(rom.size, int)
            self.assertIsInstance(rom.crc, str)
            self.assertIsInstance(rom.sha1, str)

        # deep test first game
        game = mame_games[0]
        self.assertEqual(game.name, "spl64")
        self.assertEqual(game.description,
                         "Super Plumber 64 (Europe) (En,Fr,De)")
        self.assertEqual(game.serial, ["NOS-NGEP-AOS", "NOS-NGEP-EOR"])
        self.assertEqual(game.release, "19980807")
        self.assertEqual(game.alt_title, "Tototakiki")

        self.assertEqual(game.rom.name, "nos-ngep-0.o1")
        self.assertEqual(game.rom.size, 12582911)
        self.assertEqual(game.rom.crc, "7425be2d")
        self.assertEqual(game.rom.sha1,
                         "63627dba22ae2b357c0e370e68dc5af56eeb0a24")

    def test_nointro(self):

        nointro_games = list(m64p_ini.from_nointro_dat(nointro_path))

        self.assertEqual(len(nointro_games), 2)

        # general test
        for game in nointro_games:

            self.assertIsInstance(game, m64p_ini.GameNoIntro)

            self.assertIsInstance(game.name, str)
            self.assertIsInstance(game.description, str)
            self.assertIsNotNone(game.rom)

            rom = game.rom

            self.assertIsInstance(rom, m64p_ini.RomNoIntro)
            self.assertIsNotNone(rom.name)
            self.assertIsInstance(rom.size, int)
            self.assertIsInstance(rom.crc, str)
            self.assertIsInstance(rom.md5, str)
            self.assertIsInstance(rom.sha1, str)
            self.assertIsInstance(rom.status, str)
            self.assertIsInstance(rom.serial, str)

        # deep test first game
        game = nointro_games[0]
        self.assertEqual(game.name, "Super Plumber 64 (Europe) (En,Fr,De)")
        self.assertEqual(game.description,
                         "Super Plumber 64 (Europe) (En,Fr,De)")
        self.assertEqual(game.rom.name,
                         "Super Plumber 64 (Europe) (En,Fr,De).z64")
        self.assertEqual(game.rom.size, 33554431)
        self.assertEqual(game.rom.crc, "002C2B2A")
        self.assertEqual(game.rom.md5, "34AB1DEA3111A234A8B5C5679DE22E83")
        self.assertEqual(game.rom.sha1,
                         "7FDE668850A7D1A8402AB94BB09538A537A7E38B")
        self.assertEqual(game.rom.status, "verified")
        self.assertEqual(game.rom.serial, "NO6D")

    def test_m64p(self):

        m64p_games = list(m64p_ini.from_mupen64plus_ini(m64p_path))

        self.assertEqual(len(m64p_games), 2)

        # general test
        for game in m64p_games:

            self.assertIsInstance(game, m64p_ini.GameMupen64Plus)

            self.assertIsInstance(game.good_name, str)
            self.assertIsInstance(game.md5, str)
            self.assertIsInstance(game.crc, str)
            self.assertIsInstance(game.status, int)
            self.assertIsInstance(game.rumble, str)
            self.assertIsInstance(game.players, int)
            self.assertIsInstance(game.save_type, str)

        # deep test first game
        game = m64p_games[0]
        self.assertEqual(game.good_name, "Super Plumber 64 (Europe) (En,Fr,De)")
        self.assertEqual(game.md5, "34AB1DEA3111A233A8B5C5679DE22E83")
        self.assertEqual(game.crc, "3B941695 F90A5EEB")
        self.assertEqual(game.save_type, "Controller Pack")
        self.assertEqual(game.status, 1)
        self.assertEqual(game.rumble, "Yes")
        self.assertEqual(game.players, 4)
        self.assertEqual(game.counter_per_ops, 1)
        self.assertEqual(game.mem_pak, "Yes")
        self.assertEqual(game.ref_md5, "9D58996A8AA91263B5CD45C385F45FE4")
        self.assertEqual(game.transfer_pak, "Yes")
        self.assertEqual(game.disable_extra_mem, 1)
        self.assertEqual(game.bio_pak, "Yes")
        self.assertEqual(game.si_dma_duration, 100)
        self.assertEqual(
            game.cheat_0,
            "D109A814 0320,8109A814 0000,D109A816 F809,8109A816 0000")

    def test_rom_header(self):

        roms = list(m64p_ini.from_folder(rom_path))

        self.assertEqual(len(roms), 1)

        # general test
        for rom in roms:

            self.assertIsInstance(rom, m64p_ini.RomHeader)

            self.assertIsInstance(rom.init_PI_BSB_DOM1_LAT_REG, int)
            self.assertIsInstance(rom.init_PI_BSB_DOM1_PGS_REG, int)
            self.assertIsInstance(rom.init_PI_BSB_DOM1_PWD_REG, int)
            self.assertIsInstance(rom.init_PI_BSB_DOM1_PGS_REG2, int)
            self.assertIsInstance(rom.clock_rate, int)
            self.assertIsInstance(rom.pc, int)
            self.assertIsInstance(rom.release, int)
            self.assertIsInstance(rom.crc_1, int)
            self.assertIsInstance(rom.crc_2, int)
            self.assertIsInstance(rom.name, str)
            self.assertIsInstance(rom.manufacturer_id, int)
            self.assertIsInstance(rom.cartridge_id, int)
            self.assertIsInstance(rom.country_code, int)

        # deep test first game
        rom = roms[0]

        self.assertEqual(rom.init_PI_BSB_DOM1_LAT_REG, 128)
        self.assertEqual(rom.init_PI_BSB_DOM1_PGS_REG, 55)
        self.assertEqual(rom.init_PI_BSB_DOM1_PWD_REG, 64)
        self.assertEqual(rom.init_PI_BSB_DOM1_PGS_REG2, 64)
        self.assertEqual(rom.clock_rate, 15)
        self.assertEqual(rom.pc, 2149580800)
        self.assertEqual(rom.release, 5188)
        self.assertEqual(rom.crc_1, 780044604)
        self.assertEqual(rom.crc_2, 1315485250)

        self.assertEqual(rom.manufacturer_id, 0)
        self.assertEqual(rom.cartridge_id, 0)
        self.assertEqual(rom.country_code, 0)


if __name__ == '__main__':
    unittest.main()
