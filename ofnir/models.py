from pathlib import Path

from django.core.files.storage import FileSystemStorage
from django.db.models import DateTimeField, FileField, Model, TextField
from django.forms import ValidationError


def validate_pdf_filename(value: str) -> None:
    if Path(value).suffix.lower() != ".pdf":
        raise ValidationError("Upload a PDF file.", code="invalid_file_type")


# The CV django model
class CurriculumVitae(Model):
    file_name = TextField(
        db_index=True, null=False, max_length=128, validators=[validate_pdf_filename]
    )
    file = FileField(
        null=False,
        storage=FileSystemStorage(location=Path("storage/cv/")),
    )
    contents = TextField(null=False, max_length=16 * 1024)
    last_updated = DateTimeField(auto_created=True, null=False)
    sha256_sum = TextField(null=False, max_length=320)

    def __str__(self) -> str:
        return str(self.file_name)
