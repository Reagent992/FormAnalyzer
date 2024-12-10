from typing import Final

# db
DB_NAME: Final = "form_analyzer_db"
DB_COLLECTION_NAME: Final = "form_analyzer"

# Validation
REGEX_PHONE_PATTERN: Final = (
    r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"
)
DATE_FORMAT_PATTERNS: Final = ("%d.%m.%Y", "%Y.%m.%d")
