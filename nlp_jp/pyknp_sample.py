#-*- encoding: utf-8 -*-
from pyknp import Juman
import sys
import codecs

sys.stdin = codecs.getreader('utf_8')(sys.stdin)
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
# JUMAN++をsubprocessモードで使用
jumanpp = Juman(jumanpp=False)
result = jumanpp.analysis(u"ケーキを食べる")
for mrph in result.mrph_list():
    print(u"見出し:{0}".format(mrph.midasi))
