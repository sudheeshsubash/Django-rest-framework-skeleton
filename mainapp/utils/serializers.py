from rest_framework import serializers


class DynamicFieldsBaseModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes additional `fields`, `exclude`, `read_only_fields`,
    and `extra_kwargs` arguments to control which fields are displayed and how.
    """

    def __init__(self, *args, **kwargs):
        # Extract dynamic arguments, provide defaults if not passed
        fields = kwargs.pop('fields', getattr(self.Meta, 'fields', None))
        exclude = kwargs.pop('exclude', getattr(self.Meta, 'exclude', None))
        read_only_fields = kwargs.pop('read_only_fields', getattr(self.Meta, 'read_only_fields', None))
        extra_kwargs = kwargs.pop('extra_kwargs', getattr(self.Meta, 'extra_kwargs', {}))


        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        # Update read-only fields
        if read_only_fields:
            for field_name in read_only_fields:
                if field_name in self.fields:
                   self.fields[field_name].read_only = True

        #Apply extra kwargs
        if extra_kwargs:
            for field_name, kwargs_update in extra_kwargs.items():
               if field_name in self.fields:
                   for k, v in kwargs_update.items():
                       setattr(self.fields[field_name],k,v)


        # Handle field inclusion/exclusion after instantiating parent class
        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        if exclude is not None:
           # Remove any fields listed in the exclude argument
           for field_name in exclude:
              self.fields.pop(field_name, None) # Use pop with None to avoid error if not found