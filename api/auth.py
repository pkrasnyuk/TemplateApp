from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

API_KEY_NAME = "api_key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, scheme_name="API key header", auto_error=False)


async def api_key_security(api_key_header: str = Security(api_key_header)):
    if api_key_header:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"The {API_KEY_NAME} must be passed as a header field",
    )
