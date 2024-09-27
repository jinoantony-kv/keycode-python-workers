# Function to connect to the PostgreSQL database
import os
import psycopg2
from psycopg2.extras import DictCursor

def get_db_connection():
    """Establish a database connection and return the connection object."""
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        print("Connected to the database successfully")
        return connection
    except Exception as error:
        print(f"Error connecting to the database: {error}")
        return None


# Function to perform a raw query
def perform_query(query, params=None):
    """Perform a raw SQL query."""
    connection = get_db_connection()
    results = []
    if connection:
        try:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    results = cursor.fetchall()  # For SELECT queries
                    # Convert results to a list of dictionaries
                    results = [dict(row) for row in results]
                    print(f"Query result: {results}")
                else:
                    connection.commit()  # For non-SELECT queries
                    print("Query executed successfully")
        except Exception as e:
            print(f"Error executing query: {e}")
        finally:
            connection.close()
    return results