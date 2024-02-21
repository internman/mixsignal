import numpy as np


class LogicDecision:
    def __init__(self, threshold=0.5):
        self.threshold = threshold
        
    def make_decision(self, input_value):
        if input_value >= self.threshold:
            return 1
        else:
            return 0
            

class DFlipFlop:
    
    def __init__(self):
        self.q = 0  # Output initially 0
        self.prev_q = 0  # Previous state of the clock


    def update(self, CLK, CLR):   # 在matlab里是 !CLR, 但是感叹号取名字不太好，这里就直接是CLR
        if CLR == 0:
            self.q = 0
        elif CLR != 0:
            if CLK == 1:
                self.q = 1
            elif CLK == 0:
                self.q = self.prev_q
            
        # Update the previous clock state
        self.prev_q = self.q
        
        return self.q

    
"""
# 验证 Dflipflop
dff = DFlipFlop()
input_signals = [(0, 0), (0, 1), (1, 0), (1, 1),(0,1),(1,1),(1,0),(0,1),(1,1),(0,1)] 

for clk, clr in input_signals:
    print(f"CLK: {clk}, CLR: {clr}, Q: {dff.update(clk, clr)}")
"""
    
# variable pulse delay and ANAD gate  ------------------------------------------------------------------------


class NAND:
        
    def output(self,input_up,input_down):
        self.input_up = input_up
        self.input_down = input_down
        return int(not (self.input_up and self.input_down))

"""
inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
for input_up, input_down in inputs:
    a = NAND(input_up, input_down)
    print(f"{a.output()}")
"""

# ----------------------------------------------------------------------------------

# this part I have some doubt, the test result is fine, but I'm not sure I understand it, and is it necessary or not
class PulseDelay:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.delay_time = 1e-10
        # Calculate the number of samples for the delay
        self.delay_samples = int(self.delay_time / self.sample_rate)
        # Initialize the queue with zeros
        self.queue = [0] * self.delay_samples
        
    def delay(self, input_signal):
        # Add the new signal to the queue
        self.queue.append(input_signal)
        # The output is the oldest signal in the queue
        output_signal = self.queue.pop(0)
        return output_signal

"""
sample_rate = 1e-9
pulse_delay = PulseDelay(sample_rate)
# input_signals = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]  # Example signal
input_signals = np.array([0., 1., 1., 1., 1., 1., 1., 1., 1., 1.])  # Example signal
for signal in input_signals:
    delayed_signal = pulse_delay.delay(signal)
    print(delayed_signal)
"""

# ----------------------------------------------------------------------------------


class IntegratedPhaseDetector:
    def __init__(self, sample_rate):
        self.sample_rate = sample_rate
        self.LogicOut_R = LogicDecision()
        self.LogicOut_F = LogicDecision()
        self.DFlipFlopout_CLK_R = DFlipFlop()
        self.DFlipFlopout_CLK_F = DFlipFlop()
        self.Init_CLR = 1
        self.NAND_out = NAND()
        self.PulseDelay_out = PulseDelay(self.sample_rate)
        
    def detect_phase(self, reference, feedback):
        tmp_LogicOut_R = self.LogicOut_R.make_decision(reference)
        tmp_LogicOut_F = self.LogicOut_F.make_decision(feedback)
        tmp_DFlipFlopout_QR = self.DFlipFlopout_CLK_R.update(tmp_LogicOut_R, self.Init_CLR)
        tmp_DFlipFlopout_QF = self.DFlipFlopout_CLK_F.update(tmp_LogicOut_F, self.Init_CLR)
        tmp_NAND_out = self.NAND_out.output(tmp_DFlipFlopout_QR,tmp_DFlipFlopout_QF)
        tmp_PulseDelay_out = self.PulseDelay_out.delay(tmp_NAND_out)
        self.Init_CLR = tmp_PulseDelay_out
        
        return tmp_DFlipFlopout_QR, tmp_DFlipFlopout_QF
    
        
        
        
        

        



