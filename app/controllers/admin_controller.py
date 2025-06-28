from typing import Annotated # Python 3.9+
# from typing_extensions import Annotated # Python < 3.9
from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
from services.submission_services import get_list_submission, get_submission_by_id, update_exam_submission
from services.guest_service import call_guest, delete_guest, get_list_guest
from schemas.user_schema import ExamSubmissionSchema, GuestResponseSchema, UserCreateSchema, UserResponseSchema, UserUpdatePasswordSchema, MessageResponseSchema, UserListResponseSchema
from services import user_service, exam_service, exam_set_service 
from core.deps import get_current_admin_user # Dependency để xác thực Admin
from schemas.exam_schema import AudioPath, ExamCreateResponseSchema, ExamReadingUpdate
from schemas.exam_set_schema import ExamSetCreateSchema, ExamSetListResponseSchema, ExamSetResponseSchema

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin - User Management"],
    dependencies=[Depends(get_current_admin_user)], # Áp dụng cho tất cả các route trong router này
    responses={
        401: {"description": "Not authenticated"},
        403: {"description": "Operation not permitted"},
        404: {"description": "Not found"}
    },
)

@router.post("/users", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_user_by_admin(
    user_in: UserCreateSchema,
    # current_admin: Annotated[dict, Depends(get_current_admin_user)] # Không cần ở đây nữa vì đã có ở router level
):
    """
    Admin creates a new member account.
    - **username**: Unique username for login.
    - **fullname**: Full name of the member.
    - **password**: Member's password (will be hashed).
    - **phone_number**: Optional phone number.
    """
    # current_admin sẽ chứa thông tin của admin đang thực hiện hành động, có thể dùng để log
    # print(f"Admin '{current_admin['username']}' is creating a new user.")
    
    created_user_dict = await user_service.create_new_user(user_in)
    
    # UserResponseSchema sẽ tự động parse dict và validate
    return UserResponseSchema(**created_user_dict)

@router.patch("/users/{user_id}/password", response_model=MessageResponseSchema)
async def update_member_password_by_admin(
    user_id: int, # Lấy user_id từ path parameter
    password_in: UserUpdatePasswordSchema,
    # current_admin: Annotated[dict, Depends(get_current_admin_user)] # Đã có ở router level
):
    """
    Admin updates a member's password.
    - **user_id**: The ID of the member account to update.
    - **new_password**: The new password for the member.
    """
    # print(f"Admin '{current_admin['username']}' is updating password for user ID {user_id}.")
    
    success = await user_service.update_user_password_by_admin(user_id, password_in)
    
    if success:
        return MessageResponseSchema(message=f"Password for user ID {user_id} updated successfully.")
    else:
        # Hàm service sẽ raise HTTPException nếu có lỗi, nên dòng này thường không được gọi
        # trừ khi hàm service trả về False mà không raise exception (điều này không nên).
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update password."
        )
    
@router.patch("/users/{user_id_to_deactivate}/deactivate", response_model=MessageResponseSchema)
async def deactivate_user_endpoint(
    user_id_to_deactivate: int,
    current_admin: Annotated[dict, Depends(get_current_admin_user)] # Lấy thông tin admin đang thực hiện
):
    """
    Admin deactivates a member account.
    - **user_id_to_deactivate**: The ID of the member account to deactivate.
    """
    admin_username = current_admin['username'] # Lấy username của admin để truyền vào service
    # print(f"Admin '{admin_username}' is attempting to deactivate user ID {user_id_to_deactivate}.")

    success = await user_service.deactivate_user_by_admin(user_id_to_deactivate, admin_username)
    
    if success:
        return MessageResponseSchema(message=f"User ID {user_id_to_deactivate} has been deactivated successfully.")
    else:
        # Hàm service sẽ raise exception, nên dòng này thường không được gọi
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate user."
        )

# ... (imports và các hàm đã có) ...
# fromschemas.user_schema import MessageResponseSchema # Đã có

