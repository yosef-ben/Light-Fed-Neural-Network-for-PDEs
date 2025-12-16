# importo i moduli necessari
from waveguide import Waveguide
from coupler import Coupler
import numpy as np

# Allocazione im memoria per i campi elettrici
Ein = np.zeros((2,1), dtype=np.complex128)
E1 = Ein.copy()
E2 = Ein.copy()
E3 = Ein.copy()
Eout = Ein.copy()

# Inizializzazione del campo elettrico in ingresso
Ein[0] = 1.0 + 0.0j # o anche modulo*np.exp(1j*fase)
Ein[1] = 0.0 + 1.0j # 1.0*np.exp(1j*np.pi/2)

# Definizione del circuito ottico composto da waveguide e coupler (valori sono a caso)
wg11 = Waveguide(ps=0.1, l=0.01, f=2e14, n=3.5)
wg12 = Waveguide(ps=0.2, l=0.02, f=2e14, n=3.5)

c1 = Coupler(k=0.3)

# la frequenza della luce è la stessa in tutto il circuito, l'indice di rifrazione anche solitamente
wg21 = Waveguide(ps=0.2, l=0.02, f=2e14, n=3.5)
wg22 = Waveguide(ps=0.3, l=0.03, f=2e14, n=3.5)

c2 = Coupler(k=0.4)

# Propagazione del segnale attraverso il circuito
E1[0] = wg11.propagate(Ein[0])
E1[1] = wg12.propagate(Ein[1])
E2 = c1.propagate(E1)
E3[0] = wg21.propagate(E2[0])
E3[1] = wg22.propagate(E2[1])
Eout = c2.propagate(E3)

print("Input E:", Ein[0], Ein[1])
print("Output E:", Eout[0], Eout[1])

# Piccolo esempio di struttura più complessa, poi si possono aggiungere cicli e altro
# E2 = c1.propagate([wg11.propagate(Ein[0]), wg12.propagate(Ein[1])])
# Eout1 = c2.propagate([wg21.propagate(E2[0]), wg22.propagate(E2[1])])