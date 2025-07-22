# /api/commitment_api.py

import base64
import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from services.auth_service import get_db_connection
from helpers.common import get_env_var
from core.deps import get_current_member_user
from services import commitment_service
from schemas.user_schema import CommitmentSchema

router = APIRouter(
    prefix="/api/commitment",
    tags=["USER COMMITMENT - COMMITMENT Management"],
    dependencies=[Depends(get_current_member_user)], # Áp dụng cho tất cả các route trong router này
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Operation not permitted"},
    },
)

@router.post(
    "/generate",
    tags=["PDF Generation"],
    summary="Tạo file PDF cam kết từ thông tin học viên",
    response_description="File PDF của bản cam kết đã được tạo"
)
async def generate_commitment_endpoint(data: CommitmentSchema):
    """
    Endpoint nhận dữ liệu JSON của học viên và chữ ký (base64),
    sau đó trả về một file PDF đã được điền thông tin.

    - **data**: Dữ liệu đầu vào tuân theo CommitmentSchema.
    """
    try:
        # Tạo file Word
        image_path = commitment_service.generate_filled_commitment(data)
        
        # Trả về file Word
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Đã xảy ra lỗi khi tạo tài liệu: {str(e)}"
        )
        
        
@router.post("/send_commitment_email")
def send_commitment(data: CommitmentSchema, current_user: Annotated[dict, Depends(get_current_member_user)] = None):
    output_filename = f"/app/raw_file/commitments/commitment_{data.email.replace('.', '_')}.jpg"

    # Kiểm tra file có tồn tại không
    if not os.path.exists(output_filename):
        return {"error": "Ảnh bản cam kết chưa được tạo."}

    try:
        service = commitment_service.authenticate_gmail()
        subject = "Bản cam kết đầu ra khóa học Aptis - Aptis One"
        body = f"Kính gửi bạn {data.student_name}, Trung tâm AptisOne xin gửi bạn bản cam kết đầu ra của khóa học. Chúc bạn đạt được đầu ra mong muốn."

        commitment_service.send_email_with_attachment(
            service=service,
            sender=get_env_var('GMAIL', 'SENDER_EMAIL'),  # Gmail đã đăng nhập qua OAuth2
            recipient=data.email,
            subject=subject,
            body_text=body,
            file_path=output_filename
        )
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET is_commited = true WHERE id = %s", (current_user['id'], ))
        conn.commit()
        cursor.close()
        conn.close()
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise e