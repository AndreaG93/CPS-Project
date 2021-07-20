import threading

from src.Application import Application
from src.GUI.GUICommon import GUICommon
from src.GUI.GUIRegressionLineComparison import GUIRegressionLineComparison
from src.Statistics.UnivariateRegressionLine import UnivariateRegressionLine
from src.TimeSeriesDataset.TimeSeriesDatasetGlobalClimateChange import TimeSeriesDatasetGlobalClimateChange


class GUIRegressionLineComparisonController(GUIRegressionLineComparison):
    """
    This class is used as controller for all 'ipywidgets widget' inside 'GUIRegressionLineComparison' class.
    """

    def __init__(self, application):
        super().__init__()

        if application is None:
            raise ValueError("[ERROR]: 'application' cannot be 'None'!")

        if type(application) is not Application:
            raise TypeError("[ERROR]: 'application' must be 'Application' type!")

        # Set needed 'dataset'
        application.set_current_selected_dataset("GlobalLandTemperaturesByCountry.csv")

        self.__application = application
        self.__application_options = application.get_current_application_options()
        self.__current_selected_dataset = application.get_current_selected_dataset()

        self.__lock = threading.Lock()

    def display(self):
        self.update()

        # Populate button event...
        self._widget_compare_button.on_click(self.compare_event)
        self._widgets_remove_state_comparison_list_button.on_click(self.remove_state)
        self._widgets_insert_state_comparison_list_button.on_click(self.add_state)

        super(GUIRegressionLineComparisonController, self).display()

    def add_state(self, button):
        """
        This function add a state to the list for 'Regression Line Comparison'
        """
        state = self._widgets_state_for_comparison_combobox.value

        # Check for errors...
        if state is None or state not in self.__current_selected_dataset.get_state_list():
            self._widget_error_label.value = "$\\textbf{[ERROR] Specified 'State' does not exist!}$"
            return
        else:
            self._widget_error_label.value = ""

        if state not in self.__application_options.states:
            self.__application_options.states.append(state)
            self.update()
            self._widgets_state_list_comparison_select.value = self.__application_options.states[0]

    def remove_state(self, button):
        """
        This function remove a state from the list for 'Regression Line Comparison'
        """
        state = self._widgets_state_list_comparison_select.value

        if state in self.__application_options.states:
            self.__application_options.states.remove(state)

            if len(self.__application_options.states) != 0:
                self._widgets_state_list_comparison_select.value = self.__application_options.states[0]

            self.update()

    def compare_event(self, button):
        """
        This function is used to perform the plot of data according to user specified options.
        """

        self._widget_error_label.value = ""
        self.display()

        try:
            if len(self.__application_options.states) == 0:
                raise ValueError("[ERROR]: No 'State' specified!!")
            if len(self.__application_options.states) == 1:
                raise ValueError("[ERROR]: Please, specify at least 2 states!!")

            state_regression_line_list = list()

            # Build regression lines belonging to each state...
            # ========================================= #
            for state in self.__application_options.states:

                data = self.__current_selected_dataset.get_filtered_data(self.__application_options.month_name,
                                                                         self.__application_options.month_filter_enabled,
                                                                         self.__application_options.city,
                                                                         state,
                                                                         self.__application_options.plot_time_range_as_years,
                                                                         self.__application_options.active_columns)
                if (len(data)) == 1:
                    raise ValueError("[ERROR]: Nothing to plot; only 1 record of data!!")

                regression_line = TimeSeriesDatasetGlobalClimateChange.compute_univariate_regression_line(data,
                                                                                                          name=state)
                state_regression_line_list.append(regression_line)

            # Print a title...
            # ========================================= #
            if self.__application_options.month_filter_enabled:
                print("Regression Line Rank ({} - {} - {})".format(self.__application_options.month_name,
                                                              self.__application_options.plot_time_range_as_years,
                                                              self.__application_options.active_columns))
            else:
                print("Regression Line Rank (Every Months - {} - {})".format(
                    self.__application_options.plot_time_range_as_years,
                    self.__application_options.active_columns))

            # Rank...
            # ========================================= #
            UnivariateRegressionLine.rank_regression_lines(state_regression_line_list)

        except ValueError as error:
            self._widget_error_label.value = "$\\textbf{" + "{}".format(error) + "}$"

    def update(self):
        """
        This function is used to update any information displayed by the user interface.
        """

        self.__lock.acquire()
        self.__unregister_callback()

        # Section: "Month Selection"
        # ========================================= #
        self._widget_month_checkbox.value = self.__application_options.month_filter_enabled

        self._widget_month_combobox.value = self.__application_options.month_name
        self._widget_month_combobox.disabled = not self.__application_options.month_filter_enabled

        # Section: "State Selection"
        # ========================================= #
        self._widgets_state_for_comparison_combobox.options = self.__current_selected_dataset.get_state_list()
        self._widgets_state_list_comparison_select.options = self.__application_options.states

        # Section: "Time Range Selection"
        # ========================================= #
        self._widget_time_int_range_slider.max = self.__application_options.available_time_range_as_years[1]
        self._widget_time_int_range_slider.min = self.__application_options.available_time_range_as_years[0]
        self._widget_time_int_range_slider.value = self.__application_options.plot_time_range_as_years

        # Section: "Active Column Selection"
        # ========================================= #
        self._widget_active_columns_select.options = self.__application_options.available_columns
        self._widget_active_columns_select.value = self.__application_options.active_columns[0]

        self.__register_callback()
        self.__lock.release()

    # Callbacks...
    # ================================================================================================================ #
    @staticmethod
    def __is_widget_value_changed(change):
        return change['type'] == 'change' and change['name'] == 'value'

    def _on_change_widget_month_combobox(self, change):
        if GUICommon.is_widget_value_changed(change):
            self.__application_options.month_name = change['new']

    def _on_change_widget_month_checkbox(self, change):
        if GUICommon.is_widget_value_changed(change):
            self.__application_options.month_filter_enabled = change['new']
            self._widget_month_combobox.disabled = not self.__application_options.month_filter_enabled

    def _on_change_widget_time_int_range_slider(self, change):
        if GUICommon.is_widget_value_changed(change):
            self.__application_options.plot_time_range_as_years = [change['new'][0], change['new'][1]]

    def _on_change_widget_active_columns_select(self, change):
        if GUICommon.is_widget_value_changed(change):
            self.__application_options.active_columns = [change['new']]

    def __register_callback(self):
        """
        Function used to register callbacks handlers
        """

        self._widget_month_combobox.observe(self._on_change_widget_month_combobox)
        self._widget_month_checkbox.observe(self._on_change_widget_month_checkbox)
        self._widget_time_int_range_slider.observe(self._on_change_widget_time_int_range_slider)
        self._widget_active_columns_select.observe(self._on_change_widget_active_columns_select)

    def __unregister_callback(self):
        """
        Function used to unregister callbacks handlers
        """

        self._widget_month_combobox.unobserve(self._on_change_widget_month_combobox)
        self._widget_month_checkbox.unobserve(self._on_change_widget_month_checkbox)
        self._widget_time_int_range_slider.unobserve(self._on_change_widget_time_int_range_slider)
        self._widget_active_columns_select.unobserve(self._on_change_widget_active_columns_select)
