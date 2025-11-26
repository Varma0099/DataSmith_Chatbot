# 🌟 Getting Your FREE Google Gemini API Key

Google Gemini Pro is **completely free** to use with generous limits - perfect for this project!

## Why Gemini?

✅ **FREE** - No credit card required
✅ **Generous Limits** - 60 requests per minute
✅ **High Quality** - Comparable to GPT-4
✅ **Easy Setup** - 2-minute process
✅ **Multimodal** - Supports text, images, and more

## Step-by-Step Guide

### Step 1: Go to Google AI Studio
Visit: https://makersuite.google.com/app/apikey

### Step 2: Sign In
- Use your existing Google account
- Or create a new one (takes 2 minutes)

### Step 3: Create API Key
1. Click **"Get API Key"** or **"Create API Key"** button
2. Select a project or create a new one
3. Your API key will be generated instantly

### Step 4: Copy Your Key
- Click the copy icon next to your API key
- It will look something like: `AIzaSyC...` (starts with AIza)

### Step 5: Add to .env File
```bash
# In your project directory
# Edit the .env file and add:
GOOGLE_API_KEY=AIzaSyC_your_actual_key_here
```

## Important Notes

### Rate Limits (Free Tier)
- **60 requests per minute**
- **1,500 requests per day**
- More than enough for development and testing!

### Supported Models
This project uses **gemini-pro** which includes:
- Fast response times
- Excellent medical knowledge
- Context understanding
- Reasoning capabilities

### Troubleshooting

**Problem**: "API key not valid"
- Make sure you copied the complete key
- No spaces before or after the key
- Key should start with `AIza`

**Problem**: "Quota exceeded"
- Free tier has generous limits
- If exceeded, wait a minute and try again
- Or upgrade to paid tier (optional)

**Problem**: "API not enabled"
- API should be enabled automatically
- If not, go to Google Cloud Console
- Enable "Generative Language API"

## Comparison: Gemini vs OpenAI

| Feature | Google Gemini Pro | OpenAI GPT-4o-mini |
|---------|------------------|-------------------|
| **Price** | FREE | $0.15/$0.60 per 1M tokens |
| **Quality** | Excellent | Excellent |
| **Speed** | Fast | Fast |
| **Setup** | 2 minutes | 5 minutes + billing |
| **Limits** | 60/min free | Pay per use |
| **Best for** | Development, POCs | Production at scale |

## Security Best Practices

### ✅ DO:
- Keep your API key in `.env` file
- Add `.env` to `.gitignore` (already done)
- Never commit API keys to GitHub
- Regenerate key if accidentally exposed

### ❌ DON'T:
- Share your API key publicly
- Commit it to version control
- Hardcode it in your code
- Email or message it in plain text

## Getting Help

### Official Resources
- API Documentation: https://ai.google.dev/docs
- Get API Key: https://makersuite.google.com/app/apikey
- Support: https://developers.google.com/workspace/support

### Common Questions

**Q: Is Gemini really free?**
A: Yes! The free tier has very generous limits perfect for this project.

**Q: Do I need a credit card?**
A: No! Completely free, no billing required.

**Q: What happens if I exceed limits?**
A: You'll get a rate limit error. Just wait a minute and try again.

**Q: Can I use this in production?**
A: Yes, but consider upgrading for higher limits if needed.

**Q: How does it compare to GPT-4?**
A: Gemini Pro performs excellently and is comparable in quality.

## Quick Start Checklist

- [ ] Visit https://makersuite.google.com/app/apikey
- [ ] Sign in with Google account
- [ ] Click "Get API Key"
- [ ] Copy your API key
- [ ] Add to `.env` file as `GOOGLE_API_KEY=your_key`
- [ ] Run `streamlit run app_streamlit.py`
- [ ] Test the application!

## Next Steps

Once you have your key configured:
1. Run the application: `streamlit run app_streamlit.py`
2. Test with different patients
3. Ask medical questions
4. See Gemini's responses in action!

---

**Ready?** Get your FREE API key now: https://makersuite.google.com/app/apikey

No credit card, no payment, just pure AI power! 🚀

