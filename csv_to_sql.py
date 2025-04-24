import pandas as pd
import os
from pathlib import Path

def clean_column_name(col):
    """Clean column names to be SQL-friendly"""
    # Remove special characters and spaces
    cleaned = ''.join(c if c.isalnum() else '_' for c in col)
    # Ensure it starts with a letter
    if not cleaned[0].isalpha():
        cleaned = 'col_' + cleaned
    return cleaned.lower()

def get_sql_type(dtype):
    """Convert pandas dtype to SQL type"""
    if pd.api.types.is_integer_dtype(dtype):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'TIMESTAMP'
    else:
        return 'TEXT'

def csv_to_sql(csv_file, output_dir):
    """Convert a CSV file to SQL format"""
    # Read CSV file
    df = pd.read_csv(csv_file, encoding='utf-8')
    
    # Clean column names
    df.columns = [clean_column_name(col) for col in df.columns]
    
    # Get table name from file name
    table_name = Path(csv_file).stem.lower().replace(' ', '_')
    
    # Generate SQL file content
    sql_content = []
    
    # Create table statement
    create_table = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
    columns = []
    for col, dtype in df.dtypes.items():
        sql_type = get_sql_type(dtype)
        columns.append(f"    {col} {sql_type}")
    create_table += ',\n'.join(columns)
    create_table += '\n);\n\n'
    sql_content.append(create_table)
    
    # Insert statements
    for _, row in df.iterrows():
        values = []
        for val in row:
            if pd.isna(val):
                values.append('NULL')
            elif isinstance(val, (int, float)):
                values.append(str(val))
            else:
                # Escape single quotes and wrap in quotes
                val = str(val).replace("'", "''")
                values.append(f"'{val}'")
        
        insert_stmt = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(values)});\n"
        sql_content.append(insert_stmt)
    
    # Write to SQL file
    output_file = os.path.join(output_dir, f"{table_name}.sql")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_content))
    
    return output_file

def main():
    # Create output directory if it doesn't exist
    output_dir = 'sql_output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all CSV files in the data directory
    data_dir = 'data'
    for file in os.listdir(data_dir):
        if file.endswith('.csv'):
            csv_path = os.path.join(data_dir, file)
            try:
                output_file = csv_to_sql(csv_path, output_dir)
                print(f"Successfully converted {file} to {output_file}")
            except Exception as e:
                print(f"Error converting {file}: {str(e)}")

if __name__ == '__main__':
    main() 