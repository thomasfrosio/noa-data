lowpass_01: shape:{256,256,1}, cutoff:0, width=0
lowpass_02: shape:{256,256,1}, cutoff:0.5, width=0
lowpass_03: shape:{256,256,1}, cutoff:0.35, width=0.1
lowpass_04: shape:{512,256,1}, cutoff:0.2, width=0.3
lowpass_11: shape:{128,128,128}, cutoff:0, width=0
lowpass_12: shape:{128,128,128}, cutoff:0.5, width=0
lowpass_13: shape:{64,128,128}, cutoff:0.2, width=0.3

highpass_01: shape:{256,256,1}, cutoff:0, width=0
highpass_02: shape:{256,256,1}, cutoff:0.5, width=0
highpass_03: shape:{256,256,1}, cutoff:0.35, width=0.1
highpass_04: shape:{512,256,1}, cutoff:0.2, width=0.3
highpass_11: shape:{128,128,128}, cutoff:0, width=0
highpass_12: shape:{128,128,128}, cutoff:0.5, width=0
highpass_13: shape:{64,128,128}, cutoff:0.2, width=0.3

bandpass_01: shape:{256,256,1}, cutoff1:0.4, cutoff2:0.5 , width1=0, width2=0
bandpass_02: shape:{256,512,1}, cutoff1:0.3, cutoff2:0.45 , width1=0.3, width2=0.05
bandpass_03: shape:{128,128,1}, cutoff1:0.3, cutoff2:0.4 , width1=0.05, width2=0.05
bandpass_11: shape:{128,128,128}, cutoff1:0.2, cutoff2:0.45 , width1=0.1, width2=0.05
bandpass_12: shape:{64,128,128}, cutoff1:0.1, cutoff2:0.3 , width1=0, width2=0.1
