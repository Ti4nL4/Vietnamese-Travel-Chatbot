# Tạo file evaluation_dataset.py
# Tập dữ liệu đánh giá cho hệ thống RAG và SQL

# evaluation_questions = [
#     # # Câu hỏi RAG - Thông tin từ văn bản
#     {
#         "question": "Kích thước và trọng lượng phù điêu Kala Núi Bà?",
#         "expected_answer": "Cao 60cm, đế rộng 44cm, dày 17cm, nặng 105.5kg.",
#         "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Phú Yên: Công bố Bảo vật quốc gia Phù điêu Kala Núi Bà.txt"],
#         "expected_path": "rag"
#     },
#     {
#         "question": "Festival Phở năm 2025 diễn ra ở đâu và vào thời gian nào?",
#         "expected_answer": "Festival Phở năm 2025 diễn ra tại Hoàng thành Thăng Long (Hà Nội) từ ngày 18 đến ngày 20/4/2025.",
#         "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/“Festival Phở năm 2025”: Hội tụ các thương hiệu phở khắp ba miền tại Thủ đô Hà Nội.txt"],
#         "expected_path": "rag"
#     },
#     {
#         "question": "Doanh thu từ du lịch Huế trong Quý I/2025 là bao nhiêu?",
#         "expected_answer": "Doanh thu từ du lịch Huế trong Quý I/2025 ước đạt hơn 2.600 tỷ đồng, tăng hơn 52% so với cùng kỳ.",
#         "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Du lịch Huế thu hơn 2.600 tỷ đồng trong Quý I/2025.txt"],
#         "expected_path": "rag"
#     },
    
#     # Câu hỏi SQL - Thông tin từ cơ sở dữ liệu
#     {
#         "question": "Cho tôi biết thông tin của một số hướng dẫn viên ở Hồ Chí Minh",
#         "expected_answer": "Dựa vào yêu cầu 'Cho tôi biết thông tin của một số hướng dẫn viên ở Hồ Chí Minh', tôi tìm thấy 10 kết quả:",
#         "expected_sources": [],
#         "expected_path": "sql"
#     },
#     {
#         "question": "Cho tôi biết thông tin của một số nơi lưu trú ở Hà Nội",
#         "expected_answer": "Dựa vào yêu cầu 'Cho tôi biết thông tin của một số nơi lưu trú ở Hà Nội', tôi tìm thấy 10 kết quả:",
#         "expected_sources": [],
#         "expected_path": "sql"
#     },
#     {
#         "question": "Cho tôi biết thông tin của một số hướng dẫn viên tại điểm du lịch Hội An",
#         "expected_answer": "Dựa vào yêu cầu 'Cho tôi biết thông tin của một số hướng dẫn viên tại điểm du lịch Hội An', tôi tìm thấy 10 kết quả:",
#         "expected_sources": [],
#         "expected_path": "sql"
#     },
    
#     # Câu hỏi không tìm thấy thông tin
#     # {
#     #     "question": "Thông tin về Festival Cà phê Buôn Ma Thuột năm 2026?",
#     #     "expected_answer": "Không tìm thấy thông tin",
#     #     "expected_sources": [],
#     #     "expected_path": "sql"  # Hệ thống sẽ thử RAG trước, nếu không tìm thấy sẽ chuyển sang SQL
#     # }
# ]
evaluation_questions = [
    {
        "question": "Festival Phở năm 2025 diễn ra ở đâu và vào thời gian nào?",
        "expected_answer": "Festival Phở năm 2025 diễn ra tại Hoàng thành Thăng Long (Hà Nội) từ ngày 18 đến ngày 20/4/2025.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/“Festival Phở năm 2025”: Hội tụ các thương hiệu phở khắp ba miền tại Thủ đô Hà Nội.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Mục đích chính của Festival Phở năm 2025 là gì?",
        "expected_answer": "Mục đích chính của Festival Phở năm 2025 là quảng bá hình ảnh “Phở Hà Nội“ được công nhận là di sản văn hóa phi vật thể quốc gia, góp phần phát triển lĩnh vực Công nghiệp văn hóa ẩm thực Hà Nội.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/“Festival Phở năm 2025”: Hội tụ các thương hiệu phở khắp ba miền tại Thủ đô Hà Nội.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Festival Phở 2025 có bao nhiêu gian hàng tham gia?",
        "expected_answer": "Festival Phở 2025 quy tụ hơn 50 gian hàng của các doanh nghiệp, thương hiệu ẩm thực phở khắp ba miền.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/“Festival Phở năm 2025”: Hội tụ các thương hiệu phở khắp ba miền tại Thủ đô Hà Nội.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Festival Phở 2025 có những không gian hoạt động nào?",
        "expected_answer": "Festival gồm các không gian: giới thiệu văn hóa truyền thống phở, trải nghiệm ẩm thực, tọa đàm và biểu diễn nghệ thuật.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/“Festival Phở năm 2025”: Hội tụ các thương hiệu phở khắp ba miền tại Thủ đô Hà Nội.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Địa điểm cụ thể tổ chức Festival Phở 2025 tại Hoàng thành Thăng Long?",
        "expected_answer": "Sự kiện diễn ra tại Khu vực sân vận động Cột Cờ, số 19C Hoàng Diệu, quận Ba Đình, Hà Nội.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/“Festival Phở năm 2025”: Hội tụ các thương hiệu phở khắp ba miền tại Thủ đô Hà Nội.txt"],
        "expected_path": "rag"
    },
    
    {
        "question": "Ngày hội Du lịch TP. Hồ Chí Minh năm 2025 diễn ra trong thời gian nào?",
        "expected_answer": "Ngày hội Du lịch TP. Hồ Chí Minh năm 2025 diễn ra từ ngày 03 đến ngày 06/4/2025.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Bắc Giang quảng bá, xúc tiến du lịch tại Ngày hội Du lịch TP. Hồ Chí Minh.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Bắc Giang đã giới thiệu những sản phẩm nào tại Ngày hội Du lịch TP. Hồ Chí Minh?",
        "expected_answer": "Bắc Giang đã giới thiệu các sản phẩm nông nghiệp đặc trưng, sản phẩm OCOP, và sản phẩm tiểu thủ công nghiệp làng nghề tiêu biểu như: mỳ chũ, sâm nam núi Dành, chè bản Ven, chè Hoa vàng, vải thiều, cùng các sản phẩm hoa quả đặc trưng khác của tỉnh.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Bắc Giang quảng bá, xúc tiến du lịch tại Ngày hội Du lịch TP. Hồ Chí Minh.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Mục tiêu du lịch của Bắc Giang đến năm 2025 là gì?",
        "expected_answer": "Bắc Giang đặt mục tiêu đến năm 2025 đón ít nhất 3 triệu lượt khách, tổng thu từ du lịch đạt 3 nghìn tỷ đồng, và tạo việc làm cho khoảng 6 nghìn lao động.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Bắc Giang quảng bá, xúc tiến du lịch tại Ngày hội Du lịch TP. Hồ Chí Minh.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Mục tiêu doanh thu du lịch Bắc Giang đến 2030?",
        "expected_answer": "Đến 2030, Bắc Giang phấn đấu đạt 7.5 nghìn tỷ đồng doanh thu từ du lịch và tạo 10 nghìn việc làm.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Bắc Giang quảng bá, xúc tiến du lịch tại Ngày hội Du lịch TP. Hồ Chí Minh.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Bắc Giang giới thiệu những loại hình du lịch nào tại sự kiện Ngày hội Du lịch TP. Hồ Chí Minh?",
        "expected_answer": "Bắc Giang giới thiệu các tour, tuyến du lịch, điểm cung cấp dịch vụ cùng tài nguyên văn hóa như di sản Quan họ.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Bắc Giang quảng bá, xúc tiến du lịch tại Ngày hội Du lịch TP. Hồ Chí Minh.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Các đường bay mới từ Kazakhstan đến Đà Nẵng có tần suất như thế nào?",
        "expected_answer": "Các đường bay từ Kazakhstan đến Đà Nẵng có tần suất 4 chuyến mỗi tuần từ tháng 4 đến tháng 10/2025, bao gồm 2 chuyến từ Almaty vào thứ Ba và thứ Sáu, và 2 chuyến từ Astana vào thứ Tư và thứ Bảy.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Đà Nẵng đón thêm hai chuyến bay mới.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Việc mở đường bay từ Myanmar đến Đà Nẵng có ý nghĩa gì?",
        "expected_answer": "Việc mở đường bay từ Myanmar đến Đà Nẵng đánh dấu cột mốc 8/10 quốc gia trong khu vực Đông Nam Á có đường bay trực tiếp đến Đà Nẵng, nâng tổng số đường bay quốc tế thường kỳ lên 16 đường bay.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Đà Nẵng đón thêm hai chuyến bay mới.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Ai là người phát biểu về ý nghĩa của đường bay Almaty - Đà Nẵng?",
        "expected_answer": "Bà Trương Thị Hồng Hạnh, Giám đốc Sở Du lịch Đà Nẵng, đã phát biểu về ý nghĩa của đường bay Almaty - Đà Nẵng, coi đây là cột mốc quan trọng trong kết nối du lịch với thị trường Kazakhstan và Cộng đồng các quốc gia độc lập (CIS).",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Đà Nẵng đón thêm hai chuyến bay mới.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Số lượng hành khách trên chuyến bay đầu tiên từ Kazakhstan đến Đà Nẵng?",
        "expected_answer": "Chuyến bay VJ52 từ Almaty chở gần 300 hành khách đến Đà Nẵng.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Đà Nẵng đón thêm hai chuyến bay mới.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Hoạt động chào đón khách Kazakhstan đến Đà Nẵng tại sân bay?",
        "expected_answer": "Sở Du lịch tổ chức biểu diễn nghệ thuật, tặng hoa và nón lá lưu niệm cho hành khách.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Đà Nẵng đón thêm hai chuyến bay mới.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Những sự kiện nào sẽ diễn ra tại Đà Nẵng trong năm 2025?",
        "expected_answer": "Năm 2025, Đà Nẵng sẽ tổ chức nhiều sự kiện lớn như Đại hội Du lịch golf châu Á, DIFF 2025, Liên hoan phim châu Á, lễ hội Tận hưởng Đà Nẵng, IRONMAN 70.3 Viet Nam, Lễ hội Vietnam - Asean, và lễ hội bóng đá Việt Nam - Anh Quốc 2025.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Đà Nẵng: Sản phẩm du lịch đa dạng, hướng đến chiều sâu.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Đà Nẵng đang tập trung khai thác thị trường khách du lịch nào?",
        "expected_answer": "Đà Nẵng đang tập trung khai thác thị trường khách du lịch Nga, Đông Âu, Trung Đông, với các resort biệt lập ven biển, trung tâm thương mại lớn, và các điểm du lịch như Ngũ Hành Sơn, Bà Nà Hills, phố cổ Hội An.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Đà Nẵng: Sản phẩm du lịch đa dạng, hướng đến chiều sâu.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Show Tiên Sa tại Đà Nẵng có thời lượng bao lâu?",
        "expected_answer": "Show diễn kéo dài 60 phút, giới thiệu thiên nhiên, văn hóa Đà Nẵng.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Đà Nẵng: Sản phẩm du lịch đa dạng, hướng đến chiều sâu.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Số lượng sân golf tại Đà Nẵng năm 2025?",
        "expected_answer": "Năm 2025, Đà Nẵng và miền Trung có 8 sân golf đẳng cấp quốc tế.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Đà Nẵng: Sản phẩm du lịch đa dạng, hướng đến chiều sâu.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Lợi thế của resort Đà Nẵng với khách Trung Đông?",
        "expected_answer": "Các resort biệt lập ven biển phù hợp xu hướng nghỉ dưỡng cao cấp của khách Trung Đông.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Đà Nẵng: Sản phẩm du lịch đa dạng, hướng đến chiều sâu.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Doanh thu từ du lịch Huế trong Quý I/2025 là bao nhiêu?",
        "expected_answer": "Doanh thu từ du lịch Huế trong Quý I/2025 ước đạt hơn 2.600 tỷ đồng, tăng hơn 52% so với cùng kỳ.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Du lịch Huế thu hơn 2.600 tỷ đồng trong Quý I/2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Top 10 thị trường khách hàng đầu đến Huế trong Quý I/2025 bao gồm những quốc gia nào?",
        "expected_answer": "Top 10 thị trường khách hàng đầu đến Huế trong Quý I/2025 bao gồm: Pháp, Mỹ, Đức, Anh, Malaysia, Ý, Đài Loan (Trung Quốc), Úc, Canada, Thái Lan.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Du lịch Huế thu hơn 2.600 tỷ đồng trong Quý I/2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Mục tiêu lượng khách du lịch đến Huế trong năm 2025 là gì?",
        "expected_answer": "Huế kỳ vọng thu hút khoảng 4,8 - 5 triệu lượt khách du lịch trong năm 2025, trong đó khách quốc tế chiếm khoảng 38 - 40% tổng lượt khách.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Du lịch Huế thu hơn 2.600 tỷ đồng trong Quý I/2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Tăng trưởng khách quốc tế đến Huế Quý I/2025?",
        "expected_answer": "Khách quốc tế tăng gần 50%, đạt 666 nghìn lượt so với cùng kỳ.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Du lịch Huế thu hơn 2.600 tỷ đồng trong Quý I/2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Mục tiêu doanh thu du lịch Huế 2025?",
        "expected_answer": "Dự kiến đạt 10.800 - 11.200 tỷ đồng trong năm 2025.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Du lịch Huế thu hơn 2.600 tỷ đồng trong Quý I/2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Sự kiện nào tạo điểm nhấn cho du lịch Huế đầu năm 2025?",
        "expected_answer": "Lễ khai mạc Năm Du lịch quốc gia - Huế 2025 gắn với Festival Huế.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Du lịch Huế thu hơn 2.600 tỷ đồng trong Quý I/2025.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Tàu Insignia thuộc hãng tàu nào và có quốc tịch gì?",
        "expected_answer": "Tàu Insignia thuộc hãng tàu Oceania Cruise (Mỹ) và mang quốc tịch đảo Marshall.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Khánh Hòa đón chuyến tàu du lịch biển thứ 11 trong năm 2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Hải trình của tàu Insignia tại Việt Nam bao gồm những cảng nào?",
        "expected_answer": "Hải trình gồm: Cảng Khánh Hội (TP. Hồ Chí Minh) - Cảng quốc tế Cam Ranh (Khánh Hòa) - Cảng Chân Mây (TP. Huế).",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Khánh Hòa đón chuyến tàu du lịch biển thứ 11 trong năm 2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Các hoạt động du lịch mà khách trên tàu Insignia tham gia tại Nha Trang?",
        "expected_answer": "Khách tham gia các tour: city tour Nha Trang, tour ngoại thành, tham quan bằng xích lô, Sông Cái, Làng nghề Trường Sơn, Khu bảo tồn Trầm hương Hoàng Trầm.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Khánh Hòa đón chuyến tàu du lịch biển thứ 11 trong năm 2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Thông số kỹ thuật của tàu Insignia?",
        "expected_answer": "Tàu dài 181m, sức chứa 684 hành khách và 400 thuyền viên, trang bị nhà hàng, bar, hồ bơi, spa cao cấp.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Khánh Hòa đón chuyến tàu du lịch biển thứ 11 trong năm 2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Số lượng khách du lịch trên tàu Insignia khi cập cảng Cam Ranh?",
        "expected_answer": "Tàu mang theo 550 du khách khi cập cảng Cam Ranh.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Khánh Hòa đón chuyến tàu du lịch biển thứ 11 trong năm 2025.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Mục tiêu lượng khách du lịch của TP.HCM năm 2025?",
        "expected_answer": "Đón 45 triệu lượt khách nội địa và 8.5 triệu lượt khách quốc tế.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Ngành du lịch TP Hồ Chí Minh thi đua chào mừng kỷ niệm 50 năm giải phóng miền Nam.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Giải pháp chuyển đổi số ngành du lịch TP.HCM?",
        "expected_answer": "Hoàn thiện thủ tục hành chính điện tử, xây dựng ứng dụng du lịch thông minh, bản đồ tương tác 3D/360, cổng thông tin visithcmc.vn.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Ngành du lịch TP Hồ Chí Minh thi đua chào mừng kỷ niệm 50 năm giải phóng miền Nam.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Thách thức doanh nghiệp du lịch TP.HCM đang gặp phải?",
        "expected_answer": "Chi phí vận hành cao, thiếu nhân lực chất lượng, thủ tục hành chính phức tạp, khó tiếp cận chính sách hỗ trợ tài chính.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Ngành du lịch TP Hồ Chí Minh thi đua chào mừng kỷ niệm 50 năm giải phóng miền Nam.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Đề xuất của doanh nghiệp để phát triển du lịch TP.HCM?",
        "expected_answer": "Hỗ trợ đoàn khách MICE, phát triển sản phẩm gắn với văn hóa và du lịch xanh, đẩy mạnh truyền thông quốc tế.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Ngành du lịch TP Hồ Chí Minh thi đua chào mừng kỷ niệm 50 năm giải phóng miền Nam.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Ai là người phát biểu tại hội nghị phát động thi đua chào mừng kỷ niệm 50 năm giải phóng miền Nam do sở Du lịch TP Hồ Chí Minh tổ chức?",
        "expected_answer": "Bà Nguyễn Thị Ánh Hoa - Giám đốc Sở Du lịch TP.HCM.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Ngành du lịch TP Hồ Chí Minh thi đua chào mừng kỷ niệm 50 năm giải phóng miền Nam.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Số lượng đền thờ Vua Hùng trên cả nước?",
        "expected_answer": "Gần 1.500 đền thờ, riêng Phú Thọ có hàng trăm di tích.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Phú Thọ: Lan tỏa Tín ngưỡng thờ cúng Hùng Vương.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Ngày tổ chức Lễ dâng hương tưởng niệm các Vua Hùng 2025?",
        "expected_answer": "Ngày 10/3 năm Ất Tỵ (âm lịch).",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Phú Thọ: Lan tỏa Tín ngưỡng thờ cúng Hùng Vương.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Biện pháp đảm bảo an ninh tại Đền Hùng 2025?",
        "expected_answer": "Tăng cường kiểm tra liên ngành, quản lý hộ kinh doanh, xử lý bán hàng rong, giải tỏa vi phạm.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Phú Thọ: Lan tỏa Tín ngưỡng thờ cúng Hùng Vương.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Tên 3 ngôi đền chính trên núi Nghĩa Lĩnh?",
        "expected_answer": "Đền Hạ, Đền Trung, Đền Thượng thuộc Khu Di tích Đền Hùng.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Phú Thọ: Lan tỏa Tín ngưỡng thờ cúng Hùng Vương.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Các huyện nào ở Phú Thọ có không gian thờ cúng Hùng Vương?",
        "expected_answer": "Cẩm Khê, Lâm Thao, Đoan Hùng, Hạ Hòa, Phù Ninh, Tam Nông, Thanh Ba, Thanh Sơn, Tân Sơn, Thanh Thủy, Yên Lập, thị xã Phú Thọ và thành phố Việt Trì.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Phú Thọ: Lan tỏa Tín ngưỡng thờ cúng Hùng Vương.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Kích thước và trọng lượng phù điêu Kala Núi Bà?",
        "expected_answer": "Cao 60cm, đế rộng 44cm, dày 17cm, nặng 105.5kg.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Phú Yên: Công bố Bảo vật quốc gia Phù điêu Kala Núi Bà.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Nơi phát hiện phù điêu Kala?",
        "expected_answer": "Di tích Núi Bà, xã Hòa Phong, huyện Tây Hòa (Phú Yên) năm 1993.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Phú Yên: Công bố Bảo vật quốc gia Phù điêu Kala Núi Bà.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Phong cách nghệ thuật của phù điêu Kala?",
        "expected_answer": "Thuộc phong cách Tháp Mẫm (Bình Định) muộn, thế kỷ XIV.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Phú Yên: Công bố Bảo vật quốc gia Phù điêu Kala Núi Bà.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Biểu tượng Kala trong văn hóa Champa?",
        "expected_answer": "Là đầu con quái vật bị thần Shiva khuất phục, biểu tượng của hủy diệt và tái tạo trong Ấn Độ giáo.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Phú Yên: Công bố Bảo vật quốc gia Phù điêu Kala Núi Bà.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Tên các di tích Chăm tiêu biểu tại Phú Yên?",
        "expected_answer": "Tháp Nhạn (di tích quốc gia đặc biệt), Thành Hồ, Tháp Chăm Đông Tác.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Phú Yên: Công bố Bảo vật quốc gia Phù điêu Kala Núi Bà.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Tổng giá trị ưu đãi kích cầu du lịch Quảng Nam 2025?",
        "expected_answer": "10 tỷ đồng cho các chương trình ưu đãi.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Quảng Nam dành ưu đãi 10 tỷ đồng kích cầu du lịch.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Các sản phẩm du lịch được ưu đãi 50% trong chương trình ưu đãi của Quảng Nam 2025?",
        "expected_answer": "Tour rừng dừa Bảy Mẫu, làng gốm Thanh Hà Deluxe Terra Tour, vé show Ký ức Hội An, bay dù lượn, chương trình 'ở 3 trả tiền 2'.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Quảng Nam dành ưu đãi 10 tỷ đồng kích cầu du lịch.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Số doanh nghiệp tham gia chương trình kích cầu du lịch Quảng Nam 2025?",
        "expected_answer": "Hơn 70 doanh nghiệp du lịch trên địa bàn tỉnh.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Quảng Nam dành ưu đãi 10 tỷ đồng kích cầu du lịch.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Các điểm đến độc đáo trong chương trình ưu đãi của Quảng Nam 2025?",
        "expected_answer": "Bản làng dân tộc Cơ Tu, Ca Dong, đỉnh Quế - Tây Giang, Cổng trời Đông Giang.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Quảng Nam dành ưu đãi 10 tỷ đồng kích cầu du lịch.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Tên 'Cung đường di sản' của Quảng Nam 2025 bao gồm những điểm nào?",
        "expected_answer": "Hội An - Mỹ Sơn - Cổng trời Đông Giang.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Quảng Nam dành ưu đãi 10 tỷ đồng kích cầu du lịch.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Cặp cửa khẩu nào được thông quan cho du lịch biên giới tại Quảng Ninh?",
        "expected_answer": "Cặp cửa khẩu Hoành Mô (Việt Nam) - Động Trung (Trung Quốc).",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Quảng Ninh: Thúc đẩy du lịch biên giới.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Số lượng khách Trung Quốc trung bình mỗi ngày qua cửa khẩu Hoành Mô?",
        "expected_answer": "Khoảng 200 lượt khách/ngày, chủ yếu đi về trong ngày.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Quảng Ninh: Thúc đẩy du lịch biên giới.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Các tour du lịch biên giới đặc trưng tại Bình Liêu?",
        "expected_answer": "Tour Cửa khẩu Hoành Mô - Chợ phiên Bình Liêu - Thác Khe Vằn - Núi Cao Ly; tour đến vườn hoa Cao Sơn và khu trồng dong riềng.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Quảng Ninh: Thúc đẩy du lịch biên giới.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Mục tiêu du lịch của Quảng Ninh năm 2025?",
        "expected_answer": "Đón 20 triệu lượt khách, trong đó du lịch biên giới là trọng tâm.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Quảng Ninh: Thúc đẩy du lịch biên giới.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Hoạt động giao lưu nào sẽ diễn ra tại Móng Cái dịp 30/4?",
        "expected_answer": "Giải đạp xe qua biên giới và các hoạt động văn hóa thể thao khác.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Quảng Ninh: Thúc đẩy du lịch biên giới.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Địa điểm tổ chức Lễ tri ân Quốc Tổ tại Cà Mau?",
        "expected_answer": "Khu du lịch Mũi Cà Mau, huyện Ngọc Hiển.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Sôi động, tự hào với Cà Mau - Ðiểm đến 2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Các hoạt động tại Lễ giỗ Tổ Hùng Vương ở Cà Mau?",
        "expected_answer": "Trò chơi dân gian (bơi xuồng ba lá, kéo co), văn nghệ, và nghi thức dâng hương.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Sôi động, tự hào với Cà Mau - Ðiểm đến 2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Ý nghĩa của Di tích Bến Vàm Lũng?",
        "expected_answer": "Là một trong 4 bến tiếp nhận vũ khí từ miền Bắc vào Nam trong kháng chiến chống Mỹ, thuộc đường Hồ Chí Minh trên biển.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Sôi động, tự hào với Cà Mau - Ðiểm đến 2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Đền thờ Vua Hùng tại Cà Mau có từ khi nào?",
        "expected_answer": "Hơn 200 năm trước, được công nhận Di tích cấp tỉnh năm 2011.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Sôi động, tự hào với Cà Mau - Ðiểm đến 2025.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Các môn thi đấu thể thao tại Lễ tri ân Quốc Tổ?",
        "expected_answer": "Bóng chuyền hơi nữ, kéo co, nhảy bao bố tiếp sức, sút bóng cầu môn, và đá gà ép.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Sôi động, tự hào với Cà Mau - Ðiểm đến 2025.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Mục tiêu của Hội nghị xúc tiến du lịch Thái Nguyên tại Hà Nội?",
        "expected_answer": "Quảng bá sản phẩm du lịch gắn với văn hóa Trà và tuyến đường sắt Hà Nội - Thái Nguyên, thu hút đầu tư.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Tỉnh Thái Nguyên tổ chức xúc tiến, quảng bá du lịch tại Hà Nội.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Thế mạnh du lịch của Thái Nguyên?",
        "expected_answer": "Hơn 1.000 di tích, 300 làng nghề, 300 sản phẩm OCOP, cảnh quan núi rừng, hồ nước, và thủ phủ chè với diện tích 22.200 ha.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Tỉnh Thái Nguyên tổ chức xúc tiến, quảng bá du lịch tại Hà Nội.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Sự kiện nào Thái Nguyên sẽ tổ chức cuối tháng 4/2025?",
        "expected_answer": "Tuần VHTTDL và khai mạc mùa du lịch với các giải đấu Yoga, Võ cổ truyền, đua thuyền, trình diễn khinh khí cầu.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Tỉnh Thái Nguyên tổ chức xúc tiến, quảng bá du lịch tại Hà Nội.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Doanh thu từ chè của Thái Nguyên ước đạt bao nhiêu?",
        "expected_answer": "Hơn 13.000 tỷ đồng/năm với sản lượng 267.500 tấn búp tươi.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Tỉnh Thái Nguyên tổ chức xúc tiến, quảng bá du lịch tại Hà Nội.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Các điểm du lịch sinh thái nổi bật tại Thái Nguyên?",
        "expected_answer": "Hồ Núi Cốc, Hồ Ghềnh Chè, Tam Đảo, và đồi chè Tân Cương.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Tỉnh Thái Nguyên tổ chức xúc tiến, quảng bá du lịch tại Hà Nội.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Thông điệp (slogan) du lịch TP.HCM năm 2025?",
        "expected_answer": "'Find Your Vibes' (Đi tìm cảm xúc của bạn), mời gọi khám phá đa sắc màu văn hóa.",
        "expected_sources": ["TP Hồ Chí Minh công bố bộ nhận diện và thông điệp du lịch thành phố.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Địa điểm triển lãm 50 ảnh đẹp du lịch TP.HCM?",
        "expected_answer": "Công viên 23/9, quận 1.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/TP Hồ Chí Minh công bố bộ nhận diện và thông điệp du lịch thành phố.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Giải nhất cuộc thi thiết kế chương trình du lịch chào mừng 30/4?",
        "expected_answer": "Bảng A: 'Từ Mậu Thân đến mùa xuân đại thắng' của Công ty Chim Cánh Cụt; Bảng B: 'Biệt động Sài Gòn - Những căn hầm huyền thoại' của Nhóm Penguins Team.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/TP Hồ Chí Minh công bố bộ nhận diện và thông điệp du lịch thành phố.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Thời điểm công bố bộ nhận diện du lịch TP.HCM?",
        "expected_answer": "Ngày 02/4/2025, nhân kỷ niệm 50 năm Ngày giải phóng miền Nam.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/TP Hồ Chí Minh công bố bộ nhận diện và thông điệp du lịch thành phố.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Đặc điểm thiết kế logo du lịch TP.HCM?",
        "expected_answer": "Linh hoạt, có thể biến đổi theo từng chiến dịch, thể hiện sự năng động và sáng tạo.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/TP Hồ Chí Minh công bố bộ nhận diện và thông điệp du lịch thành phố.txt"],
        "expected_path": "rag"
    },

    {
        "question": "Chủ đề và thời gian tổ chức Tuần Du lịch Ninh Bình 2025?",
        "expected_answer": "Chủ đề 'Sắc vàng Tam Cốc - Tràng An', diễn ra 7 ngày cuối tháng 5/2025.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Tuần Du lịch Ninh Bình 2025: Đánh thức giá trị di sản, bứt phá trở thành điểm đến hàng đầu châu Á.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Các hoạt động chính trong Tuần Du lịch?",
        "expected_answer": "Trình diễn thời trang 'Di sản dành cho cuộc sống', triển lãm ảnh 'Mùa vàng Tam Cốc', biểu diễn múa rối nước, hát chèo, và hội thi ẩm thực.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Tuần Du lịch Ninh Bình 2025: Đánh thức giá trị di sản, bứt phá trở thành điểm đến hàng đầu châu Á.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Giải pháp để Ninh Bình trở thành điểm đến hàng đầu châu Á?",
        "expected_answer": "Đầu tư vào sản phẩm đặc trưng (tour mùa vàng, mùa sen), truyền thông số, xây dựng hạ tầng thông minh, đào tạo nhân lực, và liên kết vùng.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Tuần Du lịch Ninh Bình 2025: Đánh thức giá trị di sản, bứt phá trở thành điểm đến hàng đầu châu Á.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Di sản thế giới nào Ninh Bình sở hữu?",
        "expected_answer": "Quần thể danh thắng Tràng An - Di sản Văn hóa và Thiên nhiên thế giới đầu tiên ở Đông Nam Á.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Tuần Du lịch Ninh Bình 2025: Đánh thức giá trị di sản, bứt phá trở thành điểm đến hàng đầu châu Á.txt"],
        "expected_path": "rag"
    },
    {
        "question": "Các địa phương nào Ninh Bình muốn liên kết du lịch?",
        "expected_answer": "Hà Nội, Quảng Ninh, Thanh Hóa để tạo hành trình di sản Bắc Bộ.",
        "expected_sources": ["/Users/letien/DoAn/myenv/rag_data/text/Tuần Du lịch Ninh Bình 2025: Đánh thức giá trị di sản, bứt phá trở thành điểm đến hàng đầu châu Á.txt"],
        "expected_path": "rag"
    },

    ##-----------------------------------SQL-----------------------------------###
    # Test cases for cơ_sở_đào_tạo table
    {
        "question": "Hãy cho tôi biết thông tin của một số cơ sở đào tạo du lịch có địa chỉ ở thành phố Hồ Chí Minh",
        "expected_answer": "Dựa vào yêu cầu 'Hãy cho tôi biết thông tin của một số cơ sở đào tạo du lịch có địa chỉ ở thành phố Hồ Chí Minh', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Hãy cho tôi biết thông tin của trường Cao đẳng Du lịch Vũng Tàu",
        "expected_answer": "Dựa vào yêu cầu 'Hãy cho tôi biết thông tin của trường Cao đẳng Du lịch Vũng Tàu', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tôi muốn tìm trường đào tạo du lịch ở Hà Nội",
        "expected_answer": "Dựa vào yêu cầu 'Tôi muốn tìm trường đào tạo du lịch ở Hà Nội', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },

    # Test cases for hướng_dẫn_viên table
    {
        "question": "Cho tôi biết thông tin của một số hướng dẫn viên ở Hồ Chí Minh",
        "expected_answer": "Dựa vào yêu cầu 'Cho tôi biết thông tin của một số hướng dẫn viên ở Hồ Chí Minh', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Liệt kê các hướng dẫn viên ở điểm du lịch Cù Lao Chàm",
        "expected_answer": "Dựa vào yêu cầu 'Liệt kê các hướng dẫn viên ở điểm du lịch Cù Lao Chàm', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tìm các hướng dẫn viên có thể nói tiếng Hàn (Korean)",
        "expected_answer": "Dựa vào yêu cầu 'Tìm các hướng dẫn viên có thể nói tiếng Hàn (Korean)', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },

    # Test cases for lưu_trú table
    {
        "question": "Cho tôi biết thông tin của một số nơi lưu trú ở Hà Nội",
        "expected_answer": "Dựa vào yêu cầu 'Cho tôi biết thông tin của một số nơi lưu trú ở Hà Nội', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Liệt kê các khách sạn có trên 300 phòng",
        "expected_answer": "Dựa vào yêu cầu 'Liệt kê các khách sạn có trên 300 phòng', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tìm các biệt thự du lịch ở Hội An",
        "expected_answer": "Dựa vào yêu cầu 'Tìm các biệt thự du lịch ở Hội An', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },

    # Test cases for nhà_hàng table
    {
        "question": "Cho tôi biết một số nhà hàng ở Cà Mau",
        "expected_answer": "Dựa vào yêu cầu 'Cho tôi biết một số nhà hàng ở Cà Mau', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tôi muốn tìm một số quán ăn The Pizza Company",
        "expected_answer": "Dựa vào yêu cầu 'Tôi muốn tìm một số quán ăn The Pizza Company', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tôi muốn tìm địa điểm ăn uống ở quận 1",
        "expected_answer": "Dựa vào yêu cầu 'Tôi muốn tìm địa điểm ăn uống ở quận 1', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },

    # Test cases for điểm_đến_nổi_tiếng table
    {
        "question": "Cho tôi biết các điểm du lịch nổi tiếng ở Huế",
        "expected_answer": "Dựa vào yêu cầu 'Cho tôi biết các điểm du lịch nổi tiếng ở Huế', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tôi muốn biết thông tin về Vườn quốc gia Bạch Mã",
        "expected_answer": "Dựa vào yêu cầu 'Tôi muốn biết thông tin về Vườn quốc gia Bạch Mã', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Hãy cho tôi một vài thông tin về Khu di tích Trường Dục Thanh",
        "expected_answer": "Dựa vào yêu cầu 'Hãy cho tôi một vài thông tin về Khu di tích Trường Dục Thanh', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },

    # Test cases for doanh_nghiệp_lữ_hành_quốc_tế table
    {
        "question": "Tôi cần tìm một vài công ty du lịch ở Đà Nẵng",
        "expected_answer": "Dựa vào yêu cầu 'Tôi cần tìm một vài công ty du lịch ở Đà Nẵng', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tôi muốn biết thông tin về Công ty TNHH Du lịch Điện Biên",
        "expected_answer": "Dựa vào yêu cầu 'Tôi muốn biết thông tin về Công ty TNHH Du lịch Điện Biên', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tôi muốn tìm đại lý du lịch ở thành phố Hồ Chí Minh",
        "expected_answer": "Dựa vào yêu cầu 'Tôi muốn tìm đại lý du lịch ở thành phố Hồ Chí Minh', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },

    # Test cases for mua_sắm table
    {
        "question": "Cho tôi biết các trung tâm thương mại lớn ở Hà Nội",
        "expected_answer": "Dựa vào yêu cầu 'Cho tôi biết các trung tâm thương mại lớn ở Hà Nội', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Liệt kê các chợ đêm nổi tiếng ở Việt Nam",
        "expected_answer": "Dựa vào yêu cầu 'Liệt kê các chợ đêm nổi tiếng ở Việt Nam', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tìm một vài điểm mua sắm ở Long An",
        "expected_answer": "Dựa vào yêu cầu 'Tìm một vài điểm mua sắm ở Long An', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },

    # Test cases for vận_tải table
    {
        "question": "Cho tôi biết các công ty taxi uy tín ở Bình Dương",
        "expected_answer": "Dựa vào yêu cầu 'Cho tôi biết các công ty taxi uy tín ở Bình Dương', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Liệt kê các doanh nghiệp vận tải ở An Giang",
        "expected_answer": "Dựa vào yêu cầu 'Liệt kê các doanh nghiệp vận tải ở An Giang', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tôi cần thông tin về nhà xe Đồng xanh Motorbike",
        "expected_answer": "Dựa vào yêu cầu 'Tôi cần thông tin về nhà xe Đồng xanh Motorbike', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },

    # Test cases for vui_chơi_giải_trí table
    {
        "question": "Cho tôi thông tin của một số trung tâm thương mại Vincom Plaza",
        "expected_answer": "Dựa vào yêu cầu 'Cho tôi thông tin của một số trung tâm thương mại Vincom Plaza', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tôi cần thông tin về Quảng trường Hồ Chí Minh",
        "expected_answer": "Dựa vào yêu cầu 'Tôi cần thông tin về Quảng trường Hồ Chí Minh', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tìm các khu vui chơi giải trí ở Khánh Hòa",
        "expected_answer": "Dựa vào yêu cầu 'Tìm các khu vui chơi giải trí ở Khánh Hòa', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },

    # Test cases for hiệp_hội table
    {
        "question": "Cho tôi biết thông tin về Hiệp hội du lịch Việt Nam",
        "expected_answer": "Dựa vào yêu cầu 'Cho tôi biết thông tin về Hiệp hội du lịch Việt Nam', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Địa chỉ của Hiệp hội du lịch Vĩnh Phúc",
        "expected_answer": "Dựa vào yêu cầu 'Địa chỉ của Hiệp hội du lịch Vĩnh Phúc', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tìm thông tin liên hệ của Hiệp hội du lịch An Giang",
        "expected_answer": "Dựa vào yêu cầu 'Tìm thông tin liên hệ của Hiệp hội du lịch An Giang', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },

    # Test cases for thể_thao table
    {
        "question": "Tôi muốn tìm sân golf ở Hà Nội",
        "expected_answer": "Dựa vào yêu cầu 'Tôi muốn tìm sân golf ở Hà Nội', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Liệt kê một vài cơ sở thể thao ở thành phố Hồ Chí Minh",
        "expected_answer": "Dựa vào yêu cầu 'Liệt kê một vài cơ sở thể thao ở thành phố Hồ Chí Minh', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    },
    {
        "question": "Tìm một vài phòng gym ở Đồng Tháp",
        "expected_answer": "Dựa vào yêu cầu 'Tìm một vài phòng gym ở Đồng Tháp', tôi tìm thấy 10 kết quả:",
        "expected_sources": [],
        "expected_path": "sql"
    }
]
