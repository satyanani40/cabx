import os
from werkzeug.serving import run_simple


from cabx.utils import constants
from cabx import app

ENVIRONMENT = os.getenv("ENVIRONMENT", constants.LOCAL)
qvd_app = app.create_app("cabx", config_path="cabdx.utils.config", env=ENVIRONMENT)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help="Port number")
    args = parser.parse_args()

    if args.port:
        port = int(args.port)
    else:
        port = 8000
    host = '0.0.0.0'
    os.environ['ENVIRONMENT'] = ENVIRONMENT
    run_simple(host, port, qvd_app, use_reloader=True, use_debugger=True)

