# for a non-real-time simulation, this may not be necessary. It can be reconsidered for addition in future designs

# class ConvertSampleTime:
#     def __init__(self):
import numpy as np
import matplotlib.pyplot as plt
        
class SecondOrderLoopFilter:
    def __init__(self, C1, C2, R, fs):
        self.C1 = C1
        self.C2 = C2
        self.R = R
        self.fs = fs  # Sampling frequency
        self.V1 = 0  # Voltage across C1
        self.V2 = 0  # Voltage across C2

    def step(self, charge_pump_output):
        # Discrete integration for each capacitor
        dV1 = charge_pump_output - self.V1 / (self.R * self.C1)
        self.V1 += dV1 / self.fs

        dV2 = (self.V1 - self.V2) / (self.C2 * self.R)
        self.V2 += dV2 / self.fs

        # The output of the filter is the voltage across C2
        return self.V2
    

"""
# Parameters for the filter
C1 = 1e-12  # Farads
C2 = 2e-12  # Farads
R = 40000   # Ohms
fs = 1e9    # Hz, the sampling frequency

# Initialize the loop filter
loop_filter = SecondOrderLoopFilter(C1, C2, R, fs)

# Simulate the charge pump output (for example purposes, let's use a square wave)
duration = 1e-6  # seconds
t = np.arange(0, duration, 1/fs)
charge_pump_output = np.sign(np.sin(2 * np.pi * 1e6 * t))  # 1 MHz square wave

# Apply the loop filter to the charge pump output
filtered_output = np.array([loop_filter.step(x) for x in charge_pump_output])

# Plot the charge pump output and the filtered output
plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
plt.plot(t, charge_pump_output, label='Charge Pump Output')
plt.title('Charge Pump Output')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(t, filtered_output, label='Loop Filter Output')
plt.title('Loop Filter Output')
plt.xlabel('Time [s]')
plt.ylabel('Voltage [V]')
plt.legend()

plt.tight_layout()
plt.show()
"""
        
        
        
        
        
        
        
        
        
        
        
        