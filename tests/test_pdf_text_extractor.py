from ofnir.admin import extract_text_from_pdf

MY_CV_CONTENTS = [
    "Jakub Kołodziej",
    "Software Engineer in Mission Control",
    "NATS, MQTT, PostgreSQL (TimescaleDB), SQL Server, SQLite3",
]


def test_pdf_text_extractor():
    with open("tests/resources/Jakub Kołodziej CV.pdf", "rb") as file:
        for word in MY_CV_CONTENTS:
            assert extract_text_from_pdf(file.read()).__contains__(word)
            file.seek(0)
