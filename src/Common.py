import os

import matplotlib


def list_files(path, extension):
    """
    This function is used to list all files having specified extension inside a given path.

    :param path:
    :param extension:
    :return:
    """
    if not isinstance(path, str):
        raise TypeError("[ERROR]: 'path' must be 'str' type.")

    if not isinstance(extension, str):
        raise TypeError("[ERROR]: 'extension' must be 'str' type.")

    if not os.path.exists(path):
        raise FileNotFoundError("[ERROR]: '{}' directory does not exist.".format(path))

    output = list()

    for file in os.listdir(path):
        if file.endswith(extension):
            output.append("{}/{}".format(path, file))

    return output


def plot(data, plot_title):
    """
    This function is used to plot
    """

    # Following statement is used to avoid following error:
    # OverflowError: Exceeded cell block limit (set 'agg.path.chunksize' rcparam)
    # ========================================= #
    matplotlib.rcParams['agg.path.chunksize'] = 100000

    # Plot...
    # ========================================= #
    data.plot(title=plot_title,
              figsize=(16, 9),
              grid=True,
              legend=True)
