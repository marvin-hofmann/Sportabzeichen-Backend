from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from src.database import database_utils
from src.models.models import Certificate
from src.schemas.certificate_schema import CertificatePostSchema


def create_certificate(athlete_id, title, blob: UploadFile, user_id: str, db: Session) -> Certificate:
    blob_data = blob.file.read()
    certificate_post_schema = CertificatePostSchema(
        athlete_id=athlete_id,
        title=title,
        blob=blob_data
    )
    certificate_dict = certificate_post_schema.model_dump(exclude_unset=True)
    certificates = Certificate(**certificate_dict, uploader=user_id)
    database_utils.add(certificates, db)
    return certificates


def get_certificates_by_id(id: str, db: Session) -> Certificate:
    certificate: Certificate | None = db.get(Certificate, id)

    if certificate is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found")
    return certificate


def delete_certificate(id: str, db: Session) -> None:
    return database_utils.delete(Certificate, id, db)
