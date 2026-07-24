import pytest
from routing.route import Route, RouteStep
from routing.learner import RouteLearner

def test_routing():
    learner = RouteLearner()
    r = Route(id="1", steps=[RouteStep("cap1", "ex1")])
    learner.add_route(r)
    best = learner.get_best_route(["cap1"])
    assert best == r
