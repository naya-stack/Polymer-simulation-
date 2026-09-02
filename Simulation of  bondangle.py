import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.patches as patches

# Setup figure
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
plt.subplots_adjust(bottom=0.2, hspace=0.4)

# Initial parameters
initial_angle = 109.5
L = 1.0  # Bond length

def calculate_positions(angle_deg):
    angle_rad = np.deg2rad(angle_deg)
    # C2 at origin
    C2 = np.array([0, 0])
    # C1 and C3
    C1 = np.array([-L * np.sin(angle_rad / 2), -L * np.cos(angle_rad / 2)])
    C3 = np.array([L * np.sin(angle_rad / 2), -L * np.cos(angle_rad / 2)])
    # Side chains (wings) - assuming they point straight up in Y for simplicity of clash visualization
    # We extend the vector from C2 to C1/C3 slightly outwards
    S1 = C1 + np.array([-0.5, 1.5]) 
    S3 = C3 + np.array([0.5, 1.5])
    return C1, C2, C3, S1, S3

def update(val):
    angle = slider.val
    C1, C2, C3, S1, S3 = calculate_positions(angle)
    
    # --- Plot 1: Molecular Structure ---
    ax1.clear()
    # Draw bonds
    ax1.plot([C1[0], C2[0]], [C1[1], C2[1]], 'k-', linewidth=3, zorder=1)
    ax1.plot([C2[0], C3[0]], [C2[1], C3[1]], 'k-', linewidth=3, zorder=1)
    ax1.plot([C1[0], S1[0]], [C1[1], S1[1]], 'k-', linewidth=2, zorder=1)
    ax1.plot([C3[0], S3[0]], [C3[1], S3[1]], 'k-', linewidth=2, zorder=1)
    
    # Draw Atoms (C1, C2, C3)
    ax1.scatter(*C2, color='gray', s=200, zorder=2, edgecolor='black')
    ax1.scatter(*C1, color='gray', s=150, zorder=2, edgecolor='black')
    ax1.scatter(*C3, color='gray', s=150, zorder=2, edgecolor='black')
    
    # Draw Side Chains as HUGE Spheres (Van der Waals representation)
    # Radius is set to 0.9 to make the clash visible
    radius = 0.9
    circle1 = plt.Circle(S1, radius, color='red', alpha=0.7, zorder=3, label='Butyl Group 1')
    circle3 = plt.Circle(S3, radius, color='blue', alpha=0.7, zorder=3, label='Butyl Group 3')
    ax1.add_patch(circle1)
    ax1.add_patch(circle3)
    
    # Calculate distance between sphere centers
    dist = np.linalg.norm(S1 - S3)
    
    # Check for clash
    clash_status = "NO CLASH (Stable)" if dist > 2*radius else "SEVERE CLASH (Unstable!)"
    color = "green" if dist > 2*radius else "red"
    
    ax1.set_xlim(-3, 3)
    ax1.set_ylim(-2, 3)
    ax1.set_aspect('equal')
    ax1.set_title(f'Bond Angle: {angle:.1f}° | Spatial Distance: {dist:.2f} AU\n'
                  f'Status: {clash_status}', color=color, fontsize=14, fontweight='bold')
    ax1.legend(loc='lower left')
    
    # --- Plot 2: Torsional Energy Barrier ---
    ax2.clear()
    # Rotation angle (0 to 360)
    theta = np.linspace(0, 2*np.pi, 100)
    
    # Energy logic: If distance is small (clash), barrier is huge. If large, barrier is small.
    # Simplified mathematical representation of Pauli Repulsion
    barrier_height = 500 / (dist**2)  # Arbitrary scaling to show dramatic drop
    
    # Potential energy curve (cosine wave representing torsion)
    # We shift it so that the baseline is 0, and peaks are at barrier_height
    energy = (barrier_height / 2) * (1 - np.cos(3 * theta))
    
    ax2.plot(np.degrees(theta), energy, 'r-', linewidth=3)
    ax2.set_ylim(0, 150)
    ax2.set_xlim(0, 360)
    ax2.set_xlabel('Backbone Rotation Angle (Degrees)', fontsize=12)
    ax2.set_ylabel('Potential Energy (kcal/mol)', fontsize=12)
    ax2.set_title(f'Torsional Energy Barrier: {barrier_height:.1f} kcal/mol\n'
                  '(Barrier collapses as groups separate)', fontsize=14, fontweight='bold')
    ax2.grid(True)

# Slider setup
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Bond Angle', 109.0, 120.0, valinit=initial_angle)

slider.on_changed(update)
update(initial_angle)

plt.show()