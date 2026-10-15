from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

# Use as a parameter type in endpoints:
#     def list_things(db: DbSession): ...
DbSession = Annotated[Session, Depends(get_db)]
