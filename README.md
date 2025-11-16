# generate_caption

Azure Function triggered by Blob Storage.  
Uses Azure Vision API to extract image tags and Azure OpenAI to rewrite them into natural captions.

## How it works

1. Upload an image to the `images` container in Blob Storage.
2. Function triggers automatically.
3. Vision API returns tags.
4. OpenAI rewrites tags into a caption.
5. Caption is logged for review or use.

## Requirements

- Azure Blob Storage
- Azure Computer Vision API
- Azure OpenAI (GPT-4o or GPT-3.5)
- Python + requests + azure-functions

## Deployment

- Push to GitHub → auto-deploy via GitHub Actions
- Set keys and endpoints in Azure Function App settings