"""
    @release_date  : $release_date
    @version       : $release_version
    @author        : Christos Matsingos, Ka Fu Man 
    
    This file is part of the TrIPP software
    (https://github.com/fornililab/TrIPP).
    Copyright (c) 2024 Christos Matsingos, Ka Fu Man and Arianna Fornili.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3.

    This program is distributed in the hope that it will be useful, but
    WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""


import MDAnalysis as mda
import numpy as np
import pandas as pd 
from tripp.visualise_pka import visualise_pka 
from tripp.model_pka_values import model_pka_values 

class Visualization: 


    """ 
    This class allows for the visualisation of pKa values using PyMOL. The 
    class is called using a strucutre of the protein and a CSV file generated 
    by the Trajectory class containing all pKa values. The method color_pka 
    can be called which generated a PyMOL session file. The arguments of 
    color_pka are the following: 
    
    coloring_method: 'mean' or 'difference_to_model_value' 
    used to determine how the color of each residue is produced. Can be 'mean', 
    where the mean pKa value accross all frames is used or 
    'difference_to_model_value' where the mean pKa value is calculated 
    and the difference to the model value of the amino acid in solution is 
    used. 
    
    lower limit: int or float 
    determines lower limit used to colour the reisdues in the PyMOL session. Any 
    value below the limit is coloured using the lowest end of the color gradient 
    used. 
    
    upper limit: int or float 
    determines upper limit used to colour the reisdues in the PyMOL session. Any 
    value above the limit is coloured using the highest end of the color gradient 
    used. 

    color_palette: 'red_white_blue', 'blue_white_red', 'red_white_green', and 'green_white_red' 
    color palettes used to color the residues in the PyMOL session according to 
    pKa value. The defaults is set to 'red_white_blue'. 
    """


    def __init__(self, structure, pka_file):

        self.structure = structure
        self.pka_file = pka_file
        

    def color_pka(self, pymol_path, pse_output_prefix, coloring_method, lower_limit, upper_limit, color_palette='red_white_blue'): 
        
        u = mda.Universe(self.structure)
        
        #load pKa values and remove time column 
        pka_values = pd.read_csv(self.pka_file) 
        del pka_values['Time [ps]'] 
        
        #calculation of values depending on colouring method 
        if coloring_method == 'mean': 
            pka_values_summary = pka_values.mean(axis=0) 
            tempfactors_output_structure= f"{self.pka_file.split('/')[-1].split('.')[0]}_mean.pdb"

        elif coloring_method == 'difference_to_model_value': 
            pka_values_mean = pka_values.mean(axis=0) 
            for residue, value in pka_values_mean.items(): 
                if 'N+' in residue: 
                    pka_values_mean[residue] = pka_values_mean[residue]-model_pka_values['NTR'] 
                elif 'C-' in residue: 
                    pka_values_mean[residue] = pka_values_mean[residue]-model_pka_values['CTR'] 
                else: 
                    pka_values_mean[residue] = pka_values_mean[residue]-model_pka_values[residue[0:3]] 
            pka_values_summary = pka_values_mean
            tempfactors_output_structure = f"{self.pka_file.split('/')[-1].split('.')[0]}_difference_to_model_value.pdb"
        
        
        Nterm_atoms = 'N H1 H2 H3'
        Cterm_atoms = 'C OC1 OC2 OT1 OT2'
        for residue, predicted_pka in pka_values_summary.items():
            if 'N+' in residue or 'C-' in residue:
                resid = int(residue[2:])
            else:
                resid = int(residue[3:])
            rounded_predicted_pka = round(predicted_pka,2)
            if 'N+' in residue:
                ag = u.select_atoms(f'resid {resid} and name {Nterm_atoms}')
            elif 'C-' in residue:
                ag = u.select_atoms(f'resid {resid} and name {Cterm_atoms}')
            elif resid == u.residues.resids[0]:
                ag = u.select_atoms(f'resid {resid} and not name {Nterm_atoms}')
            elif resid == u.residues.resids[-1]:
                ag = u.select_atoms(f'resid {resid} and not name {Cterm_atoms}')
            else:
                ag = u.select_atoms(f'resid {resid}')
            ag.tempfactors = np.full(ag.tempfactors.shape,rounded_predicted_pka)
        ag = u.select_atoms('all')
        ag.write(tempfactors_output_structure)
        pse_output_filename = f'{pse_output_prefix}_{coloring_method}.pse'
        visualise_pka(tempfactors_output_structure, pymol_path, pse_output_filename, pka_values_summary, lower_limit, upper_limit, color_palette) 

 