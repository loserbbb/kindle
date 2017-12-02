import os 


def getdata(source, filename):
    gen = os.walk(source)
    with open(filename, 'w') as f:
        for one in gen:
            path, _, namelist = one 
            for name in namelist:
                f.write('%s/%s||%s\n' % (path,name,name))
