from snowflake.connector import DictCursor
def object_check_exists(self,object_full_name: str)->bool:
    cur = self._conn.cursor(DictCursor)
    schema_name = object_full_name.split('.')[1]
    database_name = object_full_name.split('.')[0]
    schema_with_db_name = database_name + '.' + schema_name
    object_name = object_full_name.split('.')[2]
    #query = '''
    #    SHOW TABLES LIKE %s in schema identifier(%s);
    #'''
    query = '''
        SELECT TABLE_OWNER, date_part(epoch_second, LAST_DDL) as LAST_DDL FROM "''' + database_name + '''".INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s and TABLE_NAME = %s;
    '''
    try:
        cur.execute(query, (schema_name, object_name))
        rowcount = 0
        owner = None
        last_ddl = None
        for rec in cur:
            if rowcount == 0:
                rowcount+=1
                #owner = rec["owner"]
                owner = rec["TABLE_OWNER"]
                last_ddl = rec["LAST_DDL"]
        exists = True if rowcount > 0 else False 
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()
    return exists, owner, last_ddl
