# file that contains the dataclass Move and a list of all possible moves that a Rakimon may use

from dataclasses import dataclass


@dataclass()
class Move:
    name: str  # the name of the move
    type: str  # name of the rect where the TP starts
    power: int  # the power of the move
    pp: int  # number of power points
    effect: str  # eventual effect of the move


# now with dress a list of moves :

GRIFFE = Move(name="griffe", type='normal', power=30, pp=40, effect=None)
CHARGE = Move(name="charge", type='normal', power=40, pp=40, effect=None)
INTIMIDATION = Move(name="intimidation", type='normal', power=0, pp=30, effect='lower_attack')
DIVERSION = Move(name="diversion", type='normal', power=0, pp=30, effect="lower_def")
# some default move when we want to click nothing :(
NO = Move(name="", type=None, power=None, pp=None, effect=None)

# TODO : a list of all existing effects ?
