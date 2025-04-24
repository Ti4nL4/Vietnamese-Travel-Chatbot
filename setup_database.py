import psycopg2
import os
from dotenv import load_dotenv
from pathlib import Path
import sys
from sentence_transformers import SentenceTransformer

# Add myenv to Python path to import vector_search
sys.path.append('myenv')

load_dotenv()

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to default postgres database to create new database
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Create database if it doesn't exist
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (os.getenv('DB_NAME'),))
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {os.getenv('DB_NAME')}")
            print(f"Database {os.getenv('DB_NAME')} created successfully")
        
        cur.close()
        conn.close()
        
        # Connect to the new database
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()
        
        # Create required extensions
        cur.execute("CREATE EXTENSION IF NOT EXISTS unaccent;")
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        
        # Create Vietnamese text search configuration
        cur.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_ts_config WHERE cfgname = 'vietnamese'
                ) THEN
                    CREATE TEXT SEARCH CONFIGURATION vietnamese (COPY = simple);
                    ALTER TEXT SEARCH CONFIGURATION vietnamese
                    ALTER MAPPING FOR hword, hword_part, word
                    WITH unaccent, simple;
                END IF;
            END
            $$;
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error creating database: {str(e)}")
        raise

def create_tables():
    """Create tables with proper structure before importing data"""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()
        
        # Execute the table creation script
        with open('sql_output/create_huong_dan_vien.sql', 'r', encoding='utf-8') as f:
            cur.execute(f.read())
        
        conn.commit()
        cur.close()
        conn.close()
        print("Successfully created tables with proper structure")
        
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        raise

def import_data(sql_file):
    """Import data from SQL file into PostgreSQL"""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()
        
        print(f"Importing data from {sql_file}...")
        
        # Use psycopg2's copy_from to import the entire file at once
        with open(sql_file, 'r', encoding='utf-8') as f:
            try:
                cur.execute(f.read())
                conn.commit()
                print(f"Successfully imported data from {sql_file}")
            except Exception as e:
                print(f"Error executing SQL file: {str(e)}")
                conn.rollback()
                raise
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error importing {sql_file}: {str(e)}")
        raise

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def text_to_vector(text):
    """Convert text to vector embedding"""
    return model.encode(text).tolist()

def create_vector_tables():
    """Create tables with vector columns for semantic search"""
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()
        
        # Check if pgvector extension is installed
        cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
        result = cur.fetchone()
        if not result:
            print("pgvector extension not found. Please run install_pgvector.py first.")
            return False
        
        # Get all tables in the database
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cur.fetchall()]
        print(f"Found {len(tables)} tables: {tables}")
        
        # For each table, create a vector column and index if it doesn't exist
        for table in tables:
            # Get text columns for this table
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s AND data_type IN ('text', 'character varying')
            """, (table,))
            text_columns = [row[0] for row in cur.fetchall()]
            
            if not text_columns:
                print(f"No text columns found in table {table}, skipping...")
                continue
            
            # Check if vector column already exists
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s AND column_name = 'text_embedding'
            """, (table,))
            if cur.fetchone():
                print(f"Vector column already exists in table {table}, skipping...")
                continue
            
            # Add vector column
            print(f"Adding vector column to table {table}...")
            cur.execute(f"ALTER TABLE {table} ADD COLUMN text_embedding vector(384);")
            
            # Create index on vector column
            print(f"Creating vector index on table {table}...")
            cur.execute(f"CREATE INDEX ON {table} USING ivfflat (text_embedding vector_cosine_ops) WITH (lists = 100);")
            
            conn.commit()
            print(f"Successfully added vector column and index to table {table}")
        
        cur.close()
        conn.close()
        print("Vector tables setup completed successfully")
        return True
        
    except Exception as e:
        print(f"Error creating vector tables: {str(e)}")
        return False

