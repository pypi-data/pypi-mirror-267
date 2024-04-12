"""
Coordinate functionality in cryojax.
"""

from abc import abstractmethod
from typing import Any, Optional
from typing_extensions import Self

import equinox as eqx
import jax.numpy as jnp
import numpy as np
from equinox import AbstractVar
from jaxtyping import Array, Float, Inexact


class AbstractCoordinates(eqx.Module, strict=True):
    """
    A base class that wraps a coordinate array.
    """

    array: AbstractVar[Any]

    @abstractmethod
    def get(self) -> Any:
        """Get the coordinates."""
        raise NotImplementedError

    def __mul__(
        self, real_number: float | Float[np.ndarray, ""] | Float[Array, ""]
    ) -> Self:
        # The following line seems to be required for differentiability with
        # respect to arr
        rescaled_array = jnp.where(
            self.array != 0.0, self.array * jnp.asarray(real_number), 0.0
        )
        return eqx.tree_at(lambda x: x.array, self, rescaled_array)

    def __rmul__(
        self, real_number: float | Float[np.ndarray, ""] | Float[Array, ""]
    ) -> Self:
        rescaled_array = jnp.where(
            self.array != 0.0, jnp.asarray(real_number) * self.array, 0.0
        )
        return eqx.tree_at(lambda x: x.array, self, rescaled_array)

    def __truediv__(
        self, real_number: float | Float[np.ndarray, ""] | Float[Array, ""]
    ) -> Self:
        rescaled_array = jnp.where(
            self.array != 0.0, self.array / jnp.asarray(real_number), 0.0
        )
        return eqx.tree_at(lambda x: x.array, self, rescaled_array)


class CoordinateList(AbstractCoordinates, strict=True):
    """
    A Pytree that wraps a coordinate list.
    """

    array: Float[Array, "size 3"] | Float[Array, "size 2"] = eqx.field(
        converter=jnp.asarray
    )

    def __init__(
        self, coordinate_list: Float[Array, "size 2"] | Float[Array, "size 3"]
    ):
        self.array = coordinate_list

    def get(self) -> Float[Array, "size 3"] | Float[Array, "size 2"]:
        return self.array


class CoordinateGrid(AbstractCoordinates, strict=True):
    """
    A Pytree that wraps a coordinate grid.
    """

    array: Float[Array, "y_dim x_dim 2"] | Float[Array, "z_dim y_dim x_dim 3"] = (
        eqx.field(converter=jnp.asarray)
    )

    def __init__(
        self,
        shape: tuple[int, ...],
        grid_spacing: float | Float[np.ndarray, ""] = 1.0,
    ):
        self.array = make_coordinates(shape, grid_spacing)

    def get(
        self,
    ) -> Float[Array, "y_dim x_dim 2"] | Float[Array, "z_dim y_dim x_dim 3"]:
        return self.array


class FrequencyGrid(AbstractCoordinates, strict=True):
    """
    A Pytree that wraps a frequency grid.
    """

    array: Float[Array, "y_dim x_dim 2"] | Float[Array, "z_dim y_dim x_dim 3"] = (
        eqx.field(converter=jnp.asarray)
    )

    def __init__(
        self,
        shape: tuple[int, ...],
        grid_spacing: float | Float[np.ndarray, ""] = 1.0,
        half_space: bool = True,
    ):
        self.array = make_frequencies(shape, grid_spacing, half_space=half_space)

    def get(
        self,
    ) -> Float[Array, "y_dim x_dim 2"] | Float[Array, "z_dim y_dim x_dim 3"]:
        return self.array


class FrequencySlice(AbstractCoordinates, strict=True):
    """
    A Pytree that wraps a frequency slice.

    Unlike a `FrequencyGrid`, a `FrequencySlice` has the zero frequency
    component in the center.
    """

    array: Float[Array, "1 y_dim x_dim 3"] = eqx.field(converter=jnp.asarray)

    def __init__(
        self,
        shape: tuple[int, int],
        grid_spacing: float | Float[np.ndarray, ""] = 1.0,
        half_space: bool = True,
    ):
        frequency_slice = make_frequencies(shape, grid_spacing, half_space=half_space)
        if half_space:
            frequency_slice = jnp.fft.fftshift(frequency_slice, axes=(0,))
        else:
            frequency_slice = jnp.fft.fftshift(frequency_slice, axes=(0, 1))
        frequency_slice = jnp.expand_dims(
            jnp.pad(
                frequency_slice,
                ((0, 0), (0, 0), (0, 1)),
                mode="constant",
                constant_values=0.0,
            ),
            axis=0,
        )
        self.array = frequency_slice

    def get(self) -> Float[Array, "1 y_dim x_dim 3"]:
        return self.array


