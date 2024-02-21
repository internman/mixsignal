import numpy as np
import matplotlib.pyplot as plt

class LogicDecision:
    def __init__(self, threshold=0.5):
        self.threshold = threshold
        
    def make_decision(self, input_value):
        if input_value >= self.threshold:
            return 1
        else:
            return 0



class ClockDivider:
    def __init__(self, divide_by_value):
        self.divide_by_value = divide_by_value
        self.counter = 0
        self.clock_out = 0
        self.last_clock_in = 0
    
    def update(self, clock_in):
        # Detect rising edge
        if clock_in == 1 and self.last_clock_in == 0:
            self.counter += 1
            if self.counter >= self.divide_by_value:
                self.counter = 0
                self.clock_out = 1
            else:
                self.clock_out = 0
        else:
            self.clock_out = 0
        self.last_clock_in = clock_in
        
    def get_output(self):
        return self.clock_out
    
# Generate a square wave as input signal
def generate_square_wave(freq, fs, duration):
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)
    return 0.5 * (1 + np.sign(np.sin(2 * np.pi * freq * t)))


# """
# Parameters
fs = 10000  # Sampling frequency for the square wave
freq = 100  # Frequency of the square wave should be low enough to see the divider effect
duration = 1  # Duration in seconds for which to simulate
divide_by_value = 72  # The value by which the clock will be divided

# Generate input square wave signal
input_signal = generate_square_wave(freq, fs, duration)

# Initialize clock divider
clock_divider = ClockDivider(divide_by_value)

# Simulate the clock divider with the input square wave
output_signal = []
for clock_in in input_signal:
    clock_divider.update(clock_in)
    output_signal.append(clock_divider.get_output())

# Plot the input and output signals
plt.figure(figsize=(10, 6))
plt.subplot(2, 1, 1)
plt.title('Input Square Wave')
plt.plot(np.arange(len(input_signal)) / fs, input_signal)
plt.ylim(-0.1, 1.1)

plt.subplot(2, 1, 2)
plt.title('Clock Divider Output')
plt.plot(np.arange(len(output_signal)) / fs, output_signal, drawstyle='steps-post')
plt.ylim(-0.1, 1.1)

plt.xlabel('Time [s]')
plt.tight_layout()
plt.show()
# """