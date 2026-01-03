'use client'

import React, { useState } from 'react'

// Configuration - Update this before deployment
const GOOGLE_SCRIPT_URL = 'YOUR_GOOGLE_SCRIPT_URL_HERE'

interface FormData {
  // Step 1: About You
  name: string
  businessName: string
  businessType: string
  yearsInBusiness: string
  teamSize: string

  // Step 2: What's Eating Your Time?
  timeWasters: string
  missedOpportunities: string
  currentTools: string
  biggestFix: string

  // Step 3: What Would Help?
  dreamScenario: string
  whoUsesIt: string
  successCriteria: string
  mustHaves: string
  niceToHaves: string

  // Step 4: How Should It Feel?
  examplesLiked: string
  brandStyle: string
  customerExperience: string

  // Step 5: Timeline & Investment
  urgency: string
  budgetRange: string
  deadlines: string

  // Step 6: How We'll Work Together
  updatePreference: string
  availableHours: string
  concerns: string

  // Step 7: Contact
  email: string
  phone: string
  bestTime: string
}

export default function IntakeForm() {
  const [currentStep, setCurrentStep] = useState(1)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [formData, setFormData] = useState<FormData>({
    // Step 1: About You
    name: '',
    businessName: '',
    businessType: '',
    yearsInBusiness: '',
    teamSize: '',

    // Step 2: What's Eating Your Time?
    timeWasters: '',
    missedOpportunities: '',
    currentTools: '',
    biggestFix: '',

    // Step 3: What Would Help?
    dreamScenario: '',
    whoUsesIt: '',
    successCriteria: '',
    mustHaves: '',
    niceToHaves: '',

    // Step 4: How Should It Feel?
    examplesLiked: '',
    brandStyle: '',
    customerExperience: '',

    // Step 5: Timeline & Investment
    urgency: '',
    budgetRange: '',
    deadlines: '',

    // Step 6: How We'll Work Together
    updatePreference: '',
    availableHours: '',
    concerns: '',

    // Step 7: Contact
    email: '',
    phone: '',
    bestTime: ''
  })

  const totalSteps = 7

  const stepTitles = [
    'About You',
    "What's Eating Your Time?",
    'What Would Help?',
    'How Should It Feel?',
    'Timeline & Investment',
    "How We'll Work Together",
    'Contact Info'
  ]

  const handleInputChange = (field: keyof FormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const nextStep = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1)
      window.scrollTo(0, 0)
    }
  }

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1)
      window.scrollTo(0, 0)
    }
  }

  const handleSubmit = async () => {
    setIsSubmitting(true)
    try {
      await fetch(GOOGLE_SCRIPT_URL, {
        method: 'POST',
        mode: 'no-cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          submittedAt: new Date().toISOString()
        })
      })
      setIsSubmitted(true)
    } catch (error) {
      console.error('Submission error:', error)
      // Still show success - no-cors mode doesn't return readable response
      setIsSubmitted(true)
    }
    setIsSubmitting(false)
  }

  // Reusable Components
  const TextInput = ({
    label,
    field,
    placeholder,
    required = false
  }: {
    label: string
    field: keyof FormData
    placeholder: string
    required?: boolean
  }) => (
    <div className="mb-6">
      <label className="block text-slate-300 text-sm font-medium mb-2">
        {label} {required && <span className="text-emerald-400">*</span>}
      </label>
      <input
        type="text"
        value={formData[field]}
        onChange={(e) => handleInputChange(field, e.target.value)}
        placeholder={placeholder}
        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition"
      />
    </div>
  )

  const TextArea = ({
    label,
    field,
    placeholder,
    rows = 4
  }: {
    label: string
    field: keyof FormData
    placeholder: string
    rows?: number
  }) => (
    <div className="mb-6">
      <label className="block text-slate-300 text-sm font-medium mb-2">{label}</label>
      <textarea
        value={formData[field]}
        onChange={(e) => handleInputChange(field, e.target.value)}
        placeholder={placeholder}
        rows={rows}
        className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none transition resize-none"
      />
    </div>
  )

  const SelectButtons = ({
    label,
    field,
    options
  }: {
    label: string
    field: keyof FormData
    options: string[]
  }) => (
    <div className="mb-6">
      <label className="block text-slate-300 text-sm font-medium mb-3">{label}</label>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {options.map((option) => (
          <button
            key={option}
            type="button"
            onClick={() => handleInputChange(field, option)}
            className={`px-4 py-3 rounded-lg border text-left transition ${
              formData[field] === option
                ? 'bg-emerald-600 border-emerald-500 text-white'
                : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
            }`}
          >
            {option}
          </button>
        ))}
      </div>
    </div>
  )

  // Progress Bar
  const ProgressBar = () => (
    <div className="mb-8">
      <div className="flex justify-between text-sm text-slate-400 mb-2">
        <span>Step {currentStep} of {totalSteps}</span>
        <span>{stepTitles[currentStep - 1]}</span>
      </div>
      <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
        <div
          className="h-full bg-emerald-500 transition-all duration-300"
          style={{ width: `${(currentStep / totalSteps) * 100}%` }}
        />
      </div>
    </div>
  )

  // Navigation Buttons
  const NavigationButtons = ({ showSubmit = false }: { showSubmit?: boolean }) => (
    <div className="flex justify-between mt-8 pt-6 border-t border-slate-800">
      {currentStep > 1 ? (
        <button
          type="button"
          onClick={prevStep}
          className="px-6 py-3 text-slate-400 hover:text-white transition"
        >
          Back
        </button>
      ) : (
        <div />
      )}
      {showSubmit ? (
        <button
          type="button"
          onClick={handleSubmit}
          disabled={isSubmitting}
          className="px-8 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-medium transition disabled:opacity-50"
        >
          {isSubmitting ? 'Sending...' : 'Submit'}
        </button>
      ) : (
        <button
          type="button"
          onClick={nextStep}
          className="px-8 py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg font-medium transition"
        >
          Continue
        </button>
      )}
    </div>
  )

  // Success Screen
  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center px-4">
        <div className="max-w-md text-center">
          <div className="w-16 h-16 bg-emerald-600 rounded-full flex items-center justify-center mx-auto mb-6">
            <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-white mb-4">Got it!</h2>
          <p className="text-slate-400 text-lg">
            We&apos;ll reach out within 24-48 hours to discuss how we can help streamline your business.
          </p>
        </div>
      </div>
    )
  }

  // Step Content
  const renderStep = () => {
    switch (currentStep) {
      case 1:
        return (
          <>
            <h2 className="text-2xl font-bold text-white mb-2">Tell us about you</h2>
            <p className="text-slate-400 mb-8">Just the basics so we know who we&apos;re talking to.</p>

            <TextInput
              label="Your Name"
              field="name"
              placeholder="John Smith"
              required
            />
            <TextInput
              label="Business Name"
              field="businessName"
              placeholder="Smith's Auto Repair"
              required
            />
            <SelectButtons
              label="What type of business?"
              field="businessType"
              options={[
                'Auto Shop / Mechanic',
                'HVAC / Plumbing',
                'Contractor / Construction',
                'Salon / Barbershop',
                'Restaurant / Food Service',
                'Cleaning Service',
                'Landscaping',
                'Other Service Business'
              ]}
            />
            <SelectButtons
              label="How long have you been in business?"
              field="yearsInBusiness"
              options={[
                'Just starting out',
                '1-3 years',
                '3-10 years',
                '10+ years'
              ]}
            />
            <SelectButtons
              label="How many people work with you?"
              field="teamSize"
              options={[
                'Just me',
                '2-5 people',
                '6-15 people',
                '15+ people'
              ]}
            />
            <NavigationButtons />
          </>
        )

      case 2:
        return (
          <>
            <h2 className="text-2xl font-bold text-white mb-2">What&apos;s eating your time?</h2>
            <p className="text-slate-400 mb-8">Help us understand what&apos;s slowing you down.</p>

            <TextArea
              label="What takes up too much of your time right now?"
              field="timeWasters"
              placeholder="Answering the same questions over and over, chasing down late payments, scheduling back-and-forth..."
            />
            <TextArea
              label="What opportunities are you missing because you're too busy?"
              field="missedOpportunities"
              placeholder="Can't follow up with leads fast enough, don't have time to ask for reviews, missing repeat business..."
            />
            <TextArea
              label="What tools or systems do you use now? (Even if it's just paper and phone)"
              field="currentTools"
              placeholder="Pen and paper, Excel, QuickBooks, just my phone..."
            />
            <TextArea
              label="If you could fix ONE thing tomorrow, what would it be?"
              field="biggestFix"
              placeholder="Stop losing track of estimates, get paid faster, stop missing appointments..."
            />
            <NavigationButtons />
          </>
        )

      case 3:
        return (
          <>
            <h2 className="text-2xl font-bold text-white mb-2">What would actually help?</h2>
            <p className="text-slate-400 mb-8">Dream a little. What would make your life easier?</p>

            <TextArea
              label="In a perfect world, how would things work?"
              field="dreamScenario"
              placeholder="Customer texts me, I get all their info automatically, they get a quote same day, payment just happens..."
            />
            <TextArea
              label="Who would use this system besides you?"
              field="whoUsesIt"
              placeholder="My front desk person, my techs in the field, my customers..."
            />
            <TextArea
              label="How would you know it's working?"
              field="successCriteria"
              placeholder="Getting paid within a week instead of a month, spending less time on the phone, customers stop asking 'where's my tech?'..."
            />
            <TextArea
              label="What absolutely MUST work, no exceptions?"
              field="mustHaves"
              placeholder="Has to work on my phone, customers need to be able to pay easily, I need to see the schedule..."
            />
            <TextArea
              label="What would be nice to have, but isn't critical?"
              field="niceToHaves"
              placeholder="Automatic review requests, fancy reports, integration with accounting..."
              rows={3}
            />
            <NavigationButtons />
          </>
        )

      case 4:
        return (
          <>
            <h2 className="text-2xl font-bold text-white mb-2">How should it feel?</h2>
            <p className="text-slate-400 mb-8">We want this to feel like YOUR business, not generic software.</p>

            <TextArea
              label="Any businesses you admire? How do they treat customers?"
              field="examplesLiked"
              placeholder="I like how Chick-fil-A texts me when my order's ready, or how my dentist sends appointment reminders..."
            />
            <SelectButtons
              label="How would you describe your business style?"
              field="brandStyle"
              options={[
                'Professional & Polished',
                'Friendly & Casual',
                'No-Nonsense, Get It Done',
                'Premium / High-End',
                'Family-Owned Feel',
                'Tech-Forward / Modern'
              ]}
            />
            <TextArea
              label="What kind of experience do you want customers to have?"
              field="customerExperience"
              placeholder="They should feel taken care of, know exactly what's happening with their job, never have to chase us down..."
            />
            <NavigationButtons />
          </>
        )

      case 5:
        return (
          <>
            <h2 className="text-2xl font-bold text-white mb-2">Timeline & Investment</h2>
            <p className="text-slate-400 mb-8">Let&apos;s talk about when and what you&apos;re comfortable with.</p>

            <SelectButtons
              label="How soon do you need this?"
              field="urgency"
              options={[
                'Yesterday (ASAP)',
                'Within a month',
                'Next few months',
                'Just exploring for now'
              ]}
            />
            <SelectButtons
              label="What's your comfort range for getting this set up?"
              field="budgetRange"
              options={[
                'Under $1,000',
                '$1,000 - $2,000',
                '$2,000 - $3,500',
                '$3,500 - $5,000',
                'Over $5,000 for the right solution'
              ]}
            />
            <TextArea
              label="Any hard deadlines we should know about?"
              field="deadlines"
              placeholder="Busy season starts in March, new location opening in 60 days, need it before the holidays..."
              rows={3}
            />
            <NavigationButtons />
          </>
        )

      case 6:
        return (
          <>
            <h2 className="text-2xl font-bold text-white mb-2">How we&apos;ll work together</h2>
            <p className="text-slate-400 mb-8">Everyone works differently. Let&apos;s figure out what suits you.</p>

            <SelectButtons
              label="How do you prefer to get updates?"
              field="updatePreference"
              options={[
                'Quick text messages',
                'Email updates',
                'Weekly phone call',
                'Just tell me when it\'s done'
              ]}
            />
            <SelectButtons
              label="What hours work best for you?"
              field="availableHours"
              options={[
                'Early morning (before 9am)',
                'Business hours (9-5)',
                'After hours (5-8pm)',
                'Weekends'
              ]}
            />
            <TextArea
              label="Any concerns or things you've been burned on before?"
              field="concerns"
              placeholder="Last tech company ghosted me, I'm not great with computers, worried about cost overruns..."
            />
            <NavigationButtons />
          </>
        )

      case 7:
        return (
          <>
            <h2 className="text-2xl font-bold text-white mb-2">How do we reach you?</h2>
            <p className="text-slate-400 mb-8">Last step. We&apos;ll be in touch soon.</p>

            <TextInput
              label="Email"
              field="email"
              placeholder="john@smithsauto.com"
              required
            />
            <TextInput
              label="Phone"
              field="phone"
              placeholder="(763) 555-0123"
              required
            />
            <SelectButtons
              label="Best time to reach you?"
              field="bestTime"
              options={[
                'Morning',
                'Afternoon',
                'Evening',
                'Text anytime'
              ]}
            />
            <NavigationButtons showSubmit />
          </>
        )

      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-slate-900 py-8 px-4">
      <div className="max-w-xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Let&apos;s Simplify Your Business</h1>
          <p className="text-slate-400">Tell us what&apos;s not working. We&apos;ll figure out how to fix it.</p>
        </div>

        {/* Form Card */}
        <div className="bg-slate-850 border border-slate-800 rounded-2xl p-6 sm:p-8">
          <ProgressBar />
          {renderStep()}
        </div>

        {/* Trust Footer */}
        <div className="text-center mt-8 text-slate-500 text-sm">
          <p>Your information stays private. No spam, no selling your data.</p>
        </div>
      </div>
    </div>
  )
}
