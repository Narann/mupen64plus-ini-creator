import datetime
import re
from xml.etree import ElementTree


class RomMame:
    """Class representing a ROM in MAME XML database."""

    def __init__(self):

        self.name = None
        self.size = None
        self.crc = None
        self.sha1 = None

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.name}")'


class GameMame:
    """Class representing a game in MAME XML database."""

    def __init__(self):

        self.name = None
        self.clone_of = None
        self.description = None
        self.year = None
        self.publisher = None
        self.serial = None
        self.rom = None

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.name}")'


class RomNoIntro:
    """Class representing a ROM in No-Intro XML database."""

    def __init__(self):

        self.name = None
        self.size = None
        self.crc = None
        self.md5 = None
        self.sha1 = None
        self.status = None
        self.serial = None

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.name}")'


class GameNoIntro:
    """Class representing a game in No-Intro XML database."""

    def __init__(self):

        self.name = None
        self.description = None
        self.release_name = None
        self.region = None
        self.rom = None

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.name}")'


class GameMupen64Plus:
    """Class representing a game in mupen64plus INI file."""

    def __init__(self):

        self.good_name = None
        self.md5 = None
        self.CRC = None
        self.status = None
        self.rumble = None
        self.players = None
        self.counter_per_ops = None
        self.mem_pak = None
        self.ref_md5 = None
        self.save_type = None
        self.transfer_pak = None
        self.disable_extra_mem = None
        self.bio_pak = None
        self.si_dma_duration = None
        self.cheat_0 = None

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.good_name}")'


def from_mame_xml(path):
    """Parse given MAME XML database and iterate over its games"""

    tree = ElementTree.parse(path)
    root = tree.getroot()

    for sw_node in root.findall('software'):

        game = GameMame()
        game.description = sw_node.get('description')
        game.name = sw_node.attrib['name']
        game.clone_of = sw_node.attrib.get('cloneof')
        game.description = sw_node.get('description')
        game.year = sw_node.get('year')
        game.publisher = sw_node.get('publisher')

        rom_node = sw_node.find('part/dataarea/rom')
        rom = RomMame()
        rom.name = rom_node.get('name')
        rom.size = rom_node.get('size')
        rom.crc = rom_node.get('crc')
        rom.sha1 = rom_node.get('sha1')
        game.rom = rom

        yield game


def from_nointro_dat(path):
    """Parse given No-Intro database and iterate over its games"""

    tree = ElementTree.parse(path)
    root = tree.getroot()

    for game_node in root.findall('game'):

        game = GameNoIntro()
        game.name = game_node.attrib['name']
        game.description = game_node.get('description')

        rom_node = game_node.find('rom')
        rom = RomNoIntro()
        rom.name = rom_node.get('name')
        rom.size = rom_node.get('size')
        rom.crc = rom_node.get('crc')
        rom.md5 = rom_node.get('md5')
        rom.sha1 = rom_node.get('sha1')
        rom.status = rom_node.get('status')
        rom.serial = rom_node.get('serial')
        game.rom = rom

        yield game


def from_mupen64plus_ini(path):
    """Iterate over mupen64plus game found in given INI file.
    """
    with open(path, 'r') as fd:
        line_iter = (line
                     for line in fd.readlines()
                     if line and not line.startswith(';') and not line == "\n")

    cur_md5 = None

    # md5 to game
    games = {}

    for line in line_iter:

        # md5
        match_grp = re.match(r"^\[([A-F0-9]{32})\]$", line)

        if match_grp:

            # "close" currently parsed game before moving to the next
            if cur_md5 is not None:

                prev_game = games[cur_md5]
                yield prev_game

            cur_md5 = match_grp.group(1)
            assert cur_md5 not in games, cur_md5
            game = GameMupen64Plus()
            game.md5 = cur_md5
            games[cur_md5] = game
            continue

        # key/value parsing
        match_grp = re.match(r"^(.+)=(.+)$", line)

        if match_grp:
            key = match_grp.group(1)
            value = match_grp.group(2)
            game = games[cur_md5]
            if key == 'GoodName':
                game.good_name = value
            elif key == 'CRC':
                game.crc = value
            elif key == 'Status':
                game.status = int(value)
            elif key == 'Rumble':
                game.rumble = value
            elif key == 'CountPerOp':
                game.counter_per_ops = value
            elif key == 'Players':
                game.players = int(value)
            elif key == 'Mempak':
                game.mem_pak = value
            elif key == 'RefMD5':
                game.ref_md5 = value
            elif key == 'SaveType':
                game.save_type = value
            elif key == 'Transferpak':
                game.transfer_pak = value
            elif key == 'DisableExtraMem':
                game.disable_extra_mem = value
            elif key == 'Biopak':
                game.bio_pak = value
            elif key == 'SiDmaDuration':
                game.si_dma_duration = value
            elif key == 'Cheat0':
                game.cheat_0 = value
            else:
                print(f"Unknow key/value: '{key}'/{value}")
        else:
            print(f"Can't parse line: \"{line}\"")

    # "close" last game
    prev_game = games[cur_md5]
    yield prev_game


def export_as_mupen64plus_ini(games, path):
    """Write mupen64plus INI file for given games to given path destination
    """
    date = datetime.datetime.now()

    lines = ["; Mupen64Plus Rom Catalog",
             "; Generated by mupen64plus-ini-creator",
             "; Script coded by: narann",
             ";",
             f"; Total Rom Count: {len(games)}",
             date.strftime("; %a, %d %b %y %H:%M:%S %z"),
             ""]

    for game in sorted(games, key=lambda g: g.good_name):

        assert game == game

        lines += [f"[{game.md5}]",
                  f"GoodName={game.good_name}",
                  f"CRC={game.crc}"]

        if game.status:
            lines.append(f"Status={game.status}")

        if game.rumble:
            lines.append(f"Rumble={game.rumble}")

        if game.players:
            lines.append(f"Players={game.players}")

        if game.counter_per_ops:
            lines.append(f"CountPerOp={game.counter_per_ops}")

        if game.mem_pak:
            lines.append(f"Mempak={game.mem_pak}")

        if game.ref_md5:
            lines.append(f"RefMD5={game.ref_md5}")

        if game.save_type:
            lines.append(f"SaveType={game.save_type}")

        if game.transfer_pak:
            lines.append(f"Transferpak={game.transfer_pak}")

        if game.disable_extra_mem:
            lines.append(f"DisableExtraMem={game.disable_extra_mem}")

        if game.bio_pak:
            lines.append(f"Biopak={game.bio_pak}")

        if game.si_dma_duration:
            lines.append(f"SiDmaDuration={game.si_dma_duration}")

        if game.cheat_0:
            lines.append(f"Cheat0={game.cheat_0}")

        # separator line
        lines.append("")

    with open(path, 'w') as fd:
        fd.write("\n".join(lines))
