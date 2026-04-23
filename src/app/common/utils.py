import random
import bcrypt


def entity_to_model(entity, model_class):
    model_columns = model_class.__table__.columns.keys()

    data = {key: getattr(entity, key) for key in model_columns if hasattr(entity, key)}

    return model_class(**data)


def model_to_entity(model, entity_class):
    entity_fields = entity_class.__init__.__code__.co_varnames

    data = {
        column.name: getattr(model, column.name)
        for column in model.__table__.columns
        if column.name in entity_fields
    }

    return entity_class(**data) 

def generate_otp():
    otp = random.randint(100000, 999999)
    return otp


def hash_password(password: str) -> str:
    # # bcrypt hash

    # # example password
    # # converting password to array of bytes
    # bytes = password.encode("utf-8")
    # # generating the salt
    # salt = bcrypt.gensalt()
    # # Hashing the password
    # hashed_password = bcrypt.hashpw(bytes, salt)

    # return hashed_password

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password.decode("utf-8")   


async def match_password(password,stored_pw):
    print(type(stored_pw))

    # encoding user password
    # stored_bytes = stored_pw.encode("utf-8")
    # userBytes = password.encode("utf-8")
    # # hash = bcrypt.hashpw(userBytes, salt)
    # # checking password
    # print(type(userBytes))
    # result = bcrypt.checkpw(userBytes, stored_bytes)
    # return result

    return bcrypt.checkpw(
        password.encode("utf-8"),
        stored_pw.encode("utf-8")
    )
