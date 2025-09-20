# Vercel Deployment Guide

This guide will help you deploy the Image Formatter web app to Vercel.

## Project Structure for Vercel

The project has been restructured for Vercel deployment:

```
/
├── api/
│   └── index.py          # Main Flask app for Vercel
├── templates/
│   └── index.html        # HTML template
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── .vercelignore        # Files to exclude from deployment
├── app.py               # Original local development app
└── README files...
```

## Deployment Steps

### 1. Prerequisites
- Install Vercel CLI: `npm install -g vercel`
- Create a Vercel account at https://vercel.com

### 2. Deploy to Vercel

#### Option A: Deploy via CLI
1. Navigate to the project directory:
   ```bash
   cd "/Users/simonstenelid/Desktop/Python Image Formatter"
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy the project:
   ```bash
   vercel
   ```

4. Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N**
   - Project name: `image-formatter` (or your preferred name)
   - Directory: `.` (current directory)

#### Option B: Deploy via GitHub
1. Push this project to a GitHub repository
2. Go to https://vercel.com/dashboard
3. Click "Import Project"
4. Import from your GitHub repository
5. Vercel will automatically detect it as a Python project

### 3. Configuration

The following files configure the deployment:

- **`vercel.json`**: Tells Vercel how to build and route the app
- **`api/index.py`**: Main application entry point for serverless
- **`requirements.txt`**: Python dependencies with specific versions

### 4. Environment Variables (if needed)

If you need to set environment variables:
1. Go to your project dashboard on Vercel
2. Navigate to Settings → Environment Variables
3. Add any required variables

### 5. Custom Domain (Optional)

To use a custom domain:
1. Go to your project dashboard
2. Navigate to Settings → Domains
3. Add your custom domain

## Key Changes Made for Vercel

1. **Serverless Structure**: Moved Flask app to `api/index.py` for Vercel's serverless functions
2. **Template Path**: Updated template folder path for the new structure
3. **Dependencies**: Pinned dependency versions for consistent deployment
4. **Configuration**: Added `vercel.json` for proper routing and build settings
5. **Ignore File**: Added `.vercelignore` to exclude unnecessary files

## Testing Your Deployment

After deployment, your app will be available at:
- `https://your-project-name.vercel.app`

The app will function exactly the same as the local version:
- Upload multiple images
- Process them to 1200×1200 format
- Download as ZIP file

## Troubleshooting

### Common Issues:

1. **404 Error**: Usually means routing is incorrect - check `vercel.json`
2. **Build Failures**: Check `requirements.txt` and Python version compatibility
3. **Timeout Errors**: Large image processing might hit Vercel's timeout limits

### Vercel Limits:
- Function execution: 60 seconds (configured in `vercel.json`)
- Memory: 1024MB
- File size: 100MB total (already configured in the app)

## Local Development

For local development, continue using:
```bash
python3 app.py
```

The `app.py` file remains unchanged for local testing.