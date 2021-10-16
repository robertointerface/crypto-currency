from .errors import ExtractorErrorResponse


class ResponseExtractor:

    def __init__(self):
        self.extractor = None

    # @property
    # def extractor(self):
    #     return self.extractor
    #
    # @extractor.setter
    # def extractor(self, value):
    #     if self.extractor is None:
    #         self.extractor = value

    def extract_response(self, extractor):
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
        return (i for i in self.extractor)

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def __str__(self):
        return f'{self.__class__.__name__}'
