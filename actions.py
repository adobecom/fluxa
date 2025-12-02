"""
Simplified Photoshop API executor for actionJSON with multiple inputs.
Uses Adobe's actionJSON endpoint with additionalImages support.
"""

import os
import sys
import json
import time
import requests
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from datetime import datetime
import uuid

# Load environment variables
load_dotenv()

# Configuration
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
R2_ACCOUNT_ID = os.getenv('R2_ACCOUNT_ID')
R2_BUCKET_NAME = os.getenv('R2_BUCKET_NAME')
R2_ACCESS_KEY_ID = os.getenv('R2_ACCESS_KEY_ID')
R2_SECRET_ACCESS_KEY = os.getenv('R2_SECRET_ACCESS_KEY')
R2_REGION = os.getenv('R2_REGION', 'auto')


def get_access_token():
    """Get Adobe access token."""
    params = {
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': 'openid,AdobeID,read_organizations,firefly_api,ff_apis'
    }
    response = requests.post(
        f'https://ims-na1.adobelogin.com/ims/token/v2?client_id={CLIENT_ID}',
        data=params
    )
    return response.json().get('access_token')


def get_r2_client():
    """Create boto3 S3 client for Cloudflare R2."""
    endpoint_url = f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
    return boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name=R2_REGION
    )


def generate_r2_presigned_url(s3_client, object_key, operation='put_object', expiration=3600):
    """Generate pre-signed URL for R2."""
    return s3_client.generate_presigned_url(
        operation,
        Params={'Bucket': R2_BUCKET_NAME, 'Key': object_key},
        ExpiresIn=expiration
    )


def upload_to_r2(s3_client, local_path, object_key):
    """Upload file to R2."""
    s3_client.upload_file(local_path, R2_BUCKET_NAME, object_key)
    return generate_r2_presigned_url(s3_client, object_key, operation='get_object')


def download_from_r2(s3_client, object_key, local_path):
    """Download file from R2."""
    s3_client.download_file(R2_BUCKET_NAME, object_key, local_path)


