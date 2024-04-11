def database_alter(self,database_name:str, data_retention_time_in_days:int, comment:str, owner:str, tags:list, grants:list, tags_to_remove:list, grants_to_remove:list):
    cur = self._conn.cursor()
    query = ''
    try:
        query = 'ALTER DATABASE identifier(%s) SET '
        params = [database_name]
        if data_retention_time_in_days is not None:
            query += ' DATA_RETENTION_TIME_IN_DAYS = %s'
            params.append(data_retention_time_in_days)
        if comment is not None:
            query += ' COMMENT = %s'
            params.append(comment)
        if len(params) > 1: # something to execute
            cur.execute(query, params)

        if tags is not None and tags != []:
            for t in tags:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                query = 'ALTER DATABASE identifier(%s) SET TAG identifier(%s) = %s;'
                params = (database_name,tag_key,tag_val)
                cur.execute(query,params)
        if owner is not None:
            query = '''
                GRANT OWNERSHIP ON DATABASE identifier(%s) TO ROLE identifier(%s) COPY CURRENT GRANTS;
            '''
            cur.execute(query,(database_name, owner))

        if grants is not None:
            for grant in grants:
                grant_keys = grant.keys()
                grant_option = grant['GRANT_OPTION'] if 'GRANT_OPTION' in grant_keys else False
                role = ''
                permission = ''
                for key in grant_keys:
                    if key != 'GRANT_OPTION':
                        role = key
                        permission = grant[key]
                if role != '' and permission != '':
                    query = "GRANT " + permission + " ON DATABASE identifier(%s) TO ROLE " + role + ";"
                    cur.execute(query,(database_name))
                else:
                    raise Exception('Invalid grants for database: ' + database_name)

        if tags_to_remove is not None:
            for tag in tags_to_remove:
                for tag_name in tag.keys():
                    query = 'ALTER DATABASE identifier(%s) UNSET TAG identifier(%s);'
                    params = (database_name,tag_name)
                    cur.execute(query,params)

        if grants_to_remove is not None:
            for grant in grants_to_remove:
                for role_name in grant.keys():
                    permission = grant[role_name]
                    query = "REVOKE " + permission + " ON DATABASE identifier(%s) FROM ROLE " + role_name + ";"
                    cur.execute(query,(database_name))

    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()

#CREATE [ OR REPLACE ] [ TRANSIENT ] DATABASE [ IF NOT EXISTS ] <name>
#    [ CLONE <source_db>
#          [ { AT | BEFORE } ( { TIMESTAMP => <timestamp> | OFFSET => <time_difference> | STATEMENT => <id> } ) ] ]
#    [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
#    [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
#    [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
#    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
#    [ COMMENT = '<string_literal>' ]