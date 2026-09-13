import pandas as pd
import matplotlib.pyplot as plt
import os

# The name of the file your optimizer creates
filename = "optimization_history.csv"

# Safety check to make sure the file exists
if not os.path.exists(filename):
    print(f"Error: Could not find {filename}. Make sure it is in the same folder.")
else:
    # 1. Read the data
    df = pd.read_csv(filename)
    
    # Check what columns actually exist in the CSV to avoid errors
    print("Found columns:", df.columns.tolist())
    
    # We assume standard column names based on your optimizer script. 
    # If your CSV uses different headers, update the names inside the brackets below!
    iteration_col = df.columns[0] # Usually 'Iteration'
    mass_col = df.columns[2]      # Usually 'Mass (kg)'
    stress_col = df.columns[3]    # Usually 'Stress (MPa)'

    # 2. Setup a professional layout with 2 charts stacked on top of each other
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle('Automated Wing Rib Optimization: Convergence History', fontsize=16, fontweight='bold')

    # 3. Top Chart: Mass vs Iterations (The Goal)
    ax1.plot(df[iteration_col], df[mass_col], marker='o', color='#1f77b4', linewidth=2, markersize=8)
    ax1.set_title('Mass Reduction over Time', fontsize=12)
    ax1.set_ylabel('Mass (kg)', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.7)

    # 4. Bottom Chart: Stress vs Iterations (The Constraint)
    ax2.plot(df[iteration_col], df[stress_col], marker='s', color='#d62728', linewidth=2, markersize=8)
    # Draw a green dashed line to represent your 120 MPa target
    ax2.axhline(y=120, color='#2ca02c', linestyle='--', linewidth=2, label='Target Stress (120 MPa)')
    ax2.set_title('Maximum Stress Tracking', fontsize=12)
    ax2.set_xlabel('Iteration Number', fontsize=11)
    ax2.set_ylabel('Max Stress (MPa)', fontsize=11)
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.7)

    # 5. Clean up the layout and display the graphs!
    plt.tight_layout()
    plt.show()