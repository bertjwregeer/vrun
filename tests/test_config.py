import os

import pytest

from vrun import config
from vrun.compat import ConfigParser


@pytest.mark.parametrize('parts, result', [
    (
        ['simple'],
        ['simple']
    ),
    (
        ['multiple', 'simple'],
        ['multiple', 'simple']
    ),
    (
        ['with', '"quotes"'],
        ['with', '"quotes"']
    ),
    (
        ['"testing', 'quote', 'support"'],
        ['testing quote support']
    ),
    (
        ["'testing", 'quote', "support'"],
        ['testing quote support']
    ),
    (
        ['"testing', '\'quote', 'support"'],
        ['testing \'quote support']
    ),
    (
        ['"testing', '\'quote\'', 'support"'],
        ['testing \'quote\' support']
    ),
    (
        ['"testing', '\'quote', '\'support"'],
        ['testing \'quote \'support']
    ),
    (
        ['""'],
        ['""']
    ),
    (
        ['" ', ' "'],
        ['   ']
    ),
    (
        ['one', 'two', '"three', 'four"'],
        ['one', 'two', 'three four']
    ),
])
def test_quoted_combine(parts, result):
    assert list(config.quoted_combine(parts)) == result


@pytest.mark.parametrize('parts', [
    ['"testing', '\'quote', '"support"'],
    ['" ', '""'],
    ['"test', '"ing'],
])
def test_quoted_combine_invalid(parts):
    with pytest.raises(ValueError):
        assert list(config.quoted_combine(parts))


@pytest.mark.parametrize('folder, result', [
    ('configtest', 'vrun.cfg'),
    ('configtest/vrun_ini', 'vrun.ini'),
    ('configtest/setup_cfg', 'setup.cfg'),
    ('configtest/setup_cfg_no_section', None),
])
def test_find_config(folder, result):
    curpath = os.path.dirname(os.path.realpath(__file__))

    cwd = os.path.join(curpath, folder)

    if result:
        assert config.find_config(cwd).endswith(result)
    else:
        assert config.find_config(cwd) == result


@pytest.mark.parametrize('folder, result', [
    ('configtest', 'vrun.cfg'),
    ('configtest/vrun_ini', 'vrun.ini'),
    ('configtest/setup_cfg', 'setup.cfg'),
])
def test_config_from_file(folder, result):
    curpath = os.path.dirname(os.path.realpath(__file__))
    cwd = os.path.join(curpath, folder)

    config_file = config.find_config(cwd)
    assert isinstance(config.config_from_file(config_file), ConfigParser)
