from fastapi import FastAPI

from app.helpers.middlewares import catch_exceptions_middleware
from app.controllers import auth_controller, admin_controller, member_controller # Import admin_controller
# Import các routers khác nếu có
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.services.exam_service import download_all_listening

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
# ...

@app.get("/")
async def root():
    return {"message": "Welcome to Aptis Exam Web App API"}


@app.get("/secure-endpoint")
def read_secure_data(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    return {"token": credentials.credentials}
# Nếu bạn muốn chạy hàm tạo user mẫu khi khởi động app (CHỈ DÀNH CHO DEV)
# from app.services.auth_service import create_sample_user
# import asyncio

# @app.on_event("startup")
# async def startup_event():
#     print("Running startup events...")
#     # Tạo user admin mẫu
#     await create_sample_user("admin", "adminpass", "Administrator", "admin")
#     # Tạo user member mẫu
#     await create_sample_user("member", "memberpass", "Normal Member", "member")
#     print("Startup events finished.")
origins = ["http://127.0.0.1"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware('http')(catch_exceptions_middleware)
def setup_scheduler():
    scheduler = AsyncIOScheduler(timezone="Asia/Bangkok")
    trigger = CronTrigger(hour=0, minute=0)
    scheduler.add_job(download_all_listening, trigger, id='daily_download')
    scheduler.start()
    return scheduler

@app.on_event("startup")
def on_startup():
    download_all_listening()
    app.state.scheduler = setup_scheduler()
    print("Scheduler started: daily download at 00:00 VN time")

@app.on_event("shutdown")
def on_shutdown():
    app.state.scheduler.shutdown()
    print("Scheduler shut down")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5055)