# ... (router definition và các endpoint khác) ...

@router.patch("/users/{user_id_to_reactivate}/activate", response_model=MessageResponseSchema)
async def reactivate_user_endpoint(
    user_id_to_reactivate: int,
    current_admin: Annotated[dict, Depends(get_current_admin_user)]
):
    """
    Admin reactivates a previously deactivated member account.
    - **user_id_to_reactivate**: The ID of the member account to reactivate.
    """
    admin_username = current_admin['username']
    # print(f"Admin '{admin_username}' is attempting to reactivate user ID {user_id_to_reactivate}.")
    
    success = await user_service.reactivate_user_by_admin(user_id_to_reactivate, admin_username)
    
    if success:
        return MessageResponseSchema(message=f"User ID {user_id_to_reactivate} has been reactivated successfully.")
    else:
        # Hàm service sẽ raise exception, nên dòng này thường không được gọi
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reactivate user."
        )
@router.get("/users", response_model=UserListResponseSchema)
async def get_users_list_by_admin(
    # current_admin: Annotated[dict, Depends(get_current_admin_user)], # Đã có ở router level
    role: Optional[str] = Query(None, description="Filter by user role (e.g., 'member', 'admin')"),
    search: Optional[str] = Query(None, min_length=1, description="Search term for username or full name"),
    page: int = Query(0, ge=0, description="Number of page"),
    limit: int = Query(100, ge=1, le=200, description="Maximum number of records to return") # Giới hạn max limit
):
    """
    Admin retrieves a list of user accounts.
    Supports filtering by role, searching, and pagination.
    """
    # print(f"Admin '{current_admin['username']}' is fetching users list with params: role={role}, search={search}, skip={skip}, limit={limit}")
    
    users_data = await user_service.get_users_list(
        role=role,
        search=search,
        page=page,
        limit=limit
    )
    # UserListResponseSchema sẽ tự động parse dict và validate
    return UserListResponseSchema(**users_data)
@router.delete("/users/{user_id_to_delete}", response_model=MessageResponseSchema)
async def delete_user_endpoint(
    user_id_to_delete: int,
    current_admin: Annotated[dict, Depends(get_current_admin_user)]
):
    """
    Admin reactivates a previously deactivated member account.
    - **user_id_to_reactivate**: The ID of the member account to reactivate.
    """
    admin_username = current_admin['username']
    # print(f"Admin '{admin_username}' is attempting to reactivate user ID {user_id_to_reactivate}.")
    
    success = await user_service.delete_user_by_admin(user_id_to_delete, admin_username)
    
    if success:
        return MessageResponseSchema(message=f"User ID {user_id_to_delete} has been delete successfully.")
    else:
        # Hàm service sẽ raise exception, nên dòng này thường không được gọi
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user."
        )


