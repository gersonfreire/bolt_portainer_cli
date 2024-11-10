#!/usr/bin/env python3

import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv

class PortainerAPI:
    def __init__(self, base_url: str, verify_ssl: bool = False):
        self.base_url = base_url.rstrip('/')
        self.verify_ssl = verify_ssl
        self.auth_token = None

    def _create_ssl_context(self) -> ssl.SSLContext:
        if self.verify_ssl:
            return ssl.create_default_context()
        else:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            return ctx

    def _make_request(self, endpoint: str, method: str = 'GET', data: Optional[Dict] = None,
                     headers: Optional[Dict] = None) -> Tuple[Dict, int]:
        url = f"{self.base_url}{endpoint}"
        default_headers = {'Content-Type': 'application/json'}
        if self.auth_token:
            default_headers['Authorization'] = f'Bearer {self.auth_token}'
        
        if headers:
            default_headers.update(headers)

        ctx = self._create_ssl_context()
        
        try:
            request = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8') if data else None,
                headers=default_headers,
                method=method
            )
            
            with urllib.request.urlopen(request, context=ctx) as response:
                return json.loads(response.read().decode('utf-8')), response.status
                
        except urllib.error.HTTPError as e:
            error_message = e.read().decode('utf-8')
            try:
                error_data = json.loads(error_message)
            except json.JSONDecodeError:
                error_data = {'message': error_message}
            return error_data, e.code
        except urllib.error.URLError as e:
            return {'message': f'Connection error: {str(e.reason)}'}, 500
        except Exception as e:
            return {'message': f'Unexpected error: {str(e)}'}, 500

    def authenticate(self, username: str, password: str) -> bool:
        data = {
            'Username': username,
            'Password': password
        }
        
        response, status = self._make_request('/api/auth', 'POST', data)
        
        if status == 200 and 'jwt' in response:
            self.auth_token = response['jwt']
            return True
        return False

    def get_status(self) -> Dict:
        return self._make_request('/api/status')[0]

    def get_endpoints(self) -> Dict:
        return self._make_request('/api/endpoints')[0]

def load_env_file() -> Dict[str, str]:
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except FileNotFoundError:
        pass
    return env_vars

def main():
    parser = argparse.ArgumentParser(description='Portainer CLI Tool')
    parser.add_argument('url', nargs='?', help='Portainer server URL')
    parser.add_argument('username', nargs='?', help='Portainer username')
    parser.add_argument('password', nargs='?', help='Portainer password')
    parser.add_argument('--verify-ssl', action='store_true', help='Verify SSL certificate')
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()

    url = args.url or os.getenv('PORTAINER_URL')
    username = args.username or os.getenv('PORTAINER_USERNAME')
    password = args.password or os.getenv('PORTAINER_PASSWORD')
    verify_ssl = args.verify_ssl or os.getenv('PORTAINER_VERIFY_SSL', '').lower() == 'true'

    if not all([url, username, password]):
        print("Error: Missing required parameters. Please provide them via command line or .env file.")
        parser.print_help()
        sys.exit(1)

    api = PortainerAPI(url, verify_ssl)

    print(f"\nConnecting to Portainer at {url}...")
    
    if not api.authenticate(username, password):
        print("Authentication failed. Please check your credentials.")
        sys.exit(1)

    print("Authentication successful!")

    # Get and display status
    print("\nRetrieving server status...")
    status = api.get_status()
    print(f"Version: {status.get('Version', 'N/A')}")
    print(f"Instance ID: {status.get('InstanceID', 'N/A')}")

    # Get and display endpoints
    print("\nRetrieving endpoints...")
    endpoints = api.get_endpoints()
    if isinstance(endpoints, list):
        print(f"\nFound {len(endpoints)} endpoint(s):")
        for endpoint in endpoints:
            print(f"\nEndpoint: {endpoint.get('Name', 'N/A')}")
            print(f"ID: {endpoint.get('Id', 'N/A')}")
            print(f"Type: {endpoint.get('Type', 'N/A')}")
            print(f"URL: {endpoint.get('URL', 'N/A')}")
            print(f"Status: {'Active' if endpoint.get('Status', 0) == 1 else 'Inactive'}")
    else:
        print("No endpoints found or error retrieving endpoints.")

if __name__ == '__main__':
    main()