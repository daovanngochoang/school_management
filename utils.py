from starlette.responses import JSONResponse

from dtos import ResponseEntity


def exception_to_string(ex: Exception):
    if hasattr(ex, 'message'):
        msg = ex.message
    else:
        msg = ex
    return msg


def response(code: int, response_entity: ResponseEntity) -> JSONResponse:
    return JSONResponse(
        status_code=code,
        content=response_entity.model_dump()
    )


def success_response(code, data: object) -> JSONResponse:
    return response(
        code=code,
        response_entity=ResponseEntity(
            status=True,
            error_message=None,
            data=data
        )
    )


def error_response(code: int, msg: str) -> JSONResponse:
    return response(
        code=code,
        response_entity=ResponseEntity(
            status=False,
            error_message=msg,
            data=None
        )

    )
