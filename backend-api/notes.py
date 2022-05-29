
TODO BACKEND:
    - use session auth
    - implement notifications(read/unread) on transactions. 
    eg. add m2m field read_by on Transaction ...
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



# source /home/sergeman/.virtualenvs/amicopy-env/bin/activate


# python3 -c 'import channels; print(channels.__version__)'
