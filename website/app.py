import os
import sys
from flask import Flask, send_from_directory, abort, make_response

app = Flask(__name__, static_folder=None)

# Set default port
DEFAULT_PORT = 80

# Get current directory
web_dir = os.path.dirname(os.path.abspath(__file__))

def add_cache_headers(response, max_age=3600):
    response.headers['Cache-Control'] = f'public, max-age={max_age}'
    return response

@app.route('/')
def home():
    response = make_response(send_from_directory(web_dir, 'index.html'))
    return add_cache_headers(response, 3600) # 1 hour for HTML

@app.route('/moments')
@app.route('/moments/')
def moments():
    moments_dir = os.path.join(web_dir, 'moments')
    response = make_response(send_from_directory(moments_dir, 'index.html'))
    return add_cache_headers(response, 3600) # 1 hour for HTML

@app.route('/moments/policy')
@app.route('/moments/policy/')
def moments_policy():
    moments_dir = os.path.join(web_dir, 'moments')
    response = make_response(send_from_directory(moments_dir, 'policy.html'))
    return add_cache_headers(response, 3600) # 1 hour for HTML

@app.route('/<path:filename>')
def static_files(filename):
    # Prevent serving app.py itself or hidden files
    if filename == 'app.py' or filename.startswith('.') or '/.' in filename:
        abort(404)
    
    response = make_response(send_from_directory(web_dir, filename))
    
    # Add caching based on file extension
    if filename.endswith(('.css', '.js', '.png', '.jpg', '.svg')):
        add_cache_headers(response, 86400) # 1 day for assets
    else:
        add_cache_headers(response, 0) # No cache for others
        
    return response

def main(port=DEFAULT_PORT):
    try:
        print(f"Starting Flask server on http://localhost:{port}")
        print(f"Root directory: {web_dir}")
        # In production, use a WSGI server. For this script, app.run is fine.
        app.run(host='0.0.0.0', port=port)
    except OSError as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Port must be an integer")
            sys.exit(1)
    main(port)
