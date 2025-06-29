import pandas as pd
import json

def convert_writing_excel_to_json(file_path: str) -> str:
    """
    Đọc file Excel chứa đề thi Writing và chuyển đổi thành chuỗi JSON.

    File Excel phải có các cột: 'Topic', 'part', 'Instruction', 'question'.

    Args:
        file_path (str): Đường dẫn tới file Excel (.xlsx).

    Returns:
        str: Một chuỗi JSON có cấu trúc đại diện cho đề thi.
             Trả về chuỗi JSON rỗng '[]' nếu có lỗi hoặc file trống.
    """
    try:
        # Đọc file Excel
        df = pd.read_excel(file_path)

        # --- Bước 1: Tiền xử lý dữ liệu ---
        # Lấp đầy các giá trị bị thiếu trong các cột nhóm (do merged cells)
        grouping_cols = ['Topic', 'part']
        df[grouping_cols] = df[grouping_cols].ffill()
        
        # Đảm bảo cột 'part' là kiểu số nguyên
        df['part'] = df['part'].astype(int)

        # Thay thế các ô trống (NaN) bằng None để JSON hiển thị là "null"
        df = df.where(pd.notna(df), None)

        # --- Bước 2: Xây dựng cấu trúc JSON ---
        exam_parts = []
        # Nhóm DataFrame theo 'part' để xử lý từng phần thi
        for part_id, group in df.groupby('part'):
            # Lấy thông tin chung từ dòng đầu tiên của nhóm
            first_row = group.iloc[0]
            
            # Gom tất cả các câu hỏi trong nhóm thành một danh sách
            questions_list = group['question'].dropna().tolist()

            part_data = {
                "part_id": int(part_id),
                "topic": first_row['Topic'],
                # Lấy instruction, nếu không có sẽ là None
                "instruction": first_row.get('Instruction'),
                "questions": questions_list
            }
            
            exam_parts.append(part_data)

        # Chuyển đổi list Python thành chuỗi JSON
        return json.dumps(exam_parts, indent=4, ensure_ascii=False)

    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file tại '{file_path}'")
        return "[]"
    except Exception as e:
        print(f"Đã xảy ra lỗi không xác định: {e}")
        return "[]"