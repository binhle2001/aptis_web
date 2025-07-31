import os
import re
import base64
import io
import logging

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# --- PHẦN CẤU HÌNH ---

# 1. Đảm bảo file này nằm cùng thư mục với script của bạn
CLIENT_SECRETS_FILE = 'credentials.json'

# 2. File này sẽ được tự động tạo ra để lưu token sau lần đăng nhập đầu tiên
TOKEN_FILE = 'download_token.json'

# 3. Quyền (scope) mà ứng dụng của bạn cần. 'drive.readonly' là đủ để đọc/tải file.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# Cấu hình logging để xem các bước hoạt động
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_google_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        logging.info(f"Phát hiện file token '{TOKEN_FILE}'. Đang cố gắng sử dụng lại.")
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logging.info("Credentials đã hết hạn. Đang làm mới...")
            try:
                creds.refresh(Request())
            except Exception as e:
                logging.error(f"Làm mới token thất bại: {e}. Sẽ tiến hành xác thực lại từ đầu.")
                creds = None
        else:
            logging.info("Chưa có token hợp lệ. Bắt đầu quá trình xác thực mới.")
            if not os.path.exists(CLIENT_SECRETS_FILE):
                logging.critical(f"LỖI: Không tìm thấy file '{CLIENT_SECRETS_FILE}'.")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)

            try:
                # Phù hợp cho môi trường không có browser (Docker, SSH...)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                logging.critical(f"Không thể khởi động xác thực: {e}")
                return None

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds


def download_drive_file_as_base64(url: str, creds = None) -> str:
    """
    Tải file từ Google Drive bằng API và trả về chuỗi Base64.
    """
    
    try:
        if creds is None:
            creds = get_google_credentials()
        # 1. Trích xuất File ID từ URL
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', url)
        if not match:
            raise ValueError("URL không hợp lệ hoặc không chứa File ID của Google Drive.")
        file_id = match.group(1)
        logging.info(f"Đã trích xuất File ID: {file_id}")

        # 2. Xây dựng dịch vụ Google Drive API
        logging.info("Đang xây dựng dịch vụ Google Drive API...")
        service = build('drive', 'v3', credentials=creds)

        # 3. Tạo yêu cầu tải file
        request = service.files().get_media(fileId=file_id)

        # 4. Tải file vào bộ nhớ (RAM)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        
        logging.info("Bắt đầu tải file vào bộ nhớ...")
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                logging.info(f"Đã tải xuống {int(status.progress() * 100)}%.")
        
        logging.info("Tải file hoàn tất.")
        file_data = fh.getvalue()

        # 5. Mã hóa sang Base64
        logging.info("Đang mã hóa dữ liệu sang Base64...")
        base64_data = base64.b64encode(file_data).decode('utf-8')
        
        return base64_data

    except HttpError as error:
        logging.error(f"Đã xảy ra lỗi API của Google: {error}")
        if error.status_code == 404:
            logging.error("Lý do: File không tồn tại hoặc bạn không có quyền truy cập.")
        elif error.status_code == 403:
            logging.error("Lý do: Quota của API đã hết hoặc bạn không được cấp phép.")
        return None
    except Exception as e:
        logging.error(f"Đã xảy ra lỗi không xác định: {e}")
        return None