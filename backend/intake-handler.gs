/**
 * Business Intake Handler - Google Apps Script Backend
 *
 * Setup:
 * 1. Create a new Google Sheet
 * 2. Go to Extensions > Apps Script
 * 3. Paste this code
 * 4. Update NOTIFICATION_EMAIL below
 * 5. Deploy > Web app > Anyone
 * 6. Copy the deployment URL for the frontend
 */

// ==================== CONFIGURATION ====================

const SHEET_NAME = 'Intake Submissions';
const NOTIFICATION_EMAIL = 'YOUR_EMAIL_HERE'; // ← CHANGE THIS

// ==================== MAIN HANDLERS ====================

/**
 * Handle POST requests from intake form
 */
function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = getOrCreateSheet();

    // Calculate priority
    const priority = calculatePriority(data);

    // Prepare row data
    const timestamp = new Date();
    const row = [
      timestamp,                      // Timestamp
      'NEW',                          // Status
      priority,                       // Priority
      data.name || '',                // Name
      data.businessName || '',        // Business Name
      data.businessType || '',        // Business Type
      data.yearsInBusiness || '',     // Years in Business
      data.teamSize || '',            // Team Size
      data.timeWasters || '',         // Time Wasters
      data.missedOpportunities || '', // Missed Opportunities
      data.currentTools || '',        // Current Tools
      data.biggestFix || '',          // Biggest Fix
      data.dreamScenario || '',       // Dream Scenario
      data.whoUsesIt || '',           // Who Uses It
      data.successCriteria || '',     // Success Criteria
      data.mustHaves || '',           // Must Haves
      data.niceToHaves || '',         // Nice to Haves
      data.examplesLiked || '',       // Examples Liked
      data.brandStyle || '',          // Brand Style
      data.customerExperience || '',  // Customer Experience
      data.urgency || '',             // Urgency
      data.budgetRange || '',         // Budget Range
      data.deadlines || '',           // Deadlines
      data.updatePreference || '',    // Update Preference
      data.availableHours || '',      // Available Hours
      data.concerns || '',            // Concerns
      data.email || '',               // Email
      data.phone || '',               // Phone
      data.bestTime || '',            // Best Time to Call
      '',                             // Tech Plan Status (internal)
      '',                             // Assigned To (internal)
      ''                              // Notes (internal)
    ];

    // Append to sheet
    sheet.appendRow(row);

    // Send notification
    sendNotification(data, priority, timestamp);

    // Return success
    return ContentService
      .createTextOutput(JSON.stringify({ success: true, priority: priority }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    console.error('Error processing submission:', error);
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: error.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * Handle GET requests (health check)
 */
function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({
      status: 'ok',
      message: 'Business Intake API is running',
      timestamp: new Date().toISOString()
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

// ==================== SHEET MANAGEMENT ====================

/**
 * Get or create the submissions sheet
 */
function getOrCreateSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);

  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    setupHeaders(sheet);
  }

  return sheet;
}

/**
 * Set up sheet headers (run once or when creating new sheet)
 */
function setupHeaders(sheet) {
  const headers = [
    'Timestamp',
    'Status',
    'Priority',
    'Name',
    'Business Name',
    'Business Type',
    'Years in Business',
    'Team Size',
    'Time Wasters',
    'Missed Opportunities',
    'Current Tools',
    'Biggest Fix',
    'Dream Scenario',
    'Who Uses It',
    'Success Criteria',
    'Must Haves',
    'Nice to Haves',
    'Examples Liked',
    'Brand Style',
    'Customer Experience',
    'Urgency',
    'Budget Range',
    'Deadlines',
    'Update Preference',
    'Available Hours',
    'Concerns',
    'Email',
    'Phone',
    'Best Time to Call',
    'Tech Plan Status',
    'Assigned To',
    'Notes'
  ];

  // Set headers
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);

  // Format header row
  const headerRange = sheet.getRange(1, 1, 1, headers.length);
  headerRange.setBackground('#1e293b');
  headerRange.setFontColor('#ffffff');
  headerRange.setFontWeight('bold');

  // Freeze header row
  sheet.setFrozenRows(1);

  // Set column widths for better readability
  sheet.setColumnWidth(1, 150);  // Timestamp
  sheet.setColumnWidth(2, 80);   // Status
  sheet.setColumnWidth(3, 80);   // Priority
  sheet.setColumnWidth(4, 120);  // Name
  sheet.setColumnWidth(5, 150);  // Business Name

  // Add data validation for Status column
  const statusRange = sheet.getRange('B2:B1000');
  const statusRule = SpreadsheetApp.newDataValidation()
    .requireValueInList(['NEW', 'CONTACTED', 'MEETING SCHEDULED', 'PROPOSAL SENT', 'WON', 'LOST', 'ON HOLD'])
    .build();
  statusRange.setDataValidation(statusRule);

  // Add conditional formatting for priority
  const priorityRange = sheet.getRange('C2:C1000');

  // HOT = Red background
  const hotRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('HOT')
    .setBackground('#fecaca')
    .setFontColor('#991b1b')
    .setRanges([priorityRange])
    .build();

  // WARM = Yellow background
  const warmRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('WARM')
    .setBackground('#fef3c7')
    .setFontColor('#92400e')
    .setRanges([priorityRange])
    .build();

  // NORMAL = Green background
  const normalRule = SpreadsheetApp.newConditionalFormatRule()
    .whenTextEqualTo('NORMAL')
    .setBackground('#d1fae5')
    .setFontColor('#065f46')
    .setRanges([priorityRange])
    .build();

  const rules = sheet.getConditionalFormatRules();
  rules.push(hotRule, warmRule, normalRule);
  sheet.setConditionalFormatRules(rules);
}

// ==================== PRIORITY CALCULATION ====================

/**
 * Calculate priority based on urgency and budget
 */
function calculatePriority(data) {
  const urgency = data.urgency || '';
  const budget = data.budgetRange || '';

  const isUrgent = urgency.toLowerCase().includes('asap') ||
                   urgency.toLowerCase().includes('yesterday');

  const isHighBudget = budget.includes('3,500') ||
                       budget.includes('5,000') ||
                       budget.toLowerCase().includes('over');

  const isMidBudget = budget.includes('1,000') ||
                      budget.includes('2,000');

  // HOT: Urgent + high budget
  if (isUrgent && isHighBudget) {
    return 'HOT';
  }

  // HOT: Very high budget regardless of urgency
  if (budget.toLowerCase().includes('over')) {
    return 'HOT';
  }

  // WARM: Urgent OR mid-to-high budget
  if (isUrgent || isHighBudget || isMidBudget) {
    return 'WARM';
  }

  // NORMAL: Everything else
  return 'NORMAL';
}

// ==================== NOTIFICATIONS ====================

/**
 * Send email notification for new submission
 */
function sendNotification(data, priority, timestamp) {
  if (!NOTIFICATION_EMAIL || NOTIFICATION_EMAIL === 'YOUR_EMAIL_HERE') {
    console.log('Notification email not configured');
    return;
  }

  // Priority emoji
  const priorityEmoji = {
    'HOT': '🔥',
    'WARM': '🟡',
    'NORMAL': '🟢'
  }[priority] || '📋';

  const subject = `${priorityEmoji} New Intake: ${data.businessName || 'Unknown Business'} [${priority}]`;

  const body = `
NEW BUSINESS INTAKE SUBMISSION
==============================

Priority: ${priority}
Submitted: ${timestamp.toLocaleString()}

CONTACT
-------
Name: ${data.name || 'Not provided'}
Business: ${data.businessName || 'Not provided'}
Type: ${data.businessType || 'Not provided'}
Email: ${data.email || 'Not provided'}
Phone: ${data.phone || 'Not provided'}
Best Time: ${data.bestTime || 'Not provided'}

BUSINESS DETAILS
----------------
Years in Business: ${data.yearsInBusiness || 'Not provided'}
Team Size: ${data.teamSize || 'Not provided'}

THE PROBLEM
-----------
Time Wasters: ${data.timeWasters || 'Not provided'}

Biggest Fix: ${data.biggestFix || 'Not provided'}

BUDGET & TIMELINE
-----------------
Budget Range: ${data.budgetRange || 'Not provided'}
Urgency: ${data.urgency || 'Not provided'}
Deadlines: ${data.deadlines || 'Not provided'}

PREFERENCES
-----------
Update Preference: ${data.updatePreference || 'Not provided'}
Available Hours: ${data.availableHours || 'Not provided'}
Concerns: ${data.concerns || 'Not provided'}

==============================
View full submission in the sheet.
  `.trim();

  try {
    MailApp.sendEmail({
      to: NOTIFICATION_EMAIL,
      subject: subject,
      body: body
    });
  } catch (error) {
    console.error('Error sending notification:', error);
  }
}

// ==================== DASHBOARD / REPORTING ====================

/**
 * Create a summary view of submissions
 * Run this manually or on a schedule
 */
function createSummaryView() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sourceSheet = ss.getSheetByName(SHEET_NAME);

  if (!sourceSheet) {
    console.log('No submissions sheet found');
    return;
  }

  // Get or create summary sheet
  let summarySheet = ss.getSheetByName('Dashboard');
  if (!summarySheet) {
    summarySheet = ss.insertSheet('Dashboard');
  } else {
    summarySheet.clear();
  }

  const data = sourceSheet.getDataRange().getValues();
  if (data.length <= 1) {
    summarySheet.getRange('A1').setValue('No submissions yet');
    return;
  }

  // Count by status
  const statusCounts = {};
  const priorityCounts = { 'HOT': 0, 'WARM': 0, 'NORMAL': 0 };

  for (let i = 1; i < data.length; i++) {
    const status = data[i][1] || 'NEW';
    const priority = data[i][2] || 'NORMAL';

    statusCounts[status] = (statusCounts[status] || 0) + 1;
    if (priorityCounts.hasOwnProperty(priority)) {
      priorityCounts[priority]++;
    }
  }

  // Build summary
  summarySheet.getRange('A1').setValue('INTAKE DASHBOARD');
  summarySheet.getRange('A1').setFontSize(18).setFontWeight('bold');

  summarySheet.getRange('A3').setValue('Total Submissions:');
  summarySheet.getRange('B3').setValue(data.length - 1);

  summarySheet.getRange('A5').setValue('BY PRIORITY');
  summarySheet.getRange('A5').setFontWeight('bold');
  summarySheet.getRange('A6').setValue('🔥 HOT:');
  summarySheet.getRange('B6').setValue(priorityCounts['HOT']);
  summarySheet.getRange('A7').setValue('🟡 WARM:');
  summarySheet.getRange('B7').setValue(priorityCounts['WARM']);
  summarySheet.getRange('A8').setValue('🟢 NORMAL:');
  summarySheet.getRange('B8').setValue(priorityCounts['NORMAL']);

  summarySheet.getRange('A10').setValue('BY STATUS');
  summarySheet.getRange('A10').setFontWeight('bold');

  let row = 11;
  for (const [status, count] of Object.entries(statusCounts)) {
    summarySheet.getRange('A' + row).setValue(status + ':');
    summarySheet.getRange('B' + row).setValue(count);
    row++;
  }

  summarySheet.getRange('A' + (row + 1)).setValue('Last updated: ' + new Date().toLocaleString());
  summarySheet.getRange('A' + (row + 1)).setFontColor('#666666');
}

// ==================== UTILITY FUNCTIONS ====================

/**
 * Manual setup function - run once after pasting code
 */
function initialSetup() {
  const sheet = getOrCreateSheet();
  console.log('Setup complete. Sheet ready for submissions.');

  // Create dashboard
  createSummaryView();
  console.log('Dashboard created.');
}

/**
 * Test function to verify email is configured
 */
function testNotification() {
  if (!NOTIFICATION_EMAIL || NOTIFICATION_EMAIL === 'YOUR_EMAIL_HERE') {
    console.log('⚠️ NOTIFICATION_EMAIL not configured. Update the constant at the top of the script.');
    return;
  }

  const testData = {
    name: 'Test User',
    businessName: 'Test Business',
    businessType: 'Test Type',
    email: 'test@example.com',
    phone: '555-0123',
    urgency: 'Yesterday (ASAP)',
    budgetRange: '$3,500 - $5,000'
  };

  sendNotification(testData, 'HOT', new Date());
  console.log('Test notification sent to: ' + NOTIFICATION_EMAIL);
}
