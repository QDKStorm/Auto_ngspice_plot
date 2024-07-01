.title Active DC Circuit
R1 1 2 4k
R2 3 2 4k
R3 1 NR3 2k
VI NR3 0 0
R4 3 0 3k
VS1 1 3 25
IS1 3 2 3m
IS2 0 1 10m
IS3 0 2 5m

.control
op
print I(vi)
* print v(1,2)
.endc
.end