@router.post(
    "/exam-sets/{exam_set_id}/reading-exam", 
    response_model=ExamCreateResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a Reading Exam Part for an Exam Set" # Thêm summary cho Swagger
)
async def create_reading_exam_for_set_endpoint(
    exam_set_id: int, 
    current_admin: Annotated[dict, Depends(get_current_admin_user)],
    exam_part_code: str = Form(
        ..., 
        description="Unique code for this reading part within the exam set (e.g., RD001_S1).",
        example="RD_SET1_PART"
    ),
    title_for_part: str = Form(
        ..., 
        description="Title for this reading part (e.g., 'Reading Section - Aptis General Set 1').",
        example="Reading - Aptis Test Alpha"
    ),
    time_limit_minutes_for_part: int = Form(
        ..., 
        gt=0, 
        description="Time limit in minutes specifically for this reading part.",
        example=60
    ),
    file: UploadFile = File(
        ..., 
        description="The Excel file containing the reading exam content."
    )
):
    """
    Allows an Admin to upload a PDF file to create a new Reading exam part
    and associate it with an existing ExamSet.

    - **exam_set_id**: The ID of the parent ExamSet.
    - **exam_part_code**: A unique code for this specific reading exam (e.g., READING_01).
    - **title_for_part**: The title for this reading section.
    - **time_limit_minutes_for_part**: Duration in minutes for this reading section.
    - **file**: The PDF document for the exam.
    """
    if not file.filename or not file.filename.lower().endswith(".xlsx"): # Kiểm tra filename có tồn tại
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid file type or no filename. Only Excel files (.xlsx) are allowed."
        )

    created_by_user_id = current_admin['id']
    
    try:
        exam_details_dict = await exam_service.create_reading_exam_from_excel(
            exam_set_id=exam_set_id,
            exam_part_code=exam_part_code,
            descriptions=title_for_part,
            time_limit_for_part=time_limit_minutes_for_part,
            excel_file=file,
            created_by_user_id=created_by_user_id
        )
        # exam_details_dict bây giờ nên chứa các trường khớp với ExamCreateResponseSchema
        # ví dụ: exam_id (của phần thi), exam_code (của phần thi), title (của phần thi), 
        # exam_type, time_limit_minutes (của phần thi)
        
        # Tạo response object từ Pydantic model
        # Đảm bảo các key trong exam_details_dict khớp với các field của ExamCreateResponseSchema
        # Hoặc ExamCreateResponseSchema có thể cần được điều chỉnh.
        # Giả sử exam_details_dict trả về:
        # { 'exam_id': ..., 'exam_code': ..., 'title': ..., 'exam_type': 'reading', 'time_limit_minutes': ...}
        
        return ExamCreateResponseSchema(
            exam_id=exam_details_dict['id'],
            exam_code=exam_details_dict['exam_code'], # Đây là exam_part_code
            title=exam_details_dict['description'],         # Đây là title_for_part
            exam_type=exam_details_dict['exam_type'],
            time_limit_minutes=exam_details_dict.get('time_limit'), # Lấy từ record đã tạo
            message=f"Reading exam part '{exam_part_code}' created successfully for ExamSet ID {exam_set_id}."
        )
    except HTTPException as e:
        # Lỗi đã được xử lý và ném lại từ service, hoặc lỗi validation ở đây
        raise e
    except Exception as e_main:
        # Lỗi không mong muốn ở controller level (hiếm khi xảy ra nếu service xử lý tốt)
        print(f"Unexpected error in controller: {e_main}")
        raise HTTPException(status_code=500, detail=f"An error occurred in the controller: {str(e_main)}")


