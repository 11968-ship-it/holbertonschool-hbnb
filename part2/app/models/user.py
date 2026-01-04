class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin):
        super().__init__()
