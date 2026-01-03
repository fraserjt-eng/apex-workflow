# Business Intake System

A client intake form for local business automation services. Non-technical business owners submit their needs, which flow to a Google Sheet for tech team review.

## Overview

```
┌─────────────────┐     ┌────────────────┐     ┌─────────────────┐
│  Intake Form    │────▶│  Apps Script   │────▶│  Google Sheet   │
│  (Next.js)      │     │  (Backend)     │     │  + Email Alert  │
└─────────────────┘     └────────────────┘     └─────────────────┘
                                                       │
                                                       ▼
                                               ┌─────────────────┐
                                               │  Tech Team      │
                                               │  Reviews +      │
                                               │  Creates Spec   │
                                               └─────────────────┘
```

## Quick Setup

### 1. Deploy Backend (Google Apps Script)

1. **Create Google Sheet**
   - Go to [sheets.google.com](https://sheets.google.com)
   - Create a new blank spreadsheet
   - Name it "Business Intakes" or similar

2. **Add Apps Script**
   - Go to Extensions > Apps Script
   - Delete any existing code
   - Paste contents of `../../backend/intake-handler.gs`

3. **Configure Email**
   - Find the line: `const NOTIFICATION_EMAIL = 'YOUR_EMAIL_HERE';`
   - Replace with your email address

4. **Run Initial Setup**
   - In Apps Script, select `initialSetup` from the function dropdown
   - Click Run
   - Authorize when prompted

5. **Deploy as Web App**
   - Click Deploy > New deployment
   - Type: Web app
   - Execute as: Me
   - Who has access: Anyone
   - Click Deploy
   - **Copy the Web app URL** - you'll need this for the frontend

### 2. Deploy Frontend

1. **Update Script URL**
   - Open `src/components/IntakeForm.tsx`
   - Find: `const GOOGLE_SCRIPT_URL = 'YOUR_GOOGLE_SCRIPT_URL_HERE';`
   - Replace with your Apps Script Web app URL from step 1

2. **Install Dependencies**
   ```bash
   cd apps/business-intake
   npm install
   ```

3. **Test Locally**
   ```bash
   npm run dev
   # Open http://localhost:3000
   ```

4. **Deploy to Vercel**
   ```bash
   vercel deploy
   ```

5. **Get Your Intake URL**
   - Your deployed URL is what you send to prospects

### 3. Use It

1. **Send intake URL to prospects**
   - Email, text, or link from your website

2. **Submissions appear in Google Sheet**
   - Auto-calculated priority (HOT/WARM/NORMAL)
   - Email notification for each submission

3. **Process with client-engineering skill**
   - Review submission
   - Create CLAUDE.md (client-facing)
   - Create TECHNICAL.md (internal)

## Project Structure

```
apps/business-intake/
├── src/
│   ├── app/
│   │   ├── globals.css      # Tailwind + custom styles
│   │   ├── layout.tsx       # Root layout with metadata
│   │   └── page.tsx         # Home page
│   └── components/
│       └── IntakeForm.tsx   # 7-step intake form component
├── public/
├── package.json
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

## Files

| File | Description |
|------|-------------|
| `src/components/IntakeForm.tsx` | Main intake form component |
| `../../backend/intake-handler.gs` | Google Apps Script backend |
| `../../skills/client-engineering/SKILL.md` | How to process intakes |
| `../../skills/client-engineering/templates/` | Project templates |

## Form Sections

The intake form has 7 steps:

1. **About You** - Name, business, type, experience, team size
2. **What's Eating Your Time?** - Pain points, missed opportunities
3. **What Would Help?** - Dream scenario, requirements
4. **How Should It Feel?** - Brand, customer experience
5. **Timeline & Investment** - Urgency, budget, deadlines
6. **How We'll Work Together** - Communication preferences
7. **Contact** - Email, phone, best time

## Priority Calculation

Submissions are auto-prioritized:

| Priority | Criteria |
|----------|----------|
| 🔥 HOT | Urgent + budget $3,500+ |
| 🟡 WARM | Urgent OR budget $1,500+ |
| 🟢 NORMAL | Everything else |

## Customization

### Change Form Fields

Edit `src/components/IntakeForm.tsx`:
- Modify questions in the `renderStep()` function
- Update `FormData` interface to match
- Update Apps Script columns to match

### Change Sheet Columns

Edit `../../backend/intake-handler.gs`:
- Modify `setupHeaders()` for column names
- Modify the row array in `doPost()` to match

### Change Priority Logic

Edit `../../backend/intake-handler.gs`:
- Modify `calculatePriority()` function

### Change Email Format

Edit `../../backend/intake-handler.gs`:
- Modify `sendNotification()` function

## Troubleshooting

### Form submits but nothing in sheet

1. Check Apps Script deployment URL is correct
2. Check Apps Script is deployed as "Anyone"
3. Check Apps Script logs (View > Executions)

### No email notifications

1. Check `NOTIFICATION_EMAIL` is set correctly
2. Check spam folder
3. Run `testNotification()` function manually

### CORS errors

The form uses `mode: 'no-cors'` which should work. If issues persist:
1. Verify the Apps Script URL is the deployment URL (not the script URL)
2. Ensure deployment is set to "Anyone"

## Security Notes

- Apps Script handles all sensitive logic
- Form only sends data, doesn't receive secrets
- Sheet permissions control who sees submissions
- No client data stored in frontend

## Tech Stack

- **Framework:** Next.js 14
- **Styling:** Tailwind CSS
- **Language:** TypeScript
- **Deployment:** Vercel
- **Backend:** Google Apps Script
- **Database:** Google Sheets

## Support

For issues with this system, check:
1. Apps Script execution logs
2. Browser console for frontend errors
3. Google Sheet for malformed data
