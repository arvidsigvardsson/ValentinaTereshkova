import coordmapping as cm

dsts = [
    [112.5, 316],
    [294, 221.5],
    [348.6, 105.4],
    [410, 356.5],
    [564.6, 445.5],
    [475.8, 555]
]

for pt in range(0,6):
    coords = cm.bilat(400, dsts[pt][0], dsts[pt][1])
    print 'Punkt', pt + 1, 'har koordinaterna', coords

# print 'Kamerans position:', cm.bilat(400, 309.7, 385.0)
