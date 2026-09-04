# encoding=utf-8

import io

from rich.columns import Columns
from rich.console import Console

COLUMN_DATA = [
    "Ursus americanus",
    "American buffalo",
    "Bison bison",
    "American crow",
    "Corvus brachyrhynchos",
    "American marten",
    "Martes americana",
    "American racer",
    "Coluber constrictor",
    "American woodcock",
    "Scolopax minor",
    "Anaconda (unidentified)",
    "Eunectes sp.",
    "Andean goose",
    "Chloephaga melanoptera",
    "Ant",
    "Anteater, australian spiny",
    "Tachyglossus aculeatus",
    "Anteater, giant",
]


def render():
    console = Console(file=io.StringIO(), width=100, legacy_windows=False)

    console.rule("empty")
    empty_columns = Columns([])
    console.print(empty_columns)
    columns = Columns(COLUMN_DATA)
    columns.add_renderable("Myrmecophaga tridactyla")
    console.rule("optimal")
    console.print(columns)
    console.rule("optimal, expand")
    columns.expand = True
    console.print(columns)
    console.rule("column first, optimal")
    columns.column_first = True
    columns.expand = False
    console.print(columns)
    console.rule("column first, right to left")
    columns.right_to_left = True
    console.print(columns)
    console.rule("equal columns, expand")
    columns.equal = True
    columns.expand = True
    console.print(columns)
    console.rule("fixed width")
    columns.width = 16
    columns.expand = False
    console.print(columns)
    console.print()
    render_result = console.file.getvalue()
    print(render_result)
    print(repr(render_result))
    return render_result


def test_render():
    expected = "────────────────────────────────────────────── empty ───────────────────────────────────────────────\n───────────────────────────────────────────── optimal ──────────────────────────────────────────────\nUrsus americanus           American buffalo       Bison bison            American crow          \nCorvus brachyrhynchos      American marten        Martes americana       American racer         \nColuber constrictor        American woodcock      Scolopax minor         Anaconda (unidentified)\nEunectes sp.               Andean goose           Chloephaga melanoptera Ant                    \nAnteater, australian spiny Tachyglossus aculeatus Anteater, giant        Myrmecophaga tridactyla\n───────────────────────────────────────── optimal, expand ──────────────────────────────────────────\nUrsus americanus             American buffalo        Bison bison             American crow          \nCorvus brachyrhynchos        American marten         Martes americana        American racer         \nColuber constrictor          American woodcock       Scolopax minor          Anaconda (unidentified)\nEunectes sp.                 Andean goose            Chloephaga melanoptera  Ant                    \nAnteater, australian spiny   Tachyglossus aculeatus  Anteater, giant         Myrmecophaga tridactyla\n────────────────────────────────────── column first, optimal ───────────────────────────────────────\nUrsus americanus      American marten     Scolopax minor          Ant                       \nAmerican buffalo      Martes americana    Anaconda (unidentified) Anteater, australian spiny\nBison bison           American racer      Eunectes sp.            Tachyglossus aculeatus    \nAmerican crow         Coluber constrictor Andean goose            Anteater, giant           \nCorvus brachyrhynchos American woodcock   Chloephaga melanoptera  Myrmecophaga tridactyla   \n─────────────────────────────────── column first, right to left ────────────────────────────────────\nAnt                        Scolopax minor          American marten     Ursus americanus     \nAnteater, australian spiny Anaconda (unidentified) Martes americana    American buffalo     \nTachyglossus aculeatus     Eunectes sp.            American racer      Bison bison          \nAnteater, giant            Andean goose            Coluber constrictor American crow        \nMyrmecophaga tridactyla    Chloephaga melanoptera  American woodcock   Corvus brachyrhynchos\n────────────────────────────────────── equal columns, expand ───────────────────────────────────────\nChloephaga melanoptera                American racer                    Ursus americanus            \nAnt                                   Coluber constrictor               American buffalo            \nAnteater, australian spiny            American woodcock                 Bison bison                 \nTachyglossus aculeatus                Scolopax minor                    American crow               \nAnteater, giant                       Anaconda (unidentified)           Corvus brachyrhynchos       \nMyrmecophaga tridactyla               Eunectes sp.                      American marten             \n                                      Andean goose                      Martes americana            \n─────────────────────────────────────────── fixed width ────────────────────────────────────────────\nAnteater,        Eunectes sp.     Coluber          Corvus           Ursus americanus\naustralian spiny                  constrictor      brachyrhynchos                   \nTachyglossus     Andean goose     American         American marten  American buffalo\naculeatus                         woodcock                                          \nAnteater, giant  Chloephaga       Scolopax minor   Martes americana Bison bison     \n                 melanoptera                                                        \nMyrmecophaga     Ant              Anaconda         American racer   American crow   \ntridactyla                        (unidentified)                                    \n\n"
    print("--")
    print(expected)
    print("--")
    assert render() == expected


def test_columns_narrow_width_zero_division():
    # Console width equals column width with default padding (0, 1)
    console = Console(file=io.StringIO(), width=16, legacy_windows=False)
    console.print(Columns([f"file_{i:02d}.txt" for i in range(4)], width=16))
    assert (
        console.file.getvalue()
        == "file_00.txt     \nfile_01.txt     \nfile_02.txt     \nfile_03.txt     \n"
    )

    # Console width narrower than requested column width
    console = Console(file=io.StringIO(), width=10, legacy_windows=False)
    console.print(Columns(["item1", "item2"], width=16))
    assert "item1" in console.file.getvalue()
    assert "item2" in console.file.getvalue()

    # column_first=True when column count falls back to 1
    console = Console(file=io.StringIO(), width=16, legacy_windows=False)
    console.print(Columns(["a", "b", "c"], width=16, column_first=True))
    assert (
        console.file.getvalue()
        == "a               \nb               \nc               \n"
    )

    # Multi-column boundary without right padding: 16 + 1 + 16 = 33 fits 2 columns
    console = Console(file=io.StringIO(), width=33, legacy_windows=False)
    console.print(Columns(["col1", "col2", "col3", "col4"], width=16))
    assert (
        console.file.getvalue()
        == "col1             col2            \ncol3             col4            \n"
    )

    # Zero width and zero padding edge case
    console = Console(file=io.StringIO(), width=16, legacy_windows=False)
    console.print(Columns(["alpha", "beta"], width=0, padding=0))
    assert console.file.getvalue() == "…\n…\n"


if __name__ == "__main__":
    result = render()
    print(result)
    print(repr(result))
