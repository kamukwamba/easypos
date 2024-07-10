import sqlite3




def create_db():
    create = sqlite3.connect("EasyPos.db")
    create.commit()
    create.close()

def create_user_credentials_db():
    create_user_cdb = sqlite3.connect("EasyPos.db")
    create_user_cdb.execute("CREATE TABLE user_cretdentials(uuid blob, user_name text,user_password text)")
    create_user_cdb.commit()
    create_user_cdb.close()


def create_user_creadentials(uuid,user_name, password,auth):
    create_user = sqlite3.connect()






def initialize_DBs():
    print("function running")
    try:
        create_db()
    except:
        print("DB ALREADY IN EXISTANCE")
    
    try:
        create_user_credentials_db()
    except:
        print("DB USER CRIDENTIALS ALREADY IN EXISTANCE")




initialize_DBs()