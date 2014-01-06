import os, sys, cPickle
from rdkit import Chem
from rdkit import RDConfig
from rdkit import Geometry
from rdkit.Chem import ChemicalFeatures
from rdkit.Chem.Pharm3D import Pharmacophore, EmbedLib
from rdkit.Chem import AllChem
<<<<<<< HEAD
from rdkit.Chem import rdDistGeom
from rdkit.Chem.FeatMaps import FeatMapPoint
from rdkit.Numerics import rdAlignment

feat_path = os.path.join(RDConfig.RDDataDir, "BaseFeatures.fdef")
feat_fact = AllChem.BuildFeatureFactoryFromString(file(feat_path,"r").read())

mols = [ mol for mol in Chem.SDMolSupplier( "benzen.sdf" ) ]
print Chem.MolToSmiles(mols[0])
=======
from rdkit.Chem.FeatMaps import FeatMapPoint

mols = [ mol for mol in Chem.SDMolSupplier( sys.argv[1] ) ]

>>>>>>> origin/master
f = open( "p4core_rdk.pkl", "rb" )
pcophore = cPickle.load( f )
print pcophore

<<<<<<< HEAD


def check_mol( mol ):
        match, mList = EmbedLib.MatchPharmacophoreToMol( mol, feat_fact, pcophore)
        if match:
                res = []
                num_match = len( mList )
                for i in range( num_match ):
                        num_feature = len( mList[i] )
                        for j in range( num_feature ):
                                print mList[i][j].GetAtomIds(), mList[i][j].GetFamily()
                bounds = rdDistGeom.GetMoleculeBoundsMatrix( mol )
                pList = EmbedLib.GetAllPharmacophoreMatches( mList, bounds, pcophore )
                #pList = EmbedLib.MatchPharmacophore( mList, bounds, pcophore )
                print pList
                #print raw_input("-----")
                num_match = len( pList )
                print num_match
                phMatches = []
                for i in range( num_match ):
                        num_feature = len( pList[i] )
                        phMatch = []
                        for j in range( num_feature ):
                                phMatch.append( pList[i][j].GetAtomIds() )
                        phMatches.append( phMatch )
                for phMatch in phMatches:
                        bm, embeds, nFail = EmbedLib.EmbedPharmacophore( mol, phMatch, pcophore, count=20, silent=1 )
                        print "-----> embeds num:", len( embeds )
                        for embed in embeds:
                                AllChem.UFFOPtimizeMolecule( embed )
                                align_data = rdAliginment.GetAlignmetTransform( bm, bounds )
                                AllChem.TransformMol( embed, align_data[1] )
                                res.append( embed )
                return res
                
print "test!"
w = Chem.SDWriter( "out.sdf" )

res = check_mol( mols[0] )
print res
=======
def check_mol( mols, FeatFact, pcophore ):
	# define FeatFact To Do
	matched_mols = []
	for mol in mols:
		match, mList = EmbedLib.MatchPharmacophoreToMol( mol, FeatFact, pcophore )
		if match:
			matched_mols.append( mol )
			num_match = len( mList )
			for i in range( num_match ):
				num_feature = len( mList[i] )
				for j in range( num_feature ):
					print mList[i][j].GetAtomIds()
	print len( matched_mols )
	return matched_mols



>>>>>>> origin/master
