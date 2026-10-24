import jwt
from datetime import datetime, timedelta, timezone

secret_key = "your_secret_key"

payload = {
    "user_id": 123,
    }

token = jwt.encode(payload, secret_key, algorithm="HS256")
print("Generated JWT Token:", token)


def create_token(user_id, token_type):
    if token_type == "access":
        exp_time = datetime.now(timezone.utc) + timedelta(minutes=10)
    elif token_type == "refresh":
        exp_time = datetime.now(timezone.utc) + timedelta(days=7)
    else:
        raise ValueError("Invalid token type.")

    payload = {
        "sub": user_id,
        "type": token_type,
        "exp": exp_time
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token



def verify_token(token, expected_type):
    try:
        payload = jwt.decode(
            token,
            secret_key,
            algorithms=["HS256"],
            options={"require": ["sub", "exp", "type"]}
        )
        return payload

    except jwt.ExpiredSignatureError:
        print("Token has expired!")
        return None

    except jwt.InvalidTokenError:
        print("Invalid token!")
        return None
user_id = "user123"

access_token = create_token(user_id, "access")
refresh_token = create_token(user_id, "refresh")

print("ACCESS TOKEN:")
print(access_token)

print("\nREFRESH TOKEN:")
print(refresh_token)


print("\nVERIFY ACCESS TOKEN:")
result = verify_token(access_token, "access")

if result:
    print("Access granted to:", result["sub"])


print("\nREFRESH ACCESS TOKEN:")
result = verify_token(refresh_token, "refresh")

if result:
    new_access_token = create_token(result["sub"], "access")
    print("New access token created")
    print(new_access_token)


result = verify_token(access_token, "refresh")

if result is None:
    print("Access denied: wrong token type")
