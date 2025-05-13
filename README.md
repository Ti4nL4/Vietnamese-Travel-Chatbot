# Tourism LLM Router Project

## Giới thiệu
Dự án này là một hệ thống xử lý và phân tích dữ liệu du lịch sử dụng Large Language Models (LLM) và các công nghệ hiện đại. Hệ thống cho phép tìm kiếm thông tin du lịch thông minh và tạo ra các truy vấn SQL tự động từ ngôn ngữ tự nhiên.

## Kiến trúc hệ thống
![Kiến trúc hệ thống](New_Architecture.png)

## Tính năng chính
- Tìm kiếm ngữ nghĩa (Semantic Search) cho dữ liệu du lịch
- Chuyển đổi ngôn ngữ tự nhiên thành truy vấn SQL
- Xử lý và phân tích dữ liệu du lịch Việt Nam
- Tích hợp với PostgreSQL và pgvector cho lưu trữ vector
- Hỗ trợ tìm kiếm thông minh thông qua FAISS index

## Yêu cầu hệ thống
- Python 3.x
- PostgreSQL với extension pgvector
- Các thư viện Python (xem requirements.txt)

## Cài đặt

1. Clone repository:
```bash
git clone [https://github.com/Ti4nL4/Vietnamese-Travel-Chatbot.git]
cd [Vietnamese-Travel-Chatbot]
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv myenv
source myenv/bin/activate  # Linux/Mac
# hoặc
myenv\Scripts\activate  # Windows
```

3. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

4. Cài đặt pgvector cho PostgreSQL:
```bash
python install_pgvector.py
```

5. Thiết lập cơ sở dữ liệu:
```bash
python setup_database.py
```

## Cấu trúc project
- `semantic_search.py`: Module tìm kiếm ngữ nghĩa
- `llm_sql_generator.py`: Tạo truy vấn SQL từ ngôn ngữ tự nhiên
- `setup_database.py`: Script thiết lập cơ sở dữ liệu
- `data/`: Thư mục chứa dữ liệu
- `faiss_index/`: Thư mục chứa các index tìm kiếm
- `logs/`: Thư mục chứa log files

## Sử dụng
1. Đảm bảo đã cài đặt và cấu hình đúng môi trường
2. Chạy router chính:
```bash
python tourism_llm_router.py
```

## Cấu hình
Tạo file `.env` với các biến môi trường cần thiết:
```
DATABASE_URL=your_database_url
API_KEY=your_api_key
```