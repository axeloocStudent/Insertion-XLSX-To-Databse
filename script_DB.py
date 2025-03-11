import mysql.connector
import pandas as pd
from datetime import datetime
import shutil



#filtering useless data 


#function --------------------

def filter_client(data) :
    if(data.shape[1]==10) :
         return data[data.iloc[:,-6:].isna().sum(axis=1)!=6]
    else: 
        return data
#-------------------------


cod_client=filter_client(pd.read_excel("Client_AS400.xlsx"))
cod_art=pd.read_excel("Article_AS400.xlsx")




now = datetime.now()
dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
logfile= "logInsert_"+dt_string+".log"


f=open(logfile,"a")
f.write(f"Operation times :{now.strftime('%d/%m/%Y %H:%M:%S')}\n")


#connecting to databse
try:
    connection = mysql.connector.connect(host='10.11.2.74',
                                         database='EDI_PORTAL',
                                         user='ediuser',
                                         password='XXXX')

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)

        #inserting data to the table COD_CLIENTS

       
        
        sql = "DELETE FROM COD_CLIENTS "
        cursor.execute(sql)
        connection.commit()
        print(cursor.rowcount, "record(s) was deleted in COD_CLIENTS.")
        f.write( f"{cursor.rowcount} record(s) was deleted in COD_CLIENTS.\n")
        
        sql = "INSERT INTO COD_CLIENTS VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val=[]
        if(cod_client.shape[1]==10):
            for i in range(len(cod_client)):
                elt=[str(e) for e in cod_client.iloc[i,:]]
                elt = list(map(lambda x: x.replace('nan', ''), elt))
                val.append(tuple(elt))
        

        try:
            if(cod_client.shape[1]!=10):
                raise ValueError('File contain wrong number of column')
            cursor.executemany(sql, val)
            print(cursor.rowcount, " record(s) was inserted in COD_CLIENTS.")
            f.write(f"{cursor.rowcount} record(s) was inserted in COD_CLIENTS.\n")
            #we overwrite the last backup file with the new one¨
            original=r'Client_AS400.xlsx'
            target=r'C:\Users\axgontie\Desktop\axel_gontier\scripts_ddbb\scripts_ddbb\backup\Client_AS400_backup.xlsx'
            shutil.copyfile(original,target)
            f.write("Succesfully replace backup Client file\n")
            

        except Exception as e:
            #we add the data from the file in /backup as we have deleted all line in the table without inserting any
            print('Insert Error in COD_CLIENTS:', e)
            f.write(f'Insert Error in COD_CLIENTS:{e}\n Inserting backup client file into the table\n')
            
            cod_client=filter_client(pd.read_excel("backup/Client_AS400_backup.xlsx"))
            try:
                sql = "INSERT INTO COD_CLIENTS VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val=[]
                for i in range(len(cod_client)):
                    elt=[str(e) for e in cod_client.iloc[i,:]]
                    elt = list(map(lambda x: x.replace('nan', ''), elt))
                    val.append(tuple(elt))

        
                cursor.executemany(sql, val)
                print(cursor.rowcount, " record(s) from BACKUP was inserted in COD_CLIENTS.")
                f.write(f"{cursor.rowcount} record(s) from BACKUP was inserted in COD_CLIENTS.\n")
            except Exception as e:
                print('Insert backup Error in COD_CLIENTS:', e)
                f.write(f'Insert backup Error in COD_CLIENTS:{e}\n')
            





        connection.commit()
        






        #inserting data to the table COD_ARTICLES
        sql = "DELETE FROM COD_ARTICLES "
        cursor.execute(sql)
        connection.commit()
        print(cursor.rowcount, "record(s) was deleted in COD_ARTICLES.")
        f.write( f"{cursor.rowcount} record(s) was deleted in COD_ARTICLES.\n")
        #inserting new data
        sql = "INSERT INTO COD_ARTICLES VALUES (%s, %s, %s)"
        val=[]
        for i in range(len(cod_art)):
            elt=[str(e) for e in cod_art.iloc[i,:]]
            elt = list(map(lambda x: x.replace('nan', ''), elt))
            val.append(tuple(elt))
        try:
            if(cod_art.shape[1]!=3):
                raise ValueError('File contain wrong number of column')
            cursor.executemany(sql, val)
            print(cursor.rowcount, " record(s) was inserted in COD_ARTICLES.")
            f.write(f"{cursor.rowcount} record(s) was inserted in COD_ARTICLES.\n")
            #we overwrite the last backup file with the new one
            original=r'Article_AS400.xlsx'
            target=r'C:\Users\axgontie\Desktop\axel_gontier\scripts_ddbb\scripts_ddbb\backup\Article_AS400_backup.xlsx'
            shutil.copyfile(original,target)
            f.write("Succesfully replace backup Article file\n")
        except Exception as e:
                #we add the data from the file in /backup as we have deleted all line in the table without inserting any
                print('Insert Error in COD_ARTICLES:', e)
                f.write(f'Insert Error in COD_ARTICLES:{e}\n Inserting backup client file into the table\n')
                
                cod_article=pd.read_excel("backup/Article_AS400_backup.xlsx")
                try:
                    sql = "INSERT INTO COD_ARTICLES VALUES (%s, %s, %s)"
                    val=[]
                    for i in range(len(cod_article)):
                        elt=[str(e) for e in cod_article.iloc[i,:]]
                        elt = list(map(lambda x: x.replace('nan', ''), elt))
                        val.append(tuple(elt))

            
                    cursor.executemany(sql, val)
                    print(cursor.rowcount, " record(s)  from BACKUP was inserted in COD_ARTICLES.")
                    f.write(f"{cursor.rowcount} record(s) from BACKUP was inserted in COD_ARTICLES.\n")
                except Exception as e:
                    print('Insert backup Error in COD_ARTICLES:', e)
                    f.write(f'Insert backup Error in COD_ARTICLES:{e}\n')

        connection.commit()
        f.close()                              
except Exception as e:
    print("Error while connecting to MySQL", e)    

