Noa::Memory::resize()
=====================

resize_01: ishape:{64,64,1}, oshape:{81,59,1}, bleft:{11,-5,0}, bright:{6,0,0}, mode:VALUE, value:5 batch:3
resize_02: ishape:{127,128,1}, oshape:{108,130,1}, bleft:{-20,1,0}, bright:{1,1,0}, mode:ZERO, value:5 batch:1
resize_03: ishape:{63,64,1}, oshape:{255,256,1}, bleft:{192,100,0}, bright:{0,92,0}, mode:PERIODIC, value:0 batch:1
resize_04: ishape:{127,128,1}, oshape:{68,128,1}, bleft:{-50,100,0}, bright:{-9,-100,0}, mode:CLAMP, value:0 batch:2
resize_05: ishape:{256,256,1}, oshape:{256,300,1}, bleft:{0,4,0}, bright:{0,40,0}, mode:MIRROR, value:0 batch:2

resize_06: ishape:{64,64,64}, oshape:{81,59,38}, bleft:{11,-5,-30}, bright:{6,0,4}, mode:VALUE, value:1 batch:1
resize_07: ishape:{127,128,66}, oshape:{108,130,66}, bleft:{-20,1,0}, bright:{1,1,0}, mode:ZERO, value:5 batch:1
resize_08: ishape:{63,64,65}, oshape:{255,256,100}, bleft:{192,100,25}, bright:{0,92,10}, mode:PERIODIC, value:0 batch:1
resize_09: ishape:{127,128,1}, oshape:{68,128,5}, bleft:{-50,128,4}, bright:{-9,-128,0}, mode:CLAMP, value:0 batch:1
resize_10: ishape:{256,256,30}, oshape:{256,300,1}, bleft:{0,4,-10}, bright:{0,40,-19}, mode:MIRROR, value:0 batch:1

resize_11: ishape:{64,64,1}, oshape:{81,59,1}, mode:VALUE, value:5 batch:3
resize_12: ishape:{64,64,64}, oshape:{81,59,40}, mode:VALUE, value:1 batch:1
resize_13: ishape:{127,128,1}, oshape:{108,130,1}, mode:ZERO, value:5 batch:1
resize_14: ishape:{127,128,30}, oshape:{130,128,1}, mode:ZERO, value:5 batch:1
resize_15: ishape:{80,1,1}, oshape:{80,80,40}, mode:CLAMP, value:0 batch:1
resize_16: ishape:{1,50,50}, oshape:{20,31,5}, mode:CLAMP, value:0 batch:1
resize_17: ishape:{30,30,30}, oshape:{90,90,90}, mode:PERIODIC, value:0 batch:1
resize_18: ishape:{64,128,32}, oshape:{128,256,32}, mode:MIRROR, value:0 batch:1

resize_19: ishape:{64,64,1}, oshape:{81,59,1}, bleft:{11,-5,0}, bright:{6,0,0}, mode:NOTHING, value:0 batch:3
resize_20: ishape:{127,128,1}, oshape:{68,128,5}, bleft:{-50,100,4}, bright:{-9,-100,0}, mode:NOTHING, value:0 batch:1

Noa::Memory::extract(), insert()
================================

extract_10, extract_11, extract_12, extract_13, extract_14, insert_1:
ishape:{512,513,1}, subshape:{62,63,1}, subcenters:{30,31,0},{500,500,0},{128,32,0},{350,451,0},{512,0,0}, subcount:5, mode:VALUE, value:3.5

extract_20, extract_21, extract_22, insert_2:
ishape:{256,255,50}, subshape:{55,60,1}, subcenters:{0,0,0},{128,32,24},{0,255,0}, subcount:3, mode:NOTHING, value:3

extract_30, extract_31, extract_32, insert_3:
ishape:{128,127,126}, subshape:{40,42,43}, subcenters:{30,31,20},{127,126,125},{64,117,120}, subcount:3, mode:ZERO, value:5
