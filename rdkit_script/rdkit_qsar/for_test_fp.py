import sys, cPickle
import numpy as np
from rdkit import Chem
from rdkit.Chem import DataStructs
from rdkit.Chem import AllChem

trainset = sys.argv[1]
testset = sys.argv[2]

trainset = [mol for mol in Chem.SDMolSupplier(trainset) if mol is not None]
testset = [mol for mol in Chem.SDMolSupplier(testset) if mol is not None]

train_fps = [AllChem.GetMorganFingerprintAsBitVect(mol,2,nBits=1024) for mol in trainset]
train_np_fps = []
for fp in train_fps:
	arr = np.zeros((1,))
	DataStructs.ConvertToNumpyArray(fp, arr)
	train_np_fps.append(arr)
train_np_fps = np.array(train_np_fps)

test_fps = [AllChem.GetMorganFingerprintAsBitVect(mol,2,nBits=1024) for mol in testset]
test_np_fps = []
for fp in test_fps:
	arr = np.zeros((1,))
	DataStructs.ConvertToNumpyArray(fp, arr)
	test_np_fps.append(arr)
test_np_fps = np.array(test_np_fps)

classes={'(A) low':0,'(B) medium':1,'(C) high':1}
train_acts = np.array([classes[mol.GetProp("SOL_classification")] for mol in trainset],dtype="int")
test_acts = np.array([classes[mol.GetProp("SOL_classification")] for mol in testset],dtype="int")

dataset = ( (train_np_fps, train_acts),(train_np_fps, train_acts), (test_np_fps, test_acts) )

f = open("rdk_sol_set.pkl", "wb")
cPickle.dump(dataset,f)
f.close()

