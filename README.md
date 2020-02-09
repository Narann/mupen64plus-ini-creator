# mupen64plus-ini-creator

Simple python script to ROM information from various sources and write them as new mupen64plus.ini file.

Works with NoIntro and MAME database file format.

## Example

This snippet get games present in NoIntro but missing in mupen64plus.ini:

```python
from itertools import chain

from  mupen64plus_ini_creator import (from_nointro_dat,
                                      from_mupen64plus_ini)

# parse and get NoIntro games by MD5 fingerprint (merge them all)
path = 'Nintendo - Nintendo 64 (BigEndian).dat'
path1 = 'Nintendo - Nintendo 64 (BigEndian) (Parent-Clone).dat'
path2 = 'Nintendo - Nintendo 64DD.dat'

nointro_games = {g.rom.md5: g
                 for g in chain(from_nointro_dat(path),
                                from_nointro_dat(path1),
                                from_nointro_dat(path2))}

print(f"No-Intro game count: {len(nointro_games)}")

# parse and get mupen64plus.ini games by MD5 fingerprint
path = 'mupen64plus-core/data/mupen64plus.ini'

m64p_ini_games = {g.md5: g
                  for g in from_mupen64plus_ini(path)}

print(f"mupen64plus ini game count: {len(m64p_ini_games)}")

# get MD5 present in NoIntro but missing in mupen64plus.ini
md5_nointro_only = set(nointro_games.keys()) - set(m64p_ini_games.keys())

for md5 in md5_nointro_only:

    # retrieve NoIntro game
    game = nointro_games[md5]

    print(game.name)
```

MAME parsing is supported but useless as it doesn't provide MD5 values.

```python
from  mupen64plus_ini_creator import from_mame_xml

path = 'n64.xml'

mame_games = list(from_mame_xml(path))

print(f"Mame game count: {len(mame_games)}")
```

And finally, you can export mupen64plus.ini file back:

```python
from  mupen64plus_ini_creator import (from_mupen64plus_ini,
                                      export_as_mupen64plus_ini)

path = 'mupen64plus-core/data/mupen64plus.ini'
out_path = 'mupen64plus-core/data/mupen64plus_reexport.ini'

m64p_ini_games = {g.md5: g
                  for g in from_mupen64plus_ini(path)}

export_as_mupen64plus_ini(m64p_ini_games, out_path)
```
