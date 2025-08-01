#from schema.response import Book
#from sqlalchemy.engine import Row

# def map_book_row(row: Row) -> Book:
#     if not row:
#         return None

#     data = dict(row._mapping)  # clean conversion from SQLAlchemy Row
#     return Book(**data)

def map_row_to_model(row, model_class):
    return model_class(**dict(row._mapping))
