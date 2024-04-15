
![PyPI](https://img.shields.io/pypi/v/geoshapley)
![GitHub](https://img.shields.io/github/license/Ziqi-Li/geoshapley)


# GeoShapley

<img src="https://github.com/Ziqi-Li/geoshapley/assets/5518908/b450b5b3-fd59-41d8-a64c-fb202f492302" width="500">



A game theory approach to measuring spatial effects from machine learning models. GeoShapley is built on Shapley value and Kernel SHAP estimator.

### Installation:

GeoShapley can be installed from PyPI:

```bash
$ pip install geoshapley
```

### Example:

GeoShapley can explain any model that takes data + coordiantes as the input. Currently, coordinates need to be put as the last two columns of your `pandas.DataFrame`(`X_geo`). 

Below shows an example on how to explain a trained NN model.

```python
from geoshapley import GeoShapleyExplainer
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_geo, y, random_state=1)

#Fit a NN model based on training data
mlp_model = MLPRegressor().fit(X_train, y_train)

#Specify a small background data
background = X_train.sample(100).values

#Initilize a GeoShapleyExplainer
mlp_explainer = GeoShapleyExplainer(mlp_model.predict, background)

#Explain the data
mlp_rslt = mlp_explainer.explain(X_geo)

#Make a shap-style summary plot
mlp_rslt.summary_plot()

#Make partial dependence plots of the primary (non-spatial) effects
mlp_rslt.partial_dependence_plots()

#Calculate spatially varying explanations
mlp_svc = mlp_rslt.get_svc()
```
### Reference:
Li, Z. (2023a). GeoShapley: A Game Theory Approach to Measuring Spatial Effects in Machine Learning Models. arXiv preprint [https://doi.org/10.48550/arXiv.2312.03675](https://doi.org/10.48550/arXiv.2312.03675)

