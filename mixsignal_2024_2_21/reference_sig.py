import numpy as np
import matplotlib.pyplot as plt
from phase_detector import IntegratedPhaseDetector

class SignalGenerator:
    def __init__(self, frequency, sampling_rate, duration):
        self.frequency = frequency
        self.sampling_rate = sampling_rate
        self.duration = duration
        self.num_samples = int(self.duration * self.sampling_rate)
        self.time_vector = np.linspace(0, self.duration, self.num_samples, endpoint=False)
        self.sine_wave = None
        self.square_wave = None

    def generate_sine_wave(self):
        self.sine_wave = np.sin(2 * np.pi * self.frequency * self.time_vector)

    def generate_square_wave(self):
        if self.sine_wave is None:
            self.generate_sine_wave()
        self.square_wave = np.sign(self.sine_wave)

    def plot_wave(self, wave_type):
        # self.generate_sine_wave()
        # self.generate_square_wave()
        if wave_type == 'sine' and self.sine_wave is not None:
            plt.plot(self.time_vector, self.sine_wave)
            plt.title('Sine Wave')
        elif wave_type == 'square' and self.square_wave is not None:
            plt.plot(self.time_vector, self.square_wave)
            plt.title('Square Wave')
        else:
            raise ValueError("Invalid wave type or wave not generated")

        plt.xlabel('Time [s]')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.show()

# Example usage
"""
频率,sample_rate以及点的提取可以再想想,确认一下
因为信号生成后得往后传,然后任何时域的delay都需要涉及到频率和采样率---------------2024/02/20
"""
frequency = 25 * 10**6  # 25 MHz
sampling_rate = 5000 * 10**6  # 5 GHz
duration = 1 * 10**-6  # 1 microsecond

signal_gen = SignalGenerator(frequency, sampling_rate, duration)
signal_gen.generate_sine_wave()
signal_gen.generate_square_wave()
reference_signal = signal_gen.square_wave
# print(reference_signal[:10])
# signal_gen.plot_wave('square')


PFD_outR1 = []
PFD_outF1 = []
PFD_try1 = IntegratedPhaseDetector(sampling_rate)
for signal in reference_signal:
    PFD_outR, PFD_outF = PFD_try1.detect_phase(signal,signal)
    PFD_outR1.append(PFD_outR)
    PFD_outF1.append(PFD_outF)
    # print(signal,'|',PFD_outR,PFD_outF)
    

time_vector = np.linspace(0,duration,int(sampling_rate*duration))

# # plt.subplot(2,1,1)
plt.title('PFD_outR1')
plt.plot(time_vector,PFD_outR1)
plt.grid(True)

# plt.subplot(2,1,2)
# plt.title('PFD_outF')
# plt.plot(PFD_outF1)
# plt.grid(True)

plt.show()
    




