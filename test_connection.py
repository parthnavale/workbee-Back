import requests
import time
import urllib3

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_vm_connection():
    print("Testing connection to VM...")
    print("URL: https://workbee.duckdns.org")
    
    try:
        # Test with a short timeout and disable SSL verification
        response = requests.get("https://workbee.duckdns.org", timeout=10, verify=False)
        print(f"✅ Connection successful! Status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        return True
    except requests.exceptions.ConnectTimeout:
        print("❌ Connection timeout - server not responding")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_vm_connection() 