from import_export import resources

from formula.models import Constructor


class ConstructorResource(resources.ModelResource):
    class Meta:
        model = Constructor