def process_with_actionjson(
    input_images,
    action_json_file,
    output_path=None,
    preview_format="image/png",
    preview_output_path=None,
):
    """
    Process images using Adobe actionJSON endpoint with multiple inputs.
    
    According to Adobe docs, for multiple images:
    - First image goes in inputs[0]
    - Additional images go in options.additionalImages[]
    - Reference additional images in actionJSON using ACTION_JSON_OPTIONS_ADDITIONAL_IMAGES_X
    """
    print(f"\n[START] Processing {len(input_images)} images with actionJSON")
    
    # Validate inputs
    if not all([CLIENT_ID, CLIENT_SECRET, R2_ACCOUNT_ID, R2_BUCKET_NAME, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY]):
        print("Error: Missing required environment variables")
        return None
    
    for img_path in input_images:
        if not os.path.exists(img_path):
            print(f"Error: Image not found: {img_path}")
            return None
    
    if not os.path.exists(action_json_file):
        print(f"Error: Action JSON file not found: {action_json_file}")
        return None
    
    # Load action JSON
    with open(action_json_file, 'r') as f:
        action_json = json.load(f)
    
    print(f"Action JSON loaded: {len(action_json)} steps")
    
    # Initialize R2 client
    r2_client = get_r2_client()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    
    # Upload all input images to R2 and get URLs
    print("\n[UPLOAD] Uploading images to R2...")
    input_urls = []
    r2_keys = []
    
    for idx, img_path in enumerate(input_images):
        filename = os.path.basename(img_path)
        r2_key = f"temp_input_{timestamp}_{unique_id}_{idx}_{filename}"
        r2_keys.append(r2_key)
        
        url = upload_to_r2(r2_client, img_path, r2_key)
        input_urls.append(url)
        print(f"  Uploaded {idx + 1}/{len(input_images)}: {filename}")
    
    # Prepare output path in R2
    output_filename = os.path.basename(input_images[0])
    base_name = os.path.splitext(output_filename)[0]
    output_r2_key = f"output_{timestamp}_{unique_id}_{base_name}.psd"
    output_url = generate_r2_presigned_url(r2_client, output_r2_key, operation='put_object')

    preview_r2_key = None
    preview_url = None
    if preview_format:
        ext = ".png" if "png" in preview_format else ".jpg"
        preview_r2_key = f"preview_{timestamp}_{unique_id}_{base_name}{ext}"
        preview_url = generate_r2_presigned_url(r2_client, preview_r2_key, operation='put_object')
    
    print(f"\n[OUTPUT] Output will be: {output_r2_key}")
    if preview_r2_key:
        print(f"[OUTPUT] Preview will be: {preview_r2_key}")
    
    # Get Adobe access token
    print("\n[ADOBE] Getting access token...")
    access_token = get_access_token()
    if not access_token:
        print("Error: Failed to get access token")
        return None
    
    # Prepare API request
    # For multiple inputs with actionJSON:
    # - First image in inputs[0]
    # - Additional images in options.additionalImages[]
    data = {
        "inputs": [{
            "storage": "external",
            "href": input_urls[0]
        }],
        "options": {
            "actionJSON": action_json
        },
        "outputs": [{
            "storage": "external",
            "type": "image/vnd.adobe.photoshop",
            "href": output_url
        }]
    }
    if preview_r2_key and preview_url:
        data["outputs"].append({
            "storage": "external",
            "type": preview_format,
            "href": preview_url
        })
    
    # Add additional images if present
    if len(input_urls) > 1:
        data["options"]["additionalImages"] = [
            {"storage": "external", "href": url} for url in input_urls[1:]
        ]
        print(f"\n[INFO] Using {len(input_urls)} inputs: 1 primary + {len(input_urls) - 1} additional")
    
    # Call Adobe actionJSON API
    print("\n[ADOBE] Calling actionJSON API...")
    response = requests.post(
        'https://image.adobe.io/pie/psdService/actionJSON',
        headers={
            'Authorization': f'Bearer {access_token}',
            'x-api-key': CLIENT_ID,
            'Content-Type': 'application/json'
        },
        json=data
    )
    
    if response.status_code not in [200, 202]:
        print(f"Error: API call failed: {response.status_code}")
        print(response.text)
        return None
    
    result = response.json()
    print(f"Job submitted: {result.get('_links', {}).get('self', {}).get('href', 'N/A')}")
    
    # Poll for completion
    print("\n[ADOBE] Polling for job completion...")
    status = "pending"
    max_attempts = 60
    attempt = 0
    
    while status in ["running", "pending"] and attempt < max_attempts:
        time.sleep(2)
        attempt += 1
        
        job_response = requests.get(
            result['_links']['self']['href'],
            headers={
                'Authorization': f'Bearer {access_token}',
                'x-api-key': CLIENT_ID
            }
        )
        job_result = job_response.json()
        status = job_result.get("outputs", [{}])[0].get('status', 'failed')
        print(f"  Status: {status} (attempt {attempt}/{max_attempts})")
    
    if status != "succeeded":
        print(f"\nError: Job failed with status: {status}")
        print(json.dumps(job_result, indent=2))
        return None
    
    print("\n[SUCCESS] Job completed successfully!")
    
    # Download result from R2
    if output_path is None:
        os.makedirs("output_images", exist_ok=True)
        output_path = f"output_images/{base_name}_output.psd"
    
    print(f"\n[DOWNLOAD] Downloading result to: {output_path}")
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    download_from_r2(r2_client, output_r2_key, output_path)

    preview_local_path = None
    if preview_r2_key and preview_url:
        if preview_output_path is None:
            os.makedirs("output_images", exist_ok=True)
            preview_output_path = f"output_images/{base_name}_preview.png"
        print(f"[DOWNLOAD] Downloading preview to: {preview_output_path}")
        os.makedirs(os.path.dirname(preview_output_path) if os.path.dirname(preview_output_path) else '.', exist_ok=True)
        download_from_r2(r2_client, preview_r2_key, preview_output_path)
        preview_local_path = preview_output_path
    
    # Cleanup R2 files
    print("\n[CLEANUP] Cleaning up temporary files...")
    cleanup_keys = r2_keys + [output_r2_key]
    if preview_r2_key:
        cleanup_keys.append(preview_r2_key)

    for key in cleanup_keys:
        try:
            r2_client.delete_object(Bucket=R2_BUCKET_NAME, Key=key)
        except Exception as e:
            print(f"  Warning: Could not delete {key}: {e}")
    
    print(f"\n[COMPLETE] Output saved to: {output_path}")
    if preview_local_path:
        print(f"[COMPLETE] Preview saved to: {preview_local_path}")
    return {
        "output_path": output_path,
        "preview_path": preview_local_path
    }


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python actions.py <input_images> <action_json_file> [output_path]")
        print("\nExamples:")
        print("  Single image:")
        print("    python actions.py input_images/image.jpg action.json")
        print("\n  Multiple images (comma-separated):")
        print("    python actions.py input_images/img1.jpg,input_images/img2.jpg action.json")
        sys.exit(1)
    
    # Parse input images
    input_arg = sys.argv[1]
    input_images = [path.strip() for path in input_arg.split(',')]
    
    action_json_file = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    
    result = process_with_actionjson(input_images, action_json_file, output_path)
    
    if result:
        if isinstance(result, dict):
            print(f"\n✓ Success! Output: {result.get('output_path')}")
            if result.get('preview_path'):
                print(f"Preview: {result.get('preview_path')}")
        else:
            print(f"\n✓ Success! Output: {result}")
        sys.exit(0)
    else:
        print("\n✗ Failed to process")
        sys.exit(1)
