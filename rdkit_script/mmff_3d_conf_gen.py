#! /usr/local/bin/python

import sys, os
from rdkit import Chem
from rdkit.Chem import AllChem, ChemicalForceFields

mols = Chem.SDMolSupplier( sys.argv[1] )
mols = [ Chem.AddHs(mol) for mol in mols if mol != None ]
print len( mols )
output = Chem.SDWriter( "conf_gen_mols.sdf" )

for i in range( len(mols) ):
    mol = mols[ i ]
    if (mol.HasProp('_Name')):
        mol_Name = mol.GetProp( '_Name' )
    molprop = AllChem.MMFFGetMoleculeProperties( mol )
    field = AllChem.MMFFGetMoleculeForceField( mol, molprop )
    if field.Minimize() == 0:
        e = field.CalcEnergy()
        mol.SetProp( "MMFF94", "%s"%e )

    else:
        mol.SetProp( "MMFF94", "ND" )
    output.write( mol )
output.close()


