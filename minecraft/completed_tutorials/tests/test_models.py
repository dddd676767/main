import pytest
from completed_tutorials.models import CompletedTutorial
from user_profiles.models import UserProfile
from mechanics.models import Mechanic

pytestmark = pytest.mark.django_db

class TestCompletedTutorialModel:
    
    def test_create_completed_tutorial(self):
        profile = UserProfile.objects.create(user_id="player123")
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        tutorial = CompletedTutorial.objects.create(
            user=profile,
            mechanic=mechanic
        )
        assert tutorial.id is not None
        assert tutorial.user == profile
        assert tutorial.mechanic == mechanic
        assert tutorial.completed_at is not None
    
    def test_completed_tutorial_str_method(self):
        profile = UserProfile.objects.create(user_id="player123")
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        tutorial = CompletedTutorial.objects.create(
            user=profile,
            mechanic=mechanic
        )
        assert str(tutorial) == "player123 - Автоматическая ферма"
    
    def test_unique_constraint_user_mechanic(self):
        profile = UserProfile.objects.create(user_id="player123")
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        CompletedTutorial.objects.create(user=profile, mechanic=mechanic)
        
        with pytest.raises(Exception):
            CompletedTutorial.objects.create(user=profile, mechanic=mechanic)
    
    def test_multiple_tutorials_per_user(self):
        profile = UserProfile.objects.create(user_id="player123")
        mechanic1 = Mechanic.objects.create(
            mechanic_id="farm1",
            title="Ферма 1",
            title_en="Farm 1",
            category="farming",
            difficulty="beginner"
        )
        mechanic2 = Mechanic.objects.create(
            mechanic_id="farm2",
            title="Ферма 2",
            title_en="Farm 2",
            category="farming",
            difficulty="intermediate"
        )
        CompletedTutorial.objects.create(user=profile, mechanic=mechanic1)
        CompletedTutorial.objects.create(user=profile, mechanic=mechanic2)
        
        assert CompletedTutorial.objects.filter(user=profile).count() == 2
    
    def test_completed_at_auto_now_add(self):
        profile = UserProfile.objects.create(user_id="player123")
        mechanic = Mechanic.objects.create(
            mechanic_id="test",
            title="Test",
            title_en="Test",
            category="redstone",
            difficulty="beginner"
        )
        tutorial = CompletedTutorial.objects.create(
            user=profile,
            mechanic=mechanic
        )
        assert tutorial.completed_at is not None
    
    def test_user_deleted_cascade(self):
        profile = UserProfile.objects.create(user_id="player123")
        mechanic = Mechanic.objects.create(
            mechanic_id="test",
            title="Test",
            title_en="Test",
            category="redstone",
            difficulty="beginner"
        )
        CompletedTutorial.objects.create(user=profile, mechanic=mechanic)
        profile.delete()
        
        assert CompletedTutorial.objects.count() == 0
    
    def test_mechanic_deleted_cascade(self):
        profile = UserProfile.objects.create(user_id="player123")
        mechanic = Mechanic.objects.create(
            mechanic_id="test",
            title="Test",
            title_en="Test",
            category="redstone",
            difficulty="beginner"
        )
        CompletedTutorial.objects.create(user=profile, mechanic=mechanic)
        mechanic.delete()
        
        assert CompletedTutorial.objects.count() == 0