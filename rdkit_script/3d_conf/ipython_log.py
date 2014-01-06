# IPython log file

get_ipython().magic(u'logstart')
from rdkit import Chem
from rdkit.Chem import AllChem
ref = Chem.SDMolSupplier("imatinib.sdf", True, False)
print Chem.MolToSmiles(ref)
print Chem.MolToSmiles(ref.next())
prob = ref = Chem.SDMolSupplier("nilotinib.sdf", True, False)
ref =ref.next()
prob=prob.next()
out = Chem.SDWriter("out_o3a.sdf")
prbPyMP = AllChem.MMFFGetMoleculeProperties(prob)
refMP = AllChem.MMFFGetMoleculeProperties(ref)
get_ipython().magic(u'time pyo3a = AllChem.GetO3A(prob,ref,prbPyMP,refMP)')
pyo3a.Score()
pyo3a.Align()
pyo3a.Weights()
out.write(prob)
out.close()
pyo3a
pyo3a = AllChem.GetO3A(prob,ref,prbPyMP,refMP)
pyo3a.Score()
pyo3a.Align()
pyo3a.Weights()
out.write(prob)
prob
pyo3a.Align()
refMP
refMP.GetMMFFPartialCharge()
refMP.GetMMFFPartialCharge
refMP.GetMMFFAtomType()
refMP.GetMMFFAtomType[0]
refMP.GetMMFFAtomType
a=refMP.GetMMFFAtomType
a

dir(a)
w=Chem.SDWriter("test.sdf")
w.write(ref)
w.write(prob)
w.close()
ms2=Chem.SDMolSupplier("test.sdf",False,False)
r=ms2[0]
p=ms2[1]
rmp=AllChem.MMFFGetMoleculeProperties(r)
r
rmp=AllChem.MMFFGetMoleculeProperties(Chem.AddHs(r))
Chem.MolToSmiles(r)
AllChem.MMFFGetMoleculeForceField(r)
AllChem.MMFFGetMoleculeProperties(r)
AllChem.MMFFGetMoleculeProperties(p)
r.UpdatePropertyCache(strict=False)
AllChem.MMFFGetMoleculeProperties(p)
rh=Chem.AddHs(r, addCoords=True)
AllChem.MMFFGetMoleculeProperties(rh)
AllChem.MMFFGetMoleculeProperties(r)
