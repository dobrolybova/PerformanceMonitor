from uuid import UUID
import pytest
import data_validator


class TestDataValidator:
    @pytest.mark.parametrize(
        ("test_input", "expected"), (
            ({}, None),
            ({'hash': '1'}, None),
            ({'number': '10bba744-04df-48a2-aff7-9d3e68992ce0'}, None),
            ({'hash': '10bba744-04df-48a2-aff7-9d3e68992ce0'}, UUID('10bba744-04df-48a2-aff7-9d3e68992ce0')),
        )
    )
    def test_get_uuid_if_valid(self, test_input, expected):
        assert data_validator.get_uuid_if_valid(test_input) == expected

    @pytest.mark.parametrize(
        ("test_input", "expected"), (
            ({"passwd": "passwd"}, False),
            ({"user": "user"}, False),
            ({"data": "data"}, False),
            ({"user": 1, "passwd": "passwd"}, False),
            ({"user": "user", "passwd": 1}, False),
            ({"user": "user", "passwd": "passwd"}, True),
        )
    )
    def test_validate_credentials(self, test_input, expected):
        assert data_validator.validate_credentials(test_input) is expected


