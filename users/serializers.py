import serpy

from core.fields import SerpyDateTimeField


class UserSerializer(serpy.Serializer):
    username = serpy.StrField()
    email = serpy.StrField()
    is_active = serpy.BoolField()
    is_staff = serpy.BoolField()
    joined_on = SerpyDateTimeField()
    deactivated_on = SerpyDateTimeField()
    is_normal = serpy.BoolField()
    can_use_rich_text_editor = serpy.BoolField()

    # Do this to prevent circular import
    pinned_session = serpy.MethodField()

    def get_pinned_session(self, user):
        from transactions.serializers import SessionSerializer

        session = user.pinned_session
        return {} if session is None else SessionSerializer(user.pinned_session).data

