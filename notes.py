TODO:
    - work on consumers then test them(via selenium, see channels docs)
    - create get_absolute url for session, user
    - fix s3 bucket
    - handle file upload and limits too
    - setup django-admin with grappelli

TESTS:
    - transaction form widget yields that of appropriate user
    - 


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





        # Check if device has already been saved
        # (or use if device._state.adding = True)
        if device.pk:
            raise ValidationError(
                _('Device object is already saved, use only unsaved objects'),
                code='invalid'
            )

