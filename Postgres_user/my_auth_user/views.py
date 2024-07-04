# users/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from serializer import LoginSerializer, RegisterSerializer, UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })



class UserDetailsView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        current_user = request.user
        return Response({
            'current_user': current_user.username,
            'users': serializer.data
        })



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import psycopg2
import mysql.connector
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Database connection details
postgres_source_config = {
    'dbname': 'techto',
    'user': 'pradheep',
    'password': 'wessco@123',
    'host': 'localhost',
    'port': '5432'
}

postgres_target_config = {
    'dbname': 'all_users',
    'user': 'pradheep',
    'password': 'wessco@123',
    'host': 'localhost',
    'port': '5432'
}

mysql_config = {
    'database': 'testing',
    'user': 'groot',
    'password': 'Prad@246',
    'host': 'localhost'
}

def fetch_users_from_postgres(config):
    try:
        connection = psycopg2.connect(**config)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                id, password, date_joined, last_login, is_superuser, username, 
                first_name, last_name, email, is_staff, is_active 
            FROM auth_user
        """)  # Replace with the correct table name if different
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        logger.debug(f"Fetched {len(users)} users from PostgreSQL")
        return users
    except Exception as error:
        logger.error(f"Error fetching users from PostgreSQL: {error}")
        return []

def fetch_users_from_mysql(config):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                id, password, date_joined, last_login, is_superuser, username, 
                first_name, last_name, email, is_staff, is_active 
            FROM auth_user
        """)  # Replace with the correct table name if different
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        logger.debug(f"Fetched {len(users)} users from MySQL")
        return users
    except Exception as error:
        logger.error(f"Error fetching users from MySQL: {error}")
        return []

def insert_users_into_postgres(config, users):
    try:
        connection = psycopg2.connect(**config)
        cursor = connection.cursor()
        for user in users:
            cursor.execute("""
                INSERT INTO auth_user (id, password, date_joined, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    password = EXCLUDED.password,
                    date_joined = EXCLUDED.date_joined,
                    last_login = EXCLUDED.last_login,
                    is_superuser = EXCLUDED.is_superuser,
                    username = EXCLUDED.username,
                    first_name = EXCLUDED.first_name,
                    last_name = EXCLUDED.last_name,
                    email = EXCLUDED.email,
                    is_staff = EXCLUDED.is_staff,
                    is_active = EXCLUDED.is_active
            """, user)
        connection.commit()
        cursor.close()
        connection.close()
        logger.debug("Users inserted/updated in PostgreSQL successfully")
    except Exception as error:
        logger.error(f"Error inserting users into PostgreSQL: {error}")

class SyncUsersView(APIView):
    def get(self, request):
        logger.debug("Fetching users from PostgreSQL source database")
        postgres_users = fetch_users_from_postgres(postgres_source_config)
        logger.debug(f"Fetched {len(postgres_users)} users from PostgreSQL source database")

        logger.debug("Fetching users from MySQL source database")
        mysql_users = fetch_users_from_mysql(mysql_config)
        logger.debug(f"Fetched {len(mysql_users)} users from MySQL source database")
        
        all_users = postgres_users + mysql_users
        logger.debug(f"Total users to insert: {len(all_users)}")
        
        insert_users_into_postgres(postgres_target_config, all_users)
        
        return Response({"message": "Users synchronized successfully"}, status=status.HTTP_200_OK)

class GetUsersView(APIView):
    def get(self, request):
        try:
            connection = psycopg2.connect(**postgres_target_config)
            cursor = connection.cursor()
            cursor.execute("""
                SELECT 
                    id, password, date_joined, last_login, is_superuser, username, 
                    first_name, last_name, email, is_staff, is_active 
                FROM auth_user
            """)  # Replace with the correct table name if different
            users = cursor.fetchall()
            cursor.close()
            connection.close()
            return Response(users, status=status.HTTP_200_OK)
        except Exception as error:
            logger.error(f"Error fetching users from target PostgreSQL: {error}")
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# myapp/views.py

# myapp/views.py

# myapp/views.py

# myapp/views.py
# myapp/views.py
# myapp/views.py
# myapp/views.py

# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.db import connections
# from .models import User

