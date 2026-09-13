import os
import csv
import time
import pyautogui
import pygetwindow as gw
import matplotlib.pyplot as plt

# --- CONFIGURATION VARIABLES ---
TARGET_STRESS = 50.0      # MPa (Your goal)
MIN_HOLE_DIA = 30.0       # mm
MAX_HOLE_DIA = 140.0      # mm 
STARTING_HOLE_DIA = 35.0  # mm 

# --- ABSOLUTE FILE PATHS ---
CSV_PATH = r"C:\Users\Om\Documents\Automated Parametric Wing Rib Optimization (Python + CADFEA)\python code\optimization_history.csv"

def log_results(iteration, hole_dia, mass, stress):
    """Saves the data to a CSV file for graphing later."""
    file_exists = os.path.isfile(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Iteration", "Hole Diameter (mm)", "Mass (kg)", "Stress (MPa)"])
        writer.writerow([iteration, hole_dia, mass, stress])

def plot_results():
    """Reads the CSV and generates a final optimization graph."""
    iterations, diameters, masses, stresses = [], [], [], []
    
    try:
        with open(CSV_PATH, "r") as file:
            reader = csv.reader(file)
            next(reader) # Skip the header row
            for row in reader:
                iterations.append(float(row[0]))
                diameters.append(float(row[1]))
                masses.append(float(row[2]))
                stresses.append(float(row[3]))
                
        # Create a graph with two Y-axes
        fig, ax1 = plt.subplots(figsize=(10, 6))
        
        # Plot Mass on the left Y-axis
        color1 = 'tab:blue'
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Mass (kg)', color=color1, fontweight='bold')
        ax1.plot(iterations, masses, marker='o', color=color1, linewidth=2, label='Mass')
        ax1.tick_params(axis='y', labelcolor=color1)
        ax1.grid(True, linestyle='--', alpha=0.6)
        
        # Plot Stress on the right Y-axis
        ax2 = ax1.twinx()  
        color2 = 'tab:red'
        ax2.set_ylabel('Max Equivalent Stress (MPa)', color=color2, fontweight='bold')
        ax2.plot(iterations, stresses, marker='s', color=color2, linewidth=2, label='Stress')
        ax2.tick_params(axis='y', labelcolor=color2)
        
        # Draw a horizontal line for the target stress
        ax2.axhline(y=TARGET_STRESS, color='black', linestyle='--', linewidth=2, label='Target Stress')
        
        # Formatting
        plt.title('Wing Rib Optimization History', fontsize=14, fontweight='bold')
        fig.tight_layout() 
        plt.show()
        
    except Exception as e:
        print(f"Could not generate graph. Error: {e}")

def focus_window(title_keyword):
    """Searches for a window by name and brings it to the front."""
    try:
        windows = gw.getWindowsWithTitle(title_keyword)
        if windows:
            win = windows[0] 
            if win.isMinimized:
                win.restore()
            win.activate() 
            time.sleep(1.5) 
            return True
        else:
            print(f"Error: Could not find any window named '{title_keyword}'.")
            return False
    except Exception as e:
        print(f"Window switching failed: {e}")
        return False

def main():
    print("=== AEROSPACE WING RIB OPTIMIZER (FULLY AUTOMATED) ===")
    
    current_hole_dia = STARTING_HOLE_DIA
    iteration = 1
    max_iterations = 35

    while iteration <= max_iterations:
        print(f"\n--- ITERATION {iteration} ---")
        print(f"Target Hole Diameter: {current_hole_dia:.2f} mm")
        
        # ---> THE DATA BRIDGE <---
        with open("target_diameter.txt", "w") as bridge_file:
            bridge_file.write(str(current_hole_dia))
        
        # ---> THE SMART GHOST IN THE MACHINE <---
        print("\nCommencing automated GUI sequence...")
        
        # 1. Switch to the Fusion 360 project window
        print("Focusing Fusion 360...")
        if focus_window("rib_model"): 
            
            # --- FUSION SEQUENCE ---
            pyautogui.hotkey('shift', 's')
            time.sleep(2.0) 
            
            pyautogui.click(x=838, y=500) 
            time.sleep(0.5)
            
            pyautogui.press('enter')
            time.sleep(6) # Wait for STEP file to export
        else:
            print("Aborting loop. Please ensure Fusion 360 is open.")
            break 
            
        # 2. Switch to the ANSYS Mechanical window
        print("Focusing ANSYS...")
        if focus_window("Mechanical"): 
            
            # --- ANSYS UPDATE SEQUENCE ---
            pyautogui.rightClick(x=133, y=334) 
            time.sleep(1.5) 
            
            pyautogui.click(x=272, y=474) 
            time.sleep(10) # Wait for new geometry to load
            
            # --- ANSYS SOLVE SEQUENCE ---
            pyautogui.click(x=403, y=83) 
            time.sleep(40) # Wait for ANSYS to mesh and solve
            
            # --- ANSYS SCRIPT RUN SEQUENCE (Tab Navigation) ---
            pyautogui.click(x=454, y=43) 
            time.sleep(1.0)
            
            pyautogui.click(x=170, y=98) 
            time.sleep(1.0)
            
            pyautogui.click(x=1764, y=225) 
            time.sleep(3) # Wait for the text file to write
            
            pyautogui.click(x=118, y=49) 
            time.sleep(1.0)

        else:
            print("Aborting loop. Please ensure ANSYS is open.")
            break 
            
        # 3. Bring VS Code back to the front to read the results
        print("Focusing VS Code...")
        focus_window("Visual Studio Code")
        
        # ---> READ AND CALCULATE <---
        try:
            print("Reading ANSYS results...")
            
            with open("ansys_results.txt", "r") as file:
                lines = file.readlines()
                mass = float(lines[0].strip().split()[0])
                stress = float(lines[1].strip().split()[0])
                
            print(f"Auto-Read Mass: {mass:.3f} kg")
            print(f"Auto-Read Stress: {stress:.2f} MPa")
            
            log_results(iteration, current_hole_dia, mass, stress)
            
        except FileNotFoundError:
            print("Error: Could not find ansys_results.txt. Make sure ANSYS ran successfully.")
            break
        except ValueError as e:
            print(f"Error: The data inside ansys_results.txt is invalid. Details: {e}")
            break
        
        # 4. Simple Logic (The Engineering Brain)
        stress_error = stress - TARGET_STRESS
        
        if abs(stress_error) < 1.0:
            print("\n*** OPTIMIZATION CONVERGED! ***")
            plot_results() # <--- DRAWS GRAPH ON SUCCESS
            break

        # INCREASED MULTIPLIER TO 0.5 FOR FASTER CONVERGENCE
        next_dia = current_hole_dia - (stress_error * 0.5)
        next_dia = max(MIN_HOLE_DIA, min(MAX_HOLE_DIA, next_dia))
        
        if next_dia == current_hole_dia:
            print(f"\n*** OPTIMIZATION STOPPED: Reached physical limit of {current_hole_dia:.2f} mm! ***")
            plot_results() # <--- DRAWS GRAPH ON LIMIT REACHED
            break
            
        current_hole_dia = next_dia
        iteration += 1

    # If the loop maxes out at 20 iterations without converging, plot anyway
    if iteration > max_iterations:
        print("\n*** MAXIMUM ITERATIONS REACHED ***")
        plot_results()

if __name__ == "__main__":
    main()