from werkzeug.middleware.proxy_fix import ProxyFix

from app import app

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.debug = True
    app.run('0.0.0.0')
