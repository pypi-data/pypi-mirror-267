# PolyTrend

PolyTrend is a Python package aimed at facilitating polynomial trend fitting, visualization, and extrapolation. It offers a comprehensive set of functionalities to analyze and interpret data using polynomial regression techniques. Below, we provide an overview of the package along with additional formatting and explanations relevant for PyPI.

## Introduction

PolyTrend is designed to approximate and plot a polynomial function onto given data, thereby aiding in the analysis of trends and patterns within datasets. Its development contributes to various fields including interpolation, polynomial regression, and approximation theory.

## Key Functionalities

PolyTrend offers the following key functionalities:

- **polyplot()**: This method plots the polynomial fit based on specified degrees of the polynomial and the provided data.
- **polyfind()**: This method calculates the best-fit polynomial function by evaluating different polynomial degrees and selecting the one with the lowest Bayesian Information Criterion (BIC) score.
- **polygraph()**: This method visualizes the polynomial function, the known data points, and any extrapolated data points if provided.

## Usage

Users can utilize PolyTrend to perform the following tasks:

1. **Data Analysis**: Analyze trends and patterns within datasets using polynomial regression techniques.
2. **Visualization**: Visualize polynomial fits alongside original data points to gain insights into the relationship between variables.
3. **Extrapolation**: Extrapolate future values based on the fitted polynomial function, enabling predictive modeling tasks.

## Dependencies

PolyTrend relies on the following libraries for its computations and visualizations:

- NumPy
- pandas
- Matplotlib
- scikit-learn

## Additional Resources

For further details on polynomial regression, refer to [this wiki](https://en.wikipedia.org/wiki/Polynomial_regression).

## Installation

PolyTrend can be installed via pip:

```bash
pip install polytrend
```

## Example Usage

```python
from polytrend import PolyTrend

# Sample data
data = [(1, 2), (2, 3), (3, 5), (4, 7)]

# Initialize PolyTrend object
poly = PolyTrend()

# Fit polynomial and visualize
poly.polyfind(data)
poly.polygraph()
```

## Feedback and Contributions

Feedback and contributions to PolyTrend are welcomed and encouraged. Please feel free to submit any issues or pull requests via the [GitHub repository](https://github.com/asiimwemmanuel/polytrend).

## License

PolyTrend is licensed under the GNU GPL License. See the [LICENSE](./LICENSE) file for details.
