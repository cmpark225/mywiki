## summary

한개의 필드에 대해서 데이터 검증이 필요할 경우 
=> field-level의 `.validate_<field_name>` 메소드를 Serializer 클래스에 만들면 된다. 

여러개 필드를 이용해서 데이터 검증을 해야할 경우에
=> validate() 메소드를 Serializer 클래스에 만들어 검증한다. 


## Field-level validation

You can specify custom field-level validation by adding `.validate_<field_name>` methods to your Serializer subclass. These are similar to the `.clean_<field_name>` methods on Django forms.

These methods take a single argument, which is the field value that requires validations.

Your `validate_<field_name>` methods should return the validated value or raise a serializers.ValidationError.

```
from rest_framework import serializers

class BlogPostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    content = serializers.CharField()

    def validate_title(self, value):
        """
        Check that the blog post is about Django.
        """
        if 'django' not in value.lower():
            raise serializers.ValidationError("Blog post is not about Django")
        return value
```

Note: If your `<field_name>` is declared on your serializer with the parameter required=False then this validation step will not take place if the field is not included.


## Object-level validation

To do any other validation that requires access to multiple fields, add a method called .validate() to your Serializer subclass. This method takes a single argument, which is a dictionary of field values. It should raise a ValidationError if necessary, or just return the validated values. 

```
from rest_framework import serializers

class EventSerializer(serializers.Serializer):
    description = serializers.CharField(max_length=100)
    start = serializers.DateTimeField()
    finish = serializers.DateTimeField()

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data
```
