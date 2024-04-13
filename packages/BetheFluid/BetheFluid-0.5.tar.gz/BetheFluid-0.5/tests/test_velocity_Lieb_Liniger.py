import numpy as np
import pickle

import BetheFluid


# testing correct calculations of effective velocity

def rho0(l, x):
    rho = 1 / (1 + np.exp(x[np.newaxis, :] ** 2 * (l[:, np.newaxis] ** 2 - 1))) / (2 * np.pi)

    return rho

mu_max = 4
mu_num = 100

x = np.array([1, 2])
l, int_l = np.linspace(-mu_max, mu_max, num=mu_num, endpoint=False, retstep=True)
c = 2
rho_A = rho0(l, x)



def test_calculate_velocity():
    # Arrange
    instance = (BetheFluid.models.calc_Lieb_Liniger.VelocityLiebLiniger(rho_A, l, c))

    result = instance.V

    with open('./tests/velocity_Lieb_Liniger.pkl', 'rb') as file:

        expected_value = pickle.load(file)

    tolerance = 1e-5

    assert np.allclose(result, expected_value, atol=tolerance)

