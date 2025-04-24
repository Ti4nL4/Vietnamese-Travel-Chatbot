import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import sys
import time
import re
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Initialize the sentence transformer model
# Using a multilingual model that supports Vietnamese
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def preprocess_text(text):
    """
    Preprocess text to improve embedding quality
    
    Args:
        text (str): The text to preprocess
        
    Returns:
        str: Preprocessed text
    """
    if not text:
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    # Remove special characters but keep Vietnamese diacritics
    text = re.sub(r'[^\w\s\u0080-\uFFFF]', ' ', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Trim whitespace
    text = text.strip()
    
    return text

def text_to_vector(text):
    """
    Convert text to vector embedding using the sentence transformer model
    
    Args:
        text (str): The text to convert to vector
        
    Returns:
        list: Vector embedding of the text
    """
    # Preprocess the text
    processed_text = preprocess_text(text)
    
    # Generate embedding
    embedding = model.encode(processed_text)
    
    # Convert to list for PostgreSQL compatibility
    return embedding.tolist()

def create_vector_tables():
    """
    Create tables with vector columns for semantic search
    """
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()
        
        # First, ensure pgvector extension is installed
        try:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
            conn.commit()
            print("pgvector extension installed or already exists")
        except Exception as e:
            print(f"Error installing pgvector extension: {str(e)}")
            print("Please make sure pgvector is installed in your PostgreSQL instance")
            return
        
        # Get all tables in the database
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
        """)
        tables = [row[0] for row in cur.fetchall()]
        
        for table in tables:
            # Check if the table has a text_embedding column
            cur.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s AND column_name = 'text_embedding'
            """, (table,))
            
            if not cur.fetchone():
                # Add text_embedding column if it doesn't exist
                cur.execute(f"""
                    ALTER TABLE {table} 
                    ADD COLUMN text_embedding vector(384)
                """)
                print(f"Added text_embedding column to {table}")
                
                # Create index on the vector column
                cur.execute(f"""
                    CREATE INDEX ON {table} 
                    USING ivfflat (text_embedding vector_cosine_ops) 
                    WITH (lists = 100)
                """)
                print(f"Created vector index on {table}")
        
        conn.commit()
        print("Vector tables created successfully")
        
    except Exception as e:
        print(f"Error creating vector tables: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

def update_vector_embeddings():
    """
    Update vector embeddings for all tables
    """
    try:
        # Connect to the database
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()
        
        # Get all tables with text_embedding column
        cur.execute("""
            SELECT DISTINCT table_name 
            FROM information_schema.columns 
            WHERE column_name = 'text_embedding'
            AND table_schema = 'public'
        """)
        tables = [row[0] for row in cur.fetchall()]
        
        for table in tables:
            print(f"Processing table: {table}")
            
            # Get text columns for this table
            cur.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s 
                AND data_type IN ('text', 'character varying', 'character')
            """, (table,))
            
            text_columns = [row[0] for row in cur.fetchall()]
            
            if not text_columns:
                print(f"No text columns found in table {table}, skipping")
                continue
            
            # Get primary key column
            cur.execute(f"""
                SELECT a.attname
                FROM pg_index i
                JOIN pg_attribute a ON a.attrelid = i.indrelid
                AND a.attnum = ANY(i.indkey)
                WHERE i.indrelid = %s::regclass
                AND i.indisprimary
            """, (table,))
            
            pk_result = cur.fetchone()
            if pk_result:
                pk_column = pk_result[0]
            else:
                # If no primary key, use the first column
                cur.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = %s
                    ORDER BY ordinal_position
                    LIMIT 1
                """, (table,))
                pk_column = cur.fetchone()[0]
            
            # Process rows in batches to avoid memory issues
            batch_size = 100
            offset = 0
            
            while True:
                # Build the SELECT part of the query
                select_columns = [pk_column] + text_columns
                select_clause = ", ".join(select_columns)
                
                # Get a batch of rows
                cur.execute(f"""
                    SELECT {select_clause}
                    FROM {table}
                    WHERE text_embedding IS NULL
                    ORDER BY {pk_column}
                    LIMIT %s OFFSET %s
                """, (batch_size, offset))
                
                rows = cur.fetchall()
                if not rows:
                    break
                
                # Process each row
                for row in rows:
                    # Combine text columns for embedding
                    text_values = []
                    for i, col in enumerate(text_columns):
                        if i + 1 < len(row) and row[i + 1] is not None:
                            text_values.append(str(row[i + 1]))
                    
                    if not text_values:
                        continue
                    
                    combined_text = " ".join(text_values)
                    embedding = text_to_vector(combined_text)
                    
                    # Update the row with the embedding
                    cur.execute(f"""
                        UPDATE {table}
                        SET text_embedding = %s::vector
                        WHERE {pk_column} = %s
                    """, (embedding, row[0]))
                
                conn.commit()
                print(f"Processed {len(rows)} rows in {table}")
                offset += batch_size
            
            print(f"Completed processing table {table}")
        
        print("Vector embeddings updated successfully")
        
    except Exception as e:
        print(f"Error updating vector embeddings: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

def vector_search(query, table_name=None, top_k=5):
    """
    Perform vector similarity search in the database
    
    Args:
        query (str): The search query
        table_name (str, optional): Specific table to search in. If None, searches all tables
        top_k (int): Number of results to return
        
    Returns:
        list: List of dictionaries containing search results
    """
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
        
        # Preprocess and convert query to vector
        processed_query = preprocess_text(query)
        query_vector = text_to_vector(processed_query)
        
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
        
        all_results = []
        
        # Search in each table
        for table in tables:
            # Get column names for this table
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s
            """, (table,))
            columns = [row['column_name'] for row in cur.fetchall()]
            
            # Build the SELECT part of the query
            select_columns = ", ".join(columns)
            
            # Perform vector similarity search using the correct operator
            # Using cosine distance with explicit type casting
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
        
        # Sort all results by similarity
        all_results.sort(key=lambda x: x['similarity'], reverse=True)
        
        # Take only top_k results
        all_results = all_results[:top_k]
        
        return all_results
        
    except Exception as e:
        print(f"Error performing vector search: {str(e)}")
        return []
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    # Example usage
    # create_vector_tables()
    # update_vector_embeddings()
    
    # Example search
    results = vector_search("tôi cần tìm hướng dẫn viên du lịch ở hồ chí minh")
    print(f"Found {results} results") 