@router.post("/exam-sets", response_model=ExamSetResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_exam_set_endpoint(
    set_in: ExamSetCreateSchema,
    current_admin: Annotated[dict, Depends(get_current_admin_user)]
):
    created_by_user_id = current_admin['id']
    created_set = await exam_set_service.create_exam_set(set_in, created_by_user_id)
    return ExamSetResponseSchema(**created_set)

@router.get(
    "/exam-sets",
    response_model=ExamSetListResponseSchema,
)
async def list_exam_sets_endpoint(
    search: Optional[str] = Query("", description="Filter by exam code, title (e.g., 'R0001')"),
    page: int = Query(1, ge=0, description="Number of page"),
    limit: int = Query(1, ge=1, le=200, description="Maximum number of records to return"), # Giới hạn max limit,
    _: Annotated[dict, Depends(get_current_admin_user)] = None,  # nếu cần xác thực admin
):
    """
    Lấy danh sách ExamSet có thể filter theo `search`, phân trang với `page` và `limit`.
    Trả về cả `total` và `total_pages`.
    """
    data = await exam_set_service.get_exam_set(search=search, page=page, limit=limit)
    return ExamSetListResponseSchema(**data)

@router.get("/exam-sets/{exam_set_id}")
async def get_exam_set_endpoint(
    exam_set_id: int,
    current_admin: Annotated[dict, Depends(get_current_admin_user)] = None
):
    exam_set = await exam_set_service.get_exam_set_by_id(exam_set_id, current_admin)
    return JSONResponse(status_code=status.HTTP_200_OK, content=exam_set)


@router.patch(
    "/exam-sets/{exam_set_id}/activate",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseSchema
)
async def delete_exam_set_endpoint(
    exam_set_id: int,
    current_admin: Annotated[dict, Depends(get_current_admin_user)]
):
    """
    Soft‑delete một ExamSet (chỉ set is_active = false).
    """
    
    success =  exam_set_service.reactivate_exam_set(exam_set_id)
    # 204 No Content
    
    return MessageResponseSchema(message = f"Exam set {exam_set_id} deactivated")
    
@router.patch(
    "/exam-sets/{exam_set_id}/deactivate",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseSchema
)
async def delete_exam_set_endpoint(
    exam_set_id: int,
    current_admin: Annotated[dict, Depends(get_current_admin_user)]
):
    """
    Soft‑delete một ExamSet (chỉ set is_active = false).
    """
    success = await exam_set_service.deactivate_exam_set(exam_set_id, current_admin["id"])
    # 204 No Content
    return MessageResponseSchema(message = f"Exam set {exam_set_id} activated")

@router.delete(
    "/exam-sets/{exam_set_id}",
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseSchema
)
async def delete_exam_set_endpoint(
    exam_set_id: int,
    current_admin: Annotated[dict, Depends(get_current_admin_user)]
):
    """
    Soft‑delete một ExamSet (chỉ set is_active = false).
    """
    success =  exam_set_service.delete_exam_set(exam_set_id)
    # 204 No Content
    return MessageResponseSchema(message = f"Exam set {exam_set_id} deleted")

@router.get("/exam/{exam__id}")
async def get_exam_set_endpoint(
    exam__id: int,
    current_admin: Annotated[dict, Depends(get_current_admin_user)]
):
    exam_set = exam_service.get_exam_by_id(exam__id)
    return JSONResponse(status_code=status.HTTP_200_OK, content = exam_set)

@router.patch("/exam/reading/{exam_id}")
async def update_reading_exam_for_set_endpoint(
    exam_id: int, 
    current_admin: Annotated[dict, Depends(get_current_admin_user)],
    file: UploadFile = File(
        ..., 
        description="The PDF file (.pdf) containing the reading exam content."
    )
):
    """
    Allows an Admin to upload a PDF file to create a new Reading exam part
    and associate it with an existing ExamSet.

    - **exam_set_id**: The ID of the parent ExamSet.
    - **file**: The PDF document for the exam.
    """
    if not file.filename or not file.filename.lower().endswith(".xlsx"): # Kiểm tra filename có tồn tại
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid file type or no filename. Only Excel files (.xlsx) are allowed."
        )

    created_by_user_id = current_admin['id']
    
    try:
        exam_details_dict = await exam_service.update_reading_exam_from_excel(
            exam_id=exam_id,
            excel_file=file,
        )
        # exam_details_dict bây giờ nên chứa các trường khớp với ExamCreateResponseSchema
        # ví dụ: exam_id (của phần thi), exam_code (của phần thi), title (của phần thi), 
        # exam_type, time_limit_minutes (của phần thi)
        
        # Tạo response object từ Pydantic model
        # Đảm bảo các key trong exam_details_dict khớp với các field của ExamCreateResponseSchema
        # Hoặc ExamCreateResponseSchema có thể cần được điều chỉnh.
        # Giả sử exam_details_dict trả về:
        # { 'exam_id': ..., 'exam_code': ..., 'title': ..., 'exam_type': 'reading', 'time_limit_minutes': ...}
        
        return ExamCreateResponseSchema(
            exam_id=exam_details_dict['id'],
            exam_code=exam_details_dict['exam_code'], # Đây là exam_part_code
            title=exam_details_dict['description'],         # Đây là title_for_part
            exam_type=exam_details_dict['exam_type'],
            time_limit_minutes=exam_details_dict.get('time_limit'), # Lấy từ record đã tạo
            message=f"Reading exam part '{exam_details_dict['exam_code']}' update successfully for ExamSet ID {exam_details_dict['examset_id']}."
        )
    except HTTPException as e:
        # Lỗi đã được xử lý và ném lại từ service, hoặc lỗi validation ở đây
        raise e
    except Exception as e_main:
        # Lỗi không mong muốn ở controller level (hiếm khi xảy ra nếu service xử lý tốt)
        print(f"Unexpected error in controller: {e_main}")
        raise HTTPException(status_code=500, detail=f"An error occurred in the controller: {str(e_main)}")


