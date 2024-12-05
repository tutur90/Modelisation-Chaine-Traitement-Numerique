import scipy.io
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

# Fonction pour moduler un signal en PDM
def pdm_modulate(signal, fs):
    n = len(signal)
    modulated = np.zeros(n)  # Signal modulé en PDM
    integrator = 0  # Intégrateur initialisé à 0
    feedback = 0  # Signal de rétroaction initialisé à 0

    for i in range(n):
        error = signal[i] - feedback  # Calcul de l'erreur
        integrator += error  # Intégration
        modulated[i] = 1 if integrator >= 0 else -1  # Comparateur
        feedback = modulated[i]  # DAC 1-bit pour la rétroaction

    return modulated


# # Fonction pour démoduler un signal PDM (filtrage passe-bas)
# def pdm_demodulate(pdm_signal, cutoff, fs, order=16):
#     nyquist = 0.5 * fs
#     normal_cutoff = cutoff / nyquist
#     b, a = butter(order, normal_cutoff, btype='low', analog=False)
#     demodulated = filtfilt(b, a, pdm_signal)
#     return demodulat# Fonction pour démoduler un signal PDM (filtrage passe-bas)
def pdm_demodulate(pdm_signal, cutoff, fs, order=16):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    demodulated = filtfilt(b, a, pdm_signal)
    return demodulateded

def pdm_demodulate_fir(pdm_signal, cutoff, fs, order=101):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    # Filtre FIR avec fenêtre de Hamming
    num_taps = 101  # Nombre de coefficients du filtre
    fir_coeff = signal.firwin(order, normal_cutoff)

    # Appliquer le filtre
    demodulated = signal.lfilter(fir_coeff, 1.0, pdm_signal)
    return demodulated


# Paramètres
fs = 10000  # Fréquence d'échantillonnage (Hz)
t = np.linspace(0, 1, fs, endpoint=False)  # Axe temporel (1 seconde)
freq = 5  # Fréquence du signal sinusoidal (Hz)
amplitude = 0.8  # Amplitude du signal
cutoff = 50  # Fréquence de coupure pour la démodulation (Hz)

# Génération du signal sinusoidal
input_signal = amplitude * np.sin(2 * np.pi * freq * t)

# Modulation PDM
pdm_signal = pdm_modulate(input_signal, fs)

# Démodulation PDM
demodulated_signal = pdm_demodulate_fir(pdm_signal, cutoff, fs)

# Visualisation
plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(t, input_signal, label="Signal d'entrée (sinus)")
plt.title("Signal d'entrée")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(t, pdm_signal, label="Signal PDM", color='orange')
plt.title("Signal modulé en PDM")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (1 ou -1)")
plt.grid()
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(t, demodulated_signal, label="Signal démodulé", color='green')
plt.title("Signal démodulé (filtrage)")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

plt.tight_layout()
plt.show()

# Visualisation (zoom)
plt.figure(figsize=(12, 8))
plt.subplot(3, 1, 1)
plt.plot(t, input_signal, label="Signal d'entrée (sinus)")
plt.title("Signal d'entrée")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()
plt.xlim(0,0.1)

plt.subplot(3, 1, 2)
plt.plot(t, pdm_signal, label="Signal PDM", color='orange')
plt.title("Signal modulé en PDM")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude (1 ou -1)")
plt.grid()
plt.legend()
plt.xlim(0,0.1)

plt.subplot(3, 1, 3)
plt.plot(t, demodulated_signal, label="Signal démodulé", color='green')
plt.title("Signal démodulé (filtrage)")
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()

plt.tight_layout()
plt.xlim(0,0.1)
plt.show()
