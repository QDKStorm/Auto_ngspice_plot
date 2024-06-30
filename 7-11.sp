.title voltage divider netlist
V1 1 0 DC 1V
R1 1 2 50
I1 1 2 20mA
L1 2 3 0.2H
R2 3 4 50
V2 4 5 DC 0V
R3 5 0 100
S1 2 5 6 0 switchmodel
V3 6 0 PULSE(5 0 -0.5 0 0 0.5 0 1)
.model switchmodel sw vt=1 vh=0.2 ron=1m roff=1G

.tran 100us 500ms
.control
run
plot i(V2)
.endc
.end