import asyncio
from unittest.mock import Mock, call

import pytest

from upsies.uis import prompts


def test_Prompt_parameters():
    callbacks = (Mock(), Mock())
    prompt = prompts.Prompt(
        foo='bar',
        baz=123,
        callbacks=callbacks,
    )
    assert prompt.parameters == {
        'foo': 'bar',
        'baz': 123,
    }


@pytest.mark.asyncio
async def test_Prompt_set_result():
    callbacks = (Mock(), Mock())
    prompt = prompts.Prompt(
        foo='bar',
        baz=123,
        callbacks=callbacks,
    )

    assert not prompt._result_arrived.is_set()
    assert prompt.result is None
    asyncio.get_event_loop().call_soon(prompt.set_result('the result'))
    await prompt.wait()
    assert prompt._result_arrived.is_set()
    assert prompt.result == 'the result'
    for callback in callbacks:
        assert callback.call_args_list == [call('the result')]


def test_Prompt_on_result():
    callbacks = (Mock(), Mock())
    prompt = prompts.Prompt(
        foo='bar',
        baz=123,
        callbacks=callbacks,
    )
    additional_callback = Mock()
    prompt.on_result(additional_callback)
    assert prompt._callbacks == [
        callbacks[0],
        callbacks[1],
        additional_callback,
    ]


@pytest.mark.asyncio
async def test_Prompt___await__():
    prompt = prompts.Prompt()

    async def awaiter():
        results = []
        results.append(await prompt)
        results.append(await prompt)
        return results

    async def result_setter():
        await asyncio.sleep(0.01)
        prompt.set_result('Hello, world!')

    return_values = await asyncio.gather(awaiter(), result_setter())
    assert return_values == [
        ['Hello, world!', 'Hello, world!'],
        None,
    ]


@pytest.mark.parametrize(
    argnames='callbacks, exp_callbacks_string',
    argvalues=(
        (
            (str, int),
            f'callbacks=[{str}, {int}]',
        ),
    ),
    ids=lambda v: repr(v),
)
@pytest.mark.parametrize(
    argnames='parameters, exp_parameters_string',
    argvalues=(
        (
            {'foo': 'bar', 'baz': 123},
            "foo='bar', baz=123",
        ),
        (
            {},
            '',
        ),
    ),
    ids=lambda v: repr(v),
)
def test_Prompt___repr__(callbacks, exp_callbacks_string, parameters, exp_parameters_string):
    prompt = prompts.Prompt(
        callbacks=callbacks,
        **parameters,
    )
    repr_string = repr(prompt)
    exp_arguments_string = ', '.join(
        exp_arg
        for exp_arg in (exp_parameters_string, exp_callbacks_string)
        if exp_arg
    )
    assert repr_string == (
        f'{prompts.Prompt.__name__}('
        + exp_arguments_string
        + ')'
    )


@pytest.mark.parametrize('focused', ('bar', None))
@pytest.mark.parametrize('question', ('Hello?', None))
def test_RadioListPrompt(question, focused):
    callbacks = (Mock(), Mock())
    prompt = prompts.RadioListPrompt(
        options=('foo', 'bar', 'baz'),
        question=question,
        focused=focused,
        callbacks=callbacks,
    )

    assert prompt.parameters == {
        'options': ('foo', 'bar', 'baz'),
        'question': question,
        'focused': focused,
    }
    assert prompt._callbacks == list(callbacks)


@pytest.mark.parametrize('question', ('Hello?', None))
@pytest.mark.parametrize('text', ('Prefilled text', None))
def test_TextPrompt(question, text):
    callbacks = (Mock(), Mock())
    prompt = prompts.TextPrompt(
        question=question,
        text=text,
        callbacks=callbacks,
    )

    assert prompt.parameters == {
        'question': question,
        'text': text,
    }
    assert prompt._callbacks == list(callbacks)
