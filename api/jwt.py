from datetime import timedelta

from fastapi_jwt import JwtAccessBearer

blacklist = set()


def is_token_blacklisted(token: str) -> bool:
    return token in blacklist


access_security = JwtAccessBearer(
    secret_key="e3a901646eeedc5425c33352374696a4e04f1f50",
    access_expires_delta=timedelta(minutes=30),
    auto_error=True
)