def update_vector_embeddings():
    """Update vector embeddings for all tables"""
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        cur = conn.cursor()
        
        # Get all tables with vector columns
        cur.execute("""
            SELECT table_name 
            FROM information_schema.columns 
            WHERE column_name = 'text_embedding'
            AND table_schema = 'public'
        """)
        tables = [row[0] for row in cur.fetchall()]
        print(f"Found {len(tables)} tables with vector columns: {tables}")
        
        for table in tables:
            try:
                # Get text columns for this table
                cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = %s AND data_type IN ('text', 'character varying')
                """, (table,))
                text_columns = [row[0] for row in cur.fetchall()]
                
                if not text_columns:
                    print(f"No text columns found in table {table}, skipping...")
                    continue
                
                # Get primary key column for this table
                cur.execute("""
                    SELECT a.attname
                    FROM pg_index i
                    JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
                    WHERE i.indrelid = %s::regclass AND i.indisprimary
                """, (table,))
                pk_result = cur.fetchone()
                
                # If no primary key, use the first column as identifier
                if not pk_result:
                    cur.execute("""
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_name = %s
                        ORDER BY ordinal_position
                        LIMIT 1
                    """, (table,))
                    pk_result = cur.fetchone()
                
                if not pk_result:
                    print(f"No identifier column found in table {table}, skipping...")
                    continue
                    
                id_column = pk_result[0]
                print(f"Using '{id_column}' as identifier for table {table}")
                
                # Get rows that don't have embeddings yet
                cur.execute(f"SELECT COUNT(*) FROM {table} WHERE text_embedding IS NULL")
                null_count = cur.fetchone()[0]
                
                if null_count == 0:
                    print(f"All rows in table {table} already have embeddings, skipping...")
                    continue
                
                print(f"Updating {null_count} rows in table {table}...")
                
                # Process in batches to avoid memory issues
                batch_size = 100
                offset = 0
                
                while True:
                    # Get a batch of rows without embeddings
                    cur.execute(f"""
                        SELECT {id_column}, {', '.join(text_columns)}
                        FROM {table} 
                        WHERE text_embedding IS NULL
                        ORDER BY {id_column}
                        LIMIT {batch_size} OFFSET {offset}
                    """)
                    
                    batch = cur.fetchall()
                    if not batch:
                        break
                        
                    print(f"Processing batch {offset//batch_size + 1}/{(null_count + batch_size - 1)//batch_size}...")
                    
                    for row in batch:
                        # First element is the ID
                        row_id = row[0]
                        
                        # Combine text columns (skip the ID)
                        text = " ".join([str(val) for val in row[1:] if val is not None])
                        if not text.strip():
                            continue
                        
                        # Generate embedding
                        embedding = text_to_vector(text)
                        
                        # Update row with embedding
                        cur.execute(f"UPDATE {table} SET text_embedding = %s WHERE {id_column} = %s", 
                                   (embedding, row_id))
                    
                    conn.commit()
                    print(f"Updated {len(batch)} rows in table {table}")
                    
                    offset += batch_size
                    
                    # If we've processed all rows, break
                    if offset >= null_count:
                        break
                
            except Exception as e:
                print(f"Error processing table {table}: {str(e)}")
                # Continue with the next table
                continue
        
        cur.close()
        conn.close()
        print("Vector embeddings update completed successfully")
        return True
        
    except Exception as e:
        print(f"Error updating vector embeddings: {str(e)}")
        return False

def main():
    # Create database and extensions
    create_database()
    
    # Import data from SQL files
    sql_dir = 'sql_output'
    for file in os.listdir(sql_dir):
        if file.endswith('.sql') and file not in ['create_vector_indexes.sql']:
            sql_path = os.path.join(sql_dir, file)
            import_data(sql_path)
    
    # Create vector columns and indexes
    # print("Creating vector columns and indexes...")
    # if create_vector_tables():
    #     print("Successfully created vector columns and indexes")
        
    #     # Update vector embeddings
    #     print("Updating vector embeddings...")
    #     if update_vector_embeddings():
    #         print("Successfully updated vector embeddings")
    #     else:
    #         print("Failed to update vector embeddings")
    # else:
    #     print("Failed to create vector columns and indexes")
    # update_vector_embeddings()
if __name__ == '__main__':
    main() 