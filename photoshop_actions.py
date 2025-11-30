"""
General-purpose Photoshop API executor.
Executes Photoshop actions defined in JSON files on images.
"""

import os
import sys
import json
import re
import time
import requests
import dropbox
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# Configuration - Load from environment variables
# ============================================================================
DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# ============================================================================
# Helper Functions
# ============================================================================

def get_access_token(client_id, client_secret):
    """Get Adobe access token using client credentials."""
    params = {
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
        'scope': 'openid,AdobeID,read_organizations,firefly_api,ff_apis'
    }
    response = requests.post(
        f'https://ims-na1.adobelogin.com/ims/token/v2?client_id={client_id}', 
        data=params
    )
    return response.json().get('access_token')

def remove_json_comments(json_string):
    """Remove comments from a JSON string, being careful not to remove // inside string values."""
    lines = json_string.split('\n')
    cleaned_lines = []
    in_string = False
    escape_next = False
    
    for line in lines:
        cleaned_line = []
        i = 0
        while i < len(line):
            char = line[i]
            
            if escape_next:
                cleaned_line.append(char)
                escape_next = False
                i += 1
                continue
            
            if char == '\\':
                escape_next = True
                cleaned_line.append(char)
                i += 1
                continue
            
            if char == '"':
                in_string = not in_string
                cleaned_line.append(char)
                i += 1
                continue
            
            # Only remove // if we're not inside a string
            if not in_string and char == '/' and i + 1 < len(line) and line[i + 1] == '/':
                # Found a comment - skip the rest of the line
                break
            
            cleaned_line.append(char)
            i += 1
        
        cleaned_lines.append(''.join(cleaned_line))
    
    result = '\n'.join(cleaned_lines)
    # Remove multi-line comments (but be careful with strings)
    # For multi-line comments, we need a more careful approach
    # Simple approach: remove /* */ comments that don't span strings
    result = re.sub(r'/\*[\s\S]*?\*/', '', result)
    return result.strip()

def download_image(url, file_path):
    """Download an image from a URL and save it to a file."""
    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(file_path) if os.path.dirname(file_path) else '.', exist_ok=True)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded successfully and saved to {file_path}")
            return file_path
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while downloading image: {e}")
        return None

