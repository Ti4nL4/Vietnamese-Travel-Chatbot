from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

# Tải dữ liệu
loader = TextLoader("cat-facts.txt")
documents = loader.load()

# Tách văn bản thành các đoạn nhỏ
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Sử dụng mô hình nhúng để tạo vector
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Tạo cơ sở dữ liệu FAISS
db = FAISS.from_documents(texts, embeddings)
db.save_local("faiss_index")

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Chọn mô hình sinh văn bản (Ví dụ: Mistral 7B)
model_name = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

def generate_response(prompt):
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")
    output = model.generate(input_ids, max_length=512)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def rag_pipeline(query):
    # Tìm kiếm tài liệu liên quan
    docs = db.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    
    # Tạo prompt cho mô hình sinh văn bản
    prompt = f"Thông tin tham khảo:\n{context}\n\nCâu hỏi: {query}\nTrả lời:"
    
    # Sinh câu trả lời
    response = generate_response(prompt)
    return response

# Ví dụ sử dụng
query = "Những điểm du lịch nổi bật ở Đà Nẵng?"
print(rag_pipeline(query))