import calendar

import numpy
import pandas

from src.Statistics.SimpleRandomSample import SimpleRandomSample
from src.Statistics.UnivariateRegressionLine import UnivariateRegressionLine
from src.TimeSeriesDataset.TimeSeriesDataset import TimeSeriesDataset


class TimeSeriesDatasetGlobalClimateChange(TimeSeriesDataset):
    """
    This class is used to manage a 'Time Series' dataset regarding 'Global Climate Change' data.

    All data about all available 'State' and 'City', including 'State'-'Cities' mapping, are collected 'lazily',
    that is they are built only when needed.
    """

    # Following variable is used for 'month name' to 'month index' conversion...
    month_calendar_map = dict(
        (month_name, month_index) for month_name, month_index in zip(calendar.month_name[1:], range(1, 13)))

    def __init__(self, name, file):
        super().__init__(name, file)

        self.__city_list = None
        self.__state_list = None

        self.__state_to_city_map = dict()
        self.__city_to_state_map = dict()

    def get_state_list(self):
        """
        This function is used to get a list of all available 'State' inside current dataset.
        """
        if self.__state_list is None:
            self.__state_list = self._data["Country"].unique().tolist()

        return self.__state_list

    def get_city_list(self):
        """
        This function is used to get a list of all available 'City' inside current dataset.
        """
        if self.__city_list is None:
            self.__city_list = self._data["City"].unique().tolist()

        return self.__city_list

    def get_city_list_belonging_to_state(self, state_name):
        """
        This function is used to get a list of all available 'City' belonging to a specified 'State'.
        """

        if state_name == "" or state_name not in self.get_state_list():
            return None

        output = self.__state_to_city_map.get(state_name)
        if output is None:
            output = self._data[self._data["Country"] == state_name]["City"].unique().tolist()
            self.__state_to_city_map[state_name] = output

        return output

    def get_state_of_city(self, city_name):
        """
        This function is used to get the 'State' of a specified 'City' inside current dataset.
        """

        if city_name == "" or city_name not in self.get_city_list():
            return None

        output = self.__city_to_state_map.get(city_name)
        if output is None:
            output = self._data.query("City == {}".format("'{}'".format(city_name)))
            output = output.iloc[0]["Country"]
            self.__city_to_state_map[city_name] = output

        return output

    def get_filtered_data(self, month, use_month_filter, city, state, time_range, active_columns):
        """
        This function is used to filter available data according to user specified options.
        This function does not alter original data!

        It returns a 'pandas.DataFrame' object.
        """
        if not isinstance(month, str):
            raise TypeError("[ERROR]: 'month' must 'str' type object! ({})".format(type(month)))
        if not isinstance(use_month_filter, bool):
            raise TypeError("[ERROR]: 'use_month_filter' must 'bool' type object! ({})".format(type(use_month_filter)))
        if not isinstance(city, str):
            raise TypeError("[ERROR]: 'city' must 'str' type object! ({})".format(type(city)))
        if not isinstance(state, str):
            raise TypeError("[ERROR]: 'state' must 'str' type object! ({})".format(type(state)))
        if not isinstance(time_range, list):
            raise TypeError("[ERROR]: 'time_range' must 'list' type object! ({})".format(type(time_range)))
        if not isinstance(active_columns, list):
            raise TypeError("[ERROR]: 'active_columns' must 'list' type object! ({})".format(type(active_columns)))

        output = self._data

        # MONTH FILTER...
        # ========================================= #
        if use_month_filter:

            if month == "":
                raise ValueError("[ERROR]: MONTH empty!")

            elif month in TimeSeriesDatasetGlobalClimateChange.month_calendar_map.keys():
                output = output[output.index.month == TimeSeriesDatasetGlobalClimateChange.month_calendar_map[month]]

            else:
                raise ValueError("[ERROR]: Specified MONTH name does NOT exist!")

        # STATE FILTER...
        # ========================================= #
        if self.get_state_list() is not None:

            if state == "":
                raise ValueError("[ERROR]: 'STATE' field empty!")

            elif state in self.get_state_list():
                output = output[output["Country"] == state]

            else:
                raise ValueError("[ERROR]: Specified 'STATE' does NOT exist!")

        # CITY FILTER...
        # ========================================= #
        if self.get_city_list() is not None:

            if city == "":
                raise ValueError("ERROR: 'CITY' field empty!")

            elif city in self.get_city_list():
                output = output[output["City"] == city]

            else:
                raise ValueError("[ERROR]: Specified 'CITY' does NOT exist!")

        # COLUMN FILTER...
        # ========================================= #
        if len(active_columns) != 0:
            output = output[active_columns]
        else:
            raise ValueError("[ERROR]: No 'COLUMN' selected!")

        # REINDEXING IN ORDER TO FIND MISSING RECORDS...
        # ========================================= #
        new_index = pandas.date_range(start=output.index.min(),
                                      end=output.index.max(),
                                      freq="MS") # 'MS' stands for "month start frequency"

        expected_number_of_records = len(new_index)
        provided_number_of_records = len(output.index)

        if provided_number_of_records != expected_number_of_records:
            # Uncomment if you want...
            # print("Detected {} missing records! Reindexing...".format(expected_number_of_records - provided_number_of_records))
            output = output.reindex(new_index)

        # MANAGE 'NaN' VALUES...
        # ========================================= #
        number_of_nan_values = output.isnull().sum().sum()

        if number_of_nan_values == len(output):
            raise ValueError("[ERROR]: No Data!")

        if number_of_nan_values > 0:
            # Uncomment if you want...
            # print("Detected {} 'NaN' values. They will be managed with 'interpolate'...".format(number_of_nan_values))

            output = output.interpolate()

            if output.isnull().sum().sum() > 0:
                # Some 'NaN' can remain a the 'edge' of the dataset. Use 'dropna'
                output = output.dropna()

        # TIME RANGE FILTER...
        # ========================================= #
        if len(time_range) == 2:
            output = output[
                numpy.logical_and(output.index.year >= time_range[0], output.index.year <= time_range[1])]
        else:
            raise ValueError("[ERROR]: Specified 'TIME RANGE' is INVALID!")

        if len(output) == 0:
            raise ValueError("[ERROR]: No Data!")

        return output

    @staticmethod
    def compute_univariate_regression_line(data, name=""):
        """
        This function is used to create a regression line converting data properly.
        """
        if len(data.columns.tolist()) != 1:
            raise ValueError(
                "[ERROR]: Too many 'COLUMN' selected! Please select only one or disable regression line checkbox!")

        observations_x = TimeSeriesDatasetGlobalClimateChange.__convert_datetime_index_to_int_list(data.index)
        observations_y = data.values.reshape(data.values.shape[0]).tolist()

        sample_x = SimpleRandomSample(observations_x)
        sample_y = SimpleRandomSample(observations_y)

        return UnivariateRegressionLine(name, sample_x, sample_y)

    @staticmethod
    def __convert_datetime_index_to_int_list(x):
        """
        This function is used to convert a 'pandas.core.indexes.datetimes.DatetimeIndex' type object into a 'list' object.
        """
        output = list()

        for k in range(0, len(x)):
            output.append(x[k].timestamp())

        return output


class TimeSeriesDatasetGlobalClimateChangeNoCity(TimeSeriesDatasetGlobalClimateChange):
    """
    This class is used to manage a 'Time Series' dataset regarding 'Global Climate Change' data.
    Data do not have 'City' field.
    """

    def __init__(self, name, file):
        super().__init__(name, file)

    def get_city_list(self):
        return None

    def get_city_list_belonging_to_state(self, state_name):
        return None

    def get_state_of_city(self, city_name):
        return None


class TimeSeriesDatasetGlobalClimateChangeNoStateNoCity(TimeSeriesDatasetGlobalClimateChange):
    """
    This class is used to manage a 'Time Series' dataset regarding 'Global Climate Change' data.
    Data do not have 'City' and 'State' (called 'Country' inside CSV files)  fields.
    """

    def __init__(self, name, file):
        super().__init__(name, file)

    def get_state_list(self):
        return None

    def get_city_list(self):
        return None

    def get_city_list_belonging_to_state(self, state_name):
        return None

    def get_state_of_city(self, city_name):
        return None
