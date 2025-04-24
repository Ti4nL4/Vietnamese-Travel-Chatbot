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
import json
import requests

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

class TourismLLMRouter:
    """Intelligent router for tourism queries using LLM"""
    
    def __init__(self, model_name="llama3.1"):
        """Initialize the tourism router"""
        self.sql_engine = SQLQueryEngine()
        self.vector_engine = VectorSearchEngine()
        self.chat_history = []
        self.model_name = model_name
        
    def route_query(self, query: str, top_k=5) -> Dict:
        """
        Route a query to the appropriate engine(s) using LLM
        
        Args:
            query (str): User query
            top_k (int): Number of results to return
            
        Returns:
            Dict: Combined results
        """
        # Add user query to chat history
        self.chat_history.append({"role": "user", "content": query})
        
        # Get tool selection from LLM
        tool_selection = self._get_tool_selection(query)
        
        results = {
            'sql_results': [],
            'vector_results': [],
            'query_type': 'unknown',
            'llm_response': ""
        }
        
        # Execute SQL query if selected
        if tool_selection.get('use_sql', False):
            sql_query = tool_selection.get('sql_query', '')
            if sql_query:
                sql_results = self.sql_engine.query(sql_query)
                results['sql_results'] = sql_results
                results['query_type'] = 'sql'
        
        # Execute vector search if selected
        if tool_selection.get('use_vector', False):
            vector_results = self.vector_engine.search(query, top_k=top_k)
            results['vector_results'] = vector_results
            if results['query_type'] == 'unknown':
                results['query_type'] = 'vector'
            elif results['query_type'] == 'sql':
                results['query_type'] = 'hybrid'
        
        # Generate final response using LLM
        if results['sql_results'] or results['vector_results']:
            llm_response = self._generate_response(query, results)
            results['llm_response'] = llm_response
            self.chat_history.append({"role": "assistant", "content": llm_response})
        
        return results
    
    def _get_tool_selection(self, query: str) -> Dict:
        """
        Use LLM to determine which tools to use
        
        Args:
            query (str): User query
            
        Returns:
            Dict: Tool selection
        """
        # Get database schema information
        schema_info = self._get_schema_info()
        
        # Create system message
        system_message = f"""
        You are an intelligent tourism assistant that can answer questions about tourism data.
        
        You have access to two types of data sources:
        1. SQL database with structured data about tourism
        2. Vector-based semantic search for unstructured content
        
        Database schema:
        {schema_info}
        
        For each user query, determine:
        1. Whether to use SQL queries (for factual, numerical, or comparative data)
        2. Whether to use vector search (for descriptive, historical, or conceptual information)
        3. The appropriate SQL query if SQL is needed
        
        Respond in JSON format with the following structure:
        {{
            "use_sql": true/false,
            "use_vector": true/false,
            "sql_query": "SELECT ..." (only if use_sql is true),
            "reasoning": "Brief explanation of your decision"
        }}
        """
        
        # Create messages for API call
        messages = [
            {"role": "system", "content": system_message}
        ]
        
        # Add chat history (limited to last 10 exchanges)
        for msg in self.chat_history[-10:]:
            messages.append(msg)
        
        # Call Ollama API
        try:
            response = self._call_ollama(messages)
            
            # Extract JSON response
            content = response
            # Find JSON in the response (it might be wrapped in markdown code blocks)
            json_start = content.find('{')
            json_end = content.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            else:
                print(f"Could not parse JSON from LLM response: {content}")
                return {"use_sql": False, "use_vector": True, "reasoning": "Fallback to vector search"}
                
        except Exception as e:
            print(f"Error calling Ollama API: {str(e)}")
            return {"use_sql": False, "use_vector": True, "reasoning": "Error occurred, defaulting to vector search"}
    
    def _get_schema_info(self) -> str:
        """
        Get database schema information
        
        Returns:
            str: Schema information
        """
        try:
            # Get all tables
            self.sql_engine.cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
            """)
            tables = [row['table_name'] for row in self.sql_engine.cur.fetchall()]
            
            schema_info = []
            
            for table in tables:
                # Get columns for this table
                self.sql_engine.cur.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = %s
                """, (table,))
                columns = self.sql_engine.cur.fetchall()
                
                # Format table info
                table_info = f"Table: {table}\n"
                for col in columns:
                    table_info += f"  - {col['column_name']} ({col['data_type']})\n"
                
                schema_info.append(table_info)
            
            return "\n".join(schema_info)
            
        except Exception as e:
            print(f"Error getting schema info: {str(e)}")
            return "Error retrieving schema information"
    
    def _generate_response(self, query: str, results: Dict) -> str:
        """
        Generate a natural language response using LLM
        
        Args:
            query (str): User query
            results (Dict): Query results
            
        Returns:
            str: Natural language response
        """
        # Format results for LLM
        sql_results_str = json.dumps(results['sql_results'], ensure_ascii=False) if results['sql_results'] else "No SQL results"
        
        # Format vector results (limit to first 3 for brevity)
        vector_results = results['vector_results'][:3]
        vector_results_str = json.dumps(vector_results, ensure_ascii=False) if vector_results else "No vector results"
        
        # Create system message
        system_message = """
        You are a helpful tourism assistant. Generate a natural language response to the user's query based on the provided data.
        Be concise, informative, and directly answer the user's question.
        If the data doesn't fully answer the question, acknowledge the limitations.
        """
        
        # Create user message
        user_message = f"""
        User query: {query}
        
        SQL results: {sql_results_str}
        
        Vector search results: {vector_results_str}
        
        Please provide a natural language response to the user's query based on this data.
        """
        
        # Call Ollama API
        try:
            messages = [
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
            
            return self._call_ollama(messages)
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return "I'm sorry, I couldn't generate a response at this time."
    
    def _call_ollama(self, messages):
        """
        Call Ollama API with the given messages
        
        Args:
            messages (List[Dict]): List of message dictionaries
            
        Returns:
            str: Response from Ollama
        """
        # Format messages for Ollama
        formatted_messages = []
        for msg in messages:
            if msg["role"] == "system":
                formatted_messages.append({"role": "system", "content": msg["content"]})
            elif msg["role"] == "user":
                formatted_messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                formatted_messages.append({"role": "assistant", "content": msg["content"]})
            elif msg["role"] == "tool":
                # Convert tool messages to assistant messages for Ollama
                formatted_messages.append({"role": "assistant", "content": f"Tool {msg.get('name', 'unknown')} returned: {msg['content']}"})
        
        # Call Ollama API
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": self.model_name,
                "messages": formatted_messages,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            return response.json()["message"]["content"]
        else:
            raise Exception(f"Error calling Ollama API: {response.status_code} - {response.text}")
    
    def close(self):
        """Close database connections"""
        self.sql_engine.close()
        self.vector_engine.close()

def print_results(results: Dict):
    """Print search results in a readable format"""
    print(f"\nQuery type: {results['query_type']}")
    
    if results['llm_response']:
        print("\n--- LLM Response ---")
        print(results['llm_response'])
    
    if results['vector_results']:
        print("\n--- Top 5 Similarity Results ---")
        for i, result in enumerate(results['vector_results'][:5], 1):
            print(f"\n--- Result {i} (Table: {result['table_name']}, Similarity: {result['similarity']:.4f}) ---")
            
            # Print all fields except similarity, table_name, and vector fields
            for key, value in result.items():
                if key not in ['similarity', 'table_name', 'text_embedding'] and value is not None:
                    # Truncate long text values
                    if isinstance(value, str) and len(value) > 100:
                        value = value[:100] + "..."
                    print(f"{key}: {value}")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Tourism data router with LLM')
    parser.add_argument('--query', '-q', type=str, help='Search query')
    parser.add_argument('--top', '-n', type=int, default=5, help='Number of results to return (default: 5)')
    parser.add_argument('--model', '-m', type=str, default='llama3.1', help='Ollama model to use (default: llama3.1)')
    
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
    router = TourismLLMRouter(model_name=args.model)
    try:
        results = router.route_query(query, top_k)
        print_results(results)
    finally:
        router.close()

if __name__ == "__main__":
    main() 