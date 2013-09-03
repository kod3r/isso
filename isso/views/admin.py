# -*- encoding: utf-8 -*-
#
# Copyright 2012, Martin Zimmermann <info@posativ.org>. All rights reserved.
# License: BSD Style, 2 clauses. see isso/__init__.py

from os.path import join, dirname

from werkzeug.wrappers import Response
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from itsdangerous import SignatureExpired, BadSignature


def index(app, environ, request):

    if request.method == 'POST':
        print request.form.get('secret'), app.signer.secret_key
        if request.form.get('secret') == app.signer.secret_key:
            resp = redirect('/admin/', 301)
            resp.set_cookie('admin', app.signer.dumps('*'), max_age=app.MAX_AGE)
            return resp
        else:
            return abort(403)
    else:
        try:
            app.unsign(request.cookies.get('admin', ''))
        except (SignatureExpired, BadSignature):
            return Response(app.render('login.j2'), content_type='text/html')

    ctx = {'app': app, 'request': request}
    return Response(app.render('admin.j2', app=app, request=request), content_type='text/html')