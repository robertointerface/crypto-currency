from .errors import ExtractorErrorResponse


class ResponseExtractor:
    """Use an instance with attributes:
    - set_response_sequence.
    - set_response_first_result_date.
    To extract data.
    """
    def __init__(self):
        self.extractor = None

    def extract_response(self, extractor):
        """Use provided extractor to extract data."""
        self.extractor = extractor
        extract_steps = [
            extractor.set_response_sequence,
            extractor.set_response_first_result_date,
        ]
        if not extractor.is_error_response():
            [step() for step in extract_steps]
        else:
            raise ExtractorErrorResponse

    def __iter__(self):
        """Iterate over extracted data"""
        return (i for i in self.extractor)

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __str__(self):
        return f'{self.__class__.__name__}'
