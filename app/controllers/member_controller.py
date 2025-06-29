from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm # Dùng cái này tiện hơn UserLoginSchema cho form data
from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form, Depends
from services.submission_services import get_submission_by_id, put_exam_submission, save_base64_to_audio_file
from schemas.user_schema import ExamSubmissionSchema, SpeakingAudioSchema
from core.deps import get_current_member_user
from schemas.auth_schema import TokenSchema, UserLoginSchema
from schemas.exam_schema import AudioPath
from schemas.exam_set_schema import ExamSetListResponseSchema, ExamSetResponseSchema
from services import auth_service, exam_service, exam_set_service


SPEAKING_SUBMISSION_DIR = "/app/raw_file/speaking/submission"

router = APIRouter(
    prefix="/api/user",
    tags=["Member - User Management"],
    dependencies=[Depends(get_current_member_user)], # Áp dụng cho tất cả các route trong router này
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

@router.get("/exam-sets/{exam_set_id}", response_model=ExamSetResponseSchema)
async def get_exam_set_endpoint(
    exam_set_id: int,
    current_admin: Annotated[dict, Depends(get_current_member_user)]
):
    """
    Lấy danh sách các đề có trong set
    """
    exam_set = await exam_set_service.get_exam_set_by_id(exam_set_id, current_admin)
    return JSONResponse(status_code=status.HTTP_200_OK, content = exam_set)

@router.get("/exam/{exam__id}")
async def get_exam_set_endpoint(
    exam__id: int,
    current_admin: Annotated[dict, Depends(get_current_member_user)]
):
    """
    Lấy nội dung đề
    """
    exam_set = exam_service.get_exam_by_id(exam__id)
    return JSONResponse(status_code=status.HTTP_200_OK, content = exam_set)

@router.post("/exam-file")
async def get_audio_path_listening(
    item: AudioPath,
    current_admin: Annotated[dict, Depends(get_current_member_user)]
):
    """
    Lấy nội dung file audio
    """
    file = exam_service.load_audio_as_base64(item.audio_path)
    response = {"base64": file}
    return JSONResponse(status_code=status.HTTP_200_OK, content = response)

@router.post("/exam/{exam_id}/submission")
async def put_exam_submisstion_endpoint(exam_id, item: ExamSubmissionSchema, current_user: Annotated[dict, Depends(get_current_member_user)]):
    """
    Đẩy bài làm 
    """
    user_id = current_user.get("id", None)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    submission = put_exam_submission(user_id, exam_id, item.json_data, item.score)
    return JSONResponse(status_code=status.HTTP_200_OK, content = submission)


@router.get("/submission/{submission_id}")
async def get_submission_endpoint(submission_id: int):
    """
    Lấy nội dung bài đã làm
    """
    record = get_submission_by_id(submission_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content = record)

@router.post("/question/{question_id}/audio")
async def post_audio_file_endpoint(
    question_id: int,
    audio_file: SpeakingAudioSchema,
    current_user: Annotated[dict, Depends(get_current_member_user)] = None
):
    """
    Đẩy file audio lên
    """

    user_id = current_user.get("id")
    saved_audio_file_path_str = f"{SPEAKING_SUBMISSION_DIR}/{question_id}_{user_id}.mp3"
    # ĐỌC NỘI DUNG FILE UPLOAD VÀ GHI
    save_base64_to_audio_file(audio_file, saved_audio_file_path_str)
    return JSONResponse(status_code=status.HTTP_200_OK, content = {"audio_path": saved_audio_file_path_str})

    

