from pg_python.pg_python import write

db_name = 'test'
username = 'postgres'
password = 'admin'
host_address = 'localhost'

table_name = 'pg_mock_tb'
col_data = {'col1': '55', 'col2': 'test_data', 'col3': 'dataaaa'}


write(table_name, col_data)