import os
import sys
import click
from datetime import datetime

from flask import url_for
from flask_migrate import Migrate, upgrade
from app import create_app, db, fake
from app.models import User, Role, Permission, Product
from app.models.document import Document

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage

    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


@app.cli.command('deploy')
@click.option("--name", default="admin", help="设置超级管理员用户")
def deploy(name):
    upgrade()
    Role.insert_roles()
    user = User.query.filter_by(username=name).first()
    if user is not None:
        user.role = Role.query.filter_by(name='Administrator').first()
        db.session.commit()

@app.cli.command('fake-cli')
@click.option("--name", default="user", help="创建用户模拟数据")
def fake_cli(name):
    if name == 'user':
        fake.users(50)
    if name == 'news':
        fake.news(50) 


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False,
              help='Run tests under code coverage.')
def test(coverage):
    """测试覆盖率."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file.py://%s/index.html' % covdir)
        COV.erase()


@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    if __name__ == "__main__":
        app.run(debug=False)


@app.shell_context_processor
def make_shell_context():
    """数据库命令行"""
    return dict(db=db, User=User, Role=Role, product=Product, Permission=Permission, Document=Document)
