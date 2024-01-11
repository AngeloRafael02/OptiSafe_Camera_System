
from customExcepts import UnequalArrayLengthException
from dotenv import load_dotenv
from typing import List
import psycopg2.extras
import psycopg2
import os

load_dotenv()
def connect():
    conn = psycopg2.connect(
        host= os.getenv('DB_HOST'),
        database= os.getenv('DB_NAME'),
        user= os.getenv('DB_USER'),
        password= os.getenv('DB_PASSWORD'),
        sslmode='require',
        )
    return conn

def upload_metadata(filename:str,fileLoc:str,hostName:str,datetime,array:List[int]):
    '''Uploads Screenshot Metadata to postgres Database (NeonDB)'''
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(
            query='INSERT INTO ppe_log (photoName,photoURL,hostName,dateAndTime,apronCount,bunnysuitCount,maskCount,glovesCount,gogglesCount,headcapCount) VALUES (%s, %s, %s,%s, %s, %s, %s, %s,%s)',
            vars=(filename, fileLoc,hostName ,datetime, array[0], array[1], array[2], array[3], array[4], array[5])
            )
        conn.commit()
        cur.close()
    except psycopg2.InterfaceError as e:
        print('{} - connection will be reset'.format(e))
        # Close old connection 
        if conn:
            if cur:
                cur.close()
            conn.close()
        conn = None
        cur = None
        #Reconnect
        conn = connect()
        conn.cursor()

def generate_sql_condition(isEmptyArr:List[bool], columnArr, finalString:str)->str:
    """Generates WHERE Condition to Database Query where column = 0.
    Specifically, a False value in isEmptyArr on a certain index 
    corresponds to a 0 value to the column named according to the same index in columnArr 
    Returns : String
    NOTE: isEmptyArr must have teh same length as columnArr"""
    try:
        if len(isEmptyArr) != len(columnArr): 
            raise UnequalArrayLengthException()            
        conditions = []
        for i, isEmpty in enumerate(isEmptyArr):
            if not isEmpty:
                conditions.append(f"{columnArr[i]} = 0")
        if conditions:
            condition_str = ' OR '.join(conditions)
            finalString += condition_str
        else:
            finalString += '1=1'  # If no conditions, default to true condition
        return finalString    
    except Exception as e:
        return str(e)
    

def get_logs(options:str="today", DetectArr:List[bool] = [True, True, True, True, True, True]):
    """Get Logs depending on options parameter"""
    colArr = ('apronCount', 'bunnysuitCount', 'maskCount', 'glovesCount', 'gogglesCount', 'headcapCount')
    finalStr = 'Where '
    try:
        conn = connect()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if options == "today":
            query = f'SELECT * FROM todayRows ORDER BY dateAndTime ${generate_sql_condition(DetectArr,colArr,finalStr)} DESC'
            cur.execute(
                query='SELECT * FROM todayRows ORDER BY dateAndTime DESC'
            )
            rows = cur.fetchall()
            cur.close()
            return rows
        elif options == "all":
            query = "SELECT photoName,photoURL,hostName,dateAndTime,apronCount,bunnysuitCount,maskCount,glovesCount,gogglesCount,headcapCount FROM ppe_log "+generate_sql_condition(DetectArr,colArr,finalStr)
            print(query)
            cur.execute(query)
            rows = cur.fetchall()
            cur.close()
            return rows
    except psycopg2.InterfaceError as e:
        print('{} - connection will be reset'.format(e))
        # Close old connection 
        if conn:
            if cur:
                cur.close()
            conn.close()
        conn = None
        cur = None
        #Reconnect
        conn = connect()
        conn.cursor()
    except Exception as e:
        return str(e)
    
def get_log_cols():
    """Get Columns of ppe_log table"""
    try:
        conn = connect()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = 'SELECT * FROM allColumns'
        print(query)
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()
        return rows
    except Exception as e:
        return str(e)
        