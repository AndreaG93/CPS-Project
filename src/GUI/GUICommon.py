class GUICommon(object):

    @staticmethod
    def is_widget_value_changed(change):
        """
        This function is used to check if the 'value' of a 'ipywidgets widget' is been changed
        """
        return change['type'] == 'change' and change['name'] == 'value'
