import serpy

from core.fields import SerpyDateTimeField


class UserSerializer(serpy.Serializer):
    from transactions.serializers import SessionSerializer

    username = serpy.StrField()
    email = serpy.StrField()
    is_active = serpy.BoolField()
    is_staff = serpy.BoolField()
    joined_on = SerpyDateTimeField()
    deactivated_on = SerpyDateTimeField()
    pinned_session = SessionSerializer()
    is_normal = serpy.BoolField()
    
    can_use_rich_text_editor = serpy.BoolField()

