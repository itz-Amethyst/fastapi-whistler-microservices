# from bson import datetime
from datetime import datetime
from beanie import Document, Indexed


class Discount(Document):
    #! id _id autogenerate by Beanie
    # code: Indexed(str)
    code: str
    use_count: int
    start_date: datetime
    end_date: datetime
    percentage: float
    #Todo: later receive user id from request
    # created_by: int

    class Settings:
        name = 'discounts'
        # use_cache = True
        # cache_expiration_time = datetime.timedelta(seconds=10)
    #     cache_capacity = 10