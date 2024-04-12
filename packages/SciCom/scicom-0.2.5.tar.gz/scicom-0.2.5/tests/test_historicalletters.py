import math
from unittest.mock import Mock, patch
from collections import Counter
import pandas as pd
import geopandas as gpd
from pathlib import Path
import pytest

from scicom.historicalletters.model import (
    HistoricalLetters,
    createData,
    SenderAgent,
    prune,
)


def test_initial_population_creation(tmp_path):
    file = createData(
        population=30,
        populationDistribution=Path(Path(__file__).parent.parent.resolve(), "src/scicom/data/pone.0162678.s003.csv")
    )
    assert isinstance(file, gpd.GeoDataFrame)


def test_model_initialization():
    # initialize model for 30 agents with defaults
    model = HistoricalLetters(30)
    # 30 agents should be on the scheduler
    assert len(model.schedule.agents) == 30
