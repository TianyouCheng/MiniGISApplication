from Function import *

def create_map(dbm:DBM):
    map = Map()
    return map

if __name__=='__main__':
    import re
    s='aaaa'
    match=re.match(r'^aa(.*)?(b)?$',s)
    print(match)
    if match:
        print(match.group(2))