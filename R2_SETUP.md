# Cloudflare R2 Setup Instructions

The following environment variables have been added to your `.env` file. Please fill them in with your actual Cloudflare R2 credentials.

## Required R2 Credentials

```bash
R2_ACCOUNT_ID=your_cloudflare_account_id_here
R2_BUCKET_NAME=your_r2_bucket_name_here
R2_ACCESS_KEY_ID=your_r2_access_key_id_here
R2_SECRET_ACCESS_KEY=your_r2_secret_access_key_here
R2_REGION=auto
```

## How to Get R2 Credentials

1. **Log into Cloudflare Dashboard**
   - Go to https://dash.cloudflare.com/

2. **Navigate to R2 Object Storage**
   - In the left sidebar, click on "R2"

3. **Create or Select a Bucket**
   - Click "Create bucket" or select an existing bucket
   - Note down the bucket name for `R2_BUCKET_NAME`

4. **Get Account ID**
   - Your Account ID is visible in the R2 overview page URL
   - Format: `https://dash.cloudflare.com/<ACCOUNT_ID>/r2`
   - Or find it in the right sidebar under "Account ID"

5. **Create API Token**
   - Click "Manage R2 API Tokens"
   - Click "Create API token"
   - Give it a name (e.g., "Adobe Photoshop API")
   - Set permissions: "Object Read & Write"
   - Optional: Restrict to specific bucket for security
   - Click "Create API Token"

6. **Save Credentials**
   - Copy the **Access Key ID** → Use for `R2_ACCESS_KEY_ID`
   - Copy the **Secret Access Key** → Use for `R2_SECRET_ACCESS_KEY`
   - **Important**: Save these securely - the Secret Access Key won't be shown again!

7. **Update .env File**
   - Open your `.env` file
   - Replace the placeholder values with your actual credentials
   - Save the file

## What R2 Will Be Used For

R2 will be used specifically for:
- Storing composite document outputs from Adobe's `documentCreate` API
- This bypasses the FileOverwriteError issue with Dropbox temporary upload links
- Input images will still use Dropbox (which works fine)
- Final output files will still be downloaded to your local machine

## Bucket Configuration

Make sure your R2 bucket:
- Has CORS enabled if you plan to access files directly from a browser
- Has appropriate lifecycle rules if you want automatic cleanup of temporary files
- Is in a region close to your location for faster uploads/downloads (though `auto` works well)

