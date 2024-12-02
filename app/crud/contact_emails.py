from sqlmodel import Session, select

from app.models.contact_emails import ContactEmails, ContactEmailsCreate, ContactEmailsUpdate

from .base import BaseCRUD


class ContactEmailsCRUD(BaseCRUD[ContactEmails, ContactEmailsCreate, ContactEmailsUpdate]):
    async def get_unsent_count(self, db: Session) -> int:
        """Get count of unsent emails."""
        statement = select(self.model).where(self.model.sent == False)  # noqa: E712
        result = db.exec(statement).all()
        return len(result)

    async def get_filtered(
        self, db: Session, filter_status: str | None = None
    ) -> list[ContactEmails]:
        """Get filtered emails based on sent status."""
        statement = select(self.model)

        if filter_status == "sent":
            statement = statement.where(self.model.sent == True)  # noqa: E712
        elif filter_status == "not_sent":
            statement = statement.where(self.model.sent == False)  # noqa: E712

        statement = statement.order_by(self.model.created_at.desc())
        return db.exec(statement).all()


contact_emails = ContactEmailsCRUD(model=ContactEmails)
