from typing import Final


class Limits:
    """Numerical limits"""

    USERNAME_LENGTH: int = 150
    EMAIL_LENGTH: int = 254
    FIRST_NAME_LENGTH: int = 150
    LAST_NAME_LENGTH: int = 150
    PASSWORD_MAX_LENGTH: int = 150
    MIN_PASSWORD_LENGTH: int = 8
    MAX_PASSWORD_LENGTH: int = 32


class Messages:
    """Application messages"""

    EMAIL_ALREADY_EXISTS: Final = "Email already exists!"
    PROFILE_IS_INACTIVE: Final = "User profile has been deactivated"
    INCORRECT_PASSWORD: Final = "Provided password is incorrect"
    PASSWORD_WRONG_FORMAT: Final = (
        f"Password should have from {Limits.MIN_PASSWORD_LENGTH}"
        " to {Limits.MAX_PASSWORD_LENGTH} characters"
    )
    PROFILE_UPDATED: Final = "Profile has been updated"
    PROFILE_DELETED: Final = "Profile has been deleted"
