# Automated-Multidisciplinary-Design-Optimization-MDO-Pipeline
Architected an autonomous Python MDO pipeline linking Fusion 360 (CAD) and ANSYS (FEA) via GUI automation and a custom data bridge. Utilizing proportional control logic, the script hands-free optimized an aerospace wing rib over 35 iterations, cutting mass by 11% (160g) while perfectly converging on a strict structural safety limit.
# ✈️ Automated Multidisciplinary Design Optimization (MDO) Pipeline

![Optimization Status](https://img.shields.io/badge/Status-Completed-success)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Fusion 360](https://img.shields.io/badge/Autodesk-Fusion_360-orange)
![ANSYS](https://img.shields.io/badge/ANSYS-Mechanical-yellow)

## 📌 Project Overview
A fully autonomous, closed-loop software pipeline engineered to eliminate manual design iteration bottlenecks in aerospace components. This project utilizes Python as an orchestrator to seamlessly bridge **Autodesk Fusion 360** (Parametric CAD) and **ANSYS Mechanical** (FEA). 

By implementing proportional control logic, the pipeline dynamically evaluates real-time stress data and autonomously scales geometric cutouts. The system successfully optimized an aluminum aerospace wing rib completely hands-free, minimizing mass while safely converging on a strict structural stress limit.

![Insert your dual-axis convergence graph or a split-screen video GIF here]

---

## 🚀 Key Results
* **Mass Reduction:** Achieved an **11% weight savings (160 grams)** on a single aluminum wing rib.
* **Structural Integrity:** Safely converged at **48.8 MPa**, perfectly maintaining the strict 50.0 MPa maximum equivalent stress limit.
* **Automation:** Executed **35 complete CAD-to-FEA iterations** with zero human intervention.
* **Efficiency:** Completely eliminated the 15-minute manual handoff bottleneck, drastically reducing engineering cycle time.

---

## ⚙️ System Architecture & Data Bridge
Because commercial CAD and FEA software do not natively communicate, this pipeline uses a custom text-based "data bridge" and GUI automation to pass variables across platforms.

1. **The Orchestrator (Python):** Uses `pyautogui` and window management to physically drive the engineering software. It calculates target dimensions and writes them to local `.txt` files.
2. **Parametric CAD (Fusion 360 API):** A custom script reads the Python output, updates the 2D sketch constraint (`HoleDia`), regenerates the solid body, and exports a fresh `.step` 3D file.
3. **FEA Solver (ANSYS IronPython):** The system automatically ingests the new `.step` file, updates the mesh, solves the simulated aerodynamic pressure and fixed spar loads, and writes the resulting Mass and Max Equivalent Stress back to a `.txt` file.

---

## 🧠 Algorithmic Control Logic
To prevent the FEA solver from overshooting the 50 MPa safety limit and breaking the part, the Python orchestrator utilizes a **proportional control algorithm**. 

```python
# Proportional error-based step calculation
stress_error = TARGET_STRESS - current_stress
next_dia = current_hole_dia - (stress_error * 0.5)
