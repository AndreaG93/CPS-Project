from src.Statistics.SimpleRandomSample import *


class UnivariateRegressionLine(object):
    """
    This class is used to compute an univariate regression line
    """

    def __init__(self, name, sample_x, sample_y):

        self.__name = name

        if not isinstance(sample_x, SimpleRandomSample) or not isinstance(sample_y, SimpleRandomSample):
            raise ValueError("[ERROR]: 'sample_x' and 'sample_y' must be both 'SimpleRandomSample' type objects!")

        if sample_x.get_size() != sample_y.get_size():
            raise ValueError("[ERROR]: 'sample_x' and 'sample_y' must be equal size!")

        self.sample_x = sample_x
        self.sample_y = sample_y

        self.__slope = None
        self.__intercept = None
        self.__fitted_values_y = None
        self.__tss = 0
        self.__ess = 0
        self.__coefficient_of_determination = 0
        self.__sse = 0

        # Calc all information about current univariate regression line
        self.__calc_slope_and_intercept()
        self.__calc_fitted_values()
        self.__calc_tss()
        self.__calc_ess()
        self.__calc_coefficient_of_determination()

    def __calc_slope_and_intercept(self):
        """
        This function is used to calc the 'slope' and the 'intercept'
        """
        sample_covariance = SimpleRandomSample.calc_sample_covariance(self.sample_x, self.sample_y)

        self.__slope = sample_covariance / self.sample_x.get_unbiased_variance()
        self.__intercept = self.sample_y.get_mean() - self.__slope * self.sample_x.get_mean()

    def __calc_fitted_values(self):
        """
        This function is used to calc the fitted values of the dependent variable Y
        """
        self.__fitted_values_y = list()
        for value in self.sample_x.get_observations():
            self.__fitted_values_y.append(self.__intercept + self.__slope * value)

    def __calc_tss(self):
        """
        This function is used to calc TSS, that is the Total Sum of Squares
        """
        for value in self.sample_y.get_observations():
            self.__tss += (value - self.sample_y.get_mean()) ** 2

    def __calc_ess(self):
        """
        This function is used to calc ESS, that is the Explained Sum of Squares
        """
        for value in self.__fitted_values_y:
            self.__ess += (value - self.sample_y.get_mean()) ** 2

    def __calc_coefficient_of_determination(self):
        """
        This function is used to calc the coefficient of determination, also known as R^2
        """
        self.__coefficient_of_determination = self.__ess / self.__tss

    def get_slope(self):
        return self.__slope

    def get_intercept(self):
        return self.__intercept

    def get_tss(self):
        return self.__tss

    def get_ess(self):
        return self.__ess

    def get_coefficient_of_determination(self):
        return self.__coefficient_of_determination

    def get_fitted_values_y(self):
        return self.__fitted_values_y

    def get_sse(self):
        return self.__sse

    def get_name(self):
        return self.__name

    @staticmethod
    def rank_regression_lines(lines):
        """
        Function used to rank specified regression lines according to R^2 values.
        """

        # Sort...
        lines.sort(key=lambda x: x.get_coefficient_of_determination())
        lines.reverse()

        rank = 1
        for regression_line in lines:
            print("{}° {:<25}  R^2: {}".format(rank,
                                               regression_line.get_name().upper(),
                                               regression_line.get_coefficient_of_determination(),
                                               ))
            rank += 1

        worst_state = lines[len(lines) - 1].get_name()
        print("\n{} has the WORST regression line!".format(worst_state.upper()))
