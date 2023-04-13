import yaml
import os
import mysql.connector
import pandas as pd


def load_db_credentials(config_file_path=None):
    """
    This function returns the needed credentials to run the service.

    Param path: path to the file containing the credentials
    return: dict of configuration strings
    """
    
    try:
        if config_file_path is None:
            
            base_path = os.getcwd()
            operating_system = os.name

            print("######################################", operating_system)

            #try first for a windows os
            if operating_system == "nt": 
                config_file_path = base_path +"\\poc-cfg\\db.yml"
            elif operating_system == "posix":
                config_file_path = base_path + "/poc-cfg/db.yml"

            with open(config_file_path) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
            return data
                
    except:
        raise

def get_database_schema() -> pd.DataFrame():
    """ Function gets MySQL database schema """
    
    credentials = load_db_credentials()

    #Connect to server
    con = mysql.connector.connect(
        host=credentials['hostname'],
        port=credentials['port'],
        user=credentials['username'],
        password=credentials['password'],
        db=credentials['database']
    )
    
    #Get cursor
    cur = con.cursor()

    cur.execute("SHOW TABLES")  #Query to show all tables avaliable in DB
    
    #Print all tables avaliable in DB 
    tables = []
    for (table_name,) in cur:
        #print(table_name)
        tables.append(table_name)
        
        
    table_name ,col_names, col_format = [], [], []
    for table in tables:
        cur.execute(f""" SHOW COLUMNS FROM {table};""")  #same as: cur.execute(f""" DESCRIBE {tables}; """)
        result = cur.fetchall()
    
        for i in result:
            col_names.append(i[0])
            col_format.append(i[1])
            table_name.append(table)
    
    df = pd.DataFrame({'table':table_name, 
                   'cols':col_names,
                   'format':col_format})
    
    return df


def extract_schema_str(schema, table) -> str():
    """ Extracts the schema in a form of string """
    str_ = ''
    df = schema.loc[schema['table']== table]
    
    idx = 0
    for i,item in df.iterrows():
        if idx == 0:
            str_ += df['table'][i] + ' '
            str_ += '('
        idx += 1
        
        str_ += df['cols'][i]
        str_ += ', '
    
    str_ = str_[:-1] + ')\n'
    
    return str_

def execute_query(query, results_as_dict=False):
    credentials = load_db_credentials()
    #Connect to server
    con = mysql.connector.connect(
        host=credentials['hostname'],
        port=credentials['port'],
        user=credentials['username'],
        password=credentials['password'],
        db=credentials['database']
    )

    #Get cursor
    if results_as_dict:
        cur = con.cursor(dictionary=True)
    else:
        cur = con.cursor()
    #Get cursor
    cur.execute(f"{query}")

    rez = cur.fetchall()
    #print('rez: ',rez)
    return rez

def get_cols_from_query(q) -> list():
    """ Function gets column names from query and returns list """

    x = len('SELECT')
    first_s_pos = q.find('SELECT')
    first_f_pos = q.find('FROM')
    text_raw = q[first_s_pos+x:first_f_pos]
    col_l = text_raw.strip().split(',')

    return col_l


def test_query(q):
    """ Functions test query from chatGpt/Codex and returns feedback information about query"""
    query = q.strip().lower()

    #Tests 
    test_semi = query[-10:].find(';') #Checks last 10 characters if there is semicolon in query
    test_select = query.find('select')
    test_where = query.find('where')
    test_from = query.find('from')

    #ToDo: more tests? order_by, group_by,joins etc. but its specific to database env

    rez_negative = {}
    rez_pos = {}

    #ToDo: This can be written better - loop 
    if test_semi == -1:
        rez_negative['semicolon'] = False
    else:
        rez_pos['semicolon'] = True
    if test_select == -1:
        rez_negative['select'] = False
    else:
        rez_pos['select'] = True
    if test_where == -1:
        rez_negative['where'] = False
    else:
        rez_pos['where'] = True
    if test_from == -1:
        rez_negative['from'] = False
    else:
        rez_pos['from'] = True

    return rez_pos, rez_negative

def format_database_schema():
    schema = get_database_schema()
    #All tables avaliable in your database
    all_tables_list = list(schema['table'].unique())

    # Hashtags matter!
    database_schema_string = "### MySQL tables, with their properties:\n"
    i = 0
    for table in all_tables_list:
        if i == 0:
            hashtag = '# '
        else:
            hashtag = '# '
        tmp_str  = extract_schema_str(schema, table)
        database_schema_string += hashtag+tmp_str
        i=+1
    
    return database_schema_string