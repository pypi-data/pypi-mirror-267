def row_access_policy_create(self,policy_full_name:str, SIGNATURE:list, RETURN_TYPE:str, OWNER:str, COMMENT:str, BODY:str, TAGS:list, GRANTS:list, DEPLOY_ROLE:str):
    # task_name = <db>.<schema>.<task_name>
    cur = self._conn.cursor()
    query = ''
    try:
        # OPTIONS:str, OWNER:str, TAGS:list, GRANTS:list
        sql_signature = ''
        cnt = 1
        for sig in SIGNATURE:
            for key in sig.keys():
                sql_signature += ', ' if cnt > 1 else ''
                sql_signature += key + ' ' + sig[key]
                cnt += 1

        sql_return_type = "  RETURNS " + RETURN_TYPE if RETURN_TYPE is not None and RETURN_TYPE != '' else ''
        sql_comment = "  COMMENT = '" + COMMENT + "' " if COMMENT is not None else ''

        query = "CREATE OR REPLACE ROW ACCESS POLICY " + policy_full_name + " AS (" + sql_signature + ")"
        query += sql_return_type
        query += ' -> '
        query += BODY
        query += sql_comment
        
        cur.execute(query)
        
        if TAGS is not None and TAGS != []:
            for t in TAGS:
                tag_key = list(t)[0]
                tag_val = t[tag_key]
                query = 'ALTER MASKING POLICY ' + policy_full_name + ' SET TAG identifier(%s) = %s;'
                params = (tag_key,tag_val)
                cur.execute(query,params)
                
        if OWNER is not None and OWNER != DEPLOY_ROLE: #if owner is deploy role, no need to run this:
            query = "GRANT OWNERSHIP ON MASKING_POLICY " + policy_full_name + " TO ROLE identifier(%s) COPY CURRENT GRANTS;"
            cur.execute(query,(OWNER))

        if GRANTS is not None:
            for grant in GRANTS:
                grant_keys = grant.keys()
                grant_option = grant['GRANT_OPTION'] if 'GRANT_OPTION' in grant_keys else False
                role = ''
                permission = ''
                for key in grant_keys:
                    if key != 'GRANT_OPTION':
                        role = key
                        permission = grant[key]
                if role != '' and permission != '':
                    query = "GRANT " + permission + " ON ROW ACCESS POLICY " + policy_full_name + " TO ROLE " + role + ";"
                    cur.execute(query)
                else:
                    raise Exception('Invalid grants for row access policy: ' + policy_full_name)
                
    except Exception as ex:
        msg = 'SQL Error:\n\nQuery: ' + query + '\n\nError Message:\n' + str(ex) + '\n\n'
        raise Exception(msg)
    finally:
        cur.close()


""" 
CREATE [ OR REPLACE ] ROW ACCESS POLICY [ IF NOT EXISTS ] <name> AS
( <arg_name> <arg_type> [ , ... ] ) RETURNS BOOLEAN -> <expression>
[ COMMENT = '<string_literal>' ]
"""