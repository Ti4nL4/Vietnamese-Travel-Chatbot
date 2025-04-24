import os
import sys
import argparse
import asyncio
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from sentence_transformers import SentenceTransformer
import numpy as np

# Add myenv to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from myenv.vector_search import text_to_vector, preprocess_text

# Load environment variables
load_dotenv()

# Initialize the sentence transformer model
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

class SQLQueryEngine:
    """SQL query engine for structured tourism data"""
    
    def __init__(self):
        """Initialize the SQL query engine"""
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        
    def query(self, query: str) -> List[Dict]:
        """
        Execute a SQL query
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            List[Dict]: Query results
        """
        try:
            self.cur.execute(query)
            results = self.cur.fetchall()
            return results
        except Exception as e:
            print(f"Error executing SQL query: {str(e)}")
            return []
            
    def close(self):
        """Close database connection"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

class VectorSearchEngine:
    """Vector-based semantic search engine for tourism data"""
    
    def __init__(self):
        """Initialize the vector search engine"""
        self.conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        
    def search(self, query: str, table_name=None, top_k=5) -> List[Dict]:
        """
        Perform vector similarity search
        
        Args:
            query (str): Search query
            table_name (str, optional): Specific table to search in
            top_k (int): Number of results to return
            
        Returns:
            List[Dict]: Search results
        """
        try:
            # Preprocess and convert query to vector
            processed_query = preprocess_text(query)
            query_vector = text_to_vector(processed_query)
            
            # Determine which tables to search
            if table_name:
                tables = [table_name]
            else:
                # Get all tables with vector columns
                self.cur.execute("""
                    SELECT DISTINCT table_name 
                    FROM information_schema.columns 
                    WHERE column_name = 'text_embedding'
                    AND table_schema = 'public'
                """)
                tables = [row['table_name'] for row in self.cur.fetchall()]
            
            all_results = []
            
            # Search in each table
            for table in tables:
                # Get column names for this table
                self.cur.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = %s
                """, (table,))
                columns = [row['column_name'] for row in self.cur.fetchall()]
                
                # Build the SELECT part of the query
                select_columns = ", ".join(columns)
                
                # Perform vector similarity search
                self.cur.execute(f"""
                    SELECT {select_columns}, 
                           1 - (text_embedding <#> %s::vector) as similarity
                    FROM {table}
                    WHERE text_embedding IS NOT NULL
                    ORDER BY similarity DESC
                    LIMIT %s
                """, (query_vector, top_k))
                
                results = self.cur.fetchall()
                
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
            
    def close(self):
        """Close database connection"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

class TourismRouter:
    """Intelligent router for tourism queries"""
    
    def __init__(self):
        """Initialize the tourism router"""
        self.sql_engine = SQLQueryEngine()
        self.vector_engine = VectorSearchEngine()
        
    def route_query(self, query: str, top_k=5) -> Dict:
        """
        Route a query to the appropriate engine(s)
        
        Args:
            query (str): User query
            top_k (int): Number of results to return
            
        Returns:
            Dict: Combined results
        """
        # Simple heuristic-based routing
        # For more sophisticated routing, consider using an LLM
        
        # Keywords that suggest SQL queries
        sql_keywords = ['số lượng', 'bao nhiêu', 'thống kê', 'so sánh', 'lớn nhất', 'nhỏ nhất', 'trung bình', 'tổng']
        
        # Keywords that suggest vector search
        vector_keywords = ['là gì', 'ở đâu', 'như thế nào', 'mô tả', 'giới thiệu', 'lịch sử', 'đặc điểm', 'thế nào']
        
        # Check if query contains SQL keywords
        is_sql_query = any(keyword in query.lower() for keyword in sql_keywords)
        
        # Check if query contains vector search keywords
        is_vector_query = any(keyword in query.lower() for keyword in vector_keywords)
        
        results = {
            'sql_results': [],
            'vector_results': [],
            'query_type': 'unknown'
        }
        
        # Execute SQL query if appropriate
        if is_sql_query:
            # Convert natural language to SQL (simplified example)
            sql_query = self._nl_to_sql(query)
            if sql_query:
                sql_results = self.sql_engine.query(sql_query)
                results['sql_results'] = sql_results
                results['query_type'] = 'sql'
        
        # Execute vector search if appropriate
        if is_vector_query or not is_sql_query:
            vector_results = self.vector_engine.search(query, top_k=top_k)
            results['vector_results'] = vector_results
            if results['query_type'] == 'unknown':
                results['query_type'] = 'vector'
            elif results['query_type'] == 'sql':
                results['query_type'] = 'hybrid'
        
        return results
    
    def _nl_to_sql(self, query: str) -> str:
        """
        Convert natural language to SQL (simplified)
        
        Args:
            query (str): Natural language query
            
        Returns:
            str: SQL query
        """
        # This is a simplified implementation
        # For a production system, consider using an LLM for NL-to-SQL conversion
        
        query = query.lower()
        
        # Example mappings for tourism data
        if 'hướng dẫn viên' in query and 'bao nhiêu' in query:
            return "SELECT COUNT(*) as count FROM huong_dan_vien"
        
        if 'cơ sở đào tạo' in query and 'bao nhiêu' in query:
            return "SELECT COUNT(*) as count FROM co_so_dao_tao"
        
        if 'khách sạn' in query and 'bao nhiêu' in query:
            return "SELECT COUNT(*) as count FROM khach_san"
        
        # Add more mappings as needed
        
        return ""
    
    def close(self):
        """Close database connections"""
        self.sql_engine.close()
        self.vector_engine.close()

def print_results(results: Dict):
    """Print search results in a readable format"""
    print(f"\nQuery type: {results['query_type']}")
    
    if results['sql_results']:
        print("\n--- SQL Results ---")
        for i, result in enumerate(results['sql_results'], 1):
            print(f"\nResult {i}:")
            for key, value in result.items():
                print(f"{key}: {value}")
    
    if results['vector_results']:
        print("\n--- Vector Search Results ---")
        for i, result in enumerate(results['vector_results'], 1):
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
    parser = argparse.ArgumentParser(description='Tourism data router')
    parser.add_argument('--query', '-q', type=str, help='Search query')
    parser.add_argument('--top', '-n', type=int, default=5, help='Number of results to return (default: 5)')
    
    args = parser.parse_args()
    
    # If query is not provided as argument, ask for it
    query = args.query
    if not query:
        query = input("Enter your search query: ")
    
    # Use top_k from arguments or ask for it
    top_k = args.top
    if top_k == 5 and not args.query:
        try:
            top_k = int(input("Enter number of results to return (default: 5): ") or "5")
        except ValueError:
            top_k = 5
    
    # Create router and process query
    router = TourismRouter()
    try:
        results = router.route_query(query, top_k)
        print_results(results)
    finally:
        router.close()

if __name__ == "__main__":
    main() 