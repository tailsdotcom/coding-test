"""Contains all errors raised in the middleware module"""


class MiddlewareError(Exception):
    """All exceptions raised in this module use this as the base exception class."""

    pass


class MiddlewareInputError(MiddlewareError):
    """Any error that is raised where the input a function is incorrect."""

    pass


class MiddlewareInternalError(MiddlewareError):
    """Any error that is raised where an internal error has occurred (this is bad)."""

    pass