@router.post(
    "/exam-sets/{exam_set_id}/listening-exam", 
    response_model=ExamCreateResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a listening Exam Part for an Exam Set" # Thêm summary cho Swagger
)
async def create_listening_exam_for_set_endpoint(
    exam_set_id: int, 
    current_admin: Annotated[dict, Depends(get_current_admin_user)],
    exam_part_code: str = Form(
        ..., 
        description="Unique code for this listening part within the exam set (e.g., RD001_S1).",
        example="RD_SET1_PART"
    ),
    title_for_part: str = Form(
        ..., 
        description="Title for this listening part (e.g., 'listening Section - Aptis General Set 1').",
        example="listening - Aptis Test Alpha"
    ),
    time_limit_minutes_for_part: int = Form(
        ..., 
        gt=0, 
        description="Time limit in minutes specifically for this listening part.",
        example=60
    ),
    file: UploadFile = File(
        ..., 
        description="The Excel (.xlsx) containing the listening exam content."
    )
):
    """
    Allows an Admin to upload a PDF file to create a new listening exam part
    and associate it with an existing ExamSet.

    - **exam_set_id**: The ID of the parent ExamSet.
    - **exam_part_code**: A unique code for this specific listening exam (e.g., listening_01).
    - **title_for_part**: The title for this listening section.
    - **time_limit_minutes_for_part**: Duration in minutes for this listening section.
    - **file**: The PDF document for the exam.
    """
    if not file.filename or not file.filename.lower().endswith(".xlsx"): # Kiểm tra filename có tồn tại
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid file type or no filename. Only Excel files (.xlsx) are allowed."
        )

    created_by_user_id = current_admin['id']
    
    try:
        exam_details_dict = await exam_service.create_listening_exam_from_excel(
            exam_set_id=exam_set_id,
            exam_part_code=exam_part_code,
            descriptions=title_for_part,
            time_limit_for_part=time_limit_minutes_for_part,
            excel_file=file,
            created_by_user_id=created_by_user_id
        )
        # exam_details_dict bây giờ nên chứa các trường khớp với ExamCreateResponseSchema
        # ví dụ: exam_id (của phần thi), exam_code (của phần thi), title (của phần thi), 
        # exam_type, time_limit_minutes (của phần thi)
        
        # Tạo response object từ Pydantic model
        # Đảm bảo các key trong exam_details_dict khớp với các field của ExamCreateResponseSchema
        # Hoặc ExamCreateResponseSchema có thể cần được điều chỉnh.
        # Giả sử exam_details_dict trả về:
        # { 'exam_id': ..., 'exam_code': ..., 'title': ..., 'exam_type': 'listening', 'time_limit_minutes': ...}
        
        return ExamCreateResponseSchema(
            exam_id=exam_details_dict['id'],
            exam_code=exam_details_dict['exam_code'], # Đây là exam_part_code
            title=exam_details_dict['description'],         # Đây là title_for_part
            exam_type=exam_details_dict['exam_type'],
            time_limit_minutes=exam_details_dict.get('time_limit'), # Lấy từ record đã tạo
            message=f"listening exam part '{exam_part_code}' created successfully for ExamSet ID {exam_set_id}."
        )
    except HTTPException as e:
        # Lỗi đã được xử lý và ném lại từ service, hoặc lỗi validation ở đây
        raise e
    except Exception as e_main:
        # Lỗi không mong muốn ở controller level (hiếm khi xảy ra nếu service xử lý tốt)
        print(f"Unexpected error in controller: {e_main}")
        raise HTTPException(status_code=500, detail=f"An error occurred in the controller: {str(e_main)}")


