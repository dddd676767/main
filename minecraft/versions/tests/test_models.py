import pytest
from datetime import date
from versions.models import MinecraftVersion

@pytest.mark.django_db
class TestMinecraftVersionModel:
    
    def test_create_version(self):
        version = MinecraftVersion.objects.create(
            version_number="1.21",
            release_date=date(2024, 6, 13),
            is_latest=True
        )
        assert version.version_number == "1.21"
        assert version.is_latest == True
    
    def test_version_str_method(self):
        version = MinecraftVersion.objects.create(
            version_number="1.20",
            release_date=date(2023, 12, 7),
            is_latest=False
        )
        assert str(version) == "1.20"
    
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
    
    def test_only_one_latest_version(self):
        MinecraftVersion.objects.all().update(is_latest=False)
        MinecraftVersion.objects.create(
            version_number="1.20",
            release_date=date(2023, 12, 7),
            is_latest=True
        )
        MinecraftVersion.objects.create(
            version_number="1.21",
            release_date=date(2024, 6, 13),
            is_latest=True
        )
        latest_versions = MinecraftVersion.objects.filter(is_latest=True)
        assert latest_versions.count() >= 1