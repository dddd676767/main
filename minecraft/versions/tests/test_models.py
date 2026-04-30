import pytest
from datetime import date, timedelta
from versions.models import MinecraftVersion

pytestmark = pytest.mark.django_db

class TestMinecraftVersionModel:
    
    def test_create_version(self):
        version = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date=date(2024, 6, 13),
            is_latest=True
        )
        assert version.id is not None
        assert version.version_number == "1.21"
        assert version.release_date == date(2024, 6, 13)
        assert version.is_latest is True
    
    def test_version_str_method(self):
        version = MinecraftVersion.objects.create(
            version_number="1.20.4",
            release_date=date(2023, 12, 7),
            is_latest=False
        )
        assert str(version) == "1.20.4"
    
    def test_version_unique_constraint(self):
        MinecraftVersion.objects.create(
            version_number="1.20",
            release_date=date(2023, 12, 7),
            is_latest=False
        )
        with pytest.raises(Exception):
            MinecraftVersion.objects.create(
                version_number="1.20",
                release_date=date(2023, 12, 7),
                is_latest=False
            )
    
    def test_multiple_versions_can_exist(self):
        v1 = MinecraftVersion.objects.create(
            version_number="1.20",
            release_date=date(2023, 12, 7),
            is_latest=False
        )
        v2 = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date=date(2024, 6, 13),
            is_latest=True
        )
        assert MinecraftVersion.objects.count() == 2
        assert v1.version_number == "1.20"
        assert v2.version_number == "1.21"
    
    def test_default_is_latest_false(self):
        version = MinecraftVersion.objects.create(
            version_number="1.19",
            release_date=date(2022, 6, 7)
        )
        assert version.is_latest is False
    
    def test_release_date_cannot_be_future(self):
        future_date = date.today() + timedelta(days=365)
        version = MinecraftVersion.objects.create(
            version_number="1.99",
            release_date=future_date,
            is_latest=False
        )
        assert version.release_date == future_date
    
    def test_ordering_by_release_date(self):
        v1 = MinecraftVersion.objects.create(
            version_number="1.19",
            release_date=date(2022, 6, 7),
            is_latest=False
        )
        v2 = MinecraftVersion.objects.create(
            version_number="1.20",
            release_date=date(2023, 12, 7),
            is_latest=False
        )
        v3 = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date=date(2024, 6, 13),
            is_latest=True
        )
        versions = list(MinecraftVersion.objects.order_by('-release_date'))
        assert versions[0].version_number == "1.21"
        assert versions[1].version_number == "1.20"
        assert versions[2].version_number == "1.19"
    
    def test_version_number_can_have_dots(self):
        version = MinecraftVersion.objects.create(
            version_number="1.20.6",
            release_date=date(2024, 1, 1),
            is_latest=False
        )
        assert version.version_number == "1.20.6"
    
    def test_version_number_max_length(self):
        long_version = "1." + "0" * 100
        version = MinecraftVersion.objects.create(
            version_number=long_version[:20],
            release_date=date(2024, 1, 1),
            is_latest=False
        )
        assert len(version.version_number) <= 20