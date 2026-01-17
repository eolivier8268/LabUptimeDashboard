import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Configuration via Environment Variable
# Default to localhost if not set, but you should set this in Docker
GATUS_URL = os.environ.get("GATUS_URL", "http://10.200.1.3:3002/api/v1/endpoints/statuses")

@app.route('/status')
def get_status():
    try:
        # 1. Fetch data from Gatus
        response = requests.get(GATUS_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
	
        # 2. Simplify the data
        simplified = {}
        
        # Handle case where Gatus returns an empty list
        if not data:
            return jsonify({})

        for service in data:
            # Safely get key and results
            key = service.get('key', 'unknown')
            results = service.get('results', [])
            
            # Default state if no results exist yet
            status_data = {
                "online": False,
                "code": 0,
                "latency": 0
            }
            
            # If we have history, grab the latest (last item)
            if results:
                latest = results[-1]
                is_online = latest.get('success', False)
                status_data = {
                    "online": "Online" if is_online else "Offline",
                    # "online": latest.get('success', False),
                    "code": latest.get('status', 0),
                    "latency": latest.get('duration', 0)
                }
            
            simplified[key] = status_data
            
        return jsonify(simplified)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Gatus: {e}")
        return jsonify({"error": "Failed to reach Gatus instance"}), 502
    except Exception as e:
        print(f"Internal Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Bind to 0.0.0.0 inside container so Docker can map it.
    # Security is handled by Docker port mapping in docker-compose.
    app.run(host='0.0.0.0', port=5000)
