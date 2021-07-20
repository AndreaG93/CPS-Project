import calendar
import ipywidgets
from IPython.core.display import clear_output, display


class GUIRegressionLineComparison(object):
    """
    This class is used to build and manage a very simple user interface using some interactive HTML widgets
    provided by 'ipywidgets' package.

    For reference please see: https://ipywidgets.readthedocs.io/en/latest/index.html#
    """

    def __init__(self):
        self._widget_list = list()

        self._widget_month_combobox = None
        self._widget_month_checkbox = None
        self._widget_active_columns_select = None
        self._widget_time_int_range_slider = None
        self._widget_error_label = None
        self._widgets_insert_state_comparison_list_button = None
        self._widgets_state_for_comparison_combobox = None
        self._widgets_remove_state_comparison_list_button = None
        self._widgets_state_list_comparison_select = None

        self._widget_compare_button = None

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

        # Section: "Plot Current Selected Dataset"
        # ============================================================================================================ #
        label = ipywidgets.Label(value="$\\textbf{•}$ $\\textbf{Current Selected Dataset}$: "
                                       + "$\\texttt{GlobalLandTemperaturesByCountry.csv}$ ")
        self._widget_list.append(label)

        # Section: "Plot Options"
        # ============================================================================================================ #
        label = ipywidgets.Label(value="$\\textbf{•}$ $\\textbf{Comparison Options}$")
        self._widget_list.append(label)

        label = ipywidgets.Label(
            value="You can customize your $\\textit{Comparison}$ using following $\\textit{Widgets}$")
        self._widget_list.append(label)

        self._widget_month_combobox = ipywidgets.Combobox(
            placeholder="Select/Type 'Month'...",
            options=calendar.month_name[1:],
            description='Month:',
            layout=ipywidgets.Layout(width='350px'),
            continuous_update=False
        )

        self._widget_month_checkbox = ipywidgets.Checkbox(
            description="Enable 'Month Filter'",
            layout=ipywidgets.Layout(width='350px')
        )

        grid = ipywidgets.GridspecLayout(1, 2)
        grid[0, 0] = self._widget_month_combobox
        grid[0, 1] = self._widget_month_checkbox

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

        self._widget_active_columns_select = ipywidgets.Select(
            rows=10,
            description='Active Column:',
            disabled=False,
            style={'description_width': 'initial'},
            layout=ipywidgets.Layout(width='90%'),
        )

        self._widget_list.append(self._widget_active_columns_select)

        # Section: "State Selection"
        # ============================================================================================================ #

        label = ipywidgets.Label(value="$\\textbf{•}$ $\\textbf{State Selection}$")
        self._widget_list.append(label)

        label = ipywidgets.Label(value="In order to compare regression lines, use the following combobox to select "
                                       " a $\\textit{State}$, then click on $\\textit{'Add State'}$ button to insert it "
                                       + "into the list below.")
        self._widget_list.append(label)
        label = ipywidgets.Label(
            value="We will compare regression lines of all $\\textit{States}$ that appear in that list!")
        self._widget_list.append(label)

        label = ipywidgets.Label(
            value="You can remove a $\\textit{States}$ selecting it and clicking $\\textit{'Remove State'}$ button!")
        self._widget_list.append(label)

        self._widgets_state_for_comparison_combobox = ipywidgets.Combobox(
            placeholder='Select a state...',
            layout=ipywidgets.Layout(width='500px'),
            continuous_update=False,
        )

        self._widgets_state_list_comparison_select = ipywidgets.Select(
            options=[],
            disabled=False,
            layout=ipywidgets.Layout(width='500px'),
            style={'description_width': 'initial'}
        )

        self._widgets_remove_state_comparison_list_button = ipywidgets.Button(
            description="Remove 'State'",
            disabled=False,
            button_style="danger",
            icon="minus"
        )

        self._widgets_insert_state_comparison_list_button = ipywidgets.Button(
            description="Add 'State'",
            disabled=False,
            button_style="success",
            icon="plus"
        )

        items = [self._widgets_insert_state_comparison_list_button, self._widgets_state_for_comparison_combobox,
                 self._widgets_remove_state_comparison_list_button, self._widgets_state_list_comparison_select]

        self._widget_list.append(ipywidgets.GridBox(items,
                                                    layout=ipywidgets.Layout(grid_template_columns="repeat(2, 170px)")))

        # Section: "Comparison Button"
        # ============================================================================================================ #
        label = ipywidgets.Label(value="$\\textbf{•}$ $\\textbf{Comparison Section}$")
        self._widget_list.append(label)
        self._widget_compare_button = ipywidgets.Button(description='Compare!',
                                                        disabled=False,
                                                        button_style='success',
                                                        icon='star')

        self._widget_list.append(self._widget_compare_button)

        # Section: "ERROR Label"
        # ============================================================================================================ #
        self._widget_error_label = ipywidgets.Label(value="")
        self._widget_list.append(self._widget_error_label)
