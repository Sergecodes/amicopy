
TODO BACKEND:
    - fix s3 bucket and test obviously
    - handle file upload and limits too; link it with channels; test obviously
    - setup django-admin with grappelli
    - install django debug toolbar

    - optimize and test db queries (setup queryset and caching, including views and properties on models)
    (use prefetch_related! https://betterprogramming.pub/django-select-related-and-prefetch-related-f23043fd635d)
    - implement ALL todos (including celery expiration)


TESTS:
    - channels (see docs)
    - write test for forms, models, views
    - configure then test social auth with google and facebook
    - test docker
    - setup cors and websocket cors, 
    - setup frontend...


## Use cases to views/consumers:
# - create session: via api
# - end/close session: via websocket consumer command
# - join session: via websocket consumer comand; when joining, add constraint to prevent 
# using multiple browsers (like what whatsapp does);
# - leave session: websocket consumer
# - end session: via websocket consumer
# - allow/block new devices: via ws consumer
# - create transaction: websocket
# - delete transaction 4 single user(me): ws
# - delete transaction for all users: ws
# - delete session: api
# - get transactions(from session): api (note get thost that user hasn't deleted)
# - get transaction by uuid: api
# - pin session: api
# - bookmark transaction: api



NOTE:
** https://docs.djangoproject.com/en/4.0/topics/db/optimization/
** - https://github.com/Suor/django-cacheops
- https://github.com/django-cache-machine/django-cache-machine/blob/master/docs/index.rst
- https://github.com/jmoiron/johnny-cache

- https://medium.com/netscape/full-stack-django-quick-start-with-jwt-auth-and-react-redux-part-i-37853685ab57
- https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
- https://github.com/cure53/DOMPurify



TIPS:
- possibility to display graphs showing past sessions and transactions
(for golden users)


# source /home/sergeman/.virtualenvs/amicopy-env/bin/activate


# python3 -c 'import channels; print(channels.__version__)'


Note: for each page, search online for similar pages.
PAGES: total - 20
- home page: display what site is about, how to use, steps .. (ALSO USE SVG IMAGE VECTORS)
- pricing page: display monthly and yearly pricing, with differences between each plan
- session creation page (form)
- session detail page: (usage of websockets here with transactions displayed). see 
https://wordpress.ehr-crm.com/frontend-manager/dashboard responsivity
user should also see sessions that he's in, clicking on one should probably lead to a new page...
- User pages :
(login to hubs.docker.com and visit profile if possible use same structure of pages and even dropdown used)
(see https://id.atlassian.com/manage-profile/ too)
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

INSPIRATION...:
    - https://send-anywhere.com/#transfer
    
    HEADER: (see hubs.docker.com for more inspiration)
        Home; Create/join session dropdown(can call the dropdown New session); Upgrade (leads to pricing page); 
        Log in - Sign up; hubs.docker.com Profile dropdown; 
        light-dark mode switch(material ui or docs.docker.com)

    FOOTER: 
        ** oscend template in themeforest (https://themeforest.net/item/oscend-creative-agency-wordpress-theme/15583465)
        About, Social media(twitter, facebook), Newsletter, faq, 
        terms of service | privacy policy, feature request, 
