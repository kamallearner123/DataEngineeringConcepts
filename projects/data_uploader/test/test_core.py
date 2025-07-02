import pytest
from core import core

def test_add_tc_01():
    assert core.add(1,2) == 3
def test_add_tc_02():
    assert core.add(1,2) == 4