@router.patch("/exam/listening/{exam_id}")
async def update_listening_exam_for_set_endpoint(
    exam_id: int, 
    current_admin: Annotated[dict, Depends(get_current_admin_user)],
    file: UploadFile = File(
        ..., 
        description="The PDF file (.pdf) containing the listening exam content."
    )
):
    """
    Allows an Admin to upload a PDF file to create a new listening exam part
    and associate it with an existing ExamSet.

    - **exam_set_id**: The ID of the parent ExamSet.
    - **file**: The PDF document for the exam.
    """
    if not file.filename or not file.filename.lower().endswith(".xlsx"): # Kiểm tra filename có tồn tại
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid file type or no filename. Only Excel files (.xlsx) are allowed."
        )

    created_by_user_id = current_admin['id']
    
    try:
        exam_details_dict = await exam_service.update_listening_exam_from_excel(
            exam_id=exam_id,
            excel_file=file,
        )
        # exam_details_dict bây giờ nên chứa các trường khớp với ExamCreateResponseSchema
        # ví dụ: exam_id (của phần thi), exam_code (của phần thi), title (của phần thi), 
        # exam_type, time_limit_minutes (của phần thi)
        
        # Tạo response object từ Pydantic model
        # Đảm bảo các key trong exam_details_dict khớp với các field của ExamCreateResponseSchema
        # Hoặc ExamCreateResponseSchema có thể cần được điều chỉnh.
        # Giả sử exam_details_dict trả về:
        # { 'exam_id': ..., 'exam_code': ..., 'title': ..., 'exam_type': 'listening', 'time_limit_minutes': ...}
        
        return ExamCreateResponseSchema(
            exam_id=exam_details_dict['id'],
            exam_code=exam_details_dict['exam_code'], # Đây là exam_part_code
            title=exam_details_dict['description'],         # Đây là title_for_part
            exam_type=exam_details_dict['exam_type'],
            time_limit_minutes=exam_details_dict.get('time_limit'), # Lấy từ record đã tạo
            message=f"listening exam part '{exam_details_dict['exam_code']}' update successfully for ExamSet ID {exam_details_dict['examset_id']}."
        )
    except HTTPException as e:
        # Lỗi đã được xử lý và ném lại từ service, hoặc lỗi validation ở đây
        raise e
    except Exception as e_main:
        # Lỗi không mong muốn ở controller level (hiếm khi xảy ra nếu service xử lý tốt)
        print(f"Unexpected error in controller: {e_main}")
        raise HTTPException(status_code=500, detail=f"An error occurred in the controller: {str(e_main)}")
    
@router.delete("/exam/{exam_id}")
async def get_exam_set_endpoint(
    exam_id: int,
    current_admin: Annotated[dict, Depends(get_current_admin_user)]
):
    exam_set = exam_service.delete_exam_data(exam_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content = exam_set)

@router.get("/guest")
async def get_all_guests(
    page: int = Query(1, ge=0, description="Number of page"),
    limit: int = Query(100, ge=1, le=200, description="Maximum number of records to return")
):
    records = get_list_guest(page, limit)
    return GuestResponseSchema(items= records["items"], total=records["total"], limit= limit, page = page)

@router.patch("/guest/{guest_id}")
async def call_guest_endpoint(guest_id: int, current_admin: Annotated[dict, Depends(get_current_admin_user)]):
    """
    Thay đổi trạng thái của guest
    """
    return call_guest(guest_id)


@router.delete("/guest/{guest_id}")
async def delete_guest_endpoint(guest_id: int):
    """
    Xóa guest
    """
    return delete_guest(guest_id)

