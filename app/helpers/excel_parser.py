import json
from openpyxl import load_workbook

def aptis_reading_to_json(file_path):
    """
    Chuyển đổi file Excel APTIS Reading thành cấu trúc JSON
    
    Args:
        file_path (str): Đường dẫn đến file Excel
        
    Returns:
        dict: Dữ liệu đã được chuyển đổi sang JSON
    """
    # Load workbook
    wb = load_workbook(filename=file_path)
    
    # Khởi tạo cấu trúc dữ liệu
    data = {
        "part1": [],
        "part2": [],
        "part3": [],
        "part4": []
    }
    
    # Xử lý Part 1 (giữ nguyên)
    ws = wb["part1"]
    current_group = None
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0]:
            current_group = {
                "group": row[0],
                "questions": []
            }
            data["part1"].append(current_group)
        if row[1] is not None:
            question = {
                "sentence": row[1],
                "correct_answer": row[2],
                "options": [row[3], row[4], row[5]]
            }
            current_group["questions"].append(question)
    
    # Xử lý Part 2 (giữ nguyên)
    ws = wb["part2"]
    current_topic = None
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0]:
            current_topic = {
                "topic": row[0],
                "sentences": []
            }
            data["part2"].append(current_topic)
        
        if row[1] is not None:
            sentence = {
                "key": row[1],
                "text": row[2],
                "is_example_first": row[3]
            }
            current_topic["sentences"].append(sentence)
    
    # Xử lý Part 3 (cấu trúc mới)
    ws = wb["part3"]
    current_topic = None
    for row in ws.iter_rows(min_row=2, values_only=True):
        # Xử lý khi gặp topic mới
        if row[0]:
            # Lưu topic trước đó nếu có
            if current_topic is not None:
                data["part3"].append(current_topic)
            
            # Tạo topic mới với cấu trúc mới
            current_topic = {
                "topic": row[0],
                "questions": [],
                "person_A": row[3] if row[3] else "",
                "person_B": row[4] if row[4] else "",
                "person_C": row[5] if row[5] else "",
                "person_D": row[6] if row[6] else ""
            }
        
        # Thêm câu hỏi cho topic hiện tại
        if row[1]:
            question = {
                "text": row[1],
                "correct_answer": row[2]
            }
            current_topic["questions"].append(question)
    
    # Lưu topic cuối cùng
    if current_topic is not None:
        data["part3"].append(current_topic)
    
    # Xử lý Part 4 (cấu trúc mới)
    ws = wb["part4"]
    current_topic = None
    
    # Lấy tất cả các header từ cột D (bỏ qua hàng đầu tiên)
    headers = []
    for row in ws.iter_rows(min_row=2, min_col=4, max_col=4, values_only=True):
        if row[0] and row[0].strip():
            headers.append(row[0])
    
    # Xử lý nội dung
    current_topic = None
    for row in ws.iter_rows(min_row=2, max_col=3, values_only=True):
        if row[0]:
            # Lưu topic trước đó nếu có
            if current_topic is not None:
                data["part4"].append(current_topic)
            
            # Tạo topic mới với cấu trúc mới
            current_topic = {
                "topic": row[0],
                "options": headers,
                "questions": []
            }
        
        # Thêm câu hỏi nếu có nội dung đoạn văn
        if row[1]:
            # Chuyển đổi correct_answer thành số nguyên
            try:
                correct_id = int(float(row[2])) - 1 if row[2] else None
            except (TypeError, ValueError):
                correct_id = None
            
            question = {
                "text": row[1],
                "correct_answer": correct_id
            }
            current_topic["questions"].append(question)
    
    # Lưu topic cuối cùng
    if current_topic is not None:
        data["part4"].append(current_topic)
    
    return data

# Ví dụ sử dụng
if __name__ == "__main__":
    json_data = aptis_reading_to_json("aptis_1_reading_template.xlsx")
    print(json.dumps(json_data, indent=2, ensure_ascii=False))
    
    # Lưu ra file JSON
    with open("aptis_reading.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
        
