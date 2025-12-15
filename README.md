# FB Leads Automation - Final

🚗 **Automated Lead Extraction from Facebook Marketplace & OLX with Chrome Extension**

## Features

✅ **Dual Platform Support**
- Facebook Marketplace scraping
- OLX.in lead extraction
- Multi-city support (Mumbai, Delhi, Hyderabad, Pune, Lucknow, Kolkata)

✅ **Smart Data Extraction**
- Phone number extraction (Indian format: +91, 0, or 10-digit)
- Car brand auto-detection
- Year, KM, REG NO automatic extraction
- Owner type identification (Direct Owner vs Dealer)

✅ **Lead Management**
- SQLite database for lead storage
- Duplicate filtering by phone number
- Follow-up scheduling
- Status tracking (new, contacted, follow-up)

✅ **Messaging & Notifications**
- Pattern-based WhatsApp message generation
- SMS notifications
- Telegram alerts for follow-ups
- Auto message sending

✅ **Google Sheets Integration**
- Real-time lead auto-populate
- All 14 fields: DATE, NAME, MOBILE, REG NO, CAR MODEL, VARIANT, YEAR, KM, ADDRESS, FOLLOW UP, SOURCE, CONTEXT, LICENSE, REMARK
- Webhook integration for automatic updates

✅ **Chrome Extension**
- One-click lead capture from any page
- Native messaging bridge to Python agent
- Popup UI for manual extraction
- Auto-send to Google Sheets

✅ **Windows Automation**
- Auto-installer batch script
- Native host registry setup
- One-command installation

## Project Structure

```
fb-leads-automation-final/
├── python/
│   ├── enhanced_agent.py          # Main Tkinter GUI + Selenium scraping
│   ├── native_host.py             # Chrome Extension bridge
│   ├── utils.py                   # Phone, brand, KM extraction
│   ├── config.json                # Template (user fills)
│   ├── leads.db                   # SQLite database
│   ├── requirements.txt           # pip dependencies
│   └── README_HI.md               # Hindi setup guide
├── extension/
│   ├── manifest.json              # Chrome Extension config
│   ├── sw.js                      # Service worker
│   ├── popup.html                 # Popup UI
│   ├── popup.js                   # Popup logic
│   ├── content.js                 # Page content extractor
│   └── icons/                     # Extension icons
├── setup/
│   ├── windows_install.bat        # One-click installer
│   ├── register_host.bat          # Native host registry
│   └── uninstall.bat              # Cleanup script
└── docs/
    ├── SETUP_GUIDE.md             # Step-by-step setup
    ├── API_CONFIG.md              # Google Sheets webhook setup
    └── TROUBLESHOOTING.md         # Common issues & fixes
```

## Quick Start (Windows)

### 1. Clone Repository
```bash
git clone https://github.com/umairraza9464-spec/fb-leads-automation-final.git
cd fb-leads-automation-final
```

### 2. Run Windows Installer
```bash
cd setup
windows_install.bat
```
This will:
- Install Python dependencies
- Setup native host
- Register Chrome extension bridge
- Create config files

### 3. Configure Settings

Edit `python/config.json`:
```json
{
  "webhook_url": "YOUR_GOOGLE_APPS_SCRIPT_URL",
  "google_sheet_id": "1hASe1gQK2xtWbvqq0uagOmFkyoUOI2ho9XcYTpij7lU",
  "telegram_token": "YOUR_BOT_TOKEN",
  "telegram_chat_id": "YOUR_CHAT_ID",
  "accounts": {
    "mumbai": {"email": "your_email@gmail.com", "pass": "password"},
    "delhi": {"email": "...", "pass": "..."}
  }
}
```

### 4. Run Agent
```bash
cd python
python enhanced_agent.py
```

### 5. Load Chrome Extension
1. Open Chrome → Settings → Extensions → Developer mode (toggle ON)
2. Click "Load unpacked"
3. Select `extension/` folder
4. Extension will appear in toolbar

## Features Explained

### Lead Extraction
Agent automatically:
1. Opens Chrome with Selenium
2. Logs into Facebook/OLX (auto-login from config)
3. Scrolls through listings
4. Extracts all data using regex patterns
5. Sends to Google Sheets via webhook
6. Saves to SQLite for tracking

### Smart Messaging
Based on owner type:
- **Direct Owner**: "Hi {name}, are you selling this car? Please share contact."
- **Dealer**: "Hi, can you share the owner's number?"
- Auto-sends via WhatsApp/SMS

### Follow-up System
- Tracks when message was sent
- Sets follow-up date (configurable)
- Telegram notification on follow-up day
- Marks as "contacted" when response received

### Chrome Extension
1. Click extension icon
2. On any Facebook/OLX page
3. Click "Extract Lead"
4. Data automatically captured and sent to Python agent
5. Auto-updated in Google Sheets

## Google Sheets Setup

### Sheet Columns (All Required)
| Column | Field |
|--------|-------|
| A | DATE |
| B | NAME |
| C | MOBILE |
| D | REG NO |
| E | CAR MODEL |
| F | VARIANT |
| G | YEAR |
| H | KM |
| I | ADDRESS |
| J | FOLLOW UP |
| K | SOURCE |
| L | CONTEXT |
| M | LICENSE |
| N | REMARK |

### Create Google Apps Script Webhook
1. Create new Sheet (or use existing)
2. Extensions → Apps Script
3. Paste this code:

```javascript
function doPost(e) {
  const data = JSON.parse(e.postData.contents);
  const sheet = SpreadsheetApp.getActiveSheet();
  
  sheet.appendRow([
    new Date(data.date),
    data.name,
    data.mobile,
    data.reg_no,
    data.car_model,
    data.variant,
    data.year,
    data.km,
    data.address,
    data.followup_date,
    data.source,
    data.context,
    data.license,
    data.remark
  ]);
  
  return ContentService.createTextOutput('OK');
}
```

4. Deploy → New deployment → Web app
5. Copy URL and paste in `config.json` as `webhook_url`

## Troubleshooting

### Chrome Extension not connecting?
- Check native host is registered: `HKCU\Software\Google\Chrome\NativeMessagingHosts`
- Run `register_host.bat` again
- Restart Chrome

### Login failures?
- Cookies might be blocked
- 2FA might be enabled (handle manually)
- Check credentials in config.json

### Google Sheets not updating?
- Verify webhook URL in config.json
- Test webhook: `curl -X POST YOUR_WEBHOOK_URL -d '{"test": true}'`
- Check Apps Script execution logs

### Leads not extracting?
- Check Selenium + Chrome versions match
- Verify CSS selectors (page structure changes often)
- Check logs in `LIVE STATUS & LOGS` tab

## Configuration Reference

### config.json Fields
```json
{
  "webhook_url": "Google Apps Script deployment URL",
  "google_sheet_id": "Spreadsheet ID from URL",
  "telegram_token": "Telegram Bot token (optional)",
  "telegram_chat_id": "Your chat ID for notifications",
  "cities": ["mumbai", "delhi", "hyderabad", "pune", "lucknow", "kolkata"],
  "accounts": { "city": { "email": "...", "pass": "..." } },
  "limits": {
    "scroll_per_city": 20,
    "max_leads_per_day": 500,
    "timeout_seconds": 15
  },
  "messaging": {
    "owner_pattern": "Custom message for owners",
    "dealer_pattern": "Custom message for dealers",
    "followup_days": 3
  }
}
```

## Performance Tips

1. **Faster scraping**: Increase `scroll_per_city` to 50+ (but more banned risk)
2. **Accurate data**: Use multiple accounts to avoid rate limiting
3. **Better leads**: Add filters (min price, car age, location)
4. **Reliable messaging**: Use authenticated channels (WhatsApp Business API)

## Security Notes

⚠️ **Never share**:
- Facebook/OLX login credentials
- Google Sheets API keys
- Telegram bot tokens
- Contact numbers in logs

✅ **Good practices**:
- Use environment variables for secrets
- Rotate credentials regularly
- Monitor logs for errors
- Check Google Sheet for suspicious entries

## Support & Contributing

Issues? Check `TROUBLESHOOTING.md` or create GitHub issue
Want to improve? Fork + PR welcome!

## License
MIT - Feel free to use & modify

## Hindi Documentation

सेटअप गाइड हिंदी में: `python/README_HI.md`

---

**Made with ❤️ for car dealers & automation enthusiasts**