@router.post("/exam-file")
async def get_audio_path_speaking(
    item: AudioPath,
    current_admin: Annotated[dict, Depends(get_current_admin_user)]
):
    """
    Lấy file audio cho bài listening và speaking
    """
    file = exam_service.load_audio_as_base64(item.audio_path)
    response = {"base64": file}
    return JSONResponse(status_code=status.HTTP_200_OK, content = response)


@router.get("/submissions")
async def get_list_submission_endpoint(
    fullname: str = Query(None, description="Student name"),
    is_scored: bool = Query(None, description="is scored"),
    exam_id: int = Query(None, description="exam_id"),
    exam_set_id: int = Query(None, description="exam_id"),
    page: int = Query(1, ge=0, description="Number of page"),
    limit: int = Query(100, ge=1, le=200, description="Maximum number of records to return")
):
    """
    Lấy danh sách các submission
    """
    records = get_list_submission(exam_id=exam_id, is_scored=is_scored, fullname=fullname, examset_id=exam_set_id, page=page, limit = limit)
    return JSONResponse(status_code=status.HTTP_200_OK, content = records)

@router.get("/submission/{submission_id}")
async def get_submission_by_id_endpoint(
    submission_id: int
):
    """
    Chọn submission
    """
    records = get_submission_by_id(submission_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content = records)

@router.patch("/submission/{submission_id}")
async def score_submission(
    submission_id: int,
    item: ExamSubmissionSchema,
):
    """
    Cho điểm submission
    """
    response = update_exam_submission(submission_id, item.json_data, item.score)
    return JSONResponse(status_code=status.HTTP_200_OK, content = response)

@router.post(
    "/exam-sets/{exam_set_id}/speaking-exam", 
    response_model=ExamCreateResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Create a speaking Exam Part for an Exam Set" # Thêm summary cho Swagger
)
async def create_speaking_exam_for_set_endpoint(
    exam_set_id: int, 
    current_admin: Annotated[dict, Depends(get_current_admin_user)],
    exam_part_code: str = Form(
        ..., 
        description="Unique code for this speaking part within the exam set (e.g., RD001_S1).",
        example="RD_SET1_PART"
    ),
    title_for_part: str = Form(
        ..., 
        description="Title for this speaking part (e.g., 'speaking Section - Aptis General Set 1').",
        example="speaking - Aptis Test Alpha"
    ),
    time_limit_minutes_for_part: int = Form(
        ..., 
        gt=0, 
        description="Time limit in minutes specifically for this speaking part.",
        example=60
    ),
    file: UploadFile = File(
        ..., 
        description="The Excel (.xlsx) containing the speaking exam content."
    )
):
    """
    Allows an Admin to upload a PDF file to create a new speaking exam part
    and associate it with an existing ExamSet.

    - **exam_set_id**: The ID of the parent ExamSet.
    - **exam_part_code**: A unique code for this specific speaking exam (e.g., speaking_01).
    - **title_for_part**: The title for this speaking section.
    - **time_limit_minutes_for_part**: Duration in minutes for this speaking section.
    - **file**: The PDF document for the exam.
    """
    if not file.filename or not file.filename.lower().endswith(".xlsx"): # Kiểm tra filename có tồn tại
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid file type or no filename. Only Excel files (.xlsx) are allowed."
        )

    created_by_user_id = current_admin['id']
    
    try:
        exam_details_dict = await exam_service.create_speaking_exam_from_excel(
            exam_set_id=exam_set_id,
            exam_part_code=exam_part_code,
            descriptions=title_for_part,
            time_limit_for_part=time_limit_minutes_for_part,
            excel_file=file,
            created_by_user_id=created_by_user_id
        )
        # exam_details_dict bây giờ nên chứa các trường khớp với ExamCreateResponseSchema
        # ví dụ: exam_id (của phần thi), exam_code (của phần thi), title (của phần thi), 
        # exam_type, time_limit_minutes (của phần thi)
        
        # Tạo response object từ Pydantic model
        # Đảm bảo các key trong exam_details_dict khớp với các field của ExamCreateResponseSchema
        # Hoặc ExamCreateResponseSchema có thể cần được điều chỉnh.
        # Giả sử exam_details_dict trả về:
        # { 'exam_id': ..., 'exam_code': ..., 'title': ..., 'exam_type': 'listening', 'time_limit_minutes': ...}
        
        return ExamCreateResponseSchema(
            exam_id=exam_details_dict['id'],
            exam_code=exam_details_dict['exam_code'], # Đây là exam_part_code
            title=exam_details_dict['description'],         # Đây là title_for_part
            exam_type=exam_details_dict['exam_type'],
            time_limit_minutes=exam_details_dict.get('time_limit'), # Lấy từ record đã tạo
            message=f"speaking exam part '{exam_part_code}' created successfully for ExamSet ID {exam_set_id}."
        )
    except HTTPException as e:
        # Lỗi đã được xử lý và ném lại từ service, hoặc lỗi validation ở đây
        raise e
    except Exception as e_main:
        # Lỗi không mong muốn ở controller level (hiếm khi xảy ra nếu service xử lý tốt)
        print(f"Unexpected error in controller: {e_main}")
        raise HTTPException(status_code=500, detail=f"An error occurred in the controller: {str(e_main)}")

