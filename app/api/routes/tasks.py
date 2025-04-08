from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.task import Task as TaskSchema, TaskCreate
from app.db.database import SessionLocal
from app.crud import task as crud
from app.services import task_calculator

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[TaskSchema])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@router.get("/{task_id}", response_model=TaskSchema)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

@router.post("/", response_model=TaskSchema)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@router.get("/{task_id}/calculate", response_model=TaskSchema)
def calculate_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    progress, estimated_time = task_calculator.calculate_task_progress_and_time(db, task_id)
    return TaskSchema(
        id=task.id,
        parent_id=task.parent_id,
        progress=progress,
        estimated_time=estimated_time,
        created_at=task.created_at,
        updated_at=task.updated_at
    )
