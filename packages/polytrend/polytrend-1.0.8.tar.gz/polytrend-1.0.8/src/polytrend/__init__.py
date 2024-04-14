# This file is part of PolyTrend.
#
# PolyTrend is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PolyTrend is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PolyTrend. If not, see <https://www.gnu.org/licenses/>.

from .polytrend import PolyTrend
from typing import List, Tuple, Union, Callable, Optional
import numpy as np

pt = PolyTrend()


def polyplot(
    degrees: List[int],
    main_data: Union[List[Tuple[float, float]], str],
    extrapolate_data: List[float] = [],
) -> None:
    """
    Plot the polynomial fit on the known data.

    Args:
        degrees (List[int]): List of polynomial degrees to consider.
        main_data (Union[List[Tuple[float, float]], str]): List of tuples representing the known data points or CSV file path.
        extrapolate_data (List[float], optional): List of x coordinates for extrapolation. Defaults to [].

    Raises:
        ValueError: If degrees and/or known data is not specified or empty.
    """
    pt.polyplot(degrees, main_data, extrapolate_data)


def polyfind(
    degrees: List[int], main_data: Union[List[Tuple[float, float]], str]
) -> Tuple[Callable[[list], np.ndarray], int]:
    """
    Find the best-fit polynomial function.

    Args:
        degrees (List[int]): List of polynomial degrees to consider.
        main_data (Union[List[Tuple[float, float]], str]): List of tuples representing the known data points or CSV file path.

    Returns:
        Callable[[List[float]], List[float]]: A function that predicts values based on the polynomial.
    """
    return pt.polyfind(degrees, main_data)


def polygraph(
    main_data: Union[List[Tuple[float, float]], str],
    extrapolate_data: List[float] = [],
    function: Optional[Callable[[List[float]], np.ndarray]] = None,
) -> None:
    """
    Plot the function, known data, and extrapolated data.

    Args:
        main_data (Union[List[Tuple[float, float]], str]): List of tuples representing the known data points or CSV file path.
        extrapolate_data (List[float], optional): List of extrapolation data points. Defaults to [].
        func (Optional[Callable[[List[float]], np.ndarray]], optional): Function to generate predicted values. Defaults to None.

    Raises:
        ValueError: If known data is empty.
        ValueError: If extrapolation data is provided but no function is given.
    """
    pt.polygraph(main_data, extrapolate_data, function)


# # might change this due to class exposure below
# __all__ = ['PolyTrend']

# Optionally, you can also import other symbols from polytrend module if needed
