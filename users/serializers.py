from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    email = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    joined_on = serializers.DateTimeField(read_only=True)
    deactivated_on = serializers.DateTimeField(read_only=True)
    is_normal = serializers.BooleanField(read_only=True)
    can_use_rich_text_editor = serializers.BooleanField(read_only=True)

    # Do this to prevent circular import
    pinned_session = serializers.SerializerMethodField()

    def get_pinned_session(self, user):
        from transactions.serializers import SessionSerializer

        session = user.pinned_session
        return {} if session is None else SessionSerializer(user.pinned_session).data




# class UserModelSerializer(DjoserUserSerializer):
#     pinned_session = serializers.SerializerMethodField()

#     class Meta(DjoserUserSerializer.Meta):
#         fields = [
#             'username', 'email', 'is_active', 'is_staff',
#             'joined_on', 'deactivated_on', 'is_normal',
#             'can_use_rich_text_editor', 'pinned_session'
#         ]
#         # read_only_fields = (settings.LOGIN_FIELD,)

#     def get_pinned_session(self, user):
#         from transactions.serializers import SessionSerializer

#         session = user.pinned_session
#         return {} if session is None else SessionSerializer(user.pinned_session).data



# class UserSerializer(serpy.Serializer):
#     username = serpy.StrField()
#     email = serpy.StrField()
#     is_active = serpy.BoolField()
#     is_staff = serpy.BoolField()
#     joined_on = SerpyDateTimeField()
#     deactivated_on = SerpyDateTimeField()
#     is_normal = serpy.BoolField()
#     can_use_rich_text_editor = serpy.BoolField()

#     # Do this to prevent circular import
#     pinned_session = serpy.MethodField()

#     def get_pinned_session(self, user):
#         from transactions.serializers import SessionSerializer

#         session = user.pinned_session
#         return {} if session is None else SessionSerializer(user.pinned_session).data

