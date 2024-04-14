from importlib import reload

import pytest

from django.conf import settings

from fieldlogger import config

from .test_utils import (
    CREATE_FORM,
    UPDATE_FORM,
    _set_config,
    check_logs,
    set_attributes,
)
from .testapp.models import TestModel

ORIGINAL_SETTINGS = settings.FIELD_LOGGER_SETTINGS.copy()


@pytest.fixture
def test_instance():
    # Create two instances for the foreign key field
    test_fk_instance = TestModel.objects.create()
    CREATE_FORM["test_foreign_key"] = test_fk_instance
    test_fk_instance2 = TestModel.objects.create()
    UPDATE_FORM["test_foreign_key"] = test_fk_instance2
    # Create the main instance
    instance = TestModel.objects.create(**CREATE_FORM)
    yield instance
    # Reset the settings
    settings.FIELD_LOGGER_SETTINGS.clear()
    settings.FIELD_LOGGER_SETTINGS.update(ORIGINAL_SETTINGS)
    reload(config)


@pytest.mark.django_db
def test_log_on_create(test_instance):
    check_logs(test_instance, created=True)


@pytest.mark.django_db
def test_log_on_save(test_instance):
    set_attributes(test_instance, UPDATE_FORM)
    check_logs(test_instance)


@pytest.mark.django_db
def test_log_on_save_twice(test_instance):
    set_attributes(test_instance, UPDATE_FORM, update_fields=True)
    set_attributes(test_instance, UPDATE_FORM)
    check_logs(test_instance)


@pytest.mark.django_db
def test_logging_enabled_off(test_instance):
    _set_config({"logging_enabled": False}, "global")
    set_attributes(test_instance, UPDATE_FORM)
    assert test_instance.fieldlog_set.count() == len(CREATE_FORM)


@pytest.mark.django_db
def test_fail_silently_off(test_instance):
    _set_config({"fail_silently": False}, "testapp")
    with pytest.raises(Exception):
        set_attributes(test_instance, UPDATE_FORM)
