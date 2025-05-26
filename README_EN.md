# Tourism LLM Router Project

## Introduction
This project is a tourism data processing and analysis system utilizing Large Language Models (LLM) and modern technologies. The system enables intelligent tourism information search and automatic SQL query generation from natural language.

## System Architecture
![System Architecture](New_Architecture.png)

## Key Features
- Semantic Search for tourism data
- Natural language to SQL query conversion
- Processing and analysis of Vietnamese tourism data
- Integration with PostgreSQL and pgvector for vector storage
- Intelligent search support through FAISS index

## System Requirements
- Python 3.9
- PostgreSQL with pgvector extension
- Python libraries (see requirements.txt)

## Installation

1. Clone repository:
```bash
git clone [https://github.com/Ti4nL4/Vietnamese-Travel-Chatbot.git]
cd [Vietnamese-Travel-Chatbot]
```

2. Create and activate virtual environment:
```bash
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
# or
myenv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install pgvector for PostgreSQL:
```bash
python install_pgvector.py
```

5. Set up database:
```bash
python setup_database.py
```

## Project Structure
- `data/`: Contains original data in CSV format
- `evaluation/`: Contains testing code and test datasets
- `faiss_index/`: Stores FAISS index for fast semantic retrieval
- `logs/`: Records experimental results including questions, answers, and evaluation metrics
- `rag_data/`: Contains unstructured data for RAG pipeline
- `sql_output/`: Contains SQL files converted from CSV data for database insertion
- `New_Architecture.png`: System architecture diagram
- `csv_to_sql.py`: Converts CSV data to SQL statements for PostgreSQL loading
- `install_pgvector.py`: Installs pgvector extension for PostgreSQL vector search support
- `my_notebook.ipynb`, `my_notebook.py`: Contains main processing pipeline including routing, retrieval, and response generation
- `pg_query.py`: Performs direct queries to PostgreSQL database
- `setup_database.py`: Initializes database, including table creation and data loading
- `requirements.txt`: List of required Python libraries

## Usage
1. Ensure proper environment setup and configuration
2. Run main router:
```bash
python mynotebook_.py
```
3. Run test cases:
```bash
python evaluation/main_evaluation.py
```

## Configuration
Create a `.env` file with the following environment variables:
```
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
``` 