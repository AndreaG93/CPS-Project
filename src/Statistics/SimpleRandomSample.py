class SimpleRandomSample(object):
    """
    This class represents a 'Simple Random Sample' X_1,X_2...,X_n
    """

    def __init__(self, observations):

        if not isinstance(observations, list):
            raise ValueError("[ERROR]: 'observations' must be a 'list' type object!")

        self.__observations = observations
        self.__size = len(observations)

        self.__mean = None
        self.__unbiased_variance = None

    def get_mean(self):
        """
        This function is used to get x^=_n(X), that is the sample mean of size n drawn from X
        """
        if self.__mean is None:

            summation = 0
            for value in self.__observations:
                summation += value

            self.__mean = summation / self.__size

        return self.__mean

    def get_unbiased_variance(self):
        """
        This function is used to calc S^2_n(X), that is the unbiased sample variance of size n drawn from X
        """
        if self.__unbiased_variance is None:

            summation = 0
            for value in self.__observations:
                summation += (value - self.__mean) ** 2

            self.__unbiased_variance = summation / (self.__size - 1)

        return self.__unbiased_variance

    def get_size(self):
        return self.__size

    def get_observations(self):
        return self.__observations

    @staticmethod
    def calc_sample_covariance(sample_1, sample_2):
        """
        This function is used to calc S_n(X,Y), that is the sample covariance of size n drawn from X and Y
        """
        if not isinstance(sample_1, SimpleRandomSample) or not isinstance(sample_2, SimpleRandomSample):
            raise ValueError("[ERROR]: 'sample_1' and 'sample_2' must be both 'SimpleRandomSample' type objects!")

        if sample_1.get_size() != sample_2.get_size():
            raise ValueError(
                "[ERROR]: 'sample_1' and 'sample_2' must be equal size! ( {} != {} )".format(sample_1.get_size(),
                                                                                             sample_2.get_size()))

        observations_sample_1 = sample_1.get_observations()
        observations_sample_2 = sample_2.get_observations()

        sample_mean_1 = sample_1.get_mean()
        sample_mean_2 = sample_2.get_mean()

        size = sample_1.get_size()

        output = 0
        for k in range(0, size):
            output = output + ((observations_sample_1[k] - sample_mean_1) * (observations_sample_2[k] - sample_mean_2))

        return output / (size - 1)
