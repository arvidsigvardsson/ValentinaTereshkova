import coordmapping as cm

dsts = [
    [61.0, 351.7],
    [242.7, 242.0],
    [367.0, 67.7],
    [359.0, 363.3],
    [571.7, 454.5],
    [435.5, 566.7]
]

for pt in range(0,6):
    coords = cm.bilat(400, dsts[pt][0], dsts[pt][1])
    print 'Punkt', pt + 1, 'har koordinaterna', coords

print 'Kamerans position:', cm.bilat(400, 309.7, 385.0)
