import os, sys, cPickle, gzip
from rdkit import Chem
from rdkit import RDConfig
from rdkit import Geometry
from rdkit.Chem import ChemicalFeatures
from rdkit.Chem.Pharm3D import Pharmacophore, EmbedLib
from rdkit.Chem import rdDistGeom
from rdkit.Chem.FeatMaps import FeatMapPoint
from rdkit.Numerics import rdAlignment
from rdkit import DistanceGeometry as DG
from rdkit.Chem import AllChem
from sets import Set
import argparse

parser = argparse.ArgumentParser(description="search pharmacophore matched mols")
parser.add_argument( "-p", "--pharmacophore", type=str, help = "input pharmacophore.pkl" , required=True)
parser.add_argument( "-i", "--input", type=str, help = "input yourquerymols.sdf" , required=True)
parser.add_argument( "-o", "--output", type=str, help = "input output file name" ,default = "res.sdf" )
args = parser.parse_args()
print args

# feature Def
feat_def = "BaseFeatures_seri.fdef"
feat_fact = AllChem.BuildFeatureFactoryFromString(file(feat_def,"r").read())

# To Do write option parser

inF = args.input
outF = args.output
p4core = args.pharmacophore

#mols = [ mol.RemoveAllConformers() for mol in Chem.SDMolSupplier( inF )]
mols = [ mol for mol in Chem.SDMolSupplier( inF )]
print len(mols)
#print raw_input("--->>>")


f = open( p4core , "rb" )
pcophore = cPickle.load( f )
print pcophore
ref_mat = [ list(x.GetPos()) for x in pcophore.getFeatures() ]

def check_mol( mol ):
        res=[]
        mol.RemoveAllConformers()
        match, mList = EmbedLib.MatchPharmacophoreToMol( mol, feat_fact, pcophore )
        #mList = [ m for m in Set( mList ) ]
        if match:
                num_match = len( mList )
                for i in range( num_match ):
                        num_feature = len( mList[i] )
                        for j in range( num_feature ):
                                print mList[i][j].GetAtomIds(), mList[i][j].GetFamily()
                bounds = rdDistGeom.GetMoleculeBoundsMatrix( mol )
                pList = EmbedLib.GetAllPharmacophoreMatches( mList, bounds, pcophore )
                num_match = len( pList )
                phMatches = []
                for i in range( num_match ):
                        num_feature = len( pList[i] )
                        phMatch = []
                        for j in range( num_feature ):
                                phMatch.append( pList[i][j].GetAtomIds() )

                        phMatches.append( phMatch )
                for phMatch in phMatches:
                        bm, embeds, nFail = EmbedLib.EmbedPharmacophore( mol, phMatch, pcophore, count=5, silent=1 )
                        print "-----> embeds num:", len( embeds )
                        for embed in embeds:
                                AllChem.UFFOptimizeMolecule( embed )
                                feats = feat_fact.GetFeaturesForMol( embed )
                                feats_dict = GetFeatsPerAtoms( feats )
                                match_feats = [feats_dict[atomid] for atomid in phMatch]
                                pro_mat = [ list(feat.GetPos()) for feat in match_feats ]
                                align_data = rdAlignment.GetAlignmentTransform( ref_mat , pro_mat, maxIterations=200 )
                                AllChem.TransformMol( embed, align_data[1] )
                                print align_data[0]
                                print align_data[1]
                                res.append( embed )
        else:
                print "no hits"
        return res

def GetFeatsPerAtom(feats):
  """  Returns a dictionary keyed by atom id, with lists of features as
   the values

  """
  res = {}
  for feat in feats:
    for atomId in feat.GetAtomIds():
      if res.has_key(atomId):
        res[atomId].append(feat)
      else:
        res[atomId] = [feat]
  return res

def GetFeatsPerAtoms(feats):
        """  Returns a dictionary keyed by atom id, with lists of features asthe values"""
        res = {}
        for feat in feats:
                atomIds = feat.GetAtomIds()
                res[atomIds] = feat
        return res




if __name__ == "__main__":
        outfile = Chem.SDWriter( outF )
        for mol in mols:
                try:
                        ems = check_mol(mol)
                        for em in ems:
                                outfile.write( em )
                except:
                        print "Fail"
        outfile.close()
