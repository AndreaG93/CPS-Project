import numpy
import pandas


class TimeSeriesDataset(object):
    """
    This class is used to manage a 'Time Series' dataset.
    """

    def __init__(self, name, file):

        self.__file = file

        self._name = name
        self._data = None
        self._time_range = None
        self._numeric_type_columns = None

        self.__read_data()
        self.__compute_time_range()
        self.__compute_numeric_type_columns()

    def __read_data(self):
        """
        This function is used to read data from file-system.
        """

        self._data = pandas.read_csv(self.__file,
                                     index_col=0,
                                     header=0,
                                     parse_dates=True)
        self._data.index.name = 'Time'

    def __compute_time_range(self):
        """
        This function is used to compute the 'time range' of data available inside current dataset.
        """
        self._time_range = [0, 0]

        self._time_range[0] = self._data.index.min()
        self._time_range[1] = self._data.index.max()

    def __compute_numeric_type_columns(self):
        """
        This function is compute column names corresponding to numeric data.
        """
        self._numeric_type_columns = self._data.select_dtypes(include=[numpy.number]).columns.tolist()

    def get_numeric_type_columns(self):
        return self._numeric_type_columns

    def get_time_range(self):
        return self._time_range

    def get_time_range_as_years(self):
        return [self._time_range[0].year, self._time_range[1].year]

    def get_data(self):
        return self._data

    def get_name(self):
        return self._name
