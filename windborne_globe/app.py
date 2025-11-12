from flask import Flask, render_template, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

def fetch_windborne_balloons():
    """Fetch current balloon positions from Windborne API."""
    url = "https://a.windbornesystems.com/treasure/00.json"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Data format: [[lat, lon, alt_km], ...]
            balloons = []
            for item in data:
                if isinstance(item, list) and len(item) >= 3:
                    balloons.append({
                        'lat': float(item[0]),
                        'lon': float(item[1]),
                        'alt_km': float(item[2])
                    })
            
            logging.info(f"Fetched {len(balloons)} balloons")
            return balloons
            
    except Exception as e:
        logging.error(f"Error fetching Windborne: {e}")
        return []

def fetch_nasa_events():
    """Fetch active natural events from NASA EONET."""
    url = "https://eonet.gsfc.nasa.gov/api/v3/events?status=open&limit=100"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            
            events = []
            for event in data['events']:
                if event.get('geometry'):
                    # Get latest position
                    coords = event['geometry'][-1]['coordinates']
                    
                    events.append({
                        'title': event['title'],
                        'category': event['categories'][0]['title'],
                        'lat': float(coords[1]),
                        'lon': float(coords[0]),
                        'date': event['geometry'][-1].get('date', '')
                    })
            
            logging.info(f"Fetched {len(events)} NASA events")
            return events
            
    except Exception as e:
        logging.error(f"Error fetching NASA EONET: {e}")
        return []

@app.route('/')
def index():
    """Serve the main visualization page."""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """
    Main API endpoint - returns combined data.
    """
    try:
        balloons = fetch_windborne_balloons()
        events = fetch_nasa_events()
        
        # Simple stats
        event_categories = {}
        for event in events:
            cat = event['category']
            event_categories[cat] = event_categories.get(cat, 0) + 1
        
        return jsonify({
            'success': True,
            'timestamp': datetime.utcnow().isoformat(),
            'balloons': balloons,
            'events': events,
            'stats': {
                'balloon_count': len(balloons),
                'event_count': len(events),
                'event_categories': event_categories
            }
        })
        
    except Exception as e:
        logging.error(f"Error in /api/data: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
