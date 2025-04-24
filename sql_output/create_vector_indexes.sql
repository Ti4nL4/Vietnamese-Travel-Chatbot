-- Create vector-specific indexes for better vector query performance

-- First, ensure the necessary extensions are installed
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Create vector indexes for điểm_đến_nổi_tiếng table
-- Assuming you have a vector column named 'embedding' for vector similarity search
CREATE INDEX IF NOT EXISTS idx_diem_den_embedding_ivfflat ON điểm_đến_nổi_tiếng USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_diem_den_embedding_hnsw ON điểm_đến_nổi_tiếng USING hnsw (embedding vector_cosine_ops);

-- Create vector indexes for nhà_hàng table
CREATE INDEX IF NOT EXISTS idx_nha_hang_embedding_ivfflat ON nhà_hàng USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_nha_hang_embedding_hnsw ON nhà_hàng USING hnsw (embedding vector_cosine_ops);

-- Create vector indexes for lưu_trú table
CREATE INDEX IF NOT EXISTS idx_luu_tru_embedding_ivfflat ON lưu_trú USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_luu_tru_embedding_hnsw ON lưu_trú USING hnsw (embedding vector_cosine_ops);

-- Create vector indexes for vận_tải table
CREATE INDEX IF NOT EXISTS idx_van_tai_embedding_ivfflat ON vận_tải USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_van_tai_embedding_hnsw ON vận_tải USING hnsw (embedding vector_cosine_ops);

-- Create vector indexes for cơ_sở_đào_tạo table
CREATE INDEX IF NOT EXISTS idx_co_so_dao_tao_embedding_ivfflat ON cơ_sở_đào_tạo USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_co_so_dao_tao_embedding_hnsw ON cơ_sở_đào_tạo USING hnsw (embedding vector_cosine_ops);

-- Create vector indexes for hiệp_hội table
CREATE INDEX IF NOT EXISTS idx_hiep_hoi_embedding_ivfflat ON hiệp_hội USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_hiep_hoi_embedding_hnsw ON hiệp_hội USING hnsw (embedding vector_cosine_ops);

-- Create vector indexes for vui_chơi_giải_trí table
CREATE INDEX IF NOT EXISTS idx_vui_choi_embedding_ivfflat ON vui_chơi_giải_trí USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_vui_choi_embedding_hnsw ON vui_chơi_giải_trí USING hnsw (embedding vector_cosine_ops);

-- Create vector indexes for mua_sắm table
CREATE INDEX IF NOT EXISTS idx_mua_sam_embedding_ivfflat ON mua_sắm USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_mua_sam_embedding_hnsw ON mua_sắm USING hnsw (embedding vector_cosine_ops);

-- Create vector indexes for thể_thao table
CREATE INDEX IF NOT EXISTS idx_the_thao_embedding_ivfflat ON thể_thao USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_the_thao_embedding_hnsw ON thể_thao USING hnsw (embedding vector_cosine_ops);

-- Create vector indexes for hướng_dẫn_viên table
CREATE INDEX IF NOT EXISTS idx_huong_dan_vien_embedding_ivfflat ON hướng_dẫn_viên USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_huong_dan_vien_embedding_hnsw ON hướng_dẫn_viên USING hnsw (embedding vector_cosine_ops);

-- Create vector indexes for doanh_nghiệp_lữ_hành_quốc_tế table
CREATE INDEX IF NOT EXISTS idx_doanh_nghiep_lu_hanh_embedding_ivfflat ON doanh_nghiệp_lữ_hành_quốc_tế USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
CREATE INDEX IF NOT EXISTS idx_doanh_nghiep_lu_hanh_embedding_hnsw ON doanh_nghiệp_lữ_hành_quốc_tế USING hnsw (embedding vector_cosine_ops);

-- Create GiST indexes for text search on tên_cơ_sở and địa_chỉ columns
-- These will help with LIKE queries and text search operations
CREATE INDEX IF NOT EXISTS idx_diem_den_ten_co_so_gist ON điểm_đến_nổi_tiếng USING gist (tên_cơ_sở gist_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_diem_den_dia_chi_gist ON điểm_đến_nổi_tiếng USING gist (địa_chỉ gist_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_nha_hang_ten_co_so_gist ON nhà_hàng USING gist (tên_cơ_sở gist_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_nha_hang_dia_chi_gist ON nhà_hàng USING gist (địa_chỉ gist_trgm_ops);

-- Add similar GiST indexes for other tables as needed 