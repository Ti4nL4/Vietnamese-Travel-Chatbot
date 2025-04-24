import psycopg2
import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

def install_pgvector():
    """Install the pgvector extension in the PostgreSQL database"""
    try:
        # First, check if pgvector is already installed
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()
        
        # Check if vector extension already exists
        cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        result = cur.fetchone()
        if result:
            print(f"pgvector extension is already installed (version: {result[2]})")
            cur.close()
            conn.close()
            return
        
        cur.close()
        conn.close()
        
        # If not installed, we need to install it using a different approach
        print("pgvector extension not found. Attempting to install...")
        
        # Method 1: Try using CREATE EXTENSION with a specific version
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT')
            )
            cur = conn.cursor()
            
            # Try with a specific version
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector VERSION '0.4.0';")
            conn.commit()
            print("Successfully installed pgvector extension version 0.4.0")
            
            # Verify the extension is installed
            cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
            result = cur.fetchone()
            if result:
                print(f"pgvector extension is installed (version: {result[2]})")
            else:
                print("Warning: pgvector extension was not found in pg_extension table")
            
            cur.close()
            conn.close()
            
        except Exception as e:
            print(f"Error with method 1: {str(e)}")
            
            # Method 2: Try using a different version
            try:
                conn = psycopg2.connect(
                    dbname=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASSWORD'),
                    host=os.getenv('DB_HOST'),
                    port=os.getenv('DB_PORT')
                )
                cur = conn.cursor()
                
                # Try with a different version
                cur.execute("CREATE EXTENSION IF NOT EXISTS vector VERSION '0.3.0';")
                conn.commit()
                print("Successfully installed pgvector extension version 0.3.0")
                
                cur.close()
                conn.close()
                
            except Exception as e2:
                print(f"Error with method 2: {str(e2)}")
                
                # Method 3: Try without specifying version
                try:
                    conn = psycopg2.connect(
                        dbname=os.getenv('DB_NAME'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'),
                        host=os.getenv('DB_HOST'),
                        port=os.getenv('DB_PORT')
                    )
                    cur = conn.cursor()
                    
                    # Try without specifying version
                    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                    conn.commit()
                    print("Successfully installed pgvector extension (default version)")
                    
                    cur.close()
                    conn.close()
                    
                except Exception as e3:
                    print(f"Error with method 3: {str(e3)}")
                    raise Exception("Failed to install pgvector extension using all methods")
        
    except Exception as e:
        print(f"Error installing pgvector extension: {str(e)}")
        raise

if __name__ == '__main__':
    install_pgvector() 