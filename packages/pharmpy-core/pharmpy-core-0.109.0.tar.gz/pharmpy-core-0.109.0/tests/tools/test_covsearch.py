import pytest

from pharmpy.modeling import add_covariate_effect, get_covariate_effects, remove_covariate_effect
from pharmpy.tools.covsearch.tool import (
    create_workflow,
    filter_search_space_and_model,
    validate_input,
)
from pharmpy.workflows import Workflow

MINIMAL_INVALID_MFL_STRING = ''
MINIMAL_VALID_MFL_STRING = 'LET(x, 0)'
LARGE_VALID_MFL_STRING = 'COVARIATE?(@IIV, @CONTINUOUS, *);COVARIATE?(@IIV, @CATEGORICAL, CAT)'


def test_create_workflow():
    assert isinstance(create_workflow(MINIMAL_VALID_MFL_STRING), Workflow)


def test_create_workflow_with_model(load_model_for_test, testdata):
    model = load_model_for_test(testdata / 'nonmem' / 'ruvsearch' / 'mox3.mod')
    assert isinstance(create_workflow(MINIMAL_VALID_MFL_STRING, model=model), Workflow)


def test_validate_input():
    validate_input(MINIMAL_VALID_MFL_STRING)


@pytest.mark.parametrize(
    ('model_path',), ((('nonmem', 'pheno.mod'),), (('nonmem', 'ruvsearch', 'mox3.mod'),))
)
def test_validate_input_with_model(load_model_for_test, testdata, model_path):
    model = load_model_for_test(testdata.joinpath(*model_path))
    validate_input(LARGE_VALID_MFL_STRING, model=model)


@pytest.mark.parametrize(
    (
        'model_path',
        'arguments',
        'exception',
        'match',
    ),
    [
        (
            None,
            dict(p_forward='x'),
            TypeError,
            'Invalid `p_forward`',
        ),
        (
            None,
            dict(p_forward=1.05),
            ValueError,
            'Invalid `p_forward`',
        ),
        (
            None,
            dict(p_backward=[]),
            TypeError,
            'Invalid `p_backward`',
        ),
        (
            None,
            dict(p_backward=1.01),
            ValueError,
            'Invalid `p_backward`',
        ),
        (
            None,
            dict(max_steps=1.2),
            TypeError,
            'Invalid `max_steps`',
        ),
        (None, dict(algorithm=()), ValueError, 'Invalid `algorithm`'),
        (
            None,
            dict(algorithm='scm-backward'),
            ValueError,
            'Invalid `algorithm`',
        ),
        (('nonmem', 'pheno.mod'), dict(search_space=1), TypeError, 'Invalid `search_space`'),
        (
            ('nonmem', 'pheno.mod'),
            dict(search_space=MINIMAL_INVALID_MFL_STRING),
            ValueError,
            'Invalid `search_space`',
        ),
        (
            ('nonmem', 'pheno.mod'),
            dict(search_space='LAGTIME(ON)'),
            ValueError,
            'Invalid `search_space`',
        ),
        (
            ('nonmem', 'pheno.mod'),
            dict(search_space='COVARIATE([CL, VC], WGT, EXP)'),
            ValueError,
            'Invalid `search_space` because of invalid parameter',
        ),
        (
            ('nonmem', 'pheno.mod'),
            dict(search_space='COVARIATE([CL, V], SEX, EXP)'),
            ValueError,
            'Invalid `search_space` because of invalid covariate',
        ),
        (
            ('nonmem', 'pheno.mod'),
            dict(search_space='COVARIATE([CL, V], WGT, [EXP, ABC])'),
            ValueError,
            'Invalid `search_space` because of invalid effect function',
        ),
        (
            ('nonmem', 'pheno.mod'),
            dict(search_space='COVARIATE(CL, WGT, exp, -)'),
            ValueError,
            'Invalid `search_space`',
        ),
        (
            None,
            dict(model=1),
            TypeError,
            'Invalid `model`',
        ),
    ],
)
def test_validate_input_raises(
    load_model_for_test,
    testdata,
    model_path,
    arguments,
    exception,
    match,
):
    model = load_model_for_test(testdata.joinpath(*model_path)) if model_path else None

    harmless_arguments = dict(
        search_space=MINIMAL_VALID_MFL_STRING,
    )

    kwargs = {**harmless_arguments, 'model': model, **arguments}

    with pytest.raises(exception, match=match):
        validate_input(**kwargs)


def test_covariate_filtering(load_model_for_test, testdata):
    search_space = 'COVARIATE(@IIV, @CONTINUOUS, lin);COVARIATE?(@IIV, @CATEGORICAL, CAT)'
    model = load_model_for_test(testdata / 'nonmem' / 'pheno_real.mod')
    orig_cov = get_covariate_effects(model)
    assert len(orig_cov) == 3

    eff, filtered_model = filter_search_space_and_model(search_space, model)
    assert len(eff) == 2
    expected_cov_eff = set((('CL', 'APGR', 'cat', '*'), ('V', 'APGR', 'cat', '*')))
    assert set(eff.keys()) == expected_cov_eff
    assert len(get_covariate_effects(filtered_model)) == 2

    for cov_effect in get_covariate_effects(model):
        model = remove_covariate_effect(model, cov_effect[0], cov_effect[1].name)

    model = add_covariate_effect(model, 'CL', 'WGT', 'pow', '*')
    assert len(get_covariate_effects(model)) == 1
    search_space = 'COVARIATE([CL, V],WGT,pow,*)'
    eff, filtered_model = filter_search_space_and_model(search_space, model)
    assert len(get_covariate_effects(filtered_model)) == 2
    assert len(eff) == 0
