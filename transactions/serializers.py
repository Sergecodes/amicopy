import serpy

from core.fields import SerpyDateTimeField
from users.serializers import UserSerializer


class DeviceSerializer(serpy.Serializer):
    # browser_session_key = serpy.StrField()
    # ip_address = serpy.StrField()
    # deleted_on = SerpyDateTimeField()
    uuid = serpy.StrField()
    display_name = serpy.StrField()
    user = UserSerializer()


class SessionSerializer(serpy.Serializer):
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
    all_devices = serpy.MethodField()
    present_devices = serpy.MethodField()
    # present_devices = DeviceSerializer(many=True, attr='present_devices.all', call=True)

    def get_all_devices(self, session):
        return DeviceSerializer(session.all_devices.select_related('user'), many=True).data

    def get_present_devices(self, session):
        return DeviceSerializer(session.present_devices.select_related('user'), many=True).data


class TransactionSerializer(serpy.Serializer):
    uuid = serpy.StrField()
    title = serpy.StrField()
    text_content = serpy.StrField()
    files_archive_url = serpy.MethodField('get_file_url')
    created_on = SerpyDateTimeField()

    session = SessionSerializer()
    from_device = DeviceSerializer()
    to_devices = serpy.MethodField()

    def get_file_url(self, transaction):
        return transaction.files_archive.url

    def get_to_devices(self, transaction):
        return DeviceSerializer(transaction.to_devices.select_related('user'), many=True).data



# class FullSessionSerializer(SessionSerializer):
#     """Serialize related many fields"""
#     all_devices = DeviceSerializer(many=True)
#     deleted_by = UserSerializer(many=True)
#     present_devices = DeviceSerializer(many=True)

