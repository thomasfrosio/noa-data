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
