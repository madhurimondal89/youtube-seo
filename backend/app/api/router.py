from fastapi import APIRouter
from app.api.routes.research import router as research_router
from app.api.routes.audit import router as audit_router
from app.api.routes.competitor import router as competitor_router
from app.api.routes.ai import router as ai_router
from app.api.routes.system import router as system_router
from app.api.routes.workspace import router as workspace_router

api_router = APIRouter(prefix="/api")

api_router.include_router(system_router)
api_router.include_router(research_router)
api_router.include_router(audit_router)
api_router.include_router(competitor_router)
api_router.include_router(ai_router)
api_router.include_router(workspace_router)
