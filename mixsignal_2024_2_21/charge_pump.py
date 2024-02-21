import numpy as np

class LogicDecision:
    def __init__(self, threshold=0.5):
        self.threshold = threshold
        
    def make_decision(self, input_value):
        if input_value >= self.threshold:
            return 1
        else:
            return 0
            

"""
decision_maker = LogicDecision()
input_value = 0.7
decision = decision_maker.make_decision(input_value)
print(f"Input: {input_value}, Decision: {decision}")

"""
            
# ----------------------------------------------------------------------------------------
class amplifier:
    def __init__(self):
        self.output = 0
        
    def amp(self,input):
        return 0.0002*input
        

"""
a = amplifier(10)
print(f"{a.output}")
"""
# ----------------------------------------------------------------------------------------


class CurrentSum:
    def __init__(self):
        self.leakage = 0
    
    def update(self,input_up,input_down):
        self.output = input_up - input_down + self.leakage
        return self.output
        
"""
current_sum = CurrentSum()
output = current_sum.update(2, 3)
print(f"Output: {output}")
"""


class IntegratedChargePump:
    def __init__(self):
        self.LogicOut_R = LogicDecision()
        self.LogicOut_F = LogicDecision()
        self.ampout_R = amplifier()
        self.ampout_F = amplifier()
        self.CurrentSumOut = CurrentSum()
        
    def Charge_Pump(self, reference, feedback):
        tmp_LogicOut_R = self.LogicOut_R.make_decision(reference)
        tmp_LogicOut_F = self.LogicOut_F.make_decision(feedback)
        tmp_ampout_R = self.ampout_R.amp(tmp_LogicOut_R)
        tmp_ampout_F = self.ampout_F.amp(tmp_LogicOut_F)
        tmp_CurrentSumOut = self.CurrentSumOut.update(tmp_ampout_R,tmp_ampout_F)
        
        return tmp_CurrentSumOut


asd = 1


