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


import subprocess
import os
def visualise_pka(tempfactors_structure, pymol_path, pse_output_filename, pka_value_summary, lower_limit, upper_limit, color_palette): 
    
    """ 
    Function that can visualise the pka vlues of residues using PyMOL. The structure 
    and color_dictionary are used as input. The color_dicitonary contains ranges of 
    pKa values associated with lists of residues in those ranges and hues. The function 
    creates a PyMOL session file. 
    """
    with open('.template.py','a') as output:
        output.write(f"""cmd.load('{tempfactors_structure}', 'protein_str')
cmd.show("cartoon", 'protein_str')
cmd.color("white", "protein_str")\n""")
    Nterm_atoms = 'N+H1+H2+H3'
    Cterm_atoms = 'C+OC1+OC2+OT1+OT2'
    names = []
    for residue,predicted_pka in pka_value_summary.items():
        rounded_predicted_pka = round(predicted_pka,2)
        if 'N+' in residue:
            name = 'NTR'
            resid = residue[2:]
            selection = f'resi {resid} and name {Nterm_atoms}'
        elif 'C-' in residue:
            name = 'CTR'
            resid = residue[2:]
            selection = f'resi {resid} and name {Cterm_atoms}'
        else:
            name = residue
            names.append(name)
            resid = residue[3:]
            selection = f'resi {resid}'
        with open('.template.py','a') as output:
            output.write(f"""cmd.select('{name}', '{selection}') 
cmd.show('licorice', '{name}') 
cmd.spectrum('b','{color_palette}','{name}',{lower_limit},{upper_limit})
cmd.label('{name} and name CB','{rounded_predicted_pka}')\n""")
    sorted_residues = ' '.join(['NTR']+sorted(names, key=lambda x: int(x[3:]))+['CTR'])
    with open('.template.py','a') as output:
        output.write(f"""cmd.order('{sorted_residues}') 
cmd.ramp_new('colorbar', 'none', [{lower_limit}, ({lower_limit} + {upper_limit})/2, {upper_limit}], {color_palette.split('_')})
cmd.set('label_size','-2')
cmd.set('label_position','(1.2,1.2,1.2)') 
cmd.save('{pse_output_filename}')
cmd.quit()\n""")
    subprocess.run([f'{pymol_path} .template.py'],shell=True)
    os.remove('.template.py')