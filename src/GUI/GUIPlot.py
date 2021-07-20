import calendar
import ipywidgets
from IPython.core.display import clear_output, display


class GUIPlot(object):
    """
    This class is used to build and manage a very simple user interface using some interactive HTML widgets
    provided by 'ipywidgets' package.

    For reference please see: https://ipywidgets.readthedocs.io/en/latest/index.html#
    """

    def __init__(self):
        self._widget_list = list()

        self._widget_dataset_file_select = None
        self._widget_month_combobox = None
        self._widget_month_checkbox = None
        self._widget_states_summary_label = None
        self._widget_cities_summary_label = None
        self._widget_how_many_cities_inside_state_label = None
        self._widget_state_flag_image_HTML = None
        self._widget_state_combobox = None
        self._widget_city_combobox = None
        self._widget_active_columns_select_multiple = None
        self._widget_time_int_range_slider = None
        self._widget_error_label = None
        self._widget_plot_button = None
        self._widget_display_univariate_regression_line_checkbox = None
        self._widget_univariate_regression_line_info_HTMLMath = None

        self.__build()

    def display(self):
        """
        This function is used to display all widgets of the UI.
        """
        clear_output()
        display(ipywidgets.VBox(self._widget_list))

    def __build(self):
        """
        This function is used to build all widgets of the UI.
        """

        # Section: "Dataset Selection"
        # ============================================================================================================ #
        label = ipywidgets.Label(value="$\\textbf{•}$ $\\textbf{Dataset Selection}$")
        self._widget_list.append(label)
        label = ipywidgets.Label(value="Please, select a $\\texttt{.csv}$ file from the following list."
                                       + " (Only $\\texttt{.csv}$ files stored inside $\\texttt{./data}$ directory are"
                                       + " displayed).")

        self._widget_dataset_file_select = ipywidgets.Select(
            description="Current Selected Dataset:",
            style={'description_width': 'initial'},
            layout=ipywidgets.Layout(width='90%'),
            continuous_update=False
        )

        self._widget_list.append(ipywidgets.VBox([label, self._widget_dataset_file_select]))

        # Section: "Plot Options"
        # ============================================================================================================ #
        label = ipywidgets.Label(value="$\\textbf{•}$ $\\textbf{Plot Options}$")
        self._widget_list.append(label)
        label = ipywidgets.Label(value="You can customize your $\\textit{Plot}$ using following $\\textit{Widgets}$ " +
                                       "(Available $\\textit{Widgets}$ depend on $\\textit{Current Selected Dataset}$)")
        self._widget_list.append(label)

        self._widget_month_combobox = ipywidgets.Combobox(
            placeholder="Select/Type 'Month'...",
            options=calendar.month_name[1:],
            description='Month:',
            layout=ipywidgets.Layout(width='350px'),
            continuous_update=False
        )

        self._widget_state_combobox = ipywidgets.Combobox(
            placeholder="Select/Type 'State'...",
            description='State:',
            layout=ipywidgets.Layout(width='350px'),
            continuous_update=False
        )

        self._widget_city_combobox = ipywidgets.Combobox(
            placeholder="Select/Type 'City'...",
            description='City:',
            layout=ipywidgets.Layout(width='350px'),
            continuous_update=False,
        )

        self._widget_month_checkbox = ipywidgets.Checkbox(
            description="Enable 'Month Filter'",
            layout=ipywidgets.Layout(width='350px')
        )

        self._widget_display_univariate_regression_line_checkbox = ipywidgets.Checkbox(
            description="Plot 'Regression Line'",
            layout=ipywidgets.Layout(width='350px')
        )

        grid = ipywidgets.GridspecLayout(3, 2)
        grid[0, 0] = self._widget_month_combobox
        grid[1, 0] = self._widget_state_combobox
        grid[2, 0] = self._widget_city_combobox

        grid[0, 1] = self._widget_month_checkbox
        grid[1, 1] = self._widget_display_univariate_regression_line_checkbox

        self._widget_list.append(grid)

        self._widget_time_int_range_slider = ipywidgets.IntRangeSlider(
            step=1,
            description="Plot's 'Time Range'",
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='d',
            style={'description_width': 'initial'},
            layout=ipywidgets.Layout(width='90%'),
        )

        self._widget_list.append(self._widget_time_int_range_slider)

        label = ipywidgets.Label(value="Using following $\\textit{Widget}$, you can select one or more "
                                       + "$\\textit{fields}$ to customize your $\\textit{Plot}$"
                                       + " (Hold $\\texttt{CTRL}$ and click to select more $\\textit{fields}$!)")

        self._widget_list.append(label)

        self._widget_active_columns_select_multiple = ipywidgets.SelectMultiple(
            rows=10,
            description='Active Columns:',
            disabled=False,
            style={'description_width': 'initial'},
            layout=ipywidgets.Layout(width='90%'),
        )

        self._widget_list.append(self._widget_active_columns_select_multiple)

        # Section 'Dataset Indo'
        # ============================================================================================================ #
        label = ipywidgets.Label(value="$\\textbf{•}$ $\\textbf{Dataset Info}$")
        self._widget_list.append(label)
        label = ipywidgets.Label(value="Here are displayed several info about $\\textit{Current Selected Dataset}$ "
                                       + "(Displayed data depend on current selected $\\textit{Plot Options}$)")
        self._widget_list.append(label)

        self._widget_states_summary_label = ipywidgets.Label()
        self._widget_cities_summary_label = ipywidgets.Label()
        self._widget_how_many_cities_inside_state_label = ipywidgets.Label()
        self._widget_state_flag_image_HTML = ipywidgets.HTML()

        box = ipywidgets.VBox([self._widget_states_summary_label,
                               self._widget_cities_summary_label,
                               self._widget_how_many_cities_inside_state_label])

        box = ipywidgets.HBox([self._widget_state_flag_image_HTML, box])

        self._widget_list.append(box)

        # Section: "Plot Button"
        # ============================================================================================================ #
        label = ipywidgets.Label(value="$\\textbf{•}$ $\\textbf{Plot Section}$")
        self._widget_list.append(label)
        self._widget_plot_button = ipywidgets.Button(description='Plot',
                                                     disabled=False,
                                                     button_style='success',
                                                     icon='line-chart')

        self._widget_list.append(self._widget_plot_button)

        # Section: "ERROR Label"
        # ============================================================================================================ #
        self._widget_error_label = ipywidgets.Label(value="")
        self._widget_list.append(self._widget_error_label)

        # Section: "Display Univariate Regression Line"
        # ============================================================================================================ #
        self._widget_univariate_regression_line_info_HTMLMath = ipywidgets.HTMLMath(
            value="",
            style={'description_width': 'initial'},
        )
        self._widget_list.append(self._widget_univariate_regression_line_info_HTMLMath)