@router.patch("/exam/speaking/{exam_id}")
async def update_speaking_exam_for_set_endpoint(
    exam_id: int, 
    current_admin: Annotated[dict, Depends(get_current_admin_user)],
    file: UploadFile = File(
        ..., 
        description="The Excel file excel containing the speaking exam content."
    )
):
    """
    Allows an Admin to upload a Excel file to create a new speaking exam part
    and associate it with an existing ExamSet.

    - **exam_set_id**: The ID of the parent ExamSet.
    - **file**: The Excel document for the exam.
    """
    if not file.filename or not file.filename.lower().endswith(".xlsx"): # Kiểm tra filename có tồn tại
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid file type or no filename. Only Excel files (.xlsx) are allowed."
        )

    created_by_user_id = current_admin['id']
    
    try:
        exam_details_dict = await exam_service.update_speaking_exam_from_excel(
            exam_id=exam_id,
            excel_file=file,
        )
        # exam_details_dict bây giờ nên chứa các trường khớp với ExamCreateResponseSchema
        # ví dụ: exam_id (của phần thi), exam_code (của phần thi), title (của phần thi), 
        # exam_type, time_limit_minutes (của phần thi)
        
        # Tạo response object từ Pydantic model
        # Đảm bảo các key trong exam_details_dict khớp với các field của ExamCreateResponseSchema
        # Hoặc ExamCreateResponseSchema có thể cần được điều chỉnh.
        # Giả sử exam_details_dict trả về:
        # { 'exam_id': ..., 'exam_code': ..., 'title': ..., 'exam_type': 'speaking', 'time_limit_minutes': ...}
        
        return ExamCreateResponseSchema(
            exam_id=exam_details_dict['id'],
            exam_code=exam_details_dict['exam_code'], # Đây là exam_part_code
            title=exam_details_dict['description'],         # Đây là title_for_part
            exam_type=exam_details_dict['exam_type'],
            time_limit_minutes=exam_details_dict.get('time_limit'), # Lấy từ record đã tạo
            message=f"speaking exam part '{exam_details_dict['exam_code']}' update successfully for ExamSet ID {exam_details_dict['examset_id']}."
        )
    except HTTPException as e:
        # Lỗi đã được xử lý và ném lại từ service, hoặc lỗi validation ở đây
        raise e
    except Exception as e_main:
        # Lỗi không mong muốn ở controller level (hiếm khi xảy ra nếu service xử lý tốt)
        print(f"Unexpected error in controller: {e_main}")
        raise HTTPException(status_code=500, detail=f"An error occurred in the controller: {str(e_main)}")

@router.post("/sync")
async def sync_data():
    exam_service.download_all_listening()
    exam_service.create_instruction_audio()
    exam_service.download_all_images()
    

    