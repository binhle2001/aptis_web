from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm # Dùng cái này tiện hơn UserLoginSchema cho form data
from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form, Depends
from schemas.user_schema import GuestInsertSchema, GuestSchema
from services.guest_service import insert_guest_info
from core.deps import get_current_member_user
from schemas.auth_schema import TokenSchema, UserLoginSchema
from schemas.exam_schema import AudioPath
from schemas.exam_set_schema import ExamSetListResponseSchema, ExamSetResponseSchema
from services import auth_service, exam_service, exam_set_service

router = APIRouter(
    prefix="/api/guest",
    tags=["Guest - User Management"],
    dependencies=[], # Áp dụng cho tất cả các route trong router này
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Operation not permitted"},
        404: {"description": "Not found"}
    },
)

@router.get(
    "/exam-sets",
    response_model=ExamSetListResponseSchema,
)
async def list_exam_sets_endpoint(
    search: Optional[str] = Query("", description="Filter by exam code, title (e.g., 'R0001')"),
    page: int = Query(1, ge=0, description="Number of page"),
    limit: int = Query(1, ge=1, le=200, description="Maximum number of records to return"), # Giới hạn max limit,
    current_user: Annotated[dict, Depends(get_current_member_user)] = None,  # nếu cần xác thực admin
):
    """
    Lấy danh sách ExamSet có thể filter theo `search`, phân trang với `page` và `limit`.
    Trả về cả `total` và `total_pages`.
    """
    data = await exam_set_service.get_exam_set(search=search, page=page, limit=limit, current_role_user = current_user.get("role"))
    return ExamSetListResponseSchema(**data)

@router.get("/exam-sets/{exam_set_id}")
async def get_exam_set_endpoint(
    exam_set_id: int,
    current_user: Annotated[dict, Depends(get_current_member_user)]
):
    exam_set = await exam_set_service.get_exam_set_by_id(exam_set_id, current_user)
    return exam_set

@router.get("/exam/{exam__id}")
async def get_exam_set_endpoint(
    exam__id: int,
    current_user: Annotated[dict, Depends(get_current_member_user)]
):
    """
    Lấy ra nội dung đề thi thử
    """
    exam_set = exam_service.get_exam_by_id(exam__id, current_user)
    return JSONResponse(status_code=status.HTTP_200_OK, content = exam_set)

@router.post("/exam-file")
async def get_audio_path_listening(
    item: AudioPath,
    current_user: Annotated[dict, Depends(get_current_member_user)]
):
    """
    lấy file audio của phần listening
    """
    file = exam_service.load_audio_as_base64(item.audio_path, )
    response = {"base64": file}
    return JSONResponse(status_code=status.HTTP_200_OK, content = response)

@router.post("/info")
async def insert_guest_info_endpoint(item: GuestInsertSchema):
    """
    Guest điền thông tin
    """
    return insert_guest_info(item.fullname, item.phone_number)

