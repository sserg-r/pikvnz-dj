import psycopg2
from sshtunnel import SSHTunnelForwarder

try:
    with SSHTunnelForwarder(
        ('80.94.160.207',22),
        # ('192.168.251.190', 22),
        ssh_password='wjY@pa75nZTi9xZ9A',
        ssh_username='user', 
        remote_bind_address=('localhost', 5432)) as server:        
        server.start()
        print ("server connected")


        print(str(server.local_bind_port))

        params = {
            'database': 'gispik',
            'user': 'postgres',
            'password': '1',
            'host': 'localhost',
            'port': server.local_bind_port
            }

        conn = psycopg2.connect(**params)
        curs = conn.cursor()
        print ("database connected")

except:
    print ("Connection Failed")


# DATABASES={'default':{
#                     'NAME': 'gispik', 
#                     'USER': 'postgres', 
#                     'PASSWORD': '1', 
#                     'HOST': 'localhost', 
#                     'PORT': ssh_tunnel.local_bind_port, 
#                     'CONN_MAX_AGE': 600, 
#                     'ENGINE': 'django.db.backends.postgresql_psycopg2'}}