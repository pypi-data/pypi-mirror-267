# SAMBA Copyright (C) 2024 - Closed source


import numpy as np
import shutil


file = np.loadtxt('energy_scan.txt')
date_z = file[:,0]
date_E = file[:,1]
line = np.argmin(date_E)
E_min = date_E[line]
z     = date_z[line]

shutil.copyfile(str(z) + '/POSCAR', 'POSCAR')
