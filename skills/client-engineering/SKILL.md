---
name: client-engineering
description: Turn business intake submissions into technical plans. Use when reviewing intakes, creating project specs, or scoping work for non-technical local business clients. Zero technical burden on clients.
---

# CLIENT ENGINEERING SKILL

> "The client is the expert on WHAT. We are the experts on HOW."

## THE GOLDEN RULE

**Client responsibilities:**
- Tell us what's broken
- React to demos
- Pay invoices

**Client NEVER:**
- Answers technical questions
- Debugs anything
- Sees code, architecture diagrams, or technical documentation
- Chooses between frameworks, databases, or tools
- Learns our terminology

**We ALWAYS:**
- Translate their words into our work
- Make technical decisions without burdening them
- Show working things, not explain technical things
- Speak their language, not ours

---

## PROCESSING AN INTAKE

When a new submission arrives, follow this sequence:

### Step 1: Read the Submission

Focus on these fields:
- **Biggest Fix** - What they want solved first
- **Dream Scenario** - What success looks like to them
- **Must Haves** - Non-negotiables
- **Success Criteria** - How they'll know it's working
- **Concerns** - What's made them hesitant before

### Step 2: Translate to Technical Components

| They Say | We Build |
|----------|----------|
| "Stop answering the same questions" | FAQ chatbot, automated text responses |
| "Get paid faster" | Automated invoicing, payment links, reminders |
| "Stop missing appointments" | Booking system, automated reminders |
| "Know where my techs are" | Simple job tracking, status updates |
| "Customers keep asking for updates" | Automated status notifications |
| "Lose track of leads" | CRM, automated follow-up sequences |
| "Scheduling back-and-forth" | Self-booking calendar |
| "Can't get reviews" | Automated review request flow |
| "Estimates take too long" | Quote builder, templated estimates |
| "Paper everywhere" | Digital forms, cloud storage |

### Step 3: Create Two Documents

1. **CLAUDE.md** - Client-facing project file
   - Their words, not ours
   - What we're solving
   - How we'll communicate
   - Use template: `templates/CLAUDE.md.template`

2. **TECHNICAL.md** - Internal technical spec
   - Architecture decisions
   - Stack choices with rationale
   - Implementation details
   - Use template: `templates/TECHNICAL.md.template`

---

## CLAUDE.md TEMPLATE

See `templates/CLAUDE.md.template` for the full template.

Key sections:
- **Client Profile** - Name, business, style, communication preference
- **The Problem** - Their exact words from intake
- **Success Criteria** - How they'll measure success
- **Must-Haves / Nice-to-Haves** - Prioritized requirements
- **Communication Rules** - How we interact with them
- **When to Involve Client** - Only for experience-affecting decisions

---

## TECHNICAL.md TEMPLATE

See `templates/TECHNICAL.md.template` for the full template.

Key sections:
- **Architecture** - System design
- **Stack** - Component choices with rationale
- **Components** - What we're building
- **Data Flow** - How information moves
- **Testing** - How we verify it works
- **Deployment** - How it goes live

---

## COMMUNICATION TEMPLATES

### Initial Response (Send within 24-48 hours)

```
Hey [Name],

Got your info - thanks for taking the time to fill that out.

Sounds like [biggest pain point in their words] is eating up way too much of your time. We've helped other [business type]s with exactly this.

I'd love to spend 15-20 minutes on the phone to make sure I understand what you need. No sales pitch - just want to make sure we're a good fit before going further.

What works better for you - [time option A] or [time option B]?

[Your name]
[Phone]
```

### Progress Update

```
Quick update on [project name]:

✅ Done:
- [Thing they can see/use]
- [Thing they can see/use]

🔧 Working on:
- [What's next, in their language]

📅 On track for [milestone date].

Any questions? Just reply to this.
```

### Demo Invitation

```
Hey [Name],

Got something to show you.

[One sentence about what they'll see, in their words - "the new booking page" not "the scheduling integration"]

Can you take a look at [link] and let me know:
1. Does this feel like your business?
2. Anything confusing?
3. What's missing?

Takes about 5 minutes. Just text me back when you've had a chance.
```

---

## SERVICE TIERS

### Tier 1: Quick Win ($500 - $1,500)

**Typical scope:**
- Single automation (booking, reminders, review requests)
- Simple form or landing page
- Basic integration between two tools

**Timeline:** 1-2 weeks

**Monthly:** $150-200 for hosting/maintenance

### Tier 2: Core System ($1,500 - $3,000)

**Typical scope:**
- Customer-facing portal
- Multiple automations working together
- CRM setup with automated sequences
- Job tracking system

**Timeline:** 2-4 weeks

**Monthly:** $200-300 for hosting/maintenance/support

### Tier 3: Full Business System ($3,000 - $5,000+)

**Typical scope:**
- Complete customer journey automation
- Staff-facing tools (mobile-friendly)
- Dashboard and reporting
- Multiple integrations
- Training included

**Timeline:** 4-8 weeks

**Monthly:** $300-400 for hosting/maintenance/support/updates

---

## QUALITY CHECKLIST

### Before Showing Anything to Client

- [ ] Does it work on their phone?
- [ ] Would their least technical employee understand it?
- [ ] Does it use their terminology, not ours?
- [ ] Does it match their brand feel (colors, tone)?
- [ ] Can they break it by doing something unexpected?
- [ ] Is there a clear "what do I do next?" at every step?
- [ ] Have we tested with real-ish data?

### Red Flags in Communication

Stop and reconsider if you catch yourself:

| Red Flag | What to Do Instead |
|----------|---------------------|
| "Let me explain how this works technically..." | "Here's what you'll see..." |
| "Which database do you prefer?" | Just pick one. They don't care. |
| "Can you test the API endpoint?" | "Can you try booking an appointment?" |
| "There's a bug in the webhook..." | "We found an issue and fixed it." |
| "What framework should we use?" | Never ask this. Ever. |
| "Check the console for errors" | "Let me know if anything looks wrong" |

---

## INTAKE PRIORITY GUIDE

### HOT (Respond same day)
- Budget $3,500+
- "Yesterday / ASAP" urgency
- Clear problem, clear budget, ready to move

### WARM (Respond within 24 hours)
- Budget $1,500+
- Specific pain points
- Within-month timeline

### NORMAL (Respond within 48 hours)
- Exploring options
- Lower budget
- Flexible timeline

---

## EXAMPLE WORKFLOW

1. **Intake arrives** - Sheet shows new submission, email notification sent
2. **Review submission** - Read through, note priority
3. **Create CLAUDE.md** - Capture their words, their goals
4. **Create TECHNICAL.md** - Make architecture decisions
5. **Send initial response** - Within 24-48 hours
6. **Discovery call** - 15-20 min to confirm understanding
7. **Send proposal** - Scope, timeline, investment
8. **Build** - Regular demos, no technical explanations
9. **Launch** - They see it working
10. **Support** - Monthly maintenance, quick responses

---

## REMEMBER

The client hired us because they don't want to think about technology. Every time we ask them a technical question or show them something technical, we're failing at our job.

**They speak:** "Customers keep asking where their tech is."

**We hear:** Real-time job tracking with automated SMS updates.

**We say:** "We'll set it up so your customers automatically get a text when the tech is on the way."

**We never say:** "We'll integrate a webhook from your dispatch system to trigger an SMS via Twilio when the job status changes to 'en route'."

Same solution. Different language. That's the job.
