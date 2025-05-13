import psycopg2
import requests
import json
from dotenv import load_dotenv
import os
import re
import unicodedata

load_dotenv()

# ⚙️ CONFIG
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma:7b-instruct-v1.1-q4_K_M"
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def identify_relevant_table(user_question):
    question_lower = user_question.lower()
    
    # Từ khóa mapping đến các bảng (đã bổ sung đầy đủ)
    table_keywords = {
        "hướng_dẫn_viên": [
            "hướng dẫn viên", "hdv", "hướng dẫn viên du lịch",
            "thẻ hướng dẫn viên", "nơi cấp thẻ", "giấy phép hdv"
        ],
        "lưu_trú": [
            "lưu trú", "khách sạn", "nhà nghỉ", "nơi ở",
            "chỗ nghỉ", "phòng nghỉ", "đặt phòng", "resort", "biệt thự"
        ],
        "nhà_hàng": [
            "nhà hàng", "quán ăn", "địa điểm ăn uống",
            "ẩm thực", "dining", "quán nhậu", "tiệm ăn"
        ],
        "điểm_đến_nổi_tiếng": [
            "điểm đến", "địa điểm du lịch", "thắng cảnh", "vườn quốc gia", "khu di tích",
            "danh lam", "nơi tham quan", "điểm tham quan", "tourist attraction"
        ],
        "doanh_nghiệp_lữ_hành_quốc_tế": [
            "công ty du lịch", "doanh nghiệp lữ hành",
            "tour operator", "công ty quốc tế", "travel agency",
            "công ty", "đại lý du lịch"
        ],
        "mua_sắm": [
            "mua sắm", "trung tâm thương mại", "shop",
            "cửa hàng", "shopping", "mall", "chợ"
        ],
        "vận_tải": [
            "vận tải", "xe du lịch", "taxi", "thuê xe",
            "chuyển phát", "giao thông", "bus", "xe buýt", "nhà xe"
        ],
        "vui_chơi_giải_trí": [
            "vui chơi", "giải trí", "khu vui chơi",
            "công viên", "game center", "amusement park", "chợ đêm", "quảng trường"
        ],
        "cơ_sở_đào_tạo": [
            "cơ sở đào tạo", "trường dạy", "học viện du lịch",
            "đào tạo hướng dẫn viên", "lớp học du lịch",
            "khóa đào tạo", "training center", "trường"
        ],
        "hiệp_hội": [
            "hiệp hội", "association", "tổ chức du lịch",
            "hội nghề nghiệp", "trade association"
        ],
        "thể_thao": [
            "thể thao", "sport", "gym", "phòng tập",
            "hoạt động thể chất", "fitness", "sân vận động", "sân golf"
        ]
    }
    
    # Kiểm tra từ khóa trong câu hỏi (ưu tiên theo thứ tự từ khóa cụ thể đến chung)
    for table_name, keywords in table_keywords.items():
        for keyword in keywords:
            if keyword in question_lower:
                return table_name
                
    # Fallback: Dự đoán dựa trên các từ thông dụng
    if any(word in question_lower for word in ["ăn", "uống", "thức ăn", "food"]):
        return "nhà_hàng"
    elif any(word in question_lower for word in ["đi", "đến", "tham quan", "visit"]):
        return "điểm_đến_nổi_tiếng"
    elif any(word in question_lower for word in ["ngủ", "nghỉ", "phòng", "stay"]):
        return "lưu_trú"
    elif any(word in question_lower for word in ["học", "đào tạo", "training"]):
        return "cơ_sở_đào_tạo"
    elif any(word in question_lower for word in ["hội", "association", "tổ chức"]):
        return "hiệp_hội"
    elif any(word in question_lower for word in ["thể thao", "sport", "gym"]):
        return "thể_thao"
    
    return None  # Trả về None nếu không xác định được

def extract_table_schema(full_schema, table_name):
    # Trích xuất phần schema của bảng cụ thể
    pattern = rf"TABLE {table_name}: (.+?)\n"
    match = re.search(pattern, full_schema)
    return match.group(0) if match else ""

def extract_select_sql(response_text):
    match = re.search(r"(SELECT[\s\S]+?;)", response_text, re.IGNORECASE)
    if match:
        sql = match.group(1).strip()
        # Add LIMIT 10 if not present
        if 'LIMIT' not in sql.upper():
            sql = sql.rstrip(';') + ' LIMIT 10;'
        return sql
    else:
        print("❌ Không tìm thấy câu lệnh SELECT.")
        return None

