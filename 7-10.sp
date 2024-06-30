* 7-10
V1 1 2 DC 9V
I1 1 3 3mA
R1 2 3 1k
C1 3 0 25uF
R2 3 0 2k
S1 0 1 4 0 switchmodel
V2 4 0 PULSE(0 5 -1 0 0 1 0 1)
.model switchmodel sw vt=1 vh=0.2 ron=1m roff=1G

.tran 1ms 1s
.control
run
plot v(3)
.endc
.end