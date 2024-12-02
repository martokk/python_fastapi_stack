from typing import List

from sqlalchemy import text
from sqlmodel import Session, select

from app import models

from .base import BaseCRUD


class FAQCRUD(BaseCRUD[models.FAQ, models.FAQCreate, models.FAQUpdate]):
    async def get_by_program(
        self, db: Session, *, program_id: str, include_program: bool = False
    ) -> List[models.FAQ]:
        """Get FAQs for a specific program, ordered by order field."""
        statement = (
            select(models.FAQ).where(models.FAQ.program_id == program_id).order_by(text('"order"'))
        )
        if include_program:
            statement = statement.join(models.Programs)
        return list(db.exec(statement).all())

    async def get_all_ordered(self, db: Session) -> List[models.FAQ]:
        """Get all FAQs ordered by program and then by order field."""
        statement = (
            select(models.FAQ).join(models.Programs).order_by(models.Programs.name, text('"order"'))
        )
        return list(db.exec(statement).all())

    async def update_orders(
        self, db: Session, *, program_id: str, faq_orders: List[dict[str, int]]
    ) -> None:
        """Update the order of FAQs for a specific program."""
        faqs = await self.get_by_program(db=db, program_id=program_id)

        # Create a mapping of id to new order
        order_map = {str(item["id"]): item["order"] for item in faq_orders}

        # Update each FAQ's order
        for faq in faqs:
            if str(faq.id) in order_map:
                faq.order = order_map[str(faq.id)]
                db.add(faq)

        db.commit()


faq = FAQCRUD(model=models.FAQ)
