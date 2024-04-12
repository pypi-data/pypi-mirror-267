import pandas as pd

def csv(file_path, **kwargs):
    """
    Read a CSV file into a DataFrame.
    
    Parameters:
    file_path : str
        Path to the CSV file.
    **kwargs : dict
        Additional keyword arguments to pass to pd.read_csv.
    
    Returns:
    DataFrame
        A DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(file_path, **kwargs)

def excel(file_path, sheet_name=0, **kwargs):
    """
    Read an Excel file into a DataFrame.
    
    Parameters:
    file_path : str
        Path to the Excel file.
    sheet_name : str, int, list, or None, default 0
        Name or index of the sheet in the Excel file to read. 
        If None, it reads all sheets.
    **kwargs : dict
        Additional keyword arguments to pass to pd.read_excel.
    
    Returns:
    DataFrame or dict of DataFrames
        A DataFrame containing the data from the Excel file.
    """
    return pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)

def json(file_path, **kwargs):
    """
    Read a JSON file into a DataFrame.
    
    Parameters:
    file_path : str
        Path to the JSON file.
    **kwargs : dict
        Additional keyword arguments to pass to pd.read_json.
    
    Returns:
    DataFrame
        A DataFrame containing the data from the JSON file.
    """
    return pd.read_json(file_path, **kwargs)

def html(url, **kwargs):
    """
    Read HTML tables into a list of DataFrames.
    
    Parameters:
    url : str
        URL of the HTML page.
    **kwargs : dict
        Additional keyword arguments to pass to pd.read_html.
    
    Returns:
    list of DataFrames
        A list containing DataFrames representing the HTML tables.
    """
    return pd.read_html(url, **kwargs)

def sql_query(sql, con, **kwargs):
    """
    Read SQL query into a DataFrame using a SQL database connection.
    
    Parameters:
    sql : str
        SQL query to be executed.
    con : SQLAlchemy engine or DBAPI2 connection
        Connection object to the database.
    **kwargs : dict
        Additional keyword arguments to pass to pd.read_sql_query.
    
    Returns:
    DataFrame
        A DataFrame containing the result set of the query.
    """
    return pd.read_sql_query(sql, con, **kwargs)

def sql_table(table_name, con, **kwargs):
    """
    Read SQL database table into a DataFrame.
    
    Parameters:
    table_name : str
        Name of the SQL table.
    con : SQLAlchemy engine or DBAPI2 connection
        Connection object to the database.
    **kwargs : dict
        Additional keyword arguments to pass to pd.read_sql_table.
    
    Returns:
    DataFrame
        A DataFrame containing the data from the SQL table.
    """
    return pd.read_sql_table(table_name, con, **kwargs)
