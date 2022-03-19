TODO:
    - create user views
    - fix s3 bucket
    - handle file upload and limits too; link it with channels
    - setup django-admin with grappelli

TESTS:
    - transaction form widget yields that of appropriate user
    - channels
    - duplicate session uuid

- write test for forms, models, views
- test docker


# source /home/sergeman/.virtualenvs/amicopy-env/bin/activate
# python3 -c 'import channels; print(channels.__version__)'


Note: for each page, search online for similar pages.
PAGES: total - 20
- home page: display what site is about, how to use, steps .. (ALSO USE SVG IMAGE VECTORS)
- pricing page: display monthly and yearly pricing, with differences between each plan
- session creation page (form)
- ongoing / present session page: (usage of websockets here with transactions displayed).
user should also see sessions that he's in, clicking on one should probably lead to a new page...
- User pages :
(login to hubs.docker.com and visit profile if possible use same structure of pages and even dropdown used)
    - clipboard(display past sessions and corresponding transactions) 
    - profile
    - settings
    - billing
- Payment pages: see hubs.docker.com 
    - check out
    - payment confirmed
    - payment failed
- signup page
- login page 
- post email confirmation: welcome user to the site, their email has been confirmed
- change password 
- reset / forgot password 
- faq
- feature request(just use modal)
- privacy policy 
- terms of service


HEADER: (see hubs.docker.com for more inspiration)
    Home; Create/join session dropdown(can call the dropdown New session); Upgrade (leads to pricing page); 
    Log in - Sign up; hubs.docker.com Profile dropdown; 
    light-dark mode switch(material ui or docs.docker.com)

FOOTER: 
    ** oscend template in themeforest (https://themeforest.net/item/oscend-creative-agency-wordpress-theme/15583465)
    About, Social media(twitter, facebook), Newsletter, faq, 
    terms of service | privacy policy, feature request, 




# See django-channels examples / multichat githup repo

class SessionConsumer(WebsocketConsumer):
    def connect(self):
        self.session_uuid = self.scope['url_route']['kwargs']['session_uuid']
        self.session_group_name = 'session_%s' % self.session_uuid
        self.session = Session.objects.get(uuid=self.session_uuid)

        request = self.scope
        user = request.user

        if user.is_anonymous:
            browser_key = request.session._get_or_create_session_key()
            ip, is_routable = get_client_ip(request)
            Device.objects.create(ip_address=ip)

        # Join session group
        async_to_sync(self.channel_layer.group_add)(
            self.session_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave session group
        async_to_sync(self.channel_layer.group_discard)(
            self.session_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        message = text_data_json['message']

        # Send message to session group
        async_to_sync(self.channel_layer.group_send)(
            self.session_group_name,
            {
                'type': command,
                'message': message
            }
        )

    # Join session group
    def join_session(self, event):
        request = self.scope
        user = request.user
        ip, is_routable = get_client_ip(request)
        browser_id = request.session._get_or_create_session_key()
        new_device = Device.objects.create(
            ip_address=ip, 
            display_name=event['display_name'],
            browser_session_key=browser_id, 
            user=user if user.is_authenticated else None
        )

        self.session.add_device(new_device)

        # Join session group
        async_to_sync(self.channel_layer.group_add)(
            self.session_group_name,
            self.channel_name
        )

    # Receive message from session group
    def group_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

        