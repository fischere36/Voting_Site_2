from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self,id,user_name,email,password_hash):
        self.id=id
        self.user_name=user_name
        self.email=email
        self.password_hash=password_hash
    
    @classmethod
    def create(user_class, id, user_name, email, password):
        password_hash = generate_password_hash(password)
        return user_class(id, user_name, email, password_hash)

    @classmethod
    def from_db_row(cls, row):
        return cls(
            id=row[0],
            user_name=row[1],
            email=row[2],
            password_hash=row[3]
        )


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
