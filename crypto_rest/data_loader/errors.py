class NonRelatedResponseError(Exception):
    """Error raised when a request response does not contain the requested
    result"""
    pass

class ExtractorErrorResponse(Exception):
    pass