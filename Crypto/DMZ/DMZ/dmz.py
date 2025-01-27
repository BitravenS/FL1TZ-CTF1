from time import sleep
from utils import (
    fprint,
    announcer,
    COLOR_RED,
    COLOR_GREEN,
    COLOR_BLUE,
    COLOR_RESET,
    COLOR_YELLOW,
)
from levels import lvl1, lvl2, lvl3, lvl4





def main():
    header()
    sleep(1)
    announcer("Warning! This is a Demilitarized Zone !", lower=False)
    sleep(0.3)
    announcer("Any and all access is strictly prohibited", upper=False, lower=False)
    sleep(0.3)
    announcer(
        "Zombie hunters are on the lookout, and will shoot on sight",
        lower=False,
        upper=False,
    )
    sleep(0.3)
    announcer("You have been warned....", upper=False)
    sleep(0.5)
    fprint("\n")
    lvl1()
    # lvl2()
    # lvl3()
    # lvl4()


if __name__ == "__main__":
    try:
        main()

    except ValueError as val:
        fprint(
            f"{COLOR_RED}The numbers aren't adding up... Make sure to submit signatures in Base64!{COLOR_RESET}"
        )
        exit(1)
