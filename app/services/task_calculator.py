from sqlalchemy.orm import Session
from app.models.task import Task as TaskModel

def calculate_task_progress_and_time(db: Session, task_id: int, depth: int = 0, max_depth: int = 10):
    if depth > max_depth:
        return (0.0, 0)

    subtasks = db.query(TaskModel).filter(TaskModel.parent_id == task_id).all()

    if not subtasks:
        task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
        if task:
            return (float(task.progress), task.estimated_time)
        return (0.0, 0)

    total_progress_weighted = 0.0
    total_time = 0
    total_estimated_time = 0

    for subtask in subtasks:
        sub_progress, sub_time = calculate_task_progress_and_time(db, subtask.id, depth + 1, max_depth)
        total_progress_weighted += sub_progress * subtask.estimated_time
        total_estimated_time += subtask.estimated_time
        total_time += sub_time

    progress = total_progress_weighted / total_estimated_time if total_estimated_time else 0.0

    return (round(progress, 2), total_time + total_estimated_time)
