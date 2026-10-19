from datetime import UTC, datetime
from hashlib import sha256

import pymupdf
from django.contrib import admin
from django.core.files import File
from django.forms import ModelForm

from ofnir.models import CurriculumVitae


def extract_text_from_pdf(file_contents: bytes) -> str:
    with pymupdf.open(stream=file_contents, filetype="pdf") as pdf:
        return "\n".join(page.get_text() for page in pdf)


class CurriculumVitaeForm(ModelForm):
    class Meta:
        model = CurriculumVitae
        fields = ("file",)

    def save(self, commit=True):
        instance = super().save(commit=False)
        uploaded_file: File = self.cleaned_data["file"]

        instance.file_name = uploaded_file.name

        digest = sha256()
        for chunk in uploaded_file.chunks():
            digest.update(chunk)
        instance.sha256_sum = digest.hexdigest()
        uploaded_file.seek(0)
        instance.contents = extract_text_from_pdf(uploaded_file.read())

        instance.last_updated = datetime.now(tz=UTC)

        if commit:
            instance.save()
            self.save_m2m()

        return instance


@admin.register(CurriculumVitae)
class CurriculumVitaeAdmin(admin.ModelAdmin):
    fields = ("file", "file_name", "last_updated", "contents", "sha256_sum")
    readonly_fields = ("file_name", "last_updated", "contents", "sha256_sum")
    list_display = ("file_name", "last_updated", "sha256_sum")
    form = CurriculumVitaeForm
