sphere:
01: invert:1 shape:{128,128,1}, shift:{0,0,0}, radius:40, taper:0
02: invert:1 shape:{128,128,1}, shift:{0,0,0}, radius:41, taper:0
03: invert:1 shape:{256,256,1}, shift:{-127,0,0}, radius:108, taper:19
04: invert:1 shape:{100,100,100}, shift:{20,0,-20}, radius:30, taper:0
05: invert:1 shape:{100,100,100}, shift:{20,0,-20}, radius:20, taper:10

rectangle:
01: invert:0 shape:{512,512,1}, shift:{0,0,0}, radius:{50,51,1}, taper:0
02: invert:0 shape:{231,230,1}, shift:{-11,11,0}, radius:{50,51,1}, taper:0
03: invert:0 shape:{128,256,1}, shift:{12,10,0}, radius:{30,80,1}, taper:10
04: invert:0 shape:{128,128,64}, shift:{20,0,0}, radius:{30,80,5}, taper:10
05: invert:0 shape:{64,64,64}, shift:{0,-10,0}, radius:{10,10,15}, taper:15

cylinder:
01: invert:0 shape:{256,256,64}, shift:{0,0,0}, radius_xy:60, radius_z:20, taper:0
02: invert:0 shape:{128,128,128}, shift:{-11,11,0}, radius_xy:31, radius_z:45, taper:11
03: invert:0 shape:{80,91,180}, shift:{-6,0,10}, radius_xy:10, radius_z:50, taper:6

medfilt1:
1: shape={250,250,1}, window=3, mode=REFLECT
2: shape={250,250,1}, window=5, mode=ZERO
3: shape={150,150,150}, window=7, mode=REFLECT
4: shape={150,150,150}, window=9, mode=ZERO

medfilt2:
5: shape={250,250,1}, window=11, mode=REFLECT
6: shape={250,250,1}, window=9, mode=ZERO
7: shape={150,150,150}, window=7, mode=REFLECT
8: shape={150,150,150}, window=3, mode=ZERO

medfilt3:
9: shape={150,150,150}, window=5, mode=REFLECT
10: shape={150,150,150}, window=3, mode=ZERO

convolve1:
1: shape={251,250,1}, filter=31
2: shape={150,151,152}, filter=31

convolve2:
3: shape={251,250,1}, filter={17,9}
4: shape={150,151,152}, filter={17,9}

convolve3:
5: shape={150,151,152}, filter={3,3,3}
6: shape={150,151,152}, filter={5,5,5}
7: shape={150,151,152}, filter={5,3,3}

convolve separable 2D:
8: shape={251,250,1}, filter0=21, filter1=21
9: shape={251,250,1}, filter0=21
10: shape={251,250,1}, filter1=21

convolve separable 3D:
11: shape={150,151,152}, filter0=21, filter1=21, filter2=21
12: shape={150,151,152}, filter0=21, filter1=21
13: shape={150,151,152}, filter1=21, filter2=21
14: shape={150,151,152}, filter0=21, filter2=21
15: shape={150,151,152}, filter0=21
16: shape={150,151,152}, filter1=21
17: shape={150,151,152}, filter2=21
