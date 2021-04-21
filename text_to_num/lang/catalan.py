# MIT License

# Copyright (c) 2021 Joan Montané <jmontane@softcatala.org>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Dict, Optional, Set, Tuple

from .base import Language

#
# CONSTANTS
# Built once on import.
#

# Those words multiplies lesser numbers (see Rules)
# Exception: "(de) milliards" that can multiply bigger numbers ("milliards de milliards")
MULTIPLIERS = {
    "mil": 1000,
    "mils": 1000,
    "milió": 1000000,
    "milio": 1000000,
    "milions": 1000000,
    "bilio": 1000000000000,
    "bilions": 1000000000000
}


# Units are terminals (see Rules)
UNITS: Dict[str, int] = {
    word: value
    for value, word in enumerate(
        "u dos tres quatre cinc sis set vuit nou".split(), 1
    )
}
# Unit variants
UNITS["un"] = 1
UNITS["una"] = 1
UNITS["dues"] = 2
UNITS["huit"] = 8


# Single tens are terminals (see Rules)
STENS: Dict[str, int] = {
    word: value
    for value, word in enumerate(
        "deu onze dotze tretze catorze quinze setze disset divuit dinou".split(),
        10,
    )
}
#Stens variants
STENS["dèsset"] = 17
STENS["desset"] = 17
STENS["díhuit"] = 18
STENS["devuit"] = 18
STENS["dènou"] = 19
STENS["denou"] = 19



# Ten multiples
# Ten multiples may be followed by a unit only;
MTENS: Dict[str, int] = {
    word: value * 10
    for value, word in enumerate(
        "vint trenta quaranta cinquanta seixanta setanta vuitanta noranta".split(), 2
    )
}
#MTENS variants
MTENS["huitanta"] = 80

# Composites are tens already composed with terminals in one word.
# Composites are terminals.

COMPOSITES: Dict[str, int] = {
    "-i-".join((ten_word, unit_word)): ten_val + unit_val
    for ten_word, ten_val in MTENS.items()
    for unit_word, unit_val in UNITS.items()
    if ten_val == 20
}

COMPOSITES.update(
    {
        "-".join((ten_word, unit_word)): ten_val + unit_val
        for ten_word, ten_val in MTENS.items()
        for unit_word, unit_val in UNITS.items()
        if ten_val != 20
    }
)

# Ten multiples that can be combined with STENS
MTENS_WSTENS: Set[str] = set()

# "cent" has a special status (see Rules)
HUNDRED = {
    "cent": 100,
    "centes": 100,
    "dos-cents": 200,
    "dos-centes": 200,
    "dues-centes": 200,
    "tres-cents": 300,
    "tres-centes": 300,
    "quatre-cents": 400,
    "quatre-centes": 400,
    "cinc-cents": 500,
    "cinc-centes": 500,
    "sis-cents": 600,
    "sis-centes": 600,
    "set-cents": 700,
    "set-centes": 700,
    "vuit-cents": 800,
    "vuit-centes": 800,
    "nou-cents": 900,
    "nou-centes": 900,
}

#COMPOSITES: Dict[str, int] = {}

# All number words
NUMBERS = MULTIPLIERS.copy()
NUMBERS.update(UNITS)
NUMBERS.update(STENS)
NUMBERS.update(MTENS)
NUMBERS.update(HUNDRED)
NUMBERS.update(COMPOSITES)

RAD_MAP = {"primer": "un", "segon": "dos", "tercer": "tres", "quart": "quatre", "cinqu": "cinc", "nov": "nou", "des": "deu"}

class Catalan(Language):

    ISO_CODE = 'ca'
    MULTIPLIERS = MULTIPLIERS
    UNITS = UNITS
    STENS = STENS
    MTENS = MTENS
    MTENS_WSTENS = MTENS_WSTENS
    HUNDRED = HUNDRED
    NUMBERS = NUMBERS

    SIGN = {"més": "+", "menys": "-"}
    ZERO = {"zero"}
    DECIMAL_SEP = "coma"
    DECIMAL_SYM = ","

    AND_NUMS = {
        "u",
        "un",
        "una",
        "dos",
        "dues",
        "tres",
        "quatre",
        "cinc",
        "sis",
        "set",
        "vuit",
        "huit",
        "nou",
    }
    AND = "i"
    NEVER_IF_ALONE = {"un", "una"}

    # Relaxed composed numbers (two-words only)
    # start => (next, target)
    RELAXED: Dict[str, Tuple[str, str]] = {}

    def ord2card(self, word: str) -> Optional[str]:
        """Convert ordinal number to cardinal.

        Return None if word is not an ordinal or is better left in letters
        as is the case for first and second.
        """ 
        if word == "primer" or word == "primers" or word == "primera" or word == "primeres":
            ord_suff = True
            source = "un"
        elif word == "segon" or word == "segons" or word == "segona" or word == "segones":
            ord_suff = True
            source = "dos"
        elif word == "tercer" or word == "tercers" or word == "tercera" or word == "terceres":
            ord_suff = True
            source = "tres"
        elif word == "quart" or word == "quarts" or word == "quarta" or word == "quartes":
            ord_suff = True
            source = "quatre"
        elif word.endswith("ens") or word.endswith("ena"):
            ord_suff = True
            source = word[:-3]
        elif word.endswith("enes") or word.endswith("èsim"):
            ord_suff = True
            source = word[:-4]
        elif word.endswith("èsims") or word.endswith("èsima"):
            ord_suff = True
            source = word[:-5]
        elif word.endswith("èsimes"):
            ord_suff = True
            source = word[:-6]
        elif word.endswith("è") or word.endswith("é"):
            ord_suff = True
            source = word[:-1]
            if source == "dihuit": source = "divuit"
        else: ord_suff = False

        if ord_suff == False:
           return None

        if source in RAD_MAP:
            source = RAD_MAP[source]
        if source not in self.NUMBERS:
            source = source + "e"
            if source not in self.NUMBERS:
                return None

        return source

    def num_ord(self, digits: str, original_word: str) -> str:
        """Add suffix to number in digits to make an ordinal"""
        if original_word.endswith("a"):
            sf = "a"
        elif original_word.endswith("er"):
            sf = "r"
        elif original_word.endswith("ers"):
            sf = "rs"
        elif original_word.endswith("on"):
            sf = "n"
        elif original_word.endswith("ons"):
            sf = "ns"
        elif original_word.endswith("rt"):
            sf = "t"
        elif original_word.endswith("rts"):
            sf = "ts"
        elif original_word.endswith("ens"):
            sf = "ns"
        elif original_word.endswith("enes"):
            sf = "es"
        elif original_word.endswith("é"):
            sf = "é"
        elif original_word.endswith("s"):
            sf = "s"
        else: sf = "è"

        return f"{digits}{sf}"

    def normalize(self, word: str) -> str:
        return word.replace("dugues", "dues")
