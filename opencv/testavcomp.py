import coordmapping as cm

p = (308,0)
gustaf_p = cm.compensate_for_measured_error(p)
arvid_p = cm.get_weighted_compensation(p)

print 'Punkt in:', p
print 'Gustafs kompensation:', gustaf_p
print 'Arvids kompensation:', arvid_p
