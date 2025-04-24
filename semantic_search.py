import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import sys
import time
import argparse

# Add myenv to Python path to import vector_search
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from myenv.vector_search import text_to_vector

load_dotenv()

def semantic_search(query, table_name=None, top_k=5):
    """
    Perform semantic search in the database using vector similarity
    
    Args:
        query (str): The search query
        table_name (str, optional): Specific table to search in. If None, searches all tables
        top_k (int): Number of results to return
        
    Returns:
        list: List of dictionaries containing search results
    """
    start_time = time.time()
    print(f"Performing semantic search for: '{query}'")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Convert query to vector
        query_vector = text_to_vector(query)
        print(f"Query vector generated with {len(query_vector)} dimensions")
        
        # Determine which tables to search
        if table_name:
            tables = [table_name]
        else:
            # Get all tables with vector columns
            cur.execute("""
                SELECT DISTINCT table_name 
                FROM information_schema.columns 
                WHERE column_name = 'text_embedding'
                AND table_schema = 'public'
            """)
            tables = [row['table_name'] for row in cur.fetchall()]
        
        print(f"Searching in {len(tables)} tables: {tables}")
        
        all_results = []
        
        # Search in each table
        for table in tables:
            print(f"Searching in table: {table}")
            
            # Get column names for this table
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s
            """, (table,))
            columns = [row['column_name'] for row in cur.fetchall()]
            
            # Build the SELECT part of the query
            select_columns = ", ".join(columns)
            
            # Perform vector similarity search
            cur.execute(f"""
                SELECT {select_columns}, 
                       1 - (text_embedding <#> %s::vector) as similarity
                FROM {table}
                WHERE text_embedding IS NOT NULL
                ORDER BY similarity DESC
                LIMIT %s
            """, (query_vector, top_k))
            
            results = cur.fetchall()
            
            # Add table name to each result
            for result in results:
                result['table_name'] = table
                all_results.append(result)
            
            print(f"Found {len(results)} results in table {table}")
        
        # Sort all results by similarity
        all_results.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Take only top_k results
        all_results = all_results[:top_k]
        
        end_time = time.time()
        print(f"Search completed in {end_time - start_time:.2f} seconds")
        print(f"Found {len(all_results)} total results")
        
        return all_results
        
    except Exception as e:
        print(f"Error performing semantic search: {str(e)}")
        return []
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

def print_results(results):
    """Print search results in a readable format"""
    if not results:
        print("No results found")
        return
    
    for i, result in enumerate(results, 1):
        print(f"\n--- Result {i} (Table: {result['table_name']}, Similarity: {result['similarity']:.4f}) ---")
        
        # Print all fields except similarity and table_name
        for key, value in result.items():
            if key not in ['similarity', 'table_name'] and value is not None:
                # Truncate long text values
                if isinstance(value, str) and len(value) > 100:
                    value = value[:100] + "..."
                print(f"{key}: {value}")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Semantic search in the database')
    parser.add_argument('--query', '-q', type=str, help='Search query')
    parser.add_argument('--table', '-t', type=str, help='Table name (optional)')
    parser.add_argument('--top', '-n', type=int, default=5, help='Number of results to return (default: 5)')
    
    args = parser.parse_args()
    
    # If query is not provided as argument, ask for it
    query = args.query
    if not query:
        query = input("Enter your search query: ")
    
    # Use table name from arguments or ask for it
    table_name = args.table
    if not table_name:
        table_name = input("Enter table name (or press Enter to search all tables): ").strip()
        if not table_name:
            table_name = None
    
    # Use top_k from arguments or ask for it
    top_k = args.top
    if top_k == 5 and not args.query:  # Only ask if not provided as argument
        try:
            top_k = int(input("Enter number of results to return (default: 5): ") or "5")
        except ValueError:
            top_k = 5
    
    # Perform the search
    results = semantic_search(query, table_name, top_k)
    print_results(results)

if __name__ == "__main__":
    main() 