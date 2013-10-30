import sys
from rdkit import Chem
from rdkit.Chem import AllChem

sdf = Chem.SDMolSupplier( sys.argv[1] )
mols = []
for mol in sdf:
    try:
        mols.append( mol )
    except:
        pass

fps = {}

for mol in mols:
    try:
        fp = AllChem.GetMorganFingerprintAsBitVect(mol,2)
        fp_bit = fp.ToBitString()
        fps[ mol.GetProp("COMPOUND_ID") ] = fp_bit
    except:
        pass
print len(fps)

for i,v in fps.items():
    print i,v


