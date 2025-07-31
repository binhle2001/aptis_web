from datetime import datetime
import logging
from fastapi import FastAPI
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("google_genai.models").setLevel(logging.WARNING)
from services.user_service import alarm_user_with_email
from helpers.common import get_env_var
from helpers.middlewares import catch_exceptions_middleware
from controllers import auth_controller, admin_controller, member_controller, guest_controller, commitment_controller # Import admin_controller
# Import các routers khác nếu có
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from services.exam_service import cleanup_orphaned_files, create_instruction_audio, download_all_images, download_all_listening, scoring_speaking_exam_by_AI, scoring_writing_exam_by_AI

bearer_scheme = HTTPBearer()

app = FastAPI(
    title="Aptis Exam Web App API",
    description="API for managing Aptis exams and user attempts.",
    version="1.1.0",
)

# Include routers
app.include_router(auth_controller.router)
app.include_router(admin_controller.router) # Thêm admin router
app.include_router(member_controller.router)
app.include_router(guest_controller.router)
app.include_router(commitment_controller.router)
# ...

@app.get("/")
async def root():
    return {"message": "Welcome to Aptis Exam Web App API"}


@app.get("/secure-endpoint")
def read_secure_data(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    return {"token": credentials.credentials}
# Nếu bạn muốn chạy hàm tạo user mẫu khi khởi động app (CHỈ DÀNH CHO DEV)
# fromservices.auth_service import create_sample_user
# import asyncio

# @app.on_event("startup")
# async def startup_event():
#     print("Running startup events...")
#     # Tạo user admin mẫu
#     await create_sample_user("admin", "adminpass", "Administrator", "admin")
#     # Tạo user member mẫu
#     await create_sample_user("member", "memberpass", "Normal Member", "member")
#     print("Startup events finished.")
origins = ["http://localhost:3000", "https://aptisone-test.io.vn"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware('http')(catch_exceptions_middleware)
def setup_scheduler():
    scheduler = AsyncIOScheduler(timezone="Asia/Bangkok")
    trigger = CronTrigger(hour=0, minute=0)
    scheduler.add_job(download_all_listening, trigger, id='daily_download')
    scheduler.add_job(create_instruction_audio, trigger, id='daily_create_instruction')
    scheduler.add_job(download_all_images, trigger, id='daily_download_image')
    scheduler.add_job(cleanup_orphaned_files, trigger, id='cleanup_orphaned_files')
    start_date_str = get_env_var('REMIND', 'START_DATE')  # '2025/7/26 12:00:00'
    start_date = datetime.strptime(start_date_str, "%Y/%m/%d %H:%M:%S")
    two_day_trigger = IntervalTrigger(
        days=2,
        start_date=start_date,
        timezone="Asia/Bangkok"
    )
    scheduler.add_job(alarm_user_with_email, two_day_trigger, id='every_2_days_at_noon')
    queue_trigger = IntervalTrigger(seconds=30, timezone="Asia/Bangkok")
    scheduler.add_job(scoring_writing_exam_by_AI, queue_trigger, id='queue_scanner')
    speaker_trigger = IntervalTrigger(seconds=600, timezone="Asia/Bangkok")
    scheduler.add_job(scoring_speaking_exam_by_AI, speaker_trigger, id='speaking_scanner')
    scheduler.start()
    return scheduler

@app.on_event("startup")
def on_startup():
    download_all_listening()
    create_instruction_audio()
    download_all_images()
    cleanup_orphaned_files()
    app.state.scheduler = setup_scheduler()
    print("Scheduler started: daily download at 00:00 VN time")

@app.on_event("shutdown")
def on_shutdown():
    app.state.scheduler.shutdown()
    print("Scheduler shut down")
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=5055)
