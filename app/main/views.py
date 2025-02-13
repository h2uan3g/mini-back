from flask import render_template, request,current_app, abort, g
from . import main


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


# 慢SQL检测
@main.after_app_request
def after_request(response):
    queries = g.get('sqlalchemy_queries', [])
    for query in queries:
        if query.duration >= current_app.config['MINI_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n' %
                (query.statement, query.parameters, query.duration,
                 query.context))
    return response
