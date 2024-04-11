from typing import Any, Callable

import numpy as np
import pandas as pd
import pytest

from in_silico_fate_mapping.fate_mapping import FateMapping


@pytest.mark.parametrize("attr,value", [("reverse", True), ("radius", 5)])
def test_lazy_fit(attr: str, value: Any, line: np.ndarray) -> None:
    fate_map = FateMapping(data=line, reverse=True, radius=7, n_samples=5)
    assert not fate_map._fitted

    fate_map(line[0, 1:])
    assert fate_map._fitted

    setattr(fate_map, attr, value)
    assert not fate_map._fitted


def test_simple_reconstruction(
    line_factory: Callable,
    n_samples: int = 25,
    length: int = 50,
    dim: int = 3,
) -> None:

    sigma = 1
    fate_map = FateMapping(
        radius=5, n_samples=n_samples, bind_to_existing=False, sigma=sigma
    )

    line = line_factory(n_samples=1, length=length, dim=dim)
    fate_map.data = line

    tracks = fate_map(line[0, 1:])
    assert tracks.shape == (n_samples * length, dim + 2)

    avg = tracks[:, 2:].reshape((n_samples, length, dim)).mean(axis=0)
    assert avg.shape == (length, dim)

    error = np.mean(np.abs(avg - line[:, 2:]))
    assert error < 1e-8

    fate_map.heatmap = True
    heatmap = fate_map(line[0, 1:])

    avg = (
        pd.DataFrame(np.asarray(np.nonzero(heatmap)).T)
        .groupby(0)
        .mean()
        .to_numpy()
    )

    max_error = np.abs(avg - line[:, 2:]).max()
    assert max_error < 1


def test_weights_attr(line: np.ndarray) -> None:
    fate_map = FateMapping(data=line, weights="distance")
    fate_map._fit()
    for m in fate_map._models.values():
        assert m.weights == "distance"

    fate_map.weights = "uniform"
    for m in fate_map._models.values():
        assert m.weights == "uniform"


def test_binding_attr(line: np.ndarray) -> None:
    fate_map = FateMapping(data=line, bind_to_existing=True, n_samples=5)
    result = fate_map(line[0, 1:])

    lines_start = np.sort(line[line[:, 1] == 0], axis=0)
    results_start = np.sort(result[result[:, 1] == 0], axis=0)

    assert np.allclose(lines_start, results_start)
