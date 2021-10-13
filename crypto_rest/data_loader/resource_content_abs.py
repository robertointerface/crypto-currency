"""Define abstract base class for future classes that fetch data"""
import abc


class ContentResourceFetcher(abc.ABC):
    """Base Abstract class for resource fetcher, the resource could be an
     API, file, storage destination..."""

    @abc.abstractmethod
    def fetch(self):
        pass
