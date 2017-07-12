import sqlalchemy
import pandas as pd
import numpy as np
def get_con(server, username, password):
   return sqlalchemy.create_engine(('mssql+pymssql://{0}:{1}@' + server).format(username, password))
def get_avg_string_length(server, database, table, column, username, password):
   res = pd.read_sql_query(query, get_con(server, username, password))
   return res.iloc[0]['average']
srv = "server.hr.com"
db = "G_db"
usr = "ss"
pwd = "S"
query = 'select * from [dataBase].[dbo].[ANALYSIS_TABLE]' 
main_DF = pd.read_sql_query(query, get_con(srv, usr, pwd))
print(main_DF.shape)