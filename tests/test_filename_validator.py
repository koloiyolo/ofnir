import pytest
from django.forms import ValidationError

from ofnir.models import validate_pdf_filename


def test_filename_validator():
    with pytest.raises(ValidationError):
        validate_pdf_filename("test.txt")

    with pytest.raises(ValidationError):
        validate_pdf_filename("test2.pdf.txt")

    validate_pdf_filename("test3.pdf")
