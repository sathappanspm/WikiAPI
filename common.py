#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
    *.py: Description of what * does.
    Last Modified:Wed Dec 19 07:12:38 2012
"""

__author__ = "Sathappan Muthiah"
__email__ = "sathap1@vt.edu"
__version__ = "0.0.1"


commonCold = eval(open('commonCold-collocations.txt', 'r').read())
flu = eval(open('flu-collocations.txt', 'r').read())
influenza = eval(open('influenza-collocations.txt', 'r').read())


def get3Common():
    common = []
    for k in commonCold:
        if k in influenza or (k[1], k[0]) in influenza:
            if k in flu or (k[1], k[0]) in flu:
                common.append(k)
    return common


def get2Common(A, B):
    common = []
    for k in A:
        if k in B or (k[1], k[0]) in B:
            common.append(k)
    return common


def getUnique(A, AB, AC):
    '''unique elements of A,
    '''
    unique = []
    for k in A:
        if k not in AB and (k[1], k[0]) not in AB:
            if k not in AC and (k[1], k[0]) not in AC:
                unique.append(k)
    return unique


if __name__ == '__main__':
    allCommon = get3Common()
    coldFlu = get2Common(commonCold, flu)
    influenzaFlu = get2Common(influenza, flu)
    coldInfluenza = get2Common(commonCold, influenza)

    uniqueCold = getUnique(commonCold, coldInfluenza, coldFlu)
    uniqueInfluenza = getUnique(influenza, coldInfluenza, influenzaFlu)
    uniqueFlu = getUnique(flu, coldFlu, influenzaFlu)
    out = open('commons/coldFlu.txt', 'w')
    out.write(str(coldFlu))
    out.close()
    out = open('commons/coldInfluenza.txt', 'w')
    out.write(str(coldInfluenza))
    out.close()
    out = open('commons/influenzaFlu.txt', 'w')
    out.write(str(influenzaFlu))
    out.close()
    out = open('commons/all3.txt', 'w')
    out.write(str(allCommon))
    out.close()
    out = open('commons/uniqueCold', 'w')
    out.write(str(uniqueCold))
    out.close()
    out = open('commons/uniqueFlu', 'w')
    out.write(str(uniqueFlu))
    out.close()
    out = open('commons/uniqueInfluenza', 'w')
    out.write(str(uniqueInfluenza))
    out.close()
