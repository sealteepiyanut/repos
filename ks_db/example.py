from sqlalchemy import *

db = create_engine('sqlite:///ks_comp.db')
metadata = MetaData(bind=db, reflect=True)
table = metadata.tables['kinase_sarfali']