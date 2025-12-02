"""
General-purpose Photoshop API executor.
Executes Photoshop actions defined in JSON files on one or more images.
Supports both single and multiple input images.
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
# Helper Function for Direct API Calls
# ============================================================================

def process_photoshop_actionjson(
    input_links,
    action_json,
    output_link,
    storage="dropbox",
    output_type="image/vnd.adobe.photoshop"
):
    """
    Process images using Adobe Photoshop API with actionJSON and multiple input images.
    This is a lower-level function that works directly with URLs/links.
    
    Args:
        input_links: Single URL string or list of input image URLs/links (Dropbox links, URLs, etc.)
        action_json: Action JSON as string, list, or dict. If string, comments will be removed.
        output_link: Output link where the processed image will be saved
        storage: Storage type (default: "dropbox")
        output_type: Output file type (default: "image/vnd.adobe.photoshop")
        
    Returns:
        Dictionary containing the job result with status and output information
        
    Example:
        >>> input_links = [
        ...     "https://dl.dropboxusercontent.com/s/.../image1.jpg",
        ...     "https://dl.dropboxusercontent.com/s/.../image2.jpg"
        ... ]
        >>> action_json = '[{"_obj": "select", ...}]'
        >>> output_link = "https://dl.dropboxusercontent.com/s/.../output.psd"
        >>> result = process_photoshop_actionjson(
        ...     input_links=input_links,
        ...     action_json=action_json,
        ...     output_link=output_link,
        ...     client_id=CLIENT_ID,
        ...     client_secret=CLIENT_SECRET
        ... )
    """
    # Normalize input_links to list
    if isinstance(input_links, str):
        input_links = [input_links]
    
    # Prepare inputs array
    inputs = [{"storage": storage, "href": link} for link in input_links]
    
    # Process action JSON
    if isinstance(action_json, str):
        # Remove comments if it's a string
        action_json_cleaned = remove_json_comments(action_json)
        try:
            action_json_array = json.loads(action_json_cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON data: {e}")
    elif isinstance(action_json, dict):
        action_json_array = [action_json]
    else:
        action_json_array = action_json
    
    # Prepare request data
    data = {
        "inputs": inputs,
        "options": {"actionJSON": action_json_array},
        "outputs": [{
            "storage": storage,
            "type": output_type,
            "href": output_link
        }]
    }
    
    # Get access token
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    if not access_token:
        raise Exception("Failed to get Adobe access token")
    
    # Make API request
    response = requests.post(
        'https://image.adobe.io/pie/psdService/actionJSON',
        headers={
            'Authorization': f'Bearer {access_token}',
            'x-api-key': CLIENT_ID
        },
        json=data
    )
    
    if response.status_code != 200 and response.status_code != 202:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")
    
    result = response.json()
    
    # Poll for job completion
    status = "running"
    job_result = None
    
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
        
        if status == "running" or status == "pending":
            time.sleep(1)
    
    if status != "succeeded":
        raise Exception(f"Job failed with status: {status}. Result: {job_result}")
    
    return job_result

# ============================================================================
# Composite Document Function (Multiple Images)
# ============================================================================

def create_composite_and_apply_action(input_image_paths, action_json_file=None, output_image_path=None):
    """
    Create a composite PSD from multiple images and optionally apply an action JSON.
    Uses the createDocument endpoint to combine multiple images as layers.
    
    Args:
        input_image_paths: List of paths to input image files (at least 2 required)
        action_json_file: Optional path to JSON file containing the action JSON
        output_image_path: Optional path for output image (default: auto-generated)
    
    Returns:
        Path to the processed image file, or None if processing failed
    """
    import uuid
    
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
    
    # Validate we have at least 2 inputs
    if len(input_image_paths) < 2:
        print("Error: Composite mode requires at least 2 input images")
        return None
    
    # Validate input files exist
    for input_path in input_image_paths:
        if not os.path.exists(input_path):
            print(f"Error: Input image file not found: {input_path}")
            return None
    
    # Load action JSON if provided
    action_json_array = None
    if action_json_file:
        if not os.path.exists(action_json_file):
            print(f"Error: Action JSON file not found: {action_json_file}")
            return None
        action_json_array = load_action_json_from_file(action_json_file)
        if action_json_array is None:
            print("Error: Failed to load action JSON from file")
            return None
        print(f"Action JSON loaded: {json.dumps(action_json_array, indent=2)}")
    
    # Initialize Dropbox client
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    
    # Upload all input images to Dropbox
    input_links = []
    dropbox_input_paths = []
    
    for idx, input_path in enumerate(input_image_paths):
        file_name = os.path.basename(input_path)
        unique_id = str(uuid.uuid4())[:8]
        dropbox_input_path = f'/composite_input_{unique_id}_{file_name}'
        dropbox_input_paths.append(dropbox_input_path)
        
        print(f"Uploading input {idx + 1}/{len(input_image_paths)} to Dropbox: {dropbox_input_path}")
        with open(input_path, 'rb') as f:
            dbx.files_upload(f.read(), dropbox_input_path, mode=dropbox.files.WriteMode.overwrite)
        
        input_link = dbx.files_get_temporary_link(dropbox_input_path).link
        input_links.append(input_link)
        print(f"Input {idx + 1} link: {input_link}")
    
    # Prepare composite output path with unique ID
    unique_id = str(uuid.uuid4())[:8]
    base_file_name = os.path.basename(input_image_paths[0])
    composite_output_name = f'composite_{unique_id}_{os.path.splitext(base_file_name)[0]}.psd'
    composite_output_path = f'/{composite_output_name}'
    
    # Get robust upload link for composite
    upload_link_url = "https://api.dropboxapi.com/2/files/get_temporary_upload_link"
    upload_link_headers = {
        "Authorization": f"Bearer {DROPBOX_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    upload_link_payload = {
        "commit_info": {
            "path": composite_output_path,
            "mode": {
                ".tag": "overwrite"
            },
            "mute": False
        },
        "duration": 3600
    }
    
    upload_link_response = requests.post(upload_link_url, headers=upload_link_headers, json=upload_link_payload)
    if upload_link_response.status_code != 200:
        print(f"Error: Failed to generate upload link: {upload_link_response.text}")
        return None
    
    composite_upload_link = upload_link_response.json().get('link')
    print(f"Composite output path: {composite_output_path}")
    
    # Get Adobe access token
    print("Getting Adobe access token...")
    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    if not access_token:
        print("Error: Failed to get Adobe access token")
        return None
    
    # Step 1: Create composite document using createDocument endpoint
    # Name layers based on expected names in action JSON (Base Image, Overlay Image)
    # Layers are added in order: first layer is top, last layer is bottom
    # For 2 inputs: first=input[0] (top/overlay), second=input[1] (bottom/base)
    print("Creating composite document with multiple layers...")
    
    # Build layers array
    # In Photoshop API, first layer in array = bottom layer, last = top layer
    # For 2 inputs: input[0] = base (bottom), input[1] = overlay (top)
    layers = []
    if len(input_image_paths) == 2:
        # Two inputs: first input is base (bottom), second input is overlay (top)
        layers = [
            {
                "type": "layer",
                "name": "Base Image",
                "input": {
                    "storage": "dropbox",
                    "href": input_links[0]  # First input = base (bottom)
                }
            },
            {
                "type": "layer",
                "name": "Overlay Image",
                "input": {
                    "storage": "dropbox",
                    "href": input_links[1]  # Second input = overlay (top)
                }
            }
        ]
    else:
        # More than 2 inputs: name them sequentially
        for i in range(len(input_image_paths)):
            layer_name = f"Layer {i+1}"
            if i == 0:
                layer_name = "Overlay Image"
            elif i == len(input_image_paths) - 1:
                layer_name = "Base Image"
            layers.append({
                "type": "layer",
                "name": layer_name,
                "input": {
                    "storage": "dropbox",
                    "href": input_links[i]
                }
            })
    
    create_doc_data = {
        "options": {
            "document": {
                "height": 2000,
                "width": 2000,
                "resolution": 300,
                "fill": "transparent",
                "mode": "rgb"
            },
            "layers": layers
        },
        "outputs": [{
            "storage": "dropbox",
            "type": "image/vnd.adobe.photoshop",
            "href": composite_upload_link
        }]
    }
    
    response = requests.post(
        'https://image.adobe.io/pie/psdService/documentCreate',
        headers={
            'Authorization': f'Bearer {access_token}',
            'x-api-key': CLIENT_ID,
            'Content-Type': 'application/json'
        },
        json=create_doc_data
    )
    
    result = response.json()
    print(f"Create Document API Response: {json.dumps(result, indent=2)}")
    
    if '_links' not in result:
        print(f"Error: API call failed - {result}")
        return None
    
    # Poll for job status
    status = "running"
    job_result = None
    print("Polling for createDocument job status...")
    
    while status == "running" or status == "pending":
        job_response = requests.get(
            result['_links']['self']['href'], 
            headers={
                'Authorization': f'Bearer {access_token}',
                'x-api-key': CLIENT_ID
            }
        )
        job_result = job_response.json()
        status = job_result.get("outputs", [{}])[0].get('status', 'failed')
        print(f"Job status: {status}")
        time.sleep(1)
    
    if status != "succeeded":
        print(f"Create document failed with status: {status}")
        print(f"Full job result: {json.dumps(job_result, indent=2)}")
        return None
    
    print("Composite document created successfully!")
    
    # Step 2: If action JSON provided, apply it to the composite
    final_output_path = composite_output_path
    
    if action_json_array:
        print("\nApplying action JSON to composite document...")
        
        # Get link to the created composite PSD
        composite_read_link = dbx.files_get_temporary_link(composite_output_path).link
        
        # Wait a moment for Dropbox to fully process the first file
        time.sleep(2)
        
        # Prepare new output path for final result with unique ID
        final_unique_id = str(uuid.uuid4())[:8]
        final_output_name = f'final_{final_unique_id}_{os.path.splitext(base_file_name)[0]}.psd'
        final_output_path = f'/{final_output_name}'
        print(f"Final output path: {final_output_path}")
        
        # Get upload link for final output
        final_upload_payload = {
            "commit_info": {
                "path": final_output_path,
                "mode": {
                    ".tag": "overwrite"
                },
                "mute": False
            },
            "duration": 3600
        }
        
        final_upload_response = requests.post(upload_link_url, headers=upload_link_headers, json=final_upload_payload)
        if final_upload_response.status_code != 200:
            print(f"Error: Failed to generate final upload link: {final_upload_response.text}")
            return None
        
        final_output_link_url = final_upload_response.json().get('link')
        
        # Apply action JSON
        # print(composite_read_link, 'composite_read_link');
        action_data = {
            "inputs": [{"storage": "dropbox", "href": composite_read_link}],
            "options": {"actionJSON": action_json_array},
            "outputs": [{
                "storage": "dropbox",
                "type": "image/vnd.adobe.photoshop",
                "href": final_output_link_url
            }]
        }
        
        action_response = requests.post(
            'https://image.adobe.io/pie/psdService/actionJSON',
            headers={
                'Authorization': f'Bearer {access_token}',
                'x-api-key': CLIENT_ID,
                'Content-Type': 'application/json'
            },
            json=action_data
        )
        
        action_result = action_response.json()
        print(f"Action JSON API Response: {json.dumps(action_result, indent=2)}")
        
        if '_links' not in action_result:
            print(f"Error: Action API call failed - {action_result}")
            return None
        
        # Poll for action job status
        status = "running"
        print("Polling for action job status...")
        
        while status == "running" or status == "pending":
            job_response = requests.get(
                action_result['_links']['self']['href'],
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'x-api-key': CLIENT_ID
                }
            )
            job_result = job_response.json()
            status = job_result.get("outputs", [{}])[0].get('status', 'failed')
            print(f"Job status: {status}")
            time.sleep(1)
        
        if status != "succeeded":
            print(f"Action JSON failed with status: {status}")
            print(f"Full job result: {json.dumps(job_result, indent=2)}")
            return None
        
        print("Action JSON applied successfully!")
    
    # Download the result
    print(f"\nDownloading result from: {final_output_path}")
    
    # Determine local output path
    if output_image_path:
        local_output_path = output_image_path
    else:
        base_name = os.path.splitext(base_file_name)[0]
        local_output_path = f'output_images/{base_name}_composite.psd'
    
    # Download from Dropbox
    os.makedirs(os.path.dirname(local_output_path) if os.path.dirname(local_output_path) else '.', exist_ok=True)
    metadata, response = dbx.files_download(final_output_path)
    with open(local_output_path, 'wb') as f:
        f.write(response.content)
    
    print(f"Composite saved to: {local_output_path}")
    
    # Cleanup Dropbox files
    try:
        for path in dropbox_input_paths:
            dbx.files_delete_v2(path)
        if final_output_path != composite_output_path:
            dbx.files_delete_v2(composite_output_path)
        dbx.files_delete_v2(final_output_path)
    except Exception as e:
        print(f"Warning: Could not clean up some Dropbox files: {e}")
    
    return local_output_path

# ============================================================================
# Main Processing Function
# ============================================================================

def execute_photoshop_action(input_image_paths, action_json_file, output_image_path=None):
    """
    Execute a Photoshop action JSON on one or more images using Adobe Photoshop API.
    
    Args:
        input_image_paths: Path to a single input image file (str) or list of paths (List[str])
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
    
    # Normalize input to list (support both single path and list of paths)
    if isinstance(input_image_paths, str):
        input_image_paths = [input_image_paths]
    elif not isinstance(input_image_paths, list):
        print(f"Error: input_image_paths must be a string or list of strings, got {type(input_image_paths)}")
        return None
    
    # Validate all input files exist
    for input_path in input_image_paths:
        if not os.path.exists(input_path):
            print(f"Error: Input image file not found: {input_path}")
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
    
    print(f"Processing {len(input_image_paths)} input image(s)")
    print(f"Action JSON loaded: {json.dumps(action_json_array, indent=2)}")
    
    # Initialize Dropbox client
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    
    # Upload all input images to Dropbox and get their links
    input_links = []
    dropbox_input_paths = []
    
    for idx, input_path in enumerate(input_image_paths):
        file_name = os.path.basename(input_path)
        dropbox_input_path = f'/{file_name}'
        dropbox_input_paths.append(dropbox_input_path)
        
        print(f"Uploading input {idx + 1}/{len(input_image_paths)} to Dropbox: {dropbox_input_path}")
        with open(input_path, 'rb') as f:
            dbx.files_upload(f.read(), dropbox_input_path, mode=dropbox.files.WriteMode.overwrite)
        
        # Get Dropbox temporary link for input
        input_link = dbx.files_get_temporary_link(dropbox_input_path).link
        input_links.append(input_link)
        print(f"Input {idx + 1} link: {input_link}")
    
    # Prepare output path - use UUID for Dropbox to avoid conflicts
    # Use first input filename as base for output filename
    import uuid
    first_file_name = os.path.basename(input_image_paths[0])
    unique_id = str(uuid.uuid4())[:8]
    output_file_name = f'temp_{unique_id}_{first_file_name}'
    output_file_path = f'/{output_file_name}'
    
    # Get Dropbox temporary upload link for output using REST API
    upload_link_url = "https://api.dropboxapi.com/2/files/get_temporary_upload_link"
    upload_link_headers = {
        "Authorization": f"Bearer {DROPBOX_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    upload_link_payload = {
        "commit_info": {
            "path": output_file_path,
            "mode": {
                ".tag": "overwrite"
            },
            "mute": False
        },
        "duration": 3600
    }
    
    upload_link_response = requests.post(upload_link_url, headers=upload_link_headers, json=upload_link_payload)
    if upload_link_response.status_code != 200:
        print(f"Error: Failed to generate upload link: {upload_link_response.text}")
        return None
    
    output_link_url = upload_link_response.json().get('link')
    print(f"Output path: {output_file_path}")
    
    # Prepare data for Adobe API with multiple inputs
    data = {
        "inputs": [{"storage": "dropbox", "href": link} for link in input_links],
        "options": {"actionJSON": action_json_array},
        "outputs": [{
            "storage": "dropbox", 
            "type": "image/vnd.adobe.photoshop", 
            "href": output_link_url
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
    
    # Generate output path with _output suffix
    if output_image_path is None:
        # Get base filename from first input
        base_name = os.path.basename(input_image_paths[0])
        # Split filename and extension
        name_without_ext, ext = os.path.splitext(base_name)
        # Create output filename: original_name_output.ext (or add _multi if multiple inputs)
        if len(input_image_paths) > 1:
            output_filename = f"{name_without_ext}_multi_output{ext}"
        else:
            output_filename = f"{name_without_ext}_output{ext}"
        output_image_path = os.path.join("output_images", output_filename)
    
    # Download and save the image
    downloaded_path = download_image(direct_link, output_image_path)
    
    # Cleanup Dropbox files
    try:
        for path in dropbox_input_paths:
            dbx.files_delete_v2(path)
        dbx.files_delete_v2(output_file_path)
        print("Cleaned up temporary Dropbox files")
    except Exception as e:
        print(f"Warning: Could not clean up some Dropbox files: {e}")
    
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
        print("Usage: python photoshop_actions.py <input_image_path(s)> <action_json_file> [output_image_path]")
        print("\nSingle input:")
        print("  python photoshop_actions.py input_images/image.jpg action.json")
        print("  python photoshop_actions.py input_images/image.jpg action.json output_images/result.jpg")
        print("\nMultiple inputs (comma-separated):")
        print("  python photoshop_actions.py input_images/img1.jpg,input_images/img2.jpg action.json")
        print("\nMultiple inputs (space-separated, use quotes):")
        print("  python photoshop_actions.py 'input_images/img1.jpg input_images/img2.jpg' action.json")
        sys.exit(1)
    
    # Parse input paths - support comma-separated or space-separated
    input_arg = sys.argv[1]
    if ',' in input_arg:
        # Comma-separated list
        input_paths = [path.strip() for path in input_arg.split(',')]
    else:
        # Single path or space-separated (if quoted)
        input_paths = [input_arg]
    
    action_json_file = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    # If multiple inputs, use composite mode (actionJSON API only supports single input)
    if len(input_paths) > 1:
        print(f"Detected {len(input_paths)} inputs - using composite mode")
        result_path = create_composite_and_apply_action(input_paths, action_json_file, output_path)
    else:
        result_path = execute_photoshop_action(input_paths, action_json_file, output_path)
    
    if result_path:
        print(f"\n✓ Success! Processed image saved to: {result_path}")
        sys.exit(0)
    else:
        print("\n✗ Failed to process image")
        sys.exit(1)
