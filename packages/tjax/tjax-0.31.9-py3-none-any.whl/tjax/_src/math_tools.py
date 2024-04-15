from __future__ import annotations

from typing import cast

from array_api_compat import get_namespace

from .annotations import BooleanArray, ComplexArray, IntegralArray, RealArray


def abs_square(x: ComplexArray) -> RealArray:
    xp = get_namespace(x)
    return xp.square(x.real) + xp.square(x.imag)


# TODO: Remove this when the Array API has it with broadcasting under xp.linalg.norm.
def outer_product(x: RealArray, y: RealArray) -> RealArray:
    """Return the broadcasted outer product of a vector with itself.

    This is xp.einsum("...i,...j->...ij", x, y).
    """
    xp = get_namespace(x, y)
    xi = xp.reshape(x, (*x.shape, 1))
    yj = xp.reshape(y.conjugate(), (*y.shape[:-1], 1, y.shape[-1]))
    return xi * yj


def matrix_vector_mul(x: RealArray, y: RealArray) -> RealArray:
    """Return the matrix-vector product.

    This is xp.einsum("...ij,...j->...i", x, y).

    Note the speed difference:
    * 14.3 µs: xp.vecdot(matrix_vector_mul(m, x), x)
    * 4.44 µs: np.einsum("...i,...ij,...j->...", x, m, x)
    """  # noqa: RUF002
    xp = get_namespace(x, y)
    y = xp.reshape(y, (*y.shape[:-1], 1, y.shape[-1]))
    return xp.sum(x * y, axis=-1)


def matrix_dot_product(x: RealArray, y: RealArray) -> RealArray:
    """Return the "matrix dot product" of a matrix with the outer product of a vector.

    This equals:
    * 1.19 µs: xp.einsum("...ij,...ij", x, y)
    * 1.77 µs: xp.sum(x * y, axis=(-2, -1))
    # 3.87 µs: xp.linalg.trace(xp.moveaxis(x, -2, -1) @ y)
    """  # noqa: RUF002
    xp = get_namespace(x, y)
    return xp.sum(x * y, axis=(-2, -1))


def divide_where(dividend: ComplexArray,
                 divisor: ComplexArray | IntegralArray,
                 *,
                 where: BooleanArray | None = None,
                 otherwise: ComplexArray | None = None) -> ComplexArray:
    """Return the quotient or a special value when a condition is false.

    Returns: `xp.where(where, dividend / divisor, otherwise)`, but without evaluating
    `dividend / divisor` when `where` is false.  This prevents some exceptions.
    """
    if where is None:
        assert otherwise is None
        xp = get_namespace(dividend, divisor)
        return xp.true_divide(dividend, divisor)
    assert otherwise is not None
    xp = get_namespace(dividend, divisor, where, otherwise)
    dividend = xp.where(where, dividend, 1.0)
    divisor = xp.where(where, divisor, 1.0)
    quotient: ComplexArray = xp.true_divide(dividend, divisor)
    return xp.where(where, quotient, otherwise)


def divide_nonnegative(dividend: RealArray, divisor: RealArray) -> RealArray:
    """Quotient for use with positive reals that never returns NaN.

    Returns: The quotient assuming that the dividend and divisor are nonnegative, and infinite
    whenever the divisor equals zero.
    """
    xp = get_namespace(dividend, divisor)
    return cast(RealArray, divide_where(dividend, divisor, where=divisor > 0.0, otherwise=xp.inf))


# Remove when https://github.com/scipy/scipy/pull/18605 is released.
def softplus(x: RealArray) -> RealArray:
    xp = get_namespace(x)
    return xp.logaddexp(xp.asarray(0.0), x)


def inverse_softplus(y: RealArray) -> RealArray:
    xp = get_namespace(y)
    return xp.where(y > 80.0,  # noqa: PLR2004
                    y,
                    xp.log(xp.expm1(y)))


def leaky_integrate(value: ComplexArray,
                    time_step: RealArray,
                    drift: ComplexArray | None = None,
                    decay: ComplexArray | None = None,
                    *,
                    leaky_average: bool = False) -> ComplexArray:
    """Update the value so that it is the leaky integral (or leaky average).

    Args:
        value: The current value of the leaky integral or average.
        time_step: The number of seconds that have passed.
        decay: If provided, must have positive real component, and the value decays by exp(-decay)
            every second.
        drift: If provided, the value increases by this every second.
        leaky_average: A flag indicating a leaky average rather than a leaky integral.  This scales
            the drift by the real component (in case the decay is complex) of the decay.
    """
    if drift is None:
        if decay is None:
            return value
        xp = get_namespace(decay, time_step, value)
        return xp.exp(-decay * time_step) * value

    if decay is None:
        if leaky_average:
            raise ValueError
        xp = get_namespace(drift, time_step, value)
        return xp.asarray(value + drift * time_step)

    xp = get_namespace(drift, decay, time_step, value)
    scaled_integrand = (drift / decay) * -xp.expm1(-decay * time_step)

    if leaky_average:
        scaled_integrand *= decay.real

    return xp.exp(-decay * time_step) * value + scaled_integrand


def leaky_data_weight(iterations_times_time_step: RealArray | IntegralArray,
                      decay: RealArray
                      ) -> RealArray:
    """The amount of data that has been incorporated and has not been decayed.

    This equals leaky_integrate(0.0, iterations_times_time_step, 1.0, decay, leaky_average=True).
    """
    xp = get_namespace(iterations_times_time_step, decay)
    return -xp.expm1(-iterations_times_time_step * decay)