# 🧠 Gửi prompt đến LLaMA để sinh SQL
def generate_sql_from_prompt(user_question, schema):
    table_name = identify_relevant_table(user_question)
    relevant_schema = extract_table_schema(schema, table_name)
    prompt = f"""
Bạn là một chuyên gia SQL. Dựa vào yêu cầu bên dưới và cấu trúc database đã cho, hãy viết truy vấn SQL phù hợp, luôn sử dụng SELECT * cho câu lệnh sql
mệnh đề WHERE sử dụng ILIKE để tìm kiếm và luôn có dấu % ở đầu và cuối của từ cần tìm, giữ nguyên tên table trong mệnh đề FROM, Limit 10 kết quả.

# Câu hỏi:
{user_question}

# Cấu trúc các bảng:
{relevant_schema}

# Trả về:
Viết SQL truy vấn phù hợp, không cần giải thích.
    """
    print("prompt length: ", len(prompt))
    print("prompt: ", prompt)

    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })

    sql = response.json()["response"]
    return extract_select_sql(sql)

def decompose_where_values_only(sql_query):
    def replacer(match):
        column = match.group(1)
        operator = match.group(2)
        value = match.group(3)
        # Remove any existing % signs and add them back
        value = value.strip('%')
        # Wrap both column and value with unaccent
        return f"unaccent({column}) {operator} unaccent('%{value}%')"

    # Tìm phần FROM và áp dụng unaccent cho tên bảng
    from_match = re.search(r"(FROM\s+)(\w+)(\s+WHERE|\s+LIMIT|\s+;|$)", sql_query, re.IGNORECASE | re.DOTALL)
    if from_match:
        before_from = from_match.group(1)
        table_name = from_match.group(2)
        after_from = from_match.group(3)
        # Áp dụng unaccent cho tên bảng
        sql_query = f"{before_from}unaccent({table_name}){after_from}"

    # Tìm phần WHERE
    match = re.search(r"(.*WHERE\s+)(.+?)(\s+LIMIT\s+\d+|;|$)", sql_query, re.IGNORECASE | re.DOTALL)
    if not match:
        return sql_query  # không có WHERE thì không làm gì cả

    before_where = match.group(1)
    where_clause = match.group(2)
    after_where = match.group(3)

    # Regex tìm các giá trị dạng column operator 'value'
    decomposed_where = re.sub(r"(\w+)\s+(ILIKE|LIKE|=)\s*'%?([^'%]*)%?'", replacer, where_clause, flags=re.IGNORECASE)
    print("decomposed_where: ", decomposed_where)
    return f"{before_where}{decomposed_where}{after_where}"

# 🔌 Kết nối database và chạy SQL
def run_sql_query(sql_query):
    sql_query = decompose_where_values_only(sql_query)
    print("\n🔍 Executing SQL query:", sql_query)  # Debug line
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(sql_query)

        if cursor.description:  # Có dữ liệu trả về
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            cursor.close()
            conn.close()
            return columns, rows
        else:
            conn.commit()
            cursor.close()
            conn.close()
            return None, None

    except Exception as e:
        print("❌ Lỗi khi chạy SQL:", e)
        return None, None

# 📦 Tải schema từ các bảng
def get_all_tables_schema():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()

    schema = ""
    for (table_name,) in tables:
        cursor.execute(f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
        """, (table_name,))
        columns = cursor.fetchall()
        column_list = ", ".join(f"{col} ({dtype})" for col, dtype in columns)
        schema += f"\nTABLE {table_name}: {column_list}\n"

    cursor.close()
    conn.close()
    return schema

def format_column_name(column):
    # Replace underscores with spaces and capitalize first letter of each word
    return ' '.join(word.capitalize() for word in column.split('_'))

def format_results(columns, rows, user_question):
    if not rows:
        return "Không tìm thấy kết quả phù hợp với yêu cầu của bạn."
    
    # Format the results into a natural language response
    response = f"Dựa vào yêu cầu '{user_question}', tôi tìm thấy {len(rows)} kết quả:\n\n"
    
    for i, row in enumerate(rows, 1):
        response += f"Kết quả {i}:\n"
        for col, val in zip(columns, row):
            if val is not None:  # Only include non-null values
                formatted_col = format_column_name(col)
                response += f"- {formatted_col}: {val}\n"
        response += "\n"
    
    return response

# 🚀 Main pipeline
def process_query(user_question):
    schema = get_all_tables_schema()
    print("\n🤖 Generating SQL query...")
    generated_sql = generate_sql_from_prompt(user_question, schema)
    print("\n📝 SQL sinh ra:\n", generated_sql)

    print("\n▶️ Đang chạy truy vấn...")
    result = run_sql_query(generated_sql)
    if result:
        columns, rows = result
    else:
        columns, rows = None, None
    
    return format_results(columns, rows, user_question)

def main():
    user_question = "Cho tôi biết thông tin của một số hướng dẫn viên ở có nơi cấp thẻ ở Hồ Chí Minh"
    # user_question = "Cho tôi biết thông tin của một số nơi lưu trú ở Hà Nội"
    # user_question = "Cho tôi biết thông tin của một số hướng dẫn viên tại điểm du lịch Hội An"
    
    result = process_query(user_question)
    print("\n📋 Kết quả:")
    print(result)

if __name__ == "__main__":
    main()
