def loaddata(orm, fixture_name):
    """
    Overwrite the ``_get_model`` command in the serialiser to use the
    FakeORM model from south instead of the latest model.
    """
    from dingus import patch

    _get_model = lambda model_identifier: orm[model_identifier]

    with patch('django.core.serializers.python._get_model', _get_model):
        from django.core.management import call_command
        call_command("loaddata", fixture_name)
