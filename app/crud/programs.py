from sqlmodel import Session, select

from app import crud, models

from .base import BaseCRUD


class ProgramsCRUD(BaseCRUD[models.Programs, models.ProgramsCreate, models.ProgramsUpdate]):
    async def get_by_name(self, db: Session, name: str) -> models.Programs | None:
        """Get a program by its name."""
        statement = select(self.model).where(self.model.name == name)
        return db.exec(statement).first()

    async def get_faqs_by_program_name(self, db: Session, name: str) -> list[models.FAQ]:
        """Get FAQs for a program by its name."""
        program = await self.get_by_name(db=db, name=name)
        if not program:
            return []
        return await crud.faq.get_by_program(db=db, program_id=program.id)


programs = ProgramsCRUD(model=models.Programs)
