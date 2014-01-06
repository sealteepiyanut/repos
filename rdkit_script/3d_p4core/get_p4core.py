import os, sys, math
import cPickle
from rdkit import Chem
from rdkit import RDConfig
from rdkit import Geometry
from rdkit.Chem import AllChem
from rdkit.Chem import ChemicalFeatures
from rdkit.Chem.Pharm3D import Pharmacophore
from rdkit.Chem.FeatMaps import FeatMapPoint

# feature Def
feat_def = "BaseFeatures_seri.fdef"
feat_fact = AllChem.BuildFeatureFactoryFromString(file(feat_def,"r").read())

# Get Pharmacophore from q_mol
q_mol = Chem.SDMolSupplier(sys.argv[1])[0]
feats = feat_fact.GetFeaturesForMol(q_mol)
pcophore = Pharmacophore.Pharmacophore( feats )

# GetFeatures As nested list
# [[x,y,x],
#  [x,y,z],
#  [x,y,z]]
pos_list = []
for feat in feats:
    geom = list(feat.GetPos())
    pos_list.append(geom)
for i in range(len(pos_list)):
    print pos_list[i], feats[i].GetFamily()
    
def get_distance( feats ):
	dist_list = []
	n_feats = len( feats )
	fmp = FeatMapPoint.FeatMapPoint()
	for i in range( n_feats ):
		for j in range( i ):
			fmp.initFromFeat(feats[i])
			dist = math.sqrt(fmp.GetDist2( feats[j] ))
			dist_list.append( (i,j,dist) )
	return dist_list

# define lower and upper bond
dist_list = get_distance( feats )
n_dist = len( dist_list )
d_upper = 1.5
d_lower = 0.5
for i in range( n_dist ):
	pcophore.setLowerBound( dist_list[i][0],dist_list[i][1],dist_list[i][2]-d_lower )
	pcophore.setUpperBound( dist_list[i][0],dist_list[i][1],dist_list[i][2]+d_upper )
print pcophore
# OK You can get Pharmacophore from query mol !!!
# save your query as pkl
outname = sys.argv[1].split(".")[0]+"_pcophore.pkl"
f = open(outname,"wb")

cPickle.dump(pcophore,f)
f.close()

if __name__ == "__main__":
	l = get_distance( feats )
	for i in l:
		print i