def make_coordinates(
    shape: tuple[int, ...], grid_spacing: float | Float[np.ndarray, ""] = 1.0
) -> Float[Array, "*shape ndim"]:
    """
    Create a real-space cartesian coordinate system on a grid.

    Arguments
    ---------
    shape :
        Shape of the voxel grid, with
        ``ndim = len(shape)``.
    grid_spacing :
        The grid spacing, in units of length.

    Returns
    -------
    coordinate_grid :
        Cartesian coordinate system in real space.
    """
    coordinate_grid = _make_coordinates_or_frequencies(
        shape, grid_spacing=grid_spacing, real_space=True
    )
    return coordinate_grid


def make_frequencies(
    shape: tuple[int, ...],
    grid_spacing: float | Float[np.ndarray, ""] = 1.0,
    half_space: bool = True,
) -> Float[Array, "*shape ndim"]:
    """
    Create a fourier-space cartesian coordinate system on a grid.
    The zero-frequency component is in the beginning.

    Arguments
    ---------
    shape :
        Shape of the voxel grid, with
        ``ndim = len(shape)``.
    grid_spacing :
        The grid spacing, in units of length.
    half_space :
        Return a frequency grid on the half space.
        ``shape[-1]`` is the axis on which the negative
        frequencies are omitted.

    Returns
    -------
    frequency_grid :
        Cartesian coordinate system in frequency space.
    """
    frequency_grid = _make_coordinates_or_frequencies(
        shape,
        grid_spacing=grid_spacing,
        real_space=False,
        half_space=half_space,
    )
    return frequency_grid


def cartesian_to_polar(
    freqs: Float[Array, "y_dim x_dim 2"], square: bool = False
) -> tuple[Inexact[Array, "y_dim x_dim"], Inexact[Array, "y_dim x_dim"]]:
    """
    Convert from cartesian to polar coordinates.

    Arguments
    ---------
    freqs :
        The cartesian coordinate system.
    square :
        If ``True``, return the square of the
        radial coordinate :math:`|r|^2`. Otherwise,
        return :math:`|r|`.
    """
    theta = jnp.arctan2(freqs[..., 0], freqs[..., 1])
    k_sqr = jnp.sum(jnp.square(freqs), axis=-1)
    if square:
        return k_sqr, theta
    else:
        kr = jnp.sqrt(k_sqr)
        return kr, theta


def _make_coordinates_or_frequencies(
    shape: tuple[int, ...],
    grid_spacing: float | Float[np.ndarray, ""] = 1.0,
    real_space: bool = False,
    half_space: bool = True,
) -> Float[Array, "*shape ndim"]:
    ndim = len(shape)
    coords1D = []
    for idx in range(ndim):
        if real_space:
            c1D = _make_coordinates_or_frequencies_1d(
                shape[idx], grid_spacing, real_space
            )
        else:
            if not half_space:
                rfftfreq = False
            else:
                rfftfreq = False if idx < ndim - 1 else True
            c1D = _make_coordinates_or_frequencies_1d(
                shape[idx], grid_spacing, real_space, rfftfreq
            )
        coords1D.append(c1D)
    if ndim == 2:
        y, x = coords1D
        xv, yv = jnp.meshgrid(x, y, indexing="xy")
        coords = jnp.stack([xv, yv], axis=-1)
    elif ndim == 3:
        z, y, x = coords1D
        xv, yv, zv = jnp.meshgrid(x, y, z, indexing="xy")
        xv, yv, zv = [
            jnp.transpose(rv, axes=[2, 0, 1]) for rv in [xv, yv, zv]
        ]  # Change axis ordering to [z, y, x]
        coords = jnp.stack([xv, yv, zv], axis=-1)
    else:
        raise ValueError(
            "Only 2D and 3D coordinate grids are supported. "
            f"Tried to create a grid of shape {shape}."
        )

    return coords


def _make_coordinates_or_frequencies_1d(
    size: int,
    grid_spacing: float | Float[np.ndarray, ""],
    real_space: bool = False,
    rfftfreq: Optional[bool] = None,
) -> Float[Array, " size"]:
    """One-dimensional coordinates in real or fourier space"""
    if real_space:
        make_1d = (
            lambda size, dx: jnp.fft.fftshift(jnp.fft.fftfreq(size, 1 / dx)) * size
        )
    else:
        if rfftfreq is None:
            raise ValueError("Argument rfftfreq cannot be None if real_space=False.")
        else:
            fn = jnp.fft.rfftfreq if rfftfreq else jnp.fft.fftfreq
            make_1d = lambda size, dx: fn(size, grid_spacing)

    return make_1d(size, grid_spacing)
