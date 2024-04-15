**databarge | simple ETL tools for SQL Server**

<h1>About</h1>

This package includes but is not limited to:

1. A class to create a connection to SQL Server.
2. A class to transfer data from one SQL Server to another.
3. Functionality to perform basic data transformations.
3. Classes to transfer data between SQL Server and text files.
4. Functions to execute code as well as trap and log errors.
5. Functions to execute local SQL files.
6. Functions to update dimension tables.

Key notes:

1. The data is transfered in chunks of 10,000 to optimise memory usage
2. Enabling logging will produce a file that records each chunk of data transfered.

<h1>Dependencies</h1>

**python 3.8 is required for this package**

**Required Packages**

| Package	| Version	| License						|
|---------------|---------------|-------------------------------------------------------|
| pandas	| 1.3.5		| OSI Approved :: BSD License				|
| SQLAlchemy	| 1.4.27		| MIT License (MIT)					|

<h1>Config</h>

<h2>Create and populate a local config_params.ini file</h2>

Windows authentication example:

    [SOMEUSERFRIENDLYSERVERNAME]
    platform=sql_server
    server=SOMESERVERNAME
    database=SOMEDATABASE
    authentication=windows
    
Server authentication example:

    [SOMEOTHERUSERFRIENDLYSERVERNAME]
    platform=sql_server
    server=SOMESERVERNAME
    database=SOMEDATABASE
    authentication=server
    uid=SOMEGENERICUSERNAME
    pwd=SOMEGENERICPASSWORD

<h1>ETL</h>
    
<h2>Define the parameters and create the connections</h2>

    # import modules
    import sqlalchemy
    
    # import objects
    from databarge import SqlServerConnection, Etl
    
    # define mandatory generic variables
    config_params_path = r'xxx\config_params.ini'
    
    # define optional generic variables
    log_path = r'xxx\log.log'
    
    # make connections
    source_connection = SqlServerConnection('MSSQLSVRA', config_params_path)
    destination_connection = SqlServerConnection('MSSQLSVRB', config_params_path)
   
<h2>Create an ETL class</h2>

**Positional arguments:**

    # define positional etl class variables
    source_sql = r'''SELECT * FROM TESTDB.dbo.tbl_test'''
    destination_database = 'TESTDB'
    destination_table = 'tbl_test'
    
    # define optional etl class variables
    xforms = [
        "df['test_id'] = df['test_id'].astype(str)"
        , "df['test_value'] = df['test_quantity'] * df['test_rate']"
        , "df = df.drop(['test_quantity','test_rate'], axis = 1, inplace=True)"
        ]
    dtypes = {'test_text':sqlalchemy.types.NVARCHAR(length=100)}
    # destination_schema = 'someschema'
    
    # create etl class
    etl_1 = Etl(source_sql, destination_database, destination_table, source_connection, destination_connection
        , xforms = xforms
        , dtypes = dtypes
        # , destination_schema=destination_schema
        , log_path=log_path)

<h2>Create other ETL classes and put them all in a list</h2>

    # create other etl classes as required
    
    # create a list of etl classes
    xfers = [
        etl_1
        # , etl_2
        ]

<h2>Execute the ETL classes</h2>

    # iterate through the etl list and execute the etl classes
    for xf in xfers:
        
        # either drop or truncate the destination table
        xf.drop_table()
        # xf.truncate_table()
        
        # transfer the data
        xf.transfer_data()

<h1>Disclaimer</h1>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.