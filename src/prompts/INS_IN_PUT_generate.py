INSTRUCTION_GEN_PROMPT = """
# Bạn cần trả về instruction 
# Instruction chỉ chứa thông tin chung chung về vai trò nhiệm vụ role-play của model
# Instruction không được chứa nội dung câu hỏi trong đó
# Instruction ở dạng tiếng Việt.

ví dụ với câu hỏi: Khoa cử Việt Nam có vai trò gì trong việc phát triển nền giáo dục và xã hội của đất nước?
thì instruction có thể là: Bạn là chuyển gia về lịch sử Việt Nam. Nhiệm vụ của bạn là trả lời đầy đủ và chính xác các câu hỏi liên quan đến lịch sử Việt Nam.

câu hỏi: {question}
instruction:
"""

REWRITE_INPUT_PROMPT = """
# Bạn cần viết lại câu hỏi mà không làm đổi nghĩa
# Lưu ý chỉ trả về tiếng Việt
Câu hỏi gốc: {question}
Câu hỏi sau khi viết lại:
"""

PRE_OUTPUT_PROMPT = """Bạn Là một trợ lý ảo bạn cần đưa ra phần mở đầu của câu trả lời dựa vào câu hỏi và chút công tin output
## lưu ý chỉ trả về  phần giới thiệu trước khi trả lời.
## với phần trả về sau đó sẽ được nối vào đầu của ouput để thành answer.
ví dụ:
- đối với câu hỏi trắc nghiệm bạn cần trả về nguyên vần mở đầu ví dụ như: với câu hỏi của bạn là yêu cầu trả lời 1 câu hỏi trắc nghiệm. Dưới đây tôi sẽ đưa ra đáp án chính xác. Sau đó đưa ra giải thích ngắn gọn cho đáp án tôi lựa chọn.
- với yêu cầu tóm tắt văn bản bạn có thể trả về tương tự như sau: câu hỏi của bạn là một câu hỏi yêu cầu tóm tắt nội dung chính 1 đoạn văn. Dưới đây tôi sẽ cung cấp bản tóm tắt các sự kiện quan trọng có trong đoạn văn trên.

instruction of input: {instruction}
input: {input}
output: {output}
phần giới thiệu tương ứng:
"""

PARAPHRASE = """
# Bạn cần viết lại câu sau mà không làm đổi nghĩa, có thể thêm dẫn dắt
# phải giữ lại toàn ý của câu gốc.
# Lưu ý chỉ trả về tiếng Việt
# Bạn cần viết trả lại {num} câu sau viết lại để trong list ["", "", ....] và các câu không trùng nhau.
Dưới đây là các cách paraphrase (diễn đạt lại) để tạo thành cặp câu mới có nội dung tương tự nhưng cách diễn đạt khác nhau:

### 1. *Thay thế từ đồng nghĩa*
   - **Câu gốc**: "Tôi thích đi du lịch."
   - **Câu paraphrase**: "Tôi yêu thích việc đi du lịch."

### 2. *Đảo ngược cấu trúc câu*
   - **Câu gốc**: "Tôi muốn học tiếng Anh."
   - **Câu paraphrase**: "Tiếng Anh là ngôn ngữ tôi muốn học."

### 3. *Thay đổi thì của động từ*
   - **Câu gốc**: "Cô ấy đang làm việc tại công ty này."
   - **Câu paraphrase**: "Cô ấy đã làm việc tại công ty này."

### 4. *Thêm hoặc bớt các chi tiết phụ*
   - **Câu gốc**: "Anh ấy rất giỏi trong việc chơi cờ."
   - **Câu paraphrase**: "Anh ấy là người chơi cờ rất tài giỏi."

### 5. *Sử dụng câu hỏi thay cho câu khẳng định (hoặc ngược lại)*
   - **Câu gốc**: "Bạn thích đọc sách không?"
   - **Câu paraphrase**: "Bạn có sở thích đọc sách không?"

### 6. *Biến đổi thành câu bị động*
   - **Câu gốc**: "Anh ấy đã viết bức thư."
   - **Câu paraphrase**: "Bức thư đã được anh ấy viết."

### 7. *Chia câu thành nhiều câu ngắn*
   - **Câu gốc**: "Cô ấy nấu ăn rất giỏi và luôn làm những món ăn ngon."
   - **Câu paraphrase**: "Cô ấy nấu ăn rất giỏi. Món ăn của cô luôn rất ngon."

### 8. *Thay đổi cấu trúc câu phức thành câu đơn giản*
   - **Câu gốc**: "Nếu trời mưa, chúng tôi sẽ không đi dạo."
   - **Câu paraphrase**: "Chúng tôi sẽ không đi dạo nếu trời mưa."

### 9. *Sử dụng câu khẳng định thay cho câu phủ định (hoặc ngược lại)*
   - **Câu gốc**: "Tôi không thích ăn cay."
   - **Câu paraphrase**: "Tôi không ăn cay."

### 10. *Chuyển từ ngôi thứ 3 sang ngôi thứ 1 hoặc ngược lại*
   - **Câu gốc**: "Họ rất thích xem phim."
   - **Câu paraphrase**: "Chúng tôi rất thích xem phim."
   
Câu gốc: {original_query}
Câu sau khi paraphrase:
"""
