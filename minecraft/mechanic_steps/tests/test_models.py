import pytest
from mechanic_steps.models import MechanicStep
from mechanics.models import Mechanic

pytestmark = pytest.mark.django_db

class TestMechanicStepModel:
    
    def test_create_mechanic_step(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        step = MechanicStep.objects.create(
            mechanic=mechanic,
            step_number=1,
            title="Постройка платформы",
            description="Постройте платформу 10x10",
            image_path="step1.png"
        )
        assert step.id is not None
        assert step.mechanic == mechanic
        assert step.step_number == 1
        assert step.title == "Постройка платформы"
        assert step.description == "Постройте платформу 10x10"
        assert step.image_path == "step1.png"
    
    def test_mechanic_step_str_method(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        step = MechanicStep.objects.create(
            mechanic=mechanic,
            step_number=1,
            title="Шаг 1"
        )
        assert str(step) == "Шаг 1: Шаг 1"
    
    def test_multiple_steps_ordered(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        MechanicStep.objects.create(mechanic=mechanic, step_number=1, title="Шаг 1")
        MechanicStep.objects.create(mechanic=mechanic, step_number=2, title="Шаг 2")
        MechanicStep.objects.create(mechanic=mechanic, step_number=3, title="Шаг 3")
        
        steps = MechanicStep.objects.filter(mechanic=mechanic).order_by('step_number')
        assert steps[0].step_number == 1
        assert steps[1].step_number == 2
        assert steps[2].step_number == 3
    
    def test_step_numbers_unique_per_mechanic(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        MechanicStep.objects.create(mechanic=mechanic, step_number=1, title="Шаг 1")
        
        with pytest.raises(Exception):
            MechanicStep.objects.create(mechanic=mechanic, step_number=1, title="Шаг 1 дубль")
    
    def test_image_path_optional(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        step = MechanicStep.objects.create(
            mechanic=mechanic,
            step_number=1,
            title="Шаг без картинки"
        )
        assert step.image_path == ""
    
    def test_update_mechanic_step(self):
        mechanic = Mechanic.objects.create(
            mechanic_id="auto_farm",
            title="Автоматическая ферма",
            title_en="Auto Farm",
            category="farming",
            difficulty="advanced"
        )
        step = MechanicStep.objects.create(
            mechanic=mechanic,
            step_number=1,
            title="Старый заголовок"
        )
        step.title = "Новый заголовок"
        step.save()
        
        updated = MechanicStep.objects.get(id=step.id)
        assert updated.title == "Новый заголовок"