def load_action_json_from_file(json_file_path):
    """
    Load action JSON from a file.
    
    Args:
        json_file_path: Path to the JSON file containing action JSON
    
    Returns:
        Action JSON array, or None if failed
    """
    try:
        with open(json_file_path, 'r') as f:
            content = f.read()
            # Remove comments if any
            content = remove_json_comments(content)
            action_json = json.loads(content)
            return action_json
    except Exception as e:
        print(f"Error loading action JSON from file: {e}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================================
# Main Processing Function
# ============================================================================

def execute_photoshop_action(input_image_path, action_json_file, output_image_path=None):
    """
    Execute a Photoshop action JSON on an image using Adobe Photoshop API.
    
    Args:
        input_image_path: Path to the input image file
        action_json_file: Path to JSON file containing the action JSON
        output_image_path: Optional path for output image (default: auto-generated)
    
    Returns:
        Path to the processed image file, or None if processing failed
    """
    # Validate environment variables
    if not DROPBOX_ACCESS_TOKEN:
        print("Error: DROPBOX_ACCESS_TOKEN not found in environment variables")
        return None
    if not CLIENT_ID:
        print("Error: CLIENT_ID not found in environment variables")
        return None
    if not CLIENT_SECRET:
        print("Error: CLIENT_SECRET not found in environment variables")
        return None
    
    # Validate input file exists
    if not os.path.exists(input_image_path):
        print(f"Error: Input image file not found: {input_image_path}")
        return None
    
    # Validate action JSON file exists
    if not os.path.exists(action_json_file):
        print(f"Error: Action JSON file not found: {action_json_file}")
        return None
    
    # Load action JSON
    action_json_array = load_action_json_from_file(action_json_file)
    if action_json_array is None:
        print("Error: Failed to load action JSON from file")
        return None
    
    print(f"Action JSON loaded: {json.dumps(action_json_array, indent=2)}")
    
    # Initialize Dropbox client
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    
    # Upload input image to Dropbox
    file_name = os.path.basename(input_image_path)
    dropbox_input_path = f'/{file_name}'
    
    print(f"Uploading image to Dropbox: {dropbox_input_path}")
    with open(input_image_path, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_input_path, mode=dropbox.files.WriteMode.overwrite)
    
    # Get Dropbox temporary link for input
    input_link = dbx.files_get_temporary_link(dropbox_input_path).link
    print(f"Input link: {input_link}")
    
    # Prepare output path - use UUID for Dropbox to avoid conflicts
    # (final output filename will be set later)
    output_file_name = f'temp_{file_name}'
    output_file_path = f'/{output_file_name}'
    
    # Get Dropbox temporary upload link for output
    output_link = dbx.files_get_temporary_upload_link(
        commit_info=dropbox.files.CommitInfo(
            path=output_file_path, 
            mode=dropbox.files.WriteMode.overwrite
        )
    )
    print(f"Output path: {output_file_path}")
    
    # Prepare data for Adobe API
    data = {
        "inputs": [{"storage": "dropbox", "href": input_link}],
        "options": {"actionJSON": action_json_array},
        "outputs": [{
            "storage": "dropbox", 
            "type": "image/vnd.adobe.photoshop", 
            "href": output_link.link
        }]
    }
    
    # Get Adobe access token
    print("Getting Adobe access token...")
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    if not access_token:
        print("Error: Failed to get Adobe access token")
        return None
    
    # Call Adobe Photoshop API
    print("Calling Adobe Photoshop API...")
    response = requests.post(
        'https://image.adobe.io/pie/psdService/actionJSON',
        headers={
            'Authorization': f'Bearer {access_token}',
            'x-api-key': CLIENT_ID
        },
        json=data
    )
    
    result = response.json()
    print(f"API Response: {json.dumps(result, indent=2)}")
    
    # Poll for job status
    status = "running"
    job_result = None
    print("Polling for job status...")
    
    while status == "running" or status == "pending":
        job_response = requests.get(
            result['_links']['self']['href'], 
            headers={
                'Authorization': f'Bearer {access_token}',
                'x-api-key': CLIENT_ID
            }
        )
        job_result = job_response.json()
        status = job_result["outputs"][0]['status']
        print(f"Job status: {status}")
        time.sleep(1)
    
    print(f"Job completed. Final result: {json.dumps(job_result, indent=2)}")
    
    # Get shared link for the output file
    try:
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(output_file_path)
    except Exception as e:
        # Link already exists, get the existing one
        shared_link_metadata = e.error.get_shared_link_already_exists().get_metadata()
    
    common_link = shared_link_metadata.url
    direct_link = common_link.replace("www.dropbox.com", "dl.dropboxusercontent.com").replace("dl=0", "dl=1")
    print(f"Download link: {direct_link}")
    
    # Download the processed image
    os.makedirs("output_images", exist_ok=True)
    
    # Generate output path with _output suffix for 1-1 mapping
    if output_image_path is None:
        # Get base filename without directory path
        base_name = os.path.basename(input_image_path)
        # Split filename and extension
        name_without_ext, ext = os.path.splitext(base_name)
        # Create output filename: original_name_output.ext
        output_filename = f"{name_without_ext}_output{ext}"
        output_image_path = os.path.join("output_images", output_filename)
    
    # Download and save the image
    downloaded_path = download_image(direct_link, output_image_path)
    
    if downloaded_path:
        print(f"Successfully processed image saved to: {downloaded_path}")
        return downloaded_path
    else:
        print("Failed to download processed image")
        return None

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python aeroplane_remove.py <input_image_path> <action_json_file> [output_image_path]")
        print("\nExample:")
        print("  python aeroplane_remove.py input_images/image.jpg action.json")
        print("  python aeroplane_remove.py input_images/image.jpg action.json output_images/result.jpg")
        sys.exit(1)
    
    input_path = sys.argv[1]
    action_json_file = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    result_path = execute_photoshop_action(input_path, action_json_file, output_path)
    
    if result_path:
        print(f"\n✓ Success! Processed image saved to: {result_path}")
        sys.exit(0)
    else:
        print("\n✗ Failed to process image")
        sys.exit(1)
