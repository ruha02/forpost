from fastapi_filter.contrib.sqlalchemy import Filter
from models import Question


class QuestionFilter(Filter):
    source_id: int | None = None

    class Constants(Filter.Constants):
        model = Question
