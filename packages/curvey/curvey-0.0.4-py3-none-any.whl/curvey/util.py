from __future__ import annotations

from typing import Callable, Literal, overload

import scipy
from matplotlib import pyplot as plt
from numpy import arctan2, array, concatenate, cos, cross, eye, ndarray, sin, stack


def angle_to_points(theta: ndarray) -> ndarray:
    return stack([cos(theta), sin(theta)], axis=1)


def rotation_matrix(theta: float) -> ndarray:
    """A 2x2 rotation matrix"""
    cos_theta, sin_theta = cos(theta), sin(theta)
    return array([[cos_theta, -sin_theta], [sin_theta, cos_theta]])


def reflection_matrix(theta: float) -> ndarray:
    """A 2x2 reflection matrix"""
    cos_2theta, sin_2theta = cos(2 * theta), sin(2 * theta)
    return array([[cos_2theta, sin_2theta], [sin_2theta, -cos_2theta]])


@overload
def align_edges(
    src_pts: ndarray,
    src_edges: ndarray,
    tgt_pts: ndarray,
    tgt_edges: ndarray,
    return_transform: Literal[True],
) -> ndarray: ...


@overload
def align_edges(
    src_pts: ndarray,
    src_edges: ndarray,
    tgt_pts: ndarray,
    tgt_edges: ndarray,
    return_transform: Literal[False],
) -> ndarray: ...


@overload
def align_edges(
    src_pts: ndarray,
    src_edges: ndarray,
    tgt_pts: ndarray,
    tgt_edges: ndarray,
    return_transform: bool,
) -> ndarray: ...


def align_edges(
    src_pts: ndarray,
    src_edges: ndarray,
    tgt_pts: ndarray,
    tgt_edges: ndarray,
    return_transform: bool = False,
) -> ndarray:
    """Calulate mean change in angle and position between two curves

    Parameters
    ----------
    src_pts
        `(n, 2)` source vertex coordinates.

    tgt_pts
        `(n, 2)` target vertex coordinates.

    src_edges
        `(n, 2)` source edge vectors.

    tgt_edges
        `(n, 2)` target edge vectors.

    return_transform
        If True, return a 3x3 transformation matrix. Otherwise, return the transformed points.

    """
    # Calculate the mean angle between source and target edge vectors
    # Because these are unnormalized, larger edges are weighted more heavily
    cos_theta = (src_edges * tgt_edges).sum()
    sin_theta = cross(src_edges, tgt_edges).sum()
    theta = arctan2(sin_theta, cos_theta)
    # NB negative sign here bc we're post-multipying, equiv. to transposing the rot matrix
    pts = src_pts @ rotation_matrix(-theta)
    # AFTER applying the rotation, check mean change in vertex position
    offset = (tgt_pts - pts).mean(axis=0, keepdims=True)

    if return_transform:
        transform = eye(3)
        transform[:2, :2] = rotation_matrix(theta)
        transform[:2, 2] = offset
        return transform

    return pts + offset


InterpType = Literal["linear", "cubic", "pchip"]


def _periodic_interp1d(x: ndarray, f: ndarray) -> Callable[[ndarray], ndarray]:
    from scipy.interpolate import interp1d

    if x[0] != 0:
        msg = "x[0] must == 0"
        raise NotImplementedError(msg)
    if len(x) != (len(f) + 1):
        msg = "len(x) must == len(f) + 1"
        raise NotImplementedError(msg)

    f = concatenate([f, f[[0]]])
    fitted = interp1d(x, f, kind="linear", assume_sorted=True, axis=0)

    def _periodic_wrapper(xi: ndarray) -> ndarray:
        return fitted(xi % x[-1])

    return _periodic_wrapper


def _periodic_pchip(x: ndarray, f: ndarray) -> Callable[[ndarray], ndarray]:
    from scipy.interpolate import PchipInterpolator

    if x[0] != 0:
        msg = "x[0] must == 0"
        raise NotImplementedError(msg)
    if len(x) != (len(f) + 1):
        msg = "len(x) must == len(f) + 1"
        raise NotImplementedError(msg)

    # let m = len(x) - 2

    # x is (x0, x1, ..., xm, xL)
    # f is (f0, f1, fm)

    x = concatenate(
        [
            # [x[-3] - x[-1]],
            [x[-2] - x[-1]],  # negative; one before the first element, i.e. (xm -xL)
            x,  # (0, x1, x2, ..., xm, xL)
            [x[-1] + x[1]],  # > L; one past the last element (f[L] = f[0])
            # [x[-1] + x[2]],
        ]
    )

    # n.b. f is one element shorter than x so need an extra pad here
    f = concatenate(
        [
            # f[[-2]],
            f[[-1]],
            f,  # f(0), f(x1), f(x2), ..., f(x_n)
            f[[0]],  # f(L)
            f[[1]],  # f(L + x1)
            # f[[2]],
        ]
    )

    pchip = PchipInterpolator(x, f, extrapolate=False)

    def _periodic_wrapper(xi: ndarray) -> ndarray:
        return pchip(xi % x[-1])

    return _periodic_wrapper


def periodic_interpolator(
    x: ndarray,
    f: ndarray,
    typ: InterpType | str = "cubic",
) -> Callable[[ndarray], ndarray]:
    """Construct a periodic interpolator of the function f(x)

    Parameters
    ----------
    x
        `(n + 1,)` array of independent variable values.

    f
        `(n,)` or `(n, ndim)` array of function values.
        `f(x[-1])` is assumed equal to `f(x[0])`.

    typ
        The type of interpolator. One of

        - 'linear' for linear interpolation via `scipy.interpolate.interp1d`
        - `cubic` for cubic spline interpolation via `scipy.interpolate.CubicSpline`
        - 'pchip`
            - for piecewise cubic hermite interpolating polynomial via
            `scipy.interpolate.PchipInterpolator`.

    Returns
    -------
    interpolator
        A function `f` that returns interpolated values.
    """

    if typ == "linear":
        return _periodic_interp1d(x, f)

    if typ == "cubic":
        return scipy.interpolate.CubicSpline(x, concatenate([f, f[[0]]]), bc_type="periodic")

    if typ == "pchip":
        return _periodic_pchip(x, f)

    msg = f"Unrecognized interpolator type {typ}"
    raise ValueError(msg)


def _rescale(v, vout: tuple[float, float] | None = None) -> ndarray | None:
    if v is None:
        return None

    if vout is None:
        return v
    v1 = plt.Normalize()(v)  # Scale to 0, 1
    return vout[0] + v1 * (vout[1] - vout[0])
