import threading

from src import Common
from src.Application import Application
from src.GUI.GUICommon import GUICommon
from src.GUI.GUIPlot import GUIPlot
from src.GUI.RestAPI.StateFlagUrlRegistry import StateFlagUrlRegistry
from src.TimeSeriesDataset.TimeSeriesDatasetGlobalClimateChange import TimeSeriesDatasetGlobalClimateChange


class GUIPlotController(GUIPlot):
    """
    This class is used as controller for all 'ipywidgets widget' inside 'GUIPlot' class.
    """

    def __init__(self, application):
        super().__init__()

        if application is None:
            raise ValueError("[ERROR]: 'application' cannot be 'None'!")

        if type(application) is not Application:
            raise TypeError("[ERROR]: 'application' must be 'Application' type!")

        self.__application = application
        self.__application_options = None
        self.__state_flag_url_registry = StateFlagUrlRegistry()
        self.__lock = threading.Lock()

    def display(self):
        self.update()
        self._widget_plot_button.on_click(self.plot_event)

        super(GUIPlotController, self).display()

    def plot_event(self, button):
        """
        This function is used to perform the plot of data according to user specified options.
        """

        self._widget_error_label.value = ""
        self.display()

        try:
            dataset = self.__application.get_current_selected_dataset()
            options = self.__application.get_current_application_options()

            # Get filter data...
            # ========================================= #
            data = dataset.get_filtered_data(options.month_name,
                                             options.month_filter_enabled,
                                             options.city,
                                             options.state,
                                             options.plot_time_range_as_years,
                                             options.active_columns)

            # Following is used to prevent some errors...
            # ========================================= #
            if (len(data)) == 1:
                raise ValueError("[ERROR]: Nothing to plot; only 1 record of data!!")

            # If required, calc regression line...
            # ========================================= #
            if options.display_univariate_regression_line:

                univariate_regression_line = TimeSeriesDatasetGlobalClimateChange.compute_univariate_regression_line(
                    data)

                data['Regression Line'] = univariate_regression_line.get_fitted_values_y()

                self._widget_univariate_regression_line_info_HTMLMath.description = "Univariate Regression Line Info"
                self._widget_univariate_regression_line_info_HTMLMath.value = \
                    "<ul>" \
                    "<li>$\\alpha \\text{ (Intercept) = }" + "{}$</li>".format(
                        univariate_regression_line.get_intercept()) + \
                    "<li>$\\beta \\text{ (Slope) = }" + "{}$</li>".format(univariate_regression_line.get_slope()) + \
                    "<li>$R^2 \\text{ = }" + "{}$</li></ul>".format(
                        univariate_regression_line.get_coefficient_of_determination())
            else:
                self._widget_univariate_regression_line_info_HTMLMath.value = ""
                self._widget_univariate_regression_line_info_HTMLMath.description = ""

            # Make plot title...
            # ========================================= #
            plot_title = "Plot '{}' ".format(dataset.get_name())
            if options.month_filter_enabled:
                plot_title += "- {} ".format(options.month_name)
            else:
                plot_title += "- Every Month "

            if dataset.get_city_list() is not None:
                plot_title += "- {} ".format(options.city)

            if dataset.get_state_list() is not None:
                plot_title += "({})".format(options.state)

            # Make plot title...
            # ========================================= #
            Common.plot(data, plot_title)

        except ValueError as error:
            self._widget_error_label.value = "$\\textbf{" + "{}".format(error) + "}$"
            self._widget_univariate_regression_line_info_HTMLMath.value = ""
            self._widget_univariate_regression_line_info_HTMLMath.description = ""

    def update(self):
        """
        This function is used to update any information displayed by the user interface.
        """

        self.__lock.acquire()
        self.__unregister_callback()

        self.__application_options = self.__application.get_current_application_options()
        current_selected_dataset = self.__application.get_current_selected_dataset()

        # Disable following to prevent some errors and hang...
        self._widget_city_combobox.disabled = True
        self._widget_state_combobox.disabled = True

        # Section: "Dataset File Selection"
        # ============================================================================================================ #
        self._widget_dataset_file_select.options = self.__application.get_available_dataset_names()
        self._widget_dataset_file_select.value = current_selected_dataset.get_name()

        # Section: "Month Selection"
        # ============================================================================================================ #
        self._widget_month_checkbox.value = self.__application_options.month_filter_enabled

        self._widget_month_combobox.value = self.__application_options.month_name
        self._widget_month_combobox.disabled = not self.__application_options.month_filter_enabled

        # Section: "City and State Selection"
        # ============================================================================================================ #
        self._widget_state_combobox.value = self.__application_options.state
        self._widget_city_combobox.value = self.__application_options.city

        # STATE...
        # ========================================= #
        state_list = current_selected_dataset.get_state_list()

        if state_list is None:
            self._widget_state_combobox.disabled = True
            self._widget_states_summary_label.value = "No $\\textbf{State}$ inside selected dataset!"
        else:
            self._widget_state_combobox.disabled = False
            self._widget_state_combobox.options = state_list
            self._widget_states_summary_label.value = "This dataset contains ${}$ states!".format(len(state_list))

        # CITIES...
        # ========================================= #
        city_list = current_selected_dataset.get_city_list()
        city_list_inside_state = current_selected_dataset.get_city_list_belonging_to_state(
            self.__application_options.state)

        if city_list is None:
            self._widget_city_combobox.disabled = True
            self._widget_cities_summary_label.value = "No $\\textbf{City}$ inside selected dataset!"
        else:
            self._widget_city_combobox.disabled = False
            self._widget_city_combobox.options = city_list
            self._widget_cities_summary_label.value = "This dataset contains ${}$ cities!".format(len(city_list))

            if city_list_inside_state is not None:
                self._widget_city_combobox.options = city_list_inside_state

        # HOW MANY CITIES INSIDE SELECT STATE...
        # ========================================= #
        if city_list_inside_state is None:
            self._widget_how_many_cities_inside_state_label.value = ""
        else:
            bold_string_state = "$\\textbf{" + "{}".format(self.__application_options.state) + "}$"

            self._widget_how_many_cities_inside_state_label.value = "In this dataset, ${}$ cities belong to {}!".format(
                len(city_list_inside_state),
                bold_string_state)

        # FLAG...
        # ========================================= #
        self._widget_state_flag_image_HTML.value = '<svg width="100" height="50" style="border:2px solid black"><rect width="100" height="50" style="fill:rgb(255,255,255)" /></svg>'

        if state_list is not None and self.__application_options.state in state_list:

            url = self.__state_flag_url_registry.get(self.__application_options.state)
            if url is not None:
                self._widget_state_flag_image_HTML.value = '<image src="{}" style="border:2px solid black; width:90px">'.format(
                    url)

        # Section: "Time Range Selection"
        # ============================================================================================================ #
        self._widget_time_int_range_slider.max = self.__application_options.available_time_range_as_years[1]
        self._widget_time_int_range_slider.min = self.__application_options.available_time_range_as_years[0]
        self._widget_time_int_range_slider.value = self.__application_options.plot_time_range_as_years

        # Section: "Active Column Selection"
        # ============================================================================================================ #
        self._widget_active_columns_select_multiple.options = self.__application_options.available_columns
        self._widget_active_columns_select_multiple.value = self.__application_options.active_columns

        # Section: "Univariate Regression Line"
        # ============================================================================================================ #
        self._widget_display_univariate_regression_line_checkbox.value = self.__application_options.display_univariate_regression_line

        self.__register_callback()
        self.__lock.release()

    # Callbacks...
    # ================================================================================================================ #
    def __on_change_widget_dataset_file_select(self, change):
        if GUICommon.is_widget_value_changed(change):
            self.__application.set_current_selected_dataset(change['new'])
            self.update()

    def _on_change_widget_month_combobox(self, change):
        if GUICommon.is_widget_value_changed(change):
            self.__application_options.month_name = change['new']

    def _on_change_widget_month_checkbox(self, change):
        if GUICommon.is_widget_value_changed(change):
            self.__application_options.month_filter_enabled = change['new']
            self._widget_month_combobox.disabled = not self.__application_options.month_filter_enabled

    def _on_change_widget_state_combobox(self, change):
        if GUICommon.is_widget_value_changed(change):
            self.__application_options.state = change['new']
            self.update()

    def _on_change_widget_city_combobox(self, change):

        if GUICommon.is_widget_value_changed(change):
            self.__application_options.city = change['new']

            state = self.__application.get_current_selected_dataset().get_state_of_city(change['new'])
            if state is not None:
                self.__application_options.state = state

            self.update()

    def _on_change_widget_time_int_range_slider(self, change):
        if GUICommon.is_widget_value_changed(change):
            self.__application_options.plot_time_range_as_years = [change['new'][0], change['new'][1]]

    def _on_change_widget_active_columns_select_multiple(self, change):
        if GUICommon.is_widget_value_changed(change):

            output = list()
            for x in change['new']:
                output.append(x)

            self.__application_options.active_columns = output

    def _on_change_widget_display_univariate_regression_line_checkbox(self, change):
        if GUICommon.is_widget_value_changed(change):
            self.__application_options.display_univariate_regression_line = change['new']

    def __register_callback(self):
        """
        Function used to register callbacks handlers
        """

        self._widget_dataset_file_select.observe(self.__on_change_widget_dataset_file_select)
        self._widget_month_combobox.observe(self._on_change_widget_month_combobox)
        self._widget_month_checkbox.observe(self._on_change_widget_month_checkbox)
        self._widget_city_combobox.observe(self._on_change_widget_city_combobox)
        self._widget_state_combobox.observe(self._on_change_widget_state_combobox)
        self._widget_time_int_range_slider.observe(self._on_change_widget_time_int_range_slider)
        self._widget_active_columns_select_multiple.observe(self._on_change_widget_active_columns_select_multiple)
        self._widget_display_univariate_regression_line_checkbox.observe(
            self._on_change_widget_display_univariate_regression_line_checkbox)

    def __unregister_callback(self):
        """
        Function used to unregister callbacks handlers
        """

        self._widget_dataset_file_select.unobserve(self.__on_change_widget_dataset_file_select)
        self._widget_month_combobox.unobserve(self._on_change_widget_month_combobox)
        self._widget_month_checkbox.unobserve(self._on_change_widget_month_checkbox)
        self._widget_city_combobox.unobserve(self._on_change_widget_city_combobox)
        self._widget_state_combobox.unobserve(self._on_change_widget_state_combobox)
        self._widget_time_int_range_slider.unobserve(self._on_change_widget_time_int_range_slider)
        self._widget_active_columns_select_multiple.unobserve(self._on_change_widget_active_columns_select_multiple)
        self._widget_display_univariate_regression_line_checkbox.unobserve(
            self._on_change_widget_display_univariate_regression_line_checkbox)
