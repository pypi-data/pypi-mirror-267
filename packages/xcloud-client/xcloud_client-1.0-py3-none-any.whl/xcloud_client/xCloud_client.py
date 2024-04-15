import jaydebeapi

class xCloud_client:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def connect(self):

        try:
            """
            建立与数据库的连接
            """
            driver = 'com.bonc.xcloud.jdbc.XCloudDriver'
            #com\bonc\xcloud\jdbc
            url = 'jdbc:xcloud:@'+self.host+':'+self.port+'/SERVER_DATA?connectRetry=3&socketTimeOut=43200000&connectDirect=true&buffMemory=33554432'
            #user = config['acct_info']['user']  
            #password = config['acct_info']['password']
            jarFile = ['XCloudJDBC-2.10.6.7.jar','slf4j-api-1.7.5.jar','slf4j-log4j12-1.7.5.jar','slf4j-simple-1.7.5.jar','log4j-1.2.17.jar','libthrift-0.9.2.jar',
            'XCloudJDBC_SP_Procedure_Parser-0.1.3.jar'
            ,'lz4-1.3.0.jar'
            ]
            conn = jaydebeapi.connect(jclassname=driver, url=url, driver_args=[self.username, self.password], jars=jarFile)
            return conn
        except jaydebeapi.DatabaseError as e:
            print('the connection was not consistent ,because of {e}')
            raise

    def execute_query(self, query):
        """
        执行查询并返回结果
        """
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
        except jaydebeapi.Error as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            if conn:
                conn.close()
        return result
