# /api/commitment_api.py

import base64
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from core.deps import get_current_member_user
from services import commitment_service
from schemas.user_schema import CommitmentSchema

router = APIRouter(
    prefix="/api/commitment",
    tags=["USER COMMITMENT - COMMITMENT Management"],
    # dependencies=[Depends(get_current_member_user)], # Áp dụng cho tất cả các route trong router này
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