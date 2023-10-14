class AuthStatus(object):
    """docstring for AuthStatus"""
    SESSION_EXPIRED = "The session was expired, please login and try again!"
    SESSION_NOT_EXISTS = "The server could not verify that a session exists."

    MISSING_ARRAY_FIELDS = "Array field(s) is missing"

    INVALID_HEADERS = "Access Denied. Invalid Headers"
    INVALID_TOKEN_TYPE = "Access Denied. the token_type is not valid"
    INVALID_API_KEY = "Access Denied. Invalid Api key"
    INVALID_EMAIL = "Access Denied. Invalid email"
    INVALID_API_KEY_LENGTH = "the length of the Api key is not valid"

    INVALID_ROLE = "Access denied. can not be accessed with the current role"
    MISSING_ROLE = "The current user does not have an active role"
    MISSING_PRIMITIVE_ROLE = "Access denied. The system does not have a list of defined roles"

    MISSING_AUTH_KEY = "Unexpected Error: could not verify that a token exists."
    UNEXPECTED_ERROR = "Unexpected Error"

    APP_NOT_EXISTS = "The Application do not exists"
    APP_INFO_ERROR = "Check the following: The company, application, and client must exist, and be active."
    USER_NOT_EXIST = "The User do not exists"
    INVALID_PASSWORD = "The password is not valid"

    INACTIVE_USER = "The user is not active"
    COMPANY_MISMATCH = "The user does not belong to this company"
