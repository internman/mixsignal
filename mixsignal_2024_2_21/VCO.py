class NOT:
    def __init__(self,input):
        self.input = input
        
    def output(self):
        return int(not self.input)

"""
inputs = [0, 1]
for input in inputs:
    a = NOT(input)
    print(f"{a.output()}")
"""

# this part I have some doubt, the test result is fine, but I'm not sure I understand it, and is it necessary or not
class PulseDelay:
    def __init__(self, sample_rate, delay_time):
        self.sample_rate = sample_rate
        self.delay_time = delay_time
        # Calculate the number of samples for the delay
        self.delay_samples = int(delay_time / sample_rate)
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
deadband_compensation = 1e-10
pulse_delay = PulseDelay(sample_rate, deadband_compensation)
input_signals = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]  # Example signal
for signal in input_signals:
    delayed_signal = pulse_delay.delay(signal)
    print(delayed_signal)
"""


class HalfPeriodCalculator:
    def __init__(self, freq, kvco_or_vcof_f):
        self.freq = freq
        self.kvco_or_vcof_f = kvco_or_vcof_f

    def half_period(self, vin):
        nf = len(self.freq)
        nk = len(self.kvco_or_vcof_f)
        del_ = None

        if nf > 1 and nk == nf:  # Frequency vs. voltage
            direction = -1 if self.kvco_or_vcof_f[-1] < self.kvco_or_vcof_f[0] else 1
            if direction * vin <= direction * self.kvco_or_vcof_f[0]:
                del_ = 0.5 / self.freq[0]
            elif direction * vin >= direction * self.kvco_or_vcof_f[-1]:
                del_ = 0.5 / self.freq[-1]
            else:
                k = 0
                for indx in range(nk - 1):
                    if (direction * vin >= direction * self.kvco_or_vcof_f[indx] and
                       direction * vin < direction * self.kvco_or_vcof_f[indx + 1]):
                        k = indx
                        break
                del_ = 0.5 / (self.freq[k] * (self.kvco_or_vcof_f[k + 1] - vin) /
                              (self.kvco_or_vcof_f[k + 1] - self.kvco_or_vcof_f[k]) +
                              self.freq[k + 1] * (vin - self.kvco_or_vcof_f[k]) /
                              (self.kvco_or_vcof_f[k + 1] - self.kvco_or_vcof_f[k]))

        elif nf == 1 and nk == 1:  # Voltage sensitivity
            del_ = 0.5 / (self.freq[0] + self.kvco_or_vcof_f[0] * vin)
            if del_ < 0:
                raise ValueError('VCO output frequency is negative.')

        if del_ is None:
            raise ValueError('Invalid input parameters.')

        return del_

"""
# Example usage:
freq = [1.8e9]  # Example frequency array
kvco_or_vcof_f = [70e6]  # Example VCO gain or VCO frequency array
vin = 2.0  # Example voltage input

calc = HalfPeriodCalculator(freq, kvco_or_vcof_f)
delay = calc.half_period(vin)
print(f"Calculated delay: {delay}")
"""