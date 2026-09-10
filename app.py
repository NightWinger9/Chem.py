import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Zymological Kinetics Engine", page_icon="🧪", layout="centered")

st.title("🧪 In-Silico Zymological Kinetics Simulator")
st.markdown("### Sustainable Aviation Fuel (ETJ Pipeline Optimization)")
st.write("Adjust the industrial parameters below to simulate real-time D-glucose bioconversion and bio-ethanol yield.")

# Sidebar Controls for True UI Experience
st.sidebar.header("Simulation Parameters")
glucose_s0 = st.sidebar.slider("Initial Glucose ($S_0$ mol/L)", 0.5, 5.0, 2.5, 0.1)
temp_c = st.sidebar.slider("Reactor Temperature (°C)", 15.0, 60.0, 35.0, 1.0)
vmax = st.sidebar.slider("Max Velocity ($V_{max}$)", 0.01, 0.5, 0.15, 0.01)
km = st.sidebar.slider("Michaelis Constant ($K_m$)", 0.05, 1.5, 0.45, 0.05)

# Simulation Engine Logic
temp_k = temp_c + 273.15
total_time = 48
steps = 480
dt = total_time / steps
time_array = np.linspace(0, total_time, steps + 1)

g = np.zeros(steps + 1)
eth = np.zeros(steps + 1)
co2 = np.zeros(steps + 1)
g[0] = glucose_s0

E_a = 52000.0
R = 8.314
denaturation = max(0.0, 1.0 - (temp_k - 313.15) / 30.0) if temp_k > 313.15 else 1.0
eff_vmax = vmax * np.exp(-(E_a / R) * ((1.0 / temp_k) - (1.0 / 298.15))) * denaturation

for i in range(steps):
    S = g[i]
    if S <= 0:
        g[i+1] = 0
        eth[i+1] = eth[i]
        co2[i+1] = co2[i]
        continue
    v = (eff_vmax * S) / (km + S)
    g[i+1] = max(0.0, g[i] - v * dt)
    eth[i+1] = eth[i] + 2.0 * v * dt
    co2[i+1] = co2[i] + 2.0 * v * dt

# Render Clean Web UI Graph
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(time_array, g, label='D-Glucose ($C_6H_{12}O_6$)', color='#e74c3c', linewidth=2.5)
ax.plot(time_array, eth, label='Bio-Ethanol ($C_2H_5OH$)', color='#2980b9', linewidth=2.5)
ax.plot(time_array, co2, label='Carbon Dioxide ($CO_2$)', color='#27ae60', linewidth=2.5, linestyle='--')
ax.set_title(f'Fermentation Kinetics at {temp_c}°C', fontsize=12, fontweight='bold')
ax.set_xlabel('Time (Hours)', fontsize=10)
ax.set_ylabel('Concentration (mol/L)', fontsize=10)
ax.legend(frameon=True, facecolor='#f9f9f9')
ax.grid(True, linestyle=':', alpha=0.6)
st.pyplot(fig)

# Dataframe metrics view
st.markdown("---")
st.subheader("Simulated Time-Series Output Matrix")
results_df = pd.DataFrame({
    'Time (Hours)': time_array,
    'Glucose (mol/L)': g,
    'Ethanol (mol/L)': eth,
    'CO2 (mol/L)': co2
})
st.dataframe(results_df.head(10), use_container_width=True)
