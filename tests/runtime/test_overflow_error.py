import friendly_traceback


def test_Generic():
    try:
        2.0 ** 1600
    except OverflowError as e:
        message = str(e)
        friendly_traceback.explain_traceback(redirect="capture")
    result = friendly_traceback.get_output()
    
    assert (
        "OverflowError: (34, 'Result too large')" in result
        or "OverflowError: (34, 'Numerical result out of range')" in result
    )
    if friendly_traceback.get_lang() == "en":
        assert "`OverflowError` is raised when the result" in result
    return result, message


if __name__ == "__main__":
    print(test_Generic()[0])
