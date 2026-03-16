# Photonic Deep Ritz Method for PDEs

Multidisciplinary project — Politecnico di Milano, High Performance Computing Engineering  
**Yosef Ben Chedly** | a.y. 2025–2026  
Supervisors: Francesco Morichetti, Andrea Melloni (Politecnico di Milano)

---

## Overview

This project investigates the use of **photonic neural networks** (PNNs) built on
Mach-Zehnder interferometer (MZI) meshes to solve partial differential equations
(PDEs) in an unsupervised, physics-informed fashion.

The network is simulated with the [neuroptica](https://github.com/fancompute/neuroptica)
library. The unknown PDE solution is approximated by a physically parameterized neural
network composed of cascaded Optical Interference Units with holomorphic complex
activations applied digitally between layers.

The core contribution is the **Photonic Deep Ritz algorithm**: an extension of the
Deep Ritz method to photonic hardware, where training is performed via **in-situ analog
backpropagation** using the adjoint variable method. The key theoretical result is a
generalization of the adjoint source term to arbitrary differentiable loss functionals —
enabling unsupervised training directly from the variational (energy) form of the PDE,
without labeled data and without automatic differentiation.

Gradients are recovered from three intensity measurements per layer (forward field,
adjoint field, and their interference), making the training loop fully compatible with
analog photonic hardware.

---

## Repository Structure
```
.
├── neuroptica_xor.ipynb                     # Baseline: XOR classification on photonic network
├── neuroptica_pde1d.ipynb                   # 1D Poisson equation (Dirichlet and mixed BCs)
├── neuroptica_pde2d.ipynb                   # 2D Poisson equation
├── mul_proj_phc_def.pdf                     # Full written report
└── PhotonicDeepRitz_final_presentation.pdf # Slide deck (35 slides)
```

---

## Method

### Photonic Neural Network
The network alternates unitary linear layers — implemented as Clements-topology MZI
meshes — and nonlinear activations applied digitally. Each linear layer computes:

$$X_\ell = \phi_\ell(\hat{W}_\ell X_{\ell-1})$$

where $\hat{W}_\ell = D\hat{W}^{\sharp}$ is parameterized by the phase shifter settings
of the MZI mesh. The Clements topology implements a universal $N \times N$ unitary
transformation using $N(N-1)/2$ MZIs.

### Deep Ritz Loss
For the Poisson equation $-\Delta u = f$ on $\Omega$, the variational objective is:

$$\mathcal{L}_{DR}(\theta) = \int_\Omega \frac{1}{2}|\nabla u_\theta|^2 \, dx
- \int_\Omega f \, u_\theta \, dx + \lambda_{bc} \mathcal{L}_{bc}$$

The integral is approximated via Monte Carlo sampling. Spatial derivatives of the
network output are computed analytically through recursive on-chip differentiation,
propagating the Jacobian through the network layers without finite-difference
approximations.

### Adjoint Source Term — Original Contribution
The original Hughes et al. formulation used a supervised mean-square loss. This work
generalizes the adjoint injection to any differentiable loss functional:

$$\delta_L := \phi'_L(Y_L) \left(\frac{\partial \mathcal{L}_{DR}}{\partial X_L}\right)^*$$

For the Deep Ritz loss applied to the Poisson equation, this gives per sample $x_i$:

$$\delta_L(x_i) = \phi'_L(Y_L(x_i)) \, \frac{w_i}{2}\left(-f(x_i)
- \Delta u_\theta(x_i)\right) a$$

This complex vector is synthesized and injected from the output ports. Gradients are
then recovered from the interference pattern:

$$\frac{\partial \mathcal{L}}{\partial \varepsilon_\ell} =
\frac{k_0^2}{2}(I_\ell - I_\ell^\rightarrow - I_\ell^\leftarrow)$$

where $I_\ell^\rightarrow$, $I_\ell^\leftarrow$, and $I_\ell$ are the forward,
adjoint, and interference intensities measured at each phase shifter location.
The key insight is that **correct adjoint injection can be generated without targets**,
enabling fully unsupervised in-situ training.

---

## Notebooks

### `neuroptica_xor.ipynb`
Validates the photonic training pipeline on the XOR classification task using the
neuroptica simulator. Establishes the baseline for analog backpropagation on MZI meshes.

### `neuroptica_pde1d.ipynb`
Applies the Photonic Deep Ritz algorithm to the 1D Poisson equation. Two benchmarks:
- **Dirichlet BCs**: $-u''(x) = 1$ on $(0,1)$, $u(0)=u(1)=0$. Final relative
  $L^2$ error below $10^{-2}$ after 1000 epochs.
- **Mixed BCs**: $-u''(x) = \sin(\pi x)$ on $(0,1)$, $u(0)=0$, $u'(1)=0$.
  Depth comparison (2 vs 4 layers): increasing depth reduces interior RMS residual
  from $2.9 \times 10^{-1}$ to $5.4 \times 10^{-2}$ and improves Neumann boundary
  satisfaction by an order of magnitude.

### `neuroptica_pde2d.ipynb`
Extends the Photonic Deep Ritz algorithm to the 2D Poisson equation.

---

## Dependencies

- [neuroptica](https://github.com/fancompute/neuroptica) — photonic neural network simulator
- `numpy`, `scipy`, `matplotlib`

---

## References

[1] I. A. D. Williamson et al. "Reprogrammable Electro-Optic Nonlinear Activation
Functions for Optical Neural Networks". IEEE J. Sel. Topics Quantum Electron. 26.1, 2020.

[2] Y. Tang et al. "Optical neural engine for solving scientific partial differential
equations". Nature Communications, 2025.

[3] K. P. Kalinin et al. "Analog optical computer for AI inference and combinatorial
optimization". Nature, 2025.

[4] H. Yuan et al. "Microcomb-driven Photonic Chip for Solving Partial Differential
Equations". Advanced Photonics 7.1, 2025.

[5] A. Quarteroni, P. Gervasio, F. Regazzoni. "Combining physics-based and data-driven
models: advancing the frontiers of research with Scientific Machine Learning".
arXiv:2501.18708, 2025.

[6] M. W. M. G. Dissanayake and N. Phan-Thien. "Neural-network-based approximations
for solving PDEs". Communications in Numerical Methods in Engineering 10.3, 1994.

[7] W. E and B. Yu. "The Deep Ritz Method: A Deep Learning-Based Numerical Algorithm
for Solving Variational Problems". Communications in Mathematics and Statistics 6.1, 2018.

[8] C. Uriarte. Solving Partial Differential Equations Using Artificial Neural Networks.
arXiv:2403.09001, 2024.

[9] A. Quarteroni and A. Valli. Numerical Approximation of Partial Differential
Equations. Springer, 1994.

[10] K. He et al. "Deep Residual Learning for Image Recognition". CVPR, 2016.

[11] T. W. Hughes et al. "Training of photonic neural networks through in situ
backpropagation and gradient measurement". Optica 5.7, 2018.

[12] Y. Shen et al. "Deep learning with coherent nanophotonic circuits".
Nature Photonics 11.7, 2017.

[13] D. C. Plaut, S. J. Nowlan, G. E. Hinton. Experiments on Learning by Back
Propagation. Tech. rep., Carnegie-Mellon University, 1986.

[14] W. Shin and S. Fan. "Choice of the perfectly matched layer boundary condition
for frequency-domain Maxwell's equations". Journal of Computational Physics 231.8, 2012.