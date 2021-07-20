from src import Common
from src.TimeSeriesDataset.TimeSeriesDatasetGlobalClimateChange import *


class ApplicationOptions(object):
    """
    This class is used to store plot parameters and application's options specified by the user.
    """

    def __init__(self):
        self.month_filter_enabled = True
        self.month_name = ""
        self.city = ""
        self.state = ""
        self.states = list()
        self.available_time_range_as_years = None
        self.plot_time_range_as_years = None
        self.available_columns = None
        self.active_columns = None
        self.display_univariate_regression_line = False


class Application(object):
    """
    This class represent the controller of this application.
    It is used to load and hold datasets data and all options necessary to plot data.
    """

    def __init__(self, dataset_file_path=None):

        if dataset_file_path is not None and not isinstance(dataset_file_path, str):
            raise TypeError("[ERROR]: 'dataset_filename' must 'str' type object! ({})".format(type(dataset_file_path)))

        self.__current_selected_dataset = None
        self.__current_selected_application_options = None
        self.__dataset_registry = None
        self.__application_options_registry = None

        print("Please Wait\n-> Collecting dataset...")
        self.__build_dataset_registry(dataset_file_path)
        self.__build_options_registry()
        print("-> Collecting dataset COMPLETE!")

        # Select first dataset as default...
        self.set_current_selected_dataset(self.get_available_dataset_names()[0])

    def __build_dataset_registry(self, dataset_file_path):
        """
        This function is used to build a 'Dataset' object for each available datasets.
        """
        self.__dataset_registry = dict()

        datasets = Common.list_files("./data", ".csv")
        if len(datasets) == 0:
            raise RuntimeError("[ERROR] './data directory is empty. Did you download datasets?'")

        # Retrieve dataset file list...
        if dataset_file_path is not None and dataset_file_path in datasets:
            datasets = [dataset_file_path]

        # Build dataset...
        for file in datasets:

            dataset_name = file.rsplit('/', 1)[1]
            dataset_header = pandas.read_csv(file, nrows=0).columns

            if "City" in dataset_header and "Country" in dataset_header:
                dataset = TimeSeriesDatasetGlobalClimateChange(dataset_name, file)
            elif "City" not in dataset_header and "Country" in dataset_header:
                dataset = TimeSeriesDatasetGlobalClimateChangeNoCity(dataset_name, file)
            else:
                dataset = TimeSeriesDatasetGlobalClimateChangeNoStateNoCity(dataset_name, file)

            self.__dataset_registry[dataset_name] = dataset

    def __build_options_registry(self):
        """
        This function is used to build an 'ApplicationOptions' object for each available dataset.
        """
        self.__application_options_registry = dict()

        for dataset_name, dataset in self.__dataset_registry.items():
            x = ApplicationOptions()

            x.plot_time_range_as_years = dataset.get_time_range_as_years()
            x.available_time_range_as_years = dataset.get_time_range_as_years()
            x.available_columns = dataset.get_numeric_type_columns()
            x.active_columns = [x.available_columns[0]]

            self.__application_options_registry[dataset_name] = x

    def set_current_selected_dataset(self, dataset_name):

        self.__current_selected_dataset = self.__dataset_registry[dataset_name]
        self.__current_selected_application_options = self.__application_options_registry[dataset_name]

    def get_current_selected_dataset(self):
        return self.__current_selected_dataset

    def get_current_application_options(self):
        return self.__current_selected_application_options

    def get_available_dataset_names(self):
        return list(self.__dataset_registry.keys())
