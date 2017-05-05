import coordmapping as cm

dsts = [
    [54, 354.5],
    [229.5, 251.5],
    [383, 29.2],
    [364.5, 412],
    [605.5, 479.4],
    [473.2, 604.5],
]

for pt in range(0,6):
    coords = cm.bilat(400, dsts[pt][0], dsts[pt][1])
    print 'Punkt', pt + 1, 'har koordinaterna', coords

print 'Centrum:', cm.bilat(400, 281.5, 428.5)
