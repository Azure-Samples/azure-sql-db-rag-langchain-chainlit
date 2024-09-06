import json
import os
import pyodbc
import struct
import logging
from azure import identity

def get_mssql_connection(source_variable_name: str) -> pyodbc.Connection:
    logging.info('Getting MSSQL connection')
    mssql_connection_string = os.environ[source_variable_name]    
    if any(s in mssql_connection_string.lower() for s in ["uid"]):
        logging.info('Using SQL Server authentication')
        attrs_before = None
    else:
        logging.info('Getting EntraID credentials...')            
        credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)    
        token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")    
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h        
        attrs_before = {SQL_COPT_SS_ACCESS_TOKEN: token_struct}

    logging.info('Connecting to MSSQL...')    
    conn = pyodbc.connect(mssql_connection_string, attrs_before=attrs_before)
    logging.info('Connected to MSSQL.')    

    return conn

def get_similar_sessions(search_text:str) -> str:
    conn = get_mssql_connection("AZURE_SQL_CONNECTION_STRING")
    logging.info("Querying MSSQL...")
    logging.info(f"Message content: '{search_text}'")
    try:        
        cursor = conn.cursor()            
        results = cursor.execute("SET NOCOUNT ON; EXEC web.find_sessions @text=?", (search_text)).fetchall()

        logging.info(f"Found {len(results)} similar sessions.")

        payload = ""
        for row in results:
            description = str(row[2]).replace("\n", " ")
            speakers = ", ".join(json.loads(row[7]))    
            payload += f'{row[1]}|{description}|{speakers}|{row[4]}|{row[5]}' 
            payload += "\n"
    
        return payload    
    finally:
        cursor.close()    

if __name__ == "__main__":
    print(get_similar_sessions("SQL and AI"))