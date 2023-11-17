"""
This script interprets .csv data from a specified simulation, and plots variables for each axial position specified.
It also import pickled experimental data and unpacks it as a  where the values are multi-dimaensional arrays. 
The arrays are parsed to make a dictionary object similar to the siulation data with a dataframe for each value at each axial position

The radial profile for various parameters of interest are then plotted as axial progressions and compared.

Author: Andrew McFadden
Purpose: MSc. Data analysis
Date: 10/16/2023
Version: V1
"""

# Load external libraries and modules
import os
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# # DEFINE WORKSPACE AND VARS
# # ---------------------------------------------------------------------------

dir_home = 'C:\\Users\\drewm\\Documents\\2.0 MSc\\2.0 Simulations\\'
sim_locs = ['PIV_JetSim_M4']
sim_names = ['kw']
files = os.listdir(dir_home + sim_locs[0])
all_pos = []
r_tube = 0.025396
U2 = {}

sim_data = {}

# Read all radial_data.csv files, making dictionary with key of simulation, containing;
# a dictionary with key of each axial position, value of Dataframe for data
for sim in sim_names:
    sim_data.update({ sim : {} })
    for filename in files:
        if filename[:11] == 'radial_data':
            cur_pos = filename[15:-4]
            all_pos.append(cur_pos)
            # Update DF to include data for current radial postion
            sim_data[sim].update({ cur_pos : pd.read_csv(dir_home + sim_locs[0] + '\\' + filename) })
            
            # Add normalized velocity data
            u_jet = np.max(sim_data[sim][cur_pos]['UMean:0'])
            r_dimless = sim_data[sim][cur_pos]['Points:1'] / r_tube
            
            if 'UNorm:0' not in sim_data[sim][cur_pos]:
                Ux_norm = sim_data[sim][cur_pos]['UMean:0'] / u_jet 
                Uy_norm = sim_data[sim][cur_pos]['UMean:1']/ u_jet
                tke_norm = sim_data[sim][cur_pos]['kMean']/ u_jet**2
                sim_data[sim][cur_pos]['UNorm:0'] = Ux_norm
                sim_data[sim][cur_pos]['UNorm:1'] = Uy_norm
                sim_data[sim][cur_pos]['kNorm'] = tke_norm
                sim_data[sim][cur_pos].to_csv(f'{dir_home}{sim_locs[0]}\\{filename}',index=False)
                
            # Calculate secondary and excess velocities
            if 'U_secondary' not in sim_data[sim][cur_pos] and cur_pos != '0.0':
                # Trim the wall effects to find the secondary velocity stream
                y_trim_end = np.where(r_dimless > 0.85)[0][0]
                hist, bins = np.histogram(sim_data[sim][cur_pos]['UMean:0'][:y_trim_end], bins=100) 
                bin_idx = np.where(hist == np.max(hist[:90]))
                U_secondary = bins[bin_idx[0]]
                plt.hist(sim_data[sim][cur_pos]['UMean:0'][:y_trim_end], bins=100, edgecolor='black')
                plt.show()
                print(f'{cur_pos}:\t {U_secondary}')
                U2.update({ cur_pos : U_secondary[0] })
                sim_data[sim][cur_pos]['U_secondary'] = U_secondary[0]
                test = 'jholder'
               

                
                
                


# Select what positions and variable to plot        
xd_pos = np.linspace(15, 30, 7)
r_dimless = sim_data['kw']['0.0']['Points:1']/np.max(sim_data['kw']['0.0']['Points:1'])
sim_var = 'UMean:0'

# # PLOTTING
# # ---------------------------------------------------------------------------

# PLOT SETTINTGS
legend = []
plt.clf()
# styles = plt.style.available
# print(styles)
bright = sns.set_palette(sns.color_palette("bright"))
plt.style.use('seaborn-v0_8-bright')
plt.figure(dpi=1000)
mpl.rcParams['font.family'] = 'book antiqua'

# PLOT DATA
fig, ax = plt.subplots()
for pos in xd_pos:
    ax.plot(r_dimless, sim_data['kw'][f'{pos}'][sim_var], linewidth=0.85)
    legend.append('$x/D_{jet}$' + f' = {pos}')  

ax.grid(True, which='minor')
# ax.set_xlim([0, 25])
# ax.set_ylim([.25, 1])
ax.set_ylabel('Velocity: $u_i$', fontsize=14, labelpad=15)
# ax.yaxis.label.set(rotation='horizontal', ha='right');
ax.set_xlabel('Radial Position: $r/R_{tube}$', fontsize=12, labelpad=10)
ax.set_title('Radial Velocity Profile', fontsize=14, pad=12)
ax.legend(legend,fontsize=10)

fig.savefig('C:\\Users\\drewm\\Documents\\2.0 MSc\\2.0 Simulations\\Figures\\Python\\test.png',
        dpi=1000 ,bbox_inches='tight', pad_inches=0.15)
