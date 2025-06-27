import psycopg2
import psycopg2.extras # Cần thiết cho RealDictCursor
import json

# Giả sử bạn có hàm get_db_connection()
# from .database import get_db_connection

def get_speaking_exam_as_json(exam_id: int) -> str:
    """
    Lấy dữ liệu đề thi speaking từ CSDL và tái tạo lại cấu trúc JSON gốc.

    Args:
        exam_id (int): ID của bài thi (exam) cần lấy.

    Returns:
        str: Một chuỗi JSON đại diện cho đề thi. 
             Trả về một chuỗi JSON danh sách rỗng '[]' nếu không tìm thấy đề thi.
    """
    conn = None
    try:
        conn = get_db_connection()
        # RealDictCursor trả về kết quả dưới dạng dictionary, rất tiện lợi
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            # Lấy tất cả câu hỏi của exam, sắp xếp theo part và id để đảm bảo thứ tự
            cur.execute("""
                SELECT id, part_id, topic, instruction, question, image_path1, image_path2 
                FROM speaking
                WHERE exam_id = %s
                ORDER BY part_id, id;
            """, (exam_id,))
            
            rows = cur.fetchall()
            
            if not rows:
                # Nếu không có câu hỏi nào, trả về danh sách rỗng
                return "[]"

            # Dictionary để nhóm các câu hỏi theo part_id
            parts_data = {}

            # Lặp qua các hàng kết quả để xây dựng lại cấu trúc JSON
            for row in rows:
                part_id = row['part_id']
                
                # Nếu đây là lần đầu tiên gặp part_id này
                if part_id not in parts_data:
                    # Tạo một mục mới cho phần này
                    # Vì ảnh chỉ được lưu ở câu hỏi đầu tiên, ta có thể lấy luôn
                    parts_data[part_id] = {
                        "part": part_id,
                        "topic": row['topic'],
                        "instruction": row['instruction'],
                        "question": [], # Khởi tạo danh sách câu hỏi rỗng
                        "image_url_1": row['image_path1'],
                        "image_url_2": row['image_path2']
                    }
                
                # Thêm câu hỏi hiện tại vào danh sách câu hỏi của phần tương ứng
                parts_data[part_id]["question"].append(row['question'])

            # Chuyển đổi dictionary các giá trị thành một danh sách
            final_result = list(parts_data.values())

            # Chuyển đổi danh sách Python thành chuỗi JSON
            return json.dumps(final_result, indent=4, ensure_ascii=False)

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Lỗi khi lấy dữ liệu đề thi: {error}")
        # Ném lại lỗi để lớp cao hơn xử lý
        raise error
    finally:
        if conn:
            conn.close()


# --- Ví dụ cách sử dụng ---
if __name__ == '__main__':
    # Giả lập CSDL và hàm get_db_connection để chạy thử
    def get_db_connection():
        # Thay thế bằng thông tin kết nối thật của bạn
        return psycopg2.connect(
            dbname="aptis_db", user="admin", password="qwerty", host="localhost", port="5432"
        )

    # ID của bài thi bạn muốn lấy ra
    target_exam_id = 57 # Giả sử bạn đã thêm dữ liệu cho exam_id=1

    try:
        # Gọi hàm để lấy và tái tạo JSON
        json_output = get_speaking_exam_as_json(target_exam_id)

        print(f"--- ĐỀ THI SPEAKING (exam_id = {target_exam_id}) DẠNG JSON ---")
        print(json_output)
    except Exception as e:
        print(f"Không thể lấy đề thi. Lỗi: {e}")