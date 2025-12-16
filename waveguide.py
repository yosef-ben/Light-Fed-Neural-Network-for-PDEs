import numpy as np

# Classe per simulare la propagazione della luce in una guida d'onda
class Waveguide:
    c0 = 299792458.0 # velocità della luce in m/s
    
    def __init__(self, ps, l, f, n, ag=-23.02555836979): # cambia ag=0.0 per lossless
        self.ps = ps # valore di phase shift in radianti
        self.l = l   # lunghezza della guida d'onda in metri
        self.f = f   # frequenza della luce in Hz
        self.n = n   # indice di rifrazione
        self.ag = ag # attenuazione (lasciato di default al valore in input)
        self.phase = (self.ag - 1j * 2*np.pi * self.f * self.n / self.c0) * self.l - 1j * self.ps

    # Aggiorna il valore dei parametri fisici
    def update_params(self, l=None, f=None, n=None, ag=None):
        if l is not None:
            self.l = l
        if f is not None:
            self.f = f
        if n is not None:
            self.n = n
        if ag is not None:
            self.ag = ag
        self.phase = (self.ag - 1j * 2*np.pi * self.f * self.n / self.c0) * self.l

    # Aggiorna il valore del phase shift e di conseguenza la fase
    def update(self, ps):
        self.ps = ps
        self.phase = (self.ag - 1j * 2*np.pi * self.f * self.n / self.c0) * self.l - 1j * self.ps

    # Propagazione del campo elettrico attraverso la guida d'onda
    def propagate(self, Ein):
        return Ein * np.exp(self.phase)

    # Divide la potenza del segnale in ingresso, restituendo il campo trasmesso e la potenza rilevata
    def split_power(self, Ein, ratio=0.1):
        Edetected = Ein * np.sqrt(ratio)
        Eout = Ein * np.sqrt(1 - ratio)
        Pdetected = np.abs(Edetected)**2
        return Eout, Pdetected
    
    # Trasferimento per una coppia di waveguide (non utilizzabile per ora)
#    def Delay_Line(ps, l, f, n, ag=-23.02555836979):
#        ps = np.atleast_1d(ps)
#        phase = (ag - 1j * 2*np.pi * f * n / self.c0) * l
#        DL = np.zeros((ps.size, 2, 2), dtype=np.complex128)
#        DL[:,0,0] = np.exp(phase)
#        DL[:,1,1] = np.exp(phase - 1j * ps)
#        return DL
