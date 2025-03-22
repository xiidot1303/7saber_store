from app.services import *
from app.models import Subcategory, Category


def create_subcategory(billz_id, name) -> Subcategory:
    subcategory = Subcategory(
        name=name,
        billz_id=billz_id,
    )
    subcategory.save()
    return subcategory