from DataReader.constant import Constant
import numpy as np

class Processor:
    def linear_regression(self, data):

        number_of_data = len(data)

        sum_x = 0
        sum_y = 0
        sum_x_y = 0
        sum_x_square = 0

        for i in range(number_of_data):
            x = number_of_data - i
            y = data[i]
            sum_x += x
            sum_y += y
            sum_x_y += x*y
            sum_x_square += x*x

        x_average = sum_x / number_of_data
        y_average = sum_y / number_of_data

        slope = (sum_x_y - (sum_y * sum_x) / number_of_data) / (sum_x_square - sum_x * sum_x / number_of_data)
        y_intercept = y_average - slope * x_average

        unbiased_estimator = 0
        s_x_x = 0

        for i in range(number_of_data):
            x = number_of_data - i
            y = data[i]
            y_estimator = slope * x + y_intercept
            delta_y = y - y_estimator
            x_from_average = x - x_average
            unbiased_estimator += delta_y * delta_y / (number_of_data - 2)
            s_x_x += x_from_average * x_from_average
        
        t_score_1 = Constant.T_DISTRIBUTION_1
        t_score_2 = Constant.T_DISTRIBUTION_2

        delta_slope_no_score = np.sqrt(unbiased_estimator / s_x_x)
        delta_slope_1 = t_score_1 * delta_slope_no_score
        delta_slope_2 = t_score_2 * delta_slope_no_score

        delta_y_intercept_no_score = np.sqrt(unbiased_estimator * (1 / number_of_data + x_average * x_average / s_x_x))
        delta_y_intercept_1 = t_score_1 * delta_y_intercept_no_score
        delta_y_intercept_2 = t_score_2 * delta_y_intercept_no_score

        result = {
            'below-1': {'slope': self.round005(slope - delta_slope_1), 'y-intercept': self.round005(y_intercept - delta_y_intercept_1)},
            'line-1': {'slope': self.round005(slope), 'y-intercept': self.round005(y_intercept)},
            'above-1': {'slope': self.round005(slope + delta_slope_1), 'y-intercept': self.round005(y_intercept + delta_y_intercept_1)},
            'below-2': {'slope': self.round005(slope - delta_slope_2), 'y-intercept': self.round005(y_intercept - delta_y_intercept_2)},
            'line-2': {'slope': self.round005(slope), 'y-intercept': self.round005(y_intercept)},
            'above-2': {'slope': self.round005(slope + delta_slope_2), 'y-intercept': self.round005(y_intercept + delta_y_intercept_2)}
        }

        result['point_must_sell'] = self.round05(result['above-2']['slope'] * Constant.DAY_ESTIMATE + result['above-2']['y-intercept'])
        result['point_should_sell'] = self.round05(result['above-1']['slope'] * Constant.DAY_ESTIMATE + result['above-1']['y-intercept'])
        result['point_must_buy'] = self.round05(result['below-2']['slope'] * Constant.DAY_ESTIMATE + result['below-2']['y-intercept'])
        result['point_should_buy'] = self.round05(result['below-1']['slope'] * Constant.DAY_ESTIMATE + result['below-1']['y-intercept'])
        result['point_estimate'] = self.round05(result['line-1']['slope'] * Constant.DAY_ESTIMATE + result['line-1']['y-intercept'])

        return result

    def round05(self, number):
        return (round(number * 20) / 20)

    def round005(self, number):
        return round(number, 3)