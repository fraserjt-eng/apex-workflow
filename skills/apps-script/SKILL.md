---
name: apps-script
description: Google Apps Script automation patterns for educational workflows. Use when building automations for Google Workspace, data pipelines, form processing, or administrative task automation.
---

# GOOGLE APPS SCRIPT FOR EDUCATION

**Purpose:** Automation patterns specifically designed for K-12 educational contexts, emphasizing efficiency, data protection, and sustainable workflows.

## Overview

Google Apps Script enables powerful automations within the Google Workspace ecosystem. For educational leaders, this means automating repetitive tasks, connecting data sources, and creating custom tools—all while maintaining FERPA compliance and data security.

## Core Use Cases in Education

### 1. Data Collection & Processing

**Form to Spreadsheet Pipelines:**
```javascript
function onFormSubmit(e) {
  const response = e.response;
  const itemResponses = response.getItemResponses();

  // Process form data
  const data = itemResponses.map(item => ({
    question: item.getItem().getTitle(),
    answer: item.getResponse()
  }));

  // Validate and transform
  processFormData(data);
}
```

**Common Applications:**
- Student survey processing
- Staff feedback collection
- Parent communication logs
- PD registration and tracking
- Incident documentation workflows

### 2. Automated Communications

**Template-Based Emails:**
```javascript
function sendPersonalizedEmails(spreadsheetId, templateDocId) {
  const sheet = SpreadsheetApp.openById(spreadsheetId).getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const template = DocumentApp.openById(templateDocId).getBody().getText();

  // Skip header row
  for (let i = 1; i < data.length; i++) {
    const recipient = data[i][0]; // email column
    const personalized = template
      .replace('{{name}}', data[i][1])
      .replace('{{school}}', data[i][2]);

    GmailApp.sendEmail(recipient, 'Subject Here', personalized);
  }
}
```

**Common Applications:**
- Principal weekly updates
- Family engagement notifications
- Staff recognition messages
- Deadline reminders
- Meeting follow-ups

### 3. Dashboard & Reporting

**Auto-Updating Dashboards:**
```javascript
function refreshDashboardData() {
  const sources = [
    { id: 'SOURCE_SHEET_1', range: 'Data!A:Z' },
    { id: 'SOURCE_SHEET_2', range: 'Metrics!A:Z' }
  ];

  const dashboard = SpreadsheetApp.openById('DASHBOARD_ID');
  const dataSheet = dashboard.getSheetByName('RawData');

  sources.forEach((source, index) => {
    const data = SpreadsheetApp.openById(source.id)
      .getRange(source.range).getValues();
    // Write to dashboard
    updateSection(dataSheet, data, index);
  });
}
```

**Common Applications:**
- Equity metrics dashboards
- Attendance monitoring
- Academic progress tracking
- PD completion status
- Grant milestone reporting

### 4. Document Generation

**Automated Report Creation:**
```javascript
function generateReport(templateId, data, folderId) {
  const template = DriveApp.getFileById(templateId);
  const folder = DriveApp.getFolderById(folderId);

  const copy = template.makeCopy(
    `Report - ${data.name} - ${new Date().toLocaleDateString()}`,
    folder
  );

  const doc = DocumentApp.openById(copy.getId());
  const body = doc.getBody();

  // Replace placeholders
  body.replaceText('{{name}}', data.name);
  body.replaceText('{{date}}', data.date);
  body.replaceText('{{metrics}}', data.metrics);

  doc.saveAndClose();
  return copy.getUrl();
}
```

**Common Applications:**
- Principal observation reports
- Student progress summaries
- Board meeting packets
- Grant progress reports
- Equity audit documentation

## FERPA-Compliant Patterns

### Data Handling Best Practices

```javascript
// NEVER log student PII
function processStudentData(studentRecord) {
  // Log action, not data
  Logger.log(`Processing record ID: ${studentRecord.id}`);

  // Use IDs, not names in logs
  const result = performOperation(studentRecord);

  // Return sanitized output
  return {
    id: studentRecord.id,
    status: 'processed',
    timestamp: new Date()
  };
}
```

### Access Control Pattern

```javascript
function checkUserPermissions() {
  const email = Session.getActiveUser().getEmail();
  const allowedDomains = ['bccs.k12.mn.us'];
  const adminUsers = ['jfraser@bccs.k12.mn.us'];

  const domain = email.split('@')[1];

  if (!allowedDomains.includes(domain)) {
    throw new Error('Unauthorized domain');
  }

  return {
    isAdmin: adminUsers.includes(email),
    canView: true,
    canEdit: adminUsers.includes(email)
  };
}
```

### Data Minimization

```javascript
// Only collect what's needed
function sanitizeExport(fullData) {
  return fullData.map(record => ({
    // Include only non-PII fields for reporting
    schoolId: record.schoolId,
    grade: record.grade,
    metric: record.metric,
    // Exclude: name, studentId, birthdate, address
  }));
}
```

## Trigger Management

### Time-Based Triggers

