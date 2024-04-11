import json
import os
from collections.abc import Callable
from pathlib import Path
import bayesbuilding.models as mods
import warnings

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm


def r2_score(y_true, y_pred):
    numerator = ((y_true - y_pred) ** 2).sum(axis=0)
    denominator = ((y_true - np.average(y_true, axis=0)) ** 2).sum(axis=0)
    return 1 - numerator / denominator


def custom_serializer(obj):
    if callable(obj) and hasattr(obj, "__name__"):
        return obj.__name__
    else:
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


class PymcWrapper:
    """
    A class simplifying the creation of probabilistic models using PyMC3.

    This class abstracts some complexities of PyMC while enforcing a structured
     framework:
    - Features are provided as pandas DataFrames.
    - Only a single target variable, provided as a pandas Series, is allowed.
    - The model is defined by a model function, which returns deterministic outputs.
    - The likelihood function is a Normal distribution, with the mean given by the
        output of the model function and the standard deviation (sigma) being
        a variable.
    - For change point models, sigma may have multiple dimensions.
    - The likelihood function is used for prediction, with the variable
        named "observations".

    Parameters:
    -----------
    model_function : Callable
        A function defining the PyMC model. It takes two arguments: 'x' and
        'variable_dict'. 'x' is a 2D array derived from the features DataFrame.
        Use standard indexing as DataFrame column names cannot be used within
        the function's scope.
        'variable_dict' is a dictionary where keys are variable names and values
        are PyMC variables.
    priors_dict : dict[str:(Callable, dict)]
        A dictionary containing prior distributions for model parameters.
        Keys are parameter names, and values are tuples where the first element is
        a PyMC callable defining the prior distribution, and the second element is
        a dictionary of parameters for the prior distribution.
        The dictionary must include a variable called 'sigma', representing the
        likelihood standard deviation.
    sigma_change_point_idx : int, optional
        Index of 'x' in the 2nd dimension (feature axis) indicating the change point
        for sigma in change point models.

    Attributes:
    -----------
    var_names : list
        Names of the model variables.
    features_names : list
        Names of the features used in the model. Only available after performing
        prior prediction or sampling.
    target_name : str
        Name of the target variable. Only available after sampling.
    trace : InferenceData
        PyMC trace containing samples.
    sigma_change_point_idx : int, optional
        Index indicating the change point for sigma.
    _observations : pm.Normal
        PyMC3 Normal distribution defining the model's likelihood.
    _data_dict : dict
        Dictionary containing PyMC3 MutableData objects.
    _variables_dict : dict
        Dictionary containing PyMC3 variables for the model parameters.

    Methods:
    --------
    __repr__():
        Returns a string representation of the model's variables, features, and target.
    sample_prior():
        Samples from the prior predictive distribution.
    sample():
        Samples to obtain posterior distributions using the NUTS algorithm.
    sample_posterior_predictive():
        Samples from the posterior predictive distribution.
    get_summary():
        Returns a summary of the posterior distribution. Use the 'group' argument to
        select among 'prior', 'prior_predictive', 'posterior', or
        'posterior_predictive'.
    get_loo_score():
        Computes the leave-one-out cross-validation (LOO) score.
    save_model(Path):
        Save the model to the required path. It will contain 3 traces
        and a json file.
    load_model(Path):
        Load the model traces and json file contained in the desired path and build
        the pymc model.
        If the loaded model function is not in bayesbuilding.model, it must
        be provided separately and the pymc model must be build using the build_model()
        method.
    plot_dist_comparison(var_names):
        Plot compare prior and posterior distributions of variables and observations
        var_names arguments filter the values to display. default is self.var_names
    """

    def __init__(
        self,
        model_function: Callable = None,
        priors_dict: dict[str:(Callable, dict)] = None,
        sigma_change_point_idx=None,
    ):
        self.model_function = model_function
        self.priors_dict = priors_dict
        self.features_names = None
        self.target_name = None
        self.var_names = None
        self.model = None
        self.sigma_change_point_idx = sigma_change_point_idx
        self.traces = {
            "prior": az.data.inference_data.InferenceData(),
            "sampling": az.data.inference_data.InferenceData(),
            "posterior": az.data.inference_data.InferenceData(),
        }
        self._x_train = None
        self._y_train = None
        self._observations = None
        self._data_dict = None
        self._variables_dict = None

        self.build_model()

    def __repr__(self):
        string_out = """"""
        string_out += """=== Variables names : \n"""
        if self.var_names is not None:
            for var in self.var_names:
                string_out += f"""- {var} \n"""
        string_out += """\n"""

        string_out += """=== Features names: \n"""
        if self.features_names is not None:
            for feat in self.features_names:
                string_out += f"""- {feat} \n"""
        string_out += """\n"""

        string_out += """=== Target name: \n"""
        if self.target_name is not None:
            string_out += f"""- {self.target_name} \n"""

        return string_out

    def save_model(self, dir_path: Path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        for name, traces in self.traces.items():
            traces.to_netcdf((dir_path / f"{name}.nc").as_posix())

        with open(dir_path / "config.json", "w", encoding="utf-8") as f:
            to_dump = {
                "model_function": self.model_function,
                "priors_dict": self.priors_dict,
                "sigma_change_point_idx": self.sigma_change_point_idx,
                "features_names": self.features_names,
                "target_name": self.target_name,
            }
            json.dump(
                to_dump, f, ensure_ascii=False, default=custom_serializer, indent=4
            )

    def load_model(self, dir_path: Path):
        if not os.path.exists(dir_path):
            raise ValueError(f"Provided dir_path : {dir_path} not found")

        for name, _ in self.traces.items():
            self.traces[name] = az.from_netcdf((dir_path / f"{name}.nc").as_posix())

        with open(dir_path / "config.json", encoding="utf-8") as f:
            config_dict = json.load(f)

        for attr, value in config_dict.items():
            setattr(self, attr, value)

        for val in self.priors_dict.values():
            val[0] = getattr(pm, val[0])

        if self.model_function is not None:
            try:
                self.model_function = getattr(mods, self.model_function)
            except AttributeError:
                warnings.warn(
                    f"Model function {self.model_function} not found in"
                    f"bayesbuilding.models. Load a model function before running"
                    f"build_model() method"
                )
                self.model_function = None

        self.build_model()

    def build_model(self):
        if self.model_function is not None and self.priors_dict is not None:
            self.model = pm.Model()
            with self.model:
                # Set empty data objects
                self._data_dict = {
                    "x": pm.MutableData(
                        name="x", value=np.array([[]]), dims=["date", "features"]
                    ),
                    "y": pm.MutableData(name="y", value=np.array([]), dims=["target"]),
                }

                # Set priors
                self._variables_dict = {
                    name: val[0](**val[1]) for name, val in self.priors_dict.items()
                }

                mu = pm.Deterministic(
                    name="mu",
                    var=self.model_function(self._data_dict["x"], self._variables_dict),
                )

                # Combine into likelihood function
                sigma = (
                    self._variables_dict["sigma"][
                        self._data_dict["x"][:, self.sigma_change_point_idx].astype(int)
                    ]
                    if self.sigma_change_point_idx is not None
                    else self._variables_dict["sigma"]
                )

                self._observations = pm.Normal(
                    name="observations",
                    mu=mu,
                    sigma=sigma,
                    observed=self._data_dict["y"],
                    shape=self._data_dict["x"].shape[0],
                )
            self.var_names = list(self.priors_dict.keys())

    def sample_prior(
        self,
        samples: int = 500,
        x: pd.DataFrame = None,
        var_names=None,
        sample_kwargs=None,
    ):
        if sample_kwargs is None:
            sample_kwargs = {}
        with self.model:
            if x is not None:
                pm.set_data({"x": x})
                self.features_names = list(x.columns)

            self.traces["prior"] = pm.sample_prior_predictive(
                samples=samples, var_names=var_names, **sample_kwargs
            )

    def sample(
        self,
        y: pd.Series,
        x: pd.DataFrame = None,
        draws: int = 1000,
        tune: int = 1000,
        chains=None,
        sample_kwargs=None,
    ):
        if sample_kwargs is None:
            sample_kwargs = {}

        with self.model:
            if x is not None:
                pm.set_data({"x": x})
                self.features_names = list(x.columns)

            pm.set_data({"y": y})
            self.target_name = y.name

            self.traces["sampling"] = pm.sample(
                draws=draws, tune=tune, chains=chains, **sample_kwargs
            )

        self.sample_posterior_predictive()

        self._x_train = x
        self._y_train = y

    def sample_posterior_predictive(self, x: pd.DataFrame = None, sample_kwargs=None):
        if self.traces["sampling"] is None:
            raise ValueError(
                "No posterior trace available. Perform sampling before"
                "sampling from posterior"
            )

        if sample_kwargs is None:
            sample_kwargs = {}

        with self.model:
            if x is not None:
                pm.set_data({"x": x})

            self.traces["posterior"] = pm.sample_posterior_predictive(
                trace=self.traces["sampling"],
                var_names=["observations"],
                **sample_kwargs,
            )

    def get_summary(
        self, group: str = None, var_names=None, filter_vars=None, summary_kwargs=None
    ):
        if group not in self.traces.keys():
            raise ValueError(
                f"Unknown group {group} choose one of {self.traces.keys()}"
            )
        if summary_kwargs is None:
            summary_kwargs = {}

        return az.summary(
            data=self.traces[group],
            var_names=var_names,
            filter_vars=filter_vars,
            **summary_kwargs,
        )

    def get_loo_score(self, loo_kwargs=None):
        if self.traces["sampling"] is None:
            raise ValueError(
                "Sampling trace is not available, perform sampling "
                "before checking loo score"
            )
        if loo_kwargs is None:
            loo_kwargs = {}
        with self.model:
            pm.set_data({"x": self._x_train, "y": self._y_train})
            pm.compute_log_likelihood(self.traces["sampling"])
        return az.loo(data=(self.traces["sampling"]), **loo_kwargs)

    def score(
        self,
        x: pd.DataFrame,
        y: pd.Series,
        score_function: Callable = r2_score,
        sample_kwargs: dict = None,
    ):
        if sample_kwargs is None:
            sample_kwargs = {}

        self.sample_posterior_predictive(x=x, sample_kwargs=sample_kwargs)
        post_trace = self.traces["posterior"].posterior_predictive["observations"]
        flattened_trace = np.array(post_trace).reshape(-1, post_trace.shape[-1])

        scores_array = np.array(
            [score_function(y, sample) for sample in flattened_trace]
        )
        return {"mean_score": np.mean(scores_array), "sd_score": np.std(scores_array)}

    def plot_dist_comparison(self, var_names: list[str] = None, plot_dist_kwargs=None):
        if var_names is None:
            var_names = self.var_names
        if plot_dist_kwargs is None:
            plot_dist_kwargs = {}
        temp = az.data.inference_data.InferenceData()
        temp.extend(self.traces["sampling"])
        temp.extend(self.traces["prior"])
        return az.plot_dist_comparison(temp, var_names=var_names, **plot_dist_kwargs)
