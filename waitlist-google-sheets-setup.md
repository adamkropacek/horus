# HORUS waitlist -> Google Sheets (3 min)

Static site, no backend, no API keys. The form POSTs to a Google Apps Script Web App that appends a row to your Sheet.

## Steps

1. New Google Sheet (e.g. "HORUS waitlist"). Row 1 headers: `timestamp` | `email` | `referrer`.
2. In that Sheet: **Extensions -> Apps Script**.
3. Delete the placeholder, paste the code below, **Save**.
4. **Deploy -> New deployment -> type: Web app**.
   - Description: `horus-waitlist`
   - Execute as: **Me**
   - Who has access: **Anyone**
   - **Deploy**, authorize (your Google account).
5. Copy the **Web app URL** (ends in `/exec`).
6. Paste that URL into `WAITLIST_ENDPOINT="";` in `index.html` (or send it to Claude to wire + redeploy).

That's it. Every "Join the waitlist" submit writes a row. The page never sees your account; it only POSTs the email.

## Apps Script code

```javascript
function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    sheet.appendRow([ data.ts || new Date().toISOString(), data.email || "", data.ref || "" ]);
    return ContentService.createTextOutput(JSON.stringify({ok:true})).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ok:false, err:String(err)})).setMimeType(ContentService.MimeType.JSON);
  }
}
```

## Notes

- The frontend uses `mode:"no-cors"` so the browser fires the POST without a CORS preflight; the row still gets written. The page cannot read the response (that is fine - it shows its own confirmation).
- To change which sheet/columns, edit `appendRow([...])`.
- Spam control later: add a honeypot field or basic email regex in `doPost`.
- This same endpoint works no matter where the page is hosted (GitHub Pages, custom domain).