```javascript
function setupTriggers() {
  // Daily dashboard refresh at 6 AM
  ScriptApp.newTrigger('refreshDashboard')
    .timeBased()
    .atHour(6)
    .everyDays(1)
    .create();

  // Weekly report generation on Mondays at 7 AM
  ScriptApp.newTrigger('generateWeeklyReport')
    .timeBased()
    .onWeekDay(ScriptApp.WeekDay.MONDAY)
    .atHour(7)
    .create();

  // Monthly portfolio scan on 1st at 6 AM
  ScriptApp.newTrigger('monthlyPortfolioScan')
    .timeBased()
    .onMonthDay(1)
    .atHour(6)
    .create();
}
```

### Event-Based Triggers

```javascript
function setupEventTriggers() {
  // Form submission
  ScriptApp.newTrigger('onFormSubmit')
    .forForm('FORM_ID')
    .onFormSubmit()
    .create();

  // Spreadsheet edit
  ScriptApp.newTrigger('onSheetEdit')
    .forSpreadsheet('SHEET_ID')
    .onEdit()
    .create();
}
```

## Error Handling & Logging

```javascript
function robustOperation() {
  try {
    const result = performOperation();
    logSuccess('Operation completed', { recordCount: result.length });
    return result;
  } catch (error) {
    logError('Operation failed', {
      message: error.message,
      stack: error.stack
    });
    sendAlertEmail('Admin Alert: Script Error', error.message);
    throw error;
  }
}

function logError(message, details) {
  const logSheet = SpreadsheetApp.openById('LOG_SHEET_ID')
    .getSheetByName('Errors');
  logSheet.appendRow([
    new Date(),
    Session.getActiveUser().getEmail(),
    message,
    JSON.stringify(details)
  ]);
}
```

## Common Workflow Patterns

### Monday Portfolio Scan Automation

```javascript
function mondayPortfolioScan() {
  const portfolios = getActivePortfolios();
  const priorities = [];

  portfolios.forEach(portfolio => {
    const deadlines = getUpcomingDeadlines(portfolio, 7);
    const blockers = getBlockers(portfolio);
    const completions = getRecentCompletions(portfolio);

    priorities.push({
      portfolio: portfolio.name,
      deadlines: deadlines,
      blockers: blockers,
      completions: completions,
      priority: calculatePriority(deadlines, blockers)
    });
  });

  generatePortfolioEmail(priorities);
}
```

### PD Registration Workflow

```javascript
function processPDRegistration(formResponse) {
  // Extract registration data
  const registration = parseFormResponse(formResponse);

  // Check capacity
  const session = getSessionInfo(registration.sessionId);
  if (session.currentEnrollment >= session.capacity) {
    sendWaitlistNotification(registration.email);
    addToWaitlist(registration);
    return;
  }

  // Confirm registration
  addToRoster(registration);
  sendConfirmation(registration);
  updateCalendar(registration);
  notifyFacilitator(registration);
}
```

### Equity Data Pipeline

```javascript
function processEquityData() {
  // Pull data from multiple sources
  const demographicData = getDemographicData();
  const outcomeData = getOutcomeData();

  // Calculate disproportionality
  const analysis = calculateDisproportionality(demographicData, outcomeData);

  // Update dashboard
  updateEquityDashboard(analysis);

  // Flag concerning trends
  const alerts = identifyAlerts(analysis);
  if (alerts.length > 0) {
    sendEquityAlerts(alerts);
  }
}
```

## Integration Points

### With Other APEX Agents

| Agent | Integration Pattern |
|-------|---------------------|
| `data-analyst` | Generate data exports for analysis |
| `compliance-specialist` | Automate compliance tracking |
| `equity-auditor` | Pull demographic and outcome data |
| `system-integrator` | Build cross-system workflows |

### With External Systems

- **Student Information System (SIS):** API integration for roster data
- **Learning Management System (LMS):** Course completion tracking
- **Assessment Platforms:** Score import and analysis
- **HR Systems:** Staff data synchronization

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Problematic | Better Approach |
|--------------|---------------------|-----------------|
| Logging PII | FERPA violation risk | Log record IDs only |
| Hard-coded credentials | Security vulnerability | Use PropertiesService |
| No error handling | Silent failures | Try-catch with alerts |
| Overly complex triggers | Difficult maintenance | Simple, documented triggers |
| Monolithic scripts | Hard to debug | Modular functions |

## Deployment Checklist

Before deploying any automation:

- [ ] FERPA review completed
- [ ] Error handling implemented
- [ ] Logging configured (no PII)
- [ ] Access controls verified
- [ ] Test with sample data
- [ ] Documentation created
- [ ] Backup/rollback plan exists
- [ ] Stakeholders notified
- [ ] Monitoring in place

## Resources

- [Google Apps Script Documentation](https://developers.google.com/apps-script)
- [Student Privacy Compass](https://studentprivacycompass.org/)
- [FERPA for IT Administrators](https://studentprivacy.ed.gov/)
