import pytest

from scraper.providers.utils import format_measurements


class TestUtils:
    @pytest.mark.parametrize(
        "text,expected",
        [
            ("1 StückFrühlingszwiebel", "1 Stück Frühlingszwiebel"),
            ("20 gIngwer", "20 g Ingwer"),
            ("250 mlKokosmilch", "250 ml Kokosmilch"),
            ("1 StückZitrone", "1 Stück Zitrone"),
            ("1 StückLimette", "1 Stück Limette"),
        ],
    )
    def test_format_measurements(self, text, expected):
        measurements = ["Stück", "ml", "g"]
        assert format_measurements(text, measurements) == expected
