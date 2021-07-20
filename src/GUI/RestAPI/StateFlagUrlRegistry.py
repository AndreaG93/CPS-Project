import requests
import json


class StateFlagUrlRegistry(object):
    """
    Exploiting 'Registry Design Pattern', this class is used to manage URLs that contain a state's flag image.
    """

    def __init__(self):
        self.__registry = dict()

    def get(self, state_name):
        """
        This function is used to get an SVG file representing a state's flag.

        :param state_name:
        :return:
        """

        if type(state_name) is not str or state_name is None:
            raise TypeError("[ERROR]: 'state_name' must be 'str' type.")

        if state_name == "":
            return None

        output = self.__registry.get(state_name)

        if output is None:
            output = StateFlagUrlRegistry.__get_url_from_rest_api(state_name)
            self.__registry[state_name] = output

        return output

    @staticmethod
    def __get_url_from_rest_api(state_name):
        """
        This function is used to download, exploiting REST API, an SVG file representing a state's flag.

        :param state_name:
        :return:
        """
        output = None
        url = "https://restcountries.eu/rest/v2/name/{}".format(state_name)
        try:
            connection = requests.get(url)

            if connection.status_code == 200:
                json_data = connection.text
                dict_data = json.loads(json_data)

                output = dict_data[0]["flag"]
        except Exception as error:
            print("[ERROR] {}".format(error))
            output = None

        return output
