from sqlalchemy.orm import Session
from app.models.task import Task as TaskModel
from app.schemas.task import TaskCreate

def get_tasks(db: Session):
    return db.query(TaskModel).all()

def get_task(db: Session, task_id: int):
    return db.query(TaskModel).filter(TaskModel.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
    db_task = TaskModel(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
