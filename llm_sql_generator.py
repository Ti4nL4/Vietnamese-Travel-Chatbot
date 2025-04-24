#!/usr/bin/env python3
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import argparse
import json
import requests
import time

# Load environment variables
load_dotenv()

# Database connection parameters
DB_PARAMS = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Ollama API endpoint
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/chat')

def connect_to_db():
    """Connect to the PostgreSQL database"""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        return None

def get_table_schema(conn, table_name):
    """Get the schema of a table"""
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))
        
        columns = cur.fetchall()
        cur.close()
        
        schema = {
            'table_name': table_name,
            'columns': [{'name': col['column_name'], 'type': col['data_type'], 'nullable': col['is_nullable']} 
                       for col in columns]
        }
        return schema
    except Exception as e:
        print(f"Error getting table schema: {str(e)}")
        return {}

def get_all_tables(conn):
    """Get all tables in the database"""
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        
        tables = [row[0] for row in cur.fetchall()]
        cur.close()
        return tables
    except Exception as e:
        print(f"Error getting tables: {str(e)}")
        return []

def execute_sql_query(conn, query):
    """Execute a SQL query and return the results"""
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(query)
        results = cur.fetchall()
        cur.close()
        return results
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        return []

def print_results(results):
    """Print query results in a readable format"""
    if not results:
        print("No results found")
        return
    
    # Get column names from the first result
    columns = list(results[0].keys())
    
    # Print header
    header = " | ".join(columns)
    print(header)
    print("-" * len(header))
    
    # Print rows
    for row in results:
        row_values = [str(row[col]) for col in columns]
        print(" | ".join(row_values))

def generate_sql_with_ollama(query, table_schemas, model="llama3.1"):
    """
    Generate SQL query using Ollama local model
    
    Args:
        query (str): Natural language query
        table_schemas (list): List of table schemas
        model (str): Ollama model name to use
        
    Returns:
        str: Generated SQL query
    """
    # Format the table schemas into a string
    schema_str = json.dumps(table_schemas, indent=2)
    
    # Create the system prompt
    system_prompt = """
    You are an expert SQL query generator. Your task is to convert natural language queries into SQL queries.
    You will be given a database schema and a natural language query.
    Generate a valid PostgreSQL SQL query that answers the question.
    Only return the SQL query, nothing else.
    """
    
    # Create the user prompt
    user_prompt = f"""
    Database Schema:
    {schema_str}
    
    Natural Language Query:
    {query}
    
    Generate a PostgreSQL SQL query that answers this question.
    """
    
    # Prepare messages for Ollama
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    try:
        # Call the Ollama API
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": model,
                "messages": messages,
                "stream": False
            }
        )
        
        if response.status_code != 200:
            print(f"Error calling Ollama API: {response.status_code} - {response.text}")
            # Fallback to a simple query
            return f"SELECT * FROM {table_schemas[0]['table_name']} LIMIT 5"
        
        # Extract the SQL query from the response
        response_data = response.json()
        sql_query = response_data.get('message', {}).get('content', '').strip()
        
        # Clean up the SQL query (remove markdown code blocks if present)
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        if sql_query.startswith("```"):
            sql_query = sql_query[3:]
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]
        
        sql_query = sql_query.strip()
        
        return sql_query
    except Exception as e:
        print(f"Error generating SQL with Ollama: {str(e)}")
        # Fallback to a simple query
        return f"SELECT * FROM {table_schemas[0]['table_name']} LIMIT 5"

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate and execute SQL queries using LLM')
    parser.add_argument('--query', '-q', type=str, help='Natural language query')
    parser.add_argument('--table', '-t', type=str, help='Specific table to query (optional)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show verbose output')
    parser.add_argument('--model', '-m', type=str, default='llama3.1', help='Ollama model to use')
    
    args = parser.parse_args()
    
    # If query is not provided as argument, ask for it
    query = args.query
    if not query:
        query = input("Enter your natural language query: ")
    
    # Connect to the database
    conn = connect_to_db()
    if not conn:
        return
    
    try:
        # Get table information
        if args.table:
            tables = [args.table]
        else:
            tables = get_all_tables(conn)
        
        if not tables:
            print("No tables found in the database")
            return
        
        # Get schemas for all tables
        table_schemas = [get_table_schema(conn, table) for table in tables]
        
        if args.verbose:
            print(f"Found {len(tables)} tables: {', '.join(tables)}")
            print("Table schemas:")
            print(json.dumps(table_schemas, indent=2))
        
        # Generate SQL query using Ollama
        start_time = time.time()
        sql_query = generate_sql_with_ollama(query, table_schemas, args.model)
        end_time = time.time()
        
        print(f"\nGenerated SQL query: {sql_query}")
        print(f"Query generation took {end_time - start_time:.2f} seconds")
        
        # Execute the query
        start_time = time.time()
        results = execute_sql_query(conn, sql_query)
        end_time = time.time()
        
        print(f"\nQuery execution took {end_time - start_time:.2f} seconds")
        print(f"Found {len(results)} results")
        
        # Print results
        print("\nResults:")
        print_results(results)
        
    finally:
        conn.close()

if __name__ == "__main__":
    main() 