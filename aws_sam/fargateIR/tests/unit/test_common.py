from lambda_handler import common


def test_generate_arn_for_instance():
    result = common.generate_arn_for_instance("us-west-2", "mi-00fe9059acfd61abb")
    assert result == "arn:aws:ssm:*:*:managed-instance/mi-00fe9059acfd61abb"


def test_limited_scope_policy_generation():
    result = common.get_limited_policy("us-west-2", "mi-00fe9059acfd61abb")
    print(result)
    assert result is not None


def test_key_lowering():
    list_of_dicts = [{"Key": "foo", "value": "bAr"}]
    result = common.lower_keys(list_of_dicts)
    assert result is not None
    assert result == [{"key": "foo"}, {"value": "bar"}]
