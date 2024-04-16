# %%
import random
from pathlib import PurePath

# %%
__COLORS: tuple[str]
__SHADES: tuple[str]

__root = PurePath(__file__).parent

with open(__root.joinpath("colors.txt"), "rt") as f:
    __COLORS = tuple(e.strip() for e in f.readlines())

with open(__root.joinpath("shades.txt"), "rt") as f:
    __SHADES = tuple(e.strip() for e in f.readlines())


def draw(value: int, seed: int | float | str | bytes | bytearray | None = 42) -> str:
    NC, NS = len(__COLORS), len(__SHADES)
    random.seed(seed)
    __colors = random.sample(__COLORS, NC)
    __shades = random.sample(__SHADES, NS)
    color = __colors[value // NS % NC]
    shade = __shades[value % NS]
    return f"{color} {shade}"
