import numpy as np

def test():
    v = np.array(([3],[14]))
    m = np.array(([2,0],[0,2]))
    v2 = np.matmul(m, v)
    print np.array_str(np.add(v,v2))

