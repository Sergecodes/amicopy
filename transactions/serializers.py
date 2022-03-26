import serpy

from core.fields import SerpyDateTimeField
from users.serializers import UserSerializer


class DeviceSerializer(serpy.Serializer):
    browser_session_key = serpy.StrField()
    ip_address = serpy.StrField()
    display_name = serpy.StrField()
    deleted_on = SerpyDateTimeField()

    user = UserSerializer()


class SessionSerializer(serpy.Serializer):
    pk = serpy.IntField()
    uuid = serpy.StrField()
    title = serpy.StrField()
    creator_code = serpy.StrField()
    last_transaction_on = SerpyDateTimeField()
    is_active = serpy.BoolField()
    started_on = SerpyDateTimeField()
    ended_on = SerpyDateTimeField()
    expired_on = SerpyDateTimeField()

    group_name = serpy.StrField()
    creator_device = DeviceSerializer()
    all_devices = DeviceSerializer(many=True)
    present_devices = DeviceSerializer(many=True)


class TransactionSerializer(serpy.Serializer):
    title = serpy.StrField()
    text_content = serpy.StrField()
    files_archive_url = serpy.MethodField('get_file_url')
    created_on = SerpyDateTimeField()

    session = SessionSerializer()
    from_device = DeviceSerializer()
    to_devices = DeviceSerializer(many=True)

    def get_file_url(self, transaction):
        return transaction.files_archive.url



# class FullSessionSerializer(SessionSerializer):
#     """Serialize related many fields"""
#     all_devices = DeviceSerializer(many=True)
#     deleted_by = UserSerializer(many=True)
#     present_devices = DeviceSerializer(many=True)

