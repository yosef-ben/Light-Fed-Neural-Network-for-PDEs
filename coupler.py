import numpy as np

# Classe per simulare un accoppiatore direzionale
class Coupler:
    def __init__(self, k):
        self.k = k # coefficiente di accoppiamento
        self.Mat = Coupler.compute_matrix(self) # matrice 2x2 di trasferimento

    # Aggiorna il valore del coefficiente di accoppiamento e di conseguenza la matrice di trasferimento
    def update_params(self, k):
        self.k = k
        self.Mat = Coupler.compute_matrix(self)
    
    # Calcola la matrice di trasferimento dell'accoppiatore
    def compute_matrix(self):
        Tc1 = np.empty((2,2), dtype=np.complex128)
        Tc1[0, 0] = np.sqrt(1.0 - self.k)
        Tc1[0, 1] = -1j*np.sqrt(self.k)
        Tc1[1, 0] = -1j*np.sqrt(self.k)
        Tc1[1, 1] = np.sqrt(1.0 - self.k)
        return Tc1
    
    # Propagazione del campo elettrico attraverso l'accoppiatore
    def propagate(self, Ein):
        Eout = self.Mat @ Ein
        return Eout