# class SyncAllUsersView(APIView):
#     def get(self, request):
#         try:
#             # Fetch data from MySQL
#             with connections['mysql_db'].cursor() as mysql_cursor:
#                 mysql_cursor.execute("SELECT id, password, date_joined, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active FROM auth_user")
#                 mysql_users = mysql_cursor.fetchall()

#             # Fetch data from PostgreSQL
#             with connections['default'].cursor() as postgres_cursor:
#                 postgres_cursor.execute("SELECT id, password, date_joined, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active FROM auth_user")
#                 postgres_users = postgres_cursor.fetchall()

#             # Combine the user data
#             combined_users = tuple(mysql_users) + tuple(postgres_users)

#             # Insert combined data into the 'all_users' database
#             with connections['postgres_db'].cursor() as all_users_cursor:
#                 all_users_cursor.execute("DELETE FROM users")  # Clear existing data
#                 for user in combined_users:
#                     all_users_cursor.execute(
#                         "INSERT INTO users (id, password, date_joined, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
#                         user
#                     )

#             # Fetch and return the combined data from the 'all_users' database
#             with connections['postgres_db'].cursor() as all_users_cursor:
#                 all_users_cursor.execute("SELECT * FROM users")
#                 rows = all_users_cursor.fetchall()

#             # Serialize the combined data
#             users = []
#             for row in rows:
#                 user_dict = {
#                     'id': row[0],
#                     'password': row[1],
#                     'date_joined': row[2],
#                     'last_login': row[3],
#                     'is_superuser': row[4],
#                     'username': row[5],
#                     'first_name': row[6],
#                     'last_name': row[7],
#                     'email': row[8],
#                     'is_staff': row[9],
#                     'is_active': row[10],
#                 }
#                 users.append(user_dict)

#             serializer = UserSerializer(data=users, many=True)
#             serializer.is_valid(raise_exception=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Assuming your view is located in myapp/views.py

# Assuming your view is located in myapp/views.py
# Assuming your view is located in myapp/views.py
# Assuming your view is located in myapp/views.py
# Assuming your view is located in myapp/views.py
# Assuming your view is located in myapp/views.py
# Assuming your view is located in myapp/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connections
from .models import User  # Import your User model

class SyncAllUsersView(APIView):
    def get(self, request):
        try:
            # Fetch data from MySQL database 'testing'
            with connections['mysql_db'].cursor() as mysql_cursor:
                mysql_cursor.execute("SELECT id, password, date_joined, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active FROM auth_user")
                mysql_users = list(mysql_cursor.fetchall())

            # Fetch data from PostgreSQL database 'techto'
            with connections['default'].cursor() as postgres_cursor:
                postgres_cursor.execute("SELECT id, password, date_joined, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active FROM auth_user")
                postgres_users = list(postgres_cursor.fetchall())

            # Combine the user data from both databases
            combined_users = mysql_users + postgres_users

            # Insert combined data into the 'users' table within 'all_users' PostgreSQL database
            with connections['postgres_db'].cursor() as all_users_cursor:
                all_users_cursor.execute("TRUNCATE TABLE users RESTART IDENTITY")  # Clear existing data in 'users' table
                for user in combined_users:
                    all_users_cursor.execute(
                        "INSERT INTO users (id, password, date_joined, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (user[0], user[1], user[2], user[3], bool(user[4]), user[5], user[6], user[7], user[8], bool(user[9]), bool(user[10]))
                    )

            # Fetch and return the combined data from the 'users' table within 'all_users' database
            with connections['postgres_db'].cursor() as all_users_cursor:
                all_users_cursor.execute("SELECT * FROM users")
                rows = all_users_cursor.fetchall()

            # Prepare data for serialization
            users = []
            for row in rows:
                user_dict = {
                    'id': row[0],
                    'password': row[1],
                    'date_joined': row[2],
                    'last_login': row[3],
                    'is_superuser': row[4],
                    'username': row[5],
                    'first_name': row[6],
                    'last_name': row[7],
                    'email': row[8],
                    'is_staff': row[9],
                    'is_active': row[10],
                }
                users.append(user_dict)

            # Serialize the combined data
            serializer = UserSerializer(data=users, many=True)
            serializer.is_valid(raise_exception=True)

            # Return serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
