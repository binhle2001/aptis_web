import io
import base64
import os
import os
import base64
import pickle
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from PIL import Image
import base64
import io
import textwrap
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from google.oauth2.credentials import Credentials
from schemas.user_schema import CommitmentSchema
from email.message import EmailMessage


def generate_filled_commitment(data: CommitmentSchema, template_path: str = "commitment_template.png") -> str:
    """
    Nạp ảnh template 'commitment_template_v2.png', điền thông tin và chữ ký
    với tọa độ đã được canh chỉnh thủ công chính xác, sau đó xuất file JPG.
    """
    date_now = datetime.now()
    date = str(date_now.day)
    month = str(date_now.month)
    year = str(date_now.year)
    try:
        image = Image.open(template_path).convert("RGBA")
        draw = ImageDraw.Draw(image)
        
        # Font để điền dữ liệu, kích thước phù hợp với template HD
        font_data = ImageFont.truetype("times.ttf", 38)
        font_data_bold = ImageFont.truetype("timesbd.ttf", 38)
        data_color = (0, 0, 0) # Màu xanh đậm
        black_color = (0, 0, 0)
    except FileNotFoundError as e:
        print(f"LỖI: Không tìm thấy file template '{template_path}'.")
        print("Hãy đảm bảo bạn đã tạo file này từ bước trước.")
        raise e
    except IOError as e:
        print("LỖI: Không tìm thấy file font chữ. Hãy đặt 'times.ttf' và 'timesbd.ttf' vào cùng thư mục.")
        raise e

    # --- DICTIONARY TỌA ĐỘ (ĐÃ ĐO BẰNG TAY, ĐẢM BẢO CHÍNH XÁC) ---
    COORDINATES = {
        'date_now': (1466, 286),
        'month_now': (1627, 286),
        'year_now': (1751, 286),
        'student_name': (450, 793),
        'date_of_birth': (300, 846),
        'national_id': (880, 846),
        'issue_date': (308, 896),
        'address': (820, 896),
        'phone': (310, 946),
        'email': (830, 946),
        'start_date': (342, 1046),
        'end_date': (825, 1046),
        'target_output': (1347, 1046),
        'course_registered': (420, 1096),
        'fee_paid': (260, 1146),
        'fee_deadline': (1165, 1146),
        'commitment_output': (870, 1246),
        'student_name_inline': (630, 3846), # Vị trí chèn tên vào đoạn văn
        'student_signature_paste': (1300, 4430), # Tọa độ dán chữ ký BÊN B
        'student_name_signature': (1387, 4557),   # Tọa độ viết tên BÊN B
    }

    # --- Điền thông tin văn bản lên ảnh ---
    draw.text(COORDINATES['date_now'], date, font=font_data_bold, fill=data_color)
    draw.text(COORDINATES['month_now'], month, font=font_data_bold, fill=data_color)
    draw.text(COORDINATES['year_now'], year, font=font_data_bold, fill=data_color)
    draw.text(COORDINATES['student_name'], data.student_name, font=font_data_bold, fill=data_color)
    draw.text(COORDINATES['date_of_birth'], data.date_of_birth, font=font_data, fill=data_color)
    draw.text(COORDINATES['national_id'], data.national_id, font=font_data, fill=data_color)
    draw.text(COORDINATES['issue_date'], data.issue_date, font=font_data, fill=data_color)
    draw.text(COORDINATES['phone'], data.phone, font=font_data, fill=data_color)
    draw.text(COORDINATES['email'], data.email, font=font_data, fill=data_color)
    draw.text(COORDINATES['start_date'], data.start_date, font=font_data, fill=data_color)
    draw.text(COORDINATES['end_date'], data.end_date, font=font_data, fill=data_color)
    draw.text(COORDINATES['target_output'], data.target_output, font=font_data, fill=data_color)
    draw.text(COORDINATES['course_registered'], data.course_registered, font=font_data, fill=data_color)
    draw.text(COORDINATES['fee_paid'], data.fee_paid, font=font_data, fill=data_color)
    draw.text(COORDINATES['fee_deadline'], data.fee_deadline, font=font_data, fill=data_color)
    draw.text(COORDINATES['commitment_output'], data.commitment_output, font=font_data, fill=data_color)
    draw.text(COORDINATES['student_name_inline'], data.student_name, font=font_data_bold, fill=data_color)

    # Xử lý riêng cho địa chỉ để tự động xuống dòng
    address_lines = textwrap.wrap(data.address, width=55)
    y_address = COORDINATES['address'][1]
    for line in address_lines:
        draw.text((COORDINATES['address'][0], y_address), line, font=font_data, fill=data_color)
        y_address += 50 # Khoảng cách giữa các dòng của địa chỉ

    # --- Xử lý và dán chữ ký của học viên (Bên B) ---
    if data.signature_base64:
        try:
            base64_string = data.signature_base64.split(',')[-1]
            signature_bytes = base64.b64decode(base64_string)
            student_sig_img = Image.open(io.BytesIO(signature_bytes)).convert("RGBA")
            student_sig_img.thumbnail((150, 325))

            # Kiểm tra nếu có alpha channel
            if student_sig_img.mode == 'RGBA':
                alpha = student_sig_img.split()[-1]
                image.paste(student_sig_img, COORDINATES['student_signature_paste'], mask=alpha)
            else:
                image.paste(student_sig_img, COORDINATES['student_signature_paste'])

            # Ghi tên học viên dưới chữ ký (dùng anchor="mt" để tự động canh giữa)
            draw.text(COORDINATES['student_name_signature'], data.student_name, font=font_data_bold, fill=black_color, anchor="mt")
        
        except Exception as e:
            print(f"LỖI: Không thể xử lý ảnh chữ ký của học viên: {e}")

    # --- Lưu file kết quả ---
    final_image_rgb = image.convert("RGB")
    os.makedirs("/app/raw_file/commitments", exist_ok=True)
    output_filename = f"/app/raw_file/commitments/commitment_{data.email.replace('.', '_')}.jpg"
    final_image_rgb.save(output_filename, "jpeg", quality=95)
    
    print("-" * 50)
    print(f"✅ Đã tạo ảnh cam kết hoàn chỉnh thành công!")
    print(f"   File được lưu tại: {output_filename}")
    print("-" * 50)
    
    return output_filename




SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    creds = None
    TOKEN_PATH = "token.json"
    CREDENTIALS_PATH = "credentials.json"
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def send_email_with_attachment(service, sender, recipient, subject, body_text, file_path):
    message = EmailMessage()
    message['To'] = recipient
    message['From'] = sender
    message['Subject'] = subject

    # Set nội dung HTML cho email
    message.add_alternative(body_text, subtype='html')

    with open(file_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(file_path)
        message.add_attachment(file_data, maintype='image', subtype='jpeg', filename=file_name)

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}

    send_message = service.users().messages().send(userId="me", body=create_message).execute()
    print(f'Message Id: {send_message["id"]}')
    return send_message

