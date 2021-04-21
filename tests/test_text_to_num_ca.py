# MIT License

# Copyright (c) 2018-2019 Groupe Allo-Media

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


"""
Test the ``text_to_num`` library.
"""
from unittest import TestCase
from text_to_num import alpha2digit, text2num
import logging


class TestTextToNumES(TestCase):
    def test_text2num(self):
        self.assertEqual(text2num("zero", "ca"), 0)
        self.assertEqual(text2num("un", "ca"), 1)
        self.assertEqual(text2num("nou", "ca"), 9)
        self.assertEqual(text2num("deu", "ca"), 10)
        self.assertEqual(text2num("onze", "ca"), 11)
        self.assertEqual(text2num("dinou", "ca"), 19)
        self.assertEqual(text2num("vint", "ca"), 20)
        self.assertEqual(text2num("vint-i-dues", "ca"), 22)
        self.assertEqual(text2num("trenta", "ca"), 30)
        self.assertEqual(text2num("trenta-u", "ca"), 31)
        self.assertEqual(text2num("trenta-dos", "ca"), 32)
        self.assertEqual(text2num("trenta-huit", "ca"), 38)
        self.assertEqual(text2num("noranta-nou", "ca"), 99)
        self.assertEqual(text2num("cent", "ca"), 100)
        self.assertEqual(text2num("cent u", "ca"), 101)
        self.assertEqual(text2num("dues-centes", "ca"), 200)
        self.assertEqual(text2num("dues-centes una", "ca"), 201)
        self.assertEqual(text2num("mil", "ca"), 1000)
        self.assertEqual(text2num("mil un", "ca"), 1001)
        self.assertEqual(text2num("dos mil", "ca"), 2000)
        self.assertEqual(text2num("dos mil noranta-nou", "ca"), 2099)
        self.assertEqual(text2num("nou mil nou-cents noranta-nou", "ca"), 9999)
        self.assertEqual(text2num("nou-cents noranta-nou mil nou-cents noranta-nou", "ca"),
                         999999)
        long_text = "nou-cents noranta-nou mil nou-cents noranta-nou milions nou-cents noranta-nou mil nou-cents noranta-nou"
        self.assertEqual(text2num(long_text, "ca"), 999999999999)

        self.assertEqual(alpha2digit("un coma un", "ca"), '1,1')
        self.assertEqual(alpha2digit("u coma quatre-cents u", "ca"), '1,401')

        #FIXME: self.assertEqual(alpha2digit("zero coma cinc", "ca"), '0,5')

        test1 = "cinquanta-tres mil vint milions dos-cents quaranta-tres mil set-cents vint-i-quatre"
        self.assertEqual(text2num(test1, "ca"), 53020243724)

        test2 = (
            "cinquanta-un milions cinc-cents setanta-vuit mil tres-cents dos"
        )
        self.assertEqual(text2num(test2, "ca"), 51578302)

        test3 = "huitanta-cinc"
        self.assertEqual(text2num(test3, "ca"), 85)

        test4 = "vuitanta-un"
        self.assertEqual(text2num(test4, "ca"), 81)

        self.assertEqual(text2num("quinze", "ca"), 15)
        self.assertEqual(text2num("cent quinze", "ca"), 115)
        self.assertEqual(text2num("setanta-cinc mil", "ca"), 75000)
        self.assertEqual(text2num("mil nou-cents vint", "ca"), 1920)

    def test_text2num_exc(self):
        self.assertRaises(ValueError, text2num, "mil mil dos-cents", "ca")
        self.assertRaises(ValueError, text2num, "seixanta quinze", "ca")
        self.assertRaises(ValueError, text2num, "seixanta cent", "ca")

    def test_text2num_zeroes(self):
        self.assertEqual(text2num("zero", "ca"), 0)
        self.assertEqual(text2num("zero vuit", "ca"), 8)
        self.assertEqual(text2num("zero zero cent vint-i-cinc", "ca"), 125)
        self.assertRaises(ValueError, text2num, "cinc zero", "ca")
        self.assertRaises(ValueError, text2num, "cinquanta zero tres", "ca")
        self.assertRaises(ValueError, text2num, "cinquanta-tres zero", "ca")

    def test_alpha2digit_integers(self):
        source = "vint-i-cinc vaques, dotze gallines i cent vint-i-cinc kg de patates."
        expected = "25 vaques, 12 gallines i 125 kg de patates."
        self.assertEqual(alpha2digit(source, "ca"), expected)

        source = "mil dos-cents seixanta-sis dòlars."
        expected = "1266 dòlars."
        self.assertEqual(alpha2digit(source, "ca"), expected)

        source = "un dos tres quatre vint quinze"
        expected = "1 2 3 4 20 15"
        self.assertEqual(alpha2digit(source, "ca"), expected)

        source = "vint-i-un, trenta-un."
        expected = "21, 31."
        self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_relaxed(self):
        source = "un dos tres quatre trenta cinc."
        expected = "1 2 3 4 35."
        self.assertEqual(alpha2digit(source, "ca", relaxed=True), expected)

        source = "un dues tres quatre vint, cinc."
        expected = "1 2 3 4 20, 5."
        self.assertEqual(alpha2digit(source, "ca", relaxed=True), expected)

        source = "trenta-quatre == trenta quatre"
        expected = "34 == 34"
        self.assertEqual(alpha2digit(source, "ca", relaxed=True), expected)

    def test_alpha2digit_formal(self):
        source = "més trenta-tres nou seixanta zero sis dotze vint-i-u"
        expected = "+33 9 60 06 12 21"
        self.assertEqual(alpha2digit(source, "ca"), expected)

        source = "zero nou seixanta zero sis dotze vint-i-u"
        expected = "09 60 06 12 21"
        self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_and(self):
        source = "cinquanta seixanta trenta i onze"
        expected = "50 60 30 i 11"
        self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_alpha2digit_zero(self):
        source = "tretze mil zero noranta"
        expected = "13000 090"
        self.assertEqual(alpha2digit(source, "ca"), expected)

        self.assertEqual(alpha2digit("zero", "ca"), "0")

    def test_alpha2digit_decimals(self):
        source = (
            "dotze coma noranta-nou, cent vint coma zero cinc,"
            " u coma dos-cents trenta-sis, un coma dos tres sis."
        )
        expected = "12,99, 120,05, 1,236, 1,2 3 6."
        self.assertEqual(alpha2digit(source, "ca"), expected)

        self.assertEqual(alpha2digit("coma quinze", "ca"), "0,15")
        #FIXME: self.assertEqual(alpha2digit("zero coma quinze", "ca"), "0,15")  # TODO

    def test_alpha2digit_signed(self):
        source = "Tenim vint graus dins i menys quinze fora."
        expected = "Tenim 20 graus dins i -15 fora."
        #FIXME: expected = "Tenim +20 graus dins i -15 fora."
        self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_one_as_noun_or_article(self):
        source = "Un moment! trenta-un gats. Un dos tres quatre!"
        expected = "Un moment! 31 gats. 1 2 3 4!"
        self.assertEqual(alpha2digit(source, "ca"), expected)
        # End of segment
        source = "Ni un. U un. Trenta-un"
        expected = "Ni un. 1 1. 31"
        self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_accent(self):
        self.assertEqual(text2num("un milió", "ca"), 1000000)
        self.assertEqual(text2num("un milio", "ca"), 1000000)
        self.assertEqual(alpha2digit("Un milió", "ca"), "1000000")
        self.assertEqual(alpha2digit("Un milio", "ca"), "1000000")

    def test_second_as_time_unit_vs_ordinal(self):
        source = "Un segon per favor! Vint-i-dosè és diferent que vint segons."
        expected = "Un segon per favor! 22è és diferent que 20 segons."
        #FIXME: self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_alpha2digit_ordinals(self):
        source = (
            "Cinquè quart segon vint-i-unè centè cent unè."
        )
        expected = "5è 4t segon 21è 100è 101è."
        self.assertEqual(alpha2digit(source, "ca"), expected)

    def test_alpha2digit_ordinals_gender_and_number(self):
        source = "Ha quedat cinquè sisè nové huitè"
        expected = "Ha quedat 5è 6è 9é 8è" 
        self.assertEqual(alpha2digit(source, "ca"), expected)
        source = "Ha quedat primer"
        expected = "Ha quedat 1r"
        #FIXME: self.assertEqual(alpha2digit(source, "ca"), expected)
        source = "Han quedat segons"
        expected = "Han quedat 2ns"
        #FIXME: self.assertEqual(alpha2digit(source, "ca"), expected)
        source = "Ha quedat tercera"
        expected = "Ha quedat 3a"
        #FIXME: self.assertEqual(alpha2digit(source, "ca"), expected)
        source = "Ha quedat quart"
        expected = "Ha quedat 4t"
        self.assertEqual(alpha2digit(source, "ca"), expected)
        source = "Han quedat cinquè, nové i dihuitè"
        expected = "Han quedat 5è, 9é i 18è"
        self.assertEqual(alpha2digit(source, "ca"), expected)

