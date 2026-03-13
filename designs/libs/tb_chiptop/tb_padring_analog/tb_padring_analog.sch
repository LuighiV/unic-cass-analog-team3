v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 2110 -1440 2910 -1040 {flags=graph
y1=-0.51
y2=3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=3
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node="ibias
iout
net1
vdd"
color="4 7 12 17"
dataset=-1
unitx=1
logx=0
logy=0
rawfile=$netlist_dir/dc_hv_nmos.raw
autoload=1
sim_type=dc}
B 2 2110 -1040 2910 -640 {flags=graph
y1=1.6e-14
y2=8.5e-05
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=3
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=i(vmeas)
color=10
dataset=-1
unitx=1
logx=0
logy=0
}
N 710 -1380 1050 -1380 {lab=ibias}
N 1050 -1400 1050 -1380 {lab=ibias}
N 1050 -1480 1050 -1430 {lab=VDD}
N 1050 -1480 1190 -1480 {lab=VDD}
N 1190 -1480 1190 -1430 {lab=VDD}
N 1120 -1430 1150 -1430 {lab=ibias}
N 1120 -1430 1120 -1380 {lab=ibias}
N 1090 -1430 1120 -1430 {lab=ibias}
N 1050 -1380 1120 -1380 {lab=ibias}
N 1190 -1260 1190 -1230 {lab=#net1}
N 1190 -1200 1190 -1130 {lab=VSS}
N 1150 -1260 1150 -1200 {lab=#net1}
N 1150 -1260 1190 -1260 {lab=#net1}
N 1190 -1400 1190 -1260 {lab=#net1}
N 1080 -1200 1150 -1200 {lab=#net1}
N 1040 -1200 1040 -1130 {lab=VSS}
N 1040 -1340 1040 -1230 {lab=iout}
N 710 -1340 1040 -1340 {lab=iout}
N 1040 -1130 1190 -1130 {lab=VSS}
N 380 -960 380 -950 {lab=VSS}
N 380 -890 380 -870 {lab=GND}
N 380 -1080 380 -1030 {lab=VDD}
N 450 -980 450 -960 {lab=VSS}
N 380 -960 450 -960 {lab=VSS}
N 380 -970 380 -960 {lab=VSS}
N 540 -990 540 -960 {lab=iout1}
N 450 -1080 450 -1040 {lab=ibias}
N 540 -1080 540 -1050 {lab=VDD}
N 540 -900 540 -870 {lab=iout}
C {core_chiptop/padring_analog/user_project_wrapper.sym} 710 -680 0 0 {name=x1
lock=true}
C {sg13g2_pr/sg13_hv_pmos.sym} 1070 -1430 2 0 {name=M1
l=1u
w=10u
ng=1
m=5
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_hv_pmos.sym} 1170 -1430 2 1 {name=M2
l=1u
w=10u
ng=1
m=5
model=sg13_hv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 1170 -1200 0 0 {name=M3
l=1u
w=5u
ng=1
m=5
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_wire.sym} 1090 -1480 0 0 {name=p1 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 1190 -1130 0 0 {name=p2 sig_type=std_logic lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 1170 -1200 0 0 {name=M4
l=1u
w=5u
ng=1
m=5
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_wire.sym} 1190 -1130 0 0 {name=p3 sig_type=std_logic lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 1060 -1200 0 1 {name=M5
l=1u
w=5u
ng=1
m=5
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_wire.sym} 1040 -1130 0 1 {name=p4 sig_type=std_logic lab=VSS}
C {sg13g2_pr/sg13_lv_nmos.sym} 1060 -1200 0 1 {name=M6
l=1u
w=5u
ng=1
m=5
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_wire.sym} 1040 -1130 0 1 {name=p5 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 710 -1020 0 0 {name=p6 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 710 -980 0 0 {name=p7 sig_type=std_logic lab=VDD}
C {vsource.sym} 380 -1000 0 0 {name=V1 value=3 savecurrent=false}
C {gnd.sym} 380 -870 0 0 {name=l1 lab=GND}
C {vsource.sym} 380 -920 0 0 {name=V3 value=0 savecurrent=false}
C {lab_wire.sym} 380 -960 0 0 {name=p8 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 380 -1060 0 0 {name=p9 sig_type=std_logic lab=VDD}
C {isource.sym} 450 -1010 0 0 {name=I0 value=50u}
C {res.sym} 540 -1020 0 0 {name=R1
value=20k
footprint=1206
device=resistor
m=1}
C {lab_wire.sym} 710 -1380 0 0 {name=p10 sig_type=std_logic lab=ibias}
C {lab_wire.sym} 710 -1340 0 0 {name=p11 sig_type=std_logic lab=iout}
C {lab_wire.sym} 450 -1060 0 0 {name=p12 sig_type=std_logic lab=ibias}
C {lab_wire.sym} 540 -960 0 0 {name=p13 sig_type=std_logic lab=iout1}
C {devices/code_shown.sym} 140 -630 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOShv.lib mos_tt
.lib cornerMOSlv.lib mos_tt
.lib cornerRES.lib res_typ
.include diodes.lib
"}
C {devices/code_shown.sym} 500 -580 0 0 {name=NGSPICE only_toplevel=true 
value="
.options savecurrents
*.include dc_hv_nmos.save
.param temp=27
.control 
save all
op
write dc_hv_nmos.raw
set appendwrite
dc V1 0 3.0 0.01
write dc_hv_nmos.raw
.endc
"}
C {title.sym} 200 -40 0 0 {name=l2 author="Luighi Viton"}
C {lab_wire.sym} 710 -1460 0 0 {name=p14 sig_type=std_logic lab=VSS}
C {lab_wire.sym} 710 -1420 0 0 {name=p15 sig_type=std_logic lab=VDD}
C {lab_wire.sym} 540 -1070 0 0 {name=p16 sig_type=std_logic lab=VDD}
C {ammeter.sym} 540 -930 0 0 {name=Vmeas savecurrent=true spice_ignore=0}
C {lab_wire.sym} 540 -870 0 0 {name=p17 sig_type=std_logic lab=iout}
