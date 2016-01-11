'''
Created on 28. nov. 2015

@author: kga
'''


def prep_number(nr):
    nr = nr.replace("K","000")
    nr = nr.replace("k","000")
    nr = nr.replace("mill","000000")
    nr = nr.replace("MILL","000000")
    nr = nr.replace(" ","")
    nr = nr.replace(",","")
    nr = nr.replace(".","")
    
    return nr