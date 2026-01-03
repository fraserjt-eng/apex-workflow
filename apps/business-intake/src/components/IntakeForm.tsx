'use client'

import React, { useState } from 'react'

// Configuration
const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbySfoyIr6Xk_Svmftp4GQ_JIIzdcg7IWwlGb7poQKmE1z_qiLDVV5n5_EoSZc_8iJYO/exec'

interface FormData {
  name: string
  businessName: string
  businessType: string
  yearsInBusiness: string
  teamSize: string
  timeWasters: string
  missedOpportunities: string
  currentTools: string
  biggestFix: string
  dreamScenario: string
  whoUsesIt: string
  successCriteria: string
  mustHaves: string
  niceToHaves: string
  examplesLiked: string
  brandStyle: string
  customerExperience: string
  urgency: string
  budgetRange: string
  deadlines: string
  updatePreference: string
  availableHours: string
  concerns: string
  email: string
  phone: string
  bestTime: string
}

const stepTitles = [
  'About You',
  "What's Eating Your Time?",
  'What Would Help?',
  'How Should It Feel?',
  'Timeline & Investment',
  "How We'll Work Together",
  'Contact Info'
]

export default function IntakeForm() {
  const [currentStep, setCurrentStep] = useState(1)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [formData, setFormData] = useState<FormData>({
    name: '',
    businessName: '',
    businessType: '',
    yearsInBusiness: '',
    teamSize: '',
    timeWasters: '',
    missedOpportunities: '',
    currentTools: '',
    biggestFix: '',
    dreamScenario: '',
    whoUsesIt: '',
    successCriteria: '',
    mustHaves: '',
    niceToHaves: '',
    examplesLiked: '',
    brandStyle: '',
    customerExperience: '',
    urgency: '',
    budgetRange: '',
    deadlines: '',
    updatePreference: '',
    availableHours: '',
    concerns: '',
    email: '',
    phone: '',
    bestTime: ''
  })

  const totalSteps = 7

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
      setIsSubmitted(true)
    }
    setIsSubmitting(false)
  }

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
          {/* Progress Bar */}
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

          {/* Step 1 */}
          {currentStep === 1 && (
            <>
              <h2 className="text-2xl font-bold text-white mb-2">Tell us about you</h2>
              <p className="text-slate-400 mb-8">Just the basics so we know who we&apos;re talking to.</p>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">
                  Your Name <span className="text-emerald-400">*</span>
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  placeholder="John Smith"
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">
                  Business Name <span className="text-emerald-400">*</span>
                </label>
                <input
                  type="text"
                  value={formData.businessName}
                  onChange={(e) => handleInputChange('businessName', e.target.value)}
                  placeholder="Smith's Auto Repair"
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-3">What type of business?</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {['Auto Shop / Mechanic', 'HVAC / Plumbing', 'Contractor / Construction', 'Salon / Barbershop', 'Restaurant / Food Service', 'Cleaning Service', 'Landscaping', 'Other Service Business'].map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleInputChange('businessType', option)}
                      className={`px-4 py-3 rounded-lg border text-left transition ${
                        formData.businessType === option
                          ? 'bg-emerald-600 border-emerald-500 text-white'
                          : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-3">How long have you been in business?</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {['Just starting out', '1-3 years', '3-10 years', '10+ years'].map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleInputChange('yearsInBusiness', option)}
                      className={`px-4 py-3 rounded-lg border text-left transition ${
                        formData.yearsInBusiness === option
                          ? 'bg-emerald-600 border-emerald-500 text-white'
                          : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-3">How many people work with you?</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {['Just me', '2-5 people', '6-15 people', '15+ people'].map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleInputChange('teamSize', option)}
                      className={`px-4 py-3 rounded-lg border text-left transition ${
                        formData.teamSize === option
                          ? 'bg-emerald-600 border-emerald-500 text-white'
                          : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>
            </>
          )}

          {/* Step 2 */}
          {currentStep === 2 && (
            <>
              <h2 className="text-2xl font-bold text-white mb-2">What&apos;s eating your time?</h2>
              <p className="text-slate-400 mb-8">Help us understand what&apos;s slowing you down.</p>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">What takes up too much of your time right now?</label>
                <textarea
                  value={formData.timeWasters}
                  onChange={(e) => handleInputChange('timeWasters', e.target.value)}
                  placeholder="Answering the same questions over and over, chasing down late payments, scheduling back-and-forth..."
                  rows={4}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">What opportunities are you missing because you&apos;re too busy?</label>
                <textarea
                  value={formData.missedOpportunities}
                  onChange={(e) => handleInputChange('missedOpportunities', e.target.value)}
                  placeholder="Can't follow up with leads fast enough, don't have time to ask for reviews, missing repeat business..."
                  rows={4}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">What tools or systems do you use now? (Even if it&apos;s just paper and phone)</label>
                <textarea
                  value={formData.currentTools}
                  onChange={(e) => handleInputChange('currentTools', e.target.value)}
                  placeholder="Pen and paper, Excel, QuickBooks, just my phone..."
                  rows={4}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">If you could fix ONE thing tomorrow, what would it be?</label>
                <textarea
                  value={formData.biggestFix}
                  onChange={(e) => handleInputChange('biggestFix', e.target.value)}
                  placeholder="Stop losing track of estimates, get paid faster, stop missing appointments..."
                  rows={4}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>
            </>
          )}

          {/* Step 3 */}
          {currentStep === 3 && (
            <>
              <h2 className="text-2xl font-bold text-white mb-2">What would actually help?</h2>
              <p className="text-slate-400 mb-8">Dream a little. What would make your life easier?</p>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">In a perfect world, how would things work?</label>
                <textarea
                  value={formData.dreamScenario}
                  onChange={(e) => handleInputChange('dreamScenario', e.target.value)}
                  placeholder="Customer texts me, I get all their info automatically, they get a quote same day, payment just happens..."
                  rows={4}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">Who would use this system besides you?</label>
                <textarea
                  value={formData.whoUsesIt}
                  onChange={(e) => handleInputChange('whoUsesIt', e.target.value)}
                  placeholder="My front desk person, my techs in the field, my customers..."
                  rows={4}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">How would you know it&apos;s working?</label>
                <textarea
                  value={formData.successCriteria}
                  onChange={(e) => handleInputChange('successCriteria', e.target.value)}
                  placeholder="Getting paid within a week instead of a month, spending less time on the phone, customers stop asking 'where's my tech?'..."
                  rows={4}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">What absolutely MUST work, no exceptions?</label>
                <textarea
                  value={formData.mustHaves}
                  onChange={(e) => handleInputChange('mustHaves', e.target.value)}
                  placeholder="Has to work on my phone, customers need to be able to pay easily, I need to see the schedule..."
                  rows={4}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">What would be nice to have, but isn&apos;t critical?</label>
                <textarea
                  value={formData.niceToHaves}
                  onChange={(e) => handleInputChange('niceToHaves', e.target.value)}
                  placeholder="Automatic review requests, fancy reports, integration with accounting..."
                  rows={3}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>
            </>
          )}

          {/* Step 4 */}
          {currentStep === 4 && (
            <>
              <h2 className="text-2xl font-bold text-white mb-2">How should it feel?</h2>
              <p className="text-slate-400 mb-8">We want this to feel like YOUR business, not generic software.</p>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">Any businesses you admire? How do they treat customers?</label>
                <textarea
                  value={formData.examplesLiked}
                  onChange={(e) => handleInputChange('examplesLiked', e.target.value)}
                  placeholder="I like how Chick-fil-A texts me when my order's ready, or how my dentist sends appointment reminders..."
                  rows={4}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-3">How would you describe your business style?</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {['Professional & Polished', 'Friendly & Casual', 'No-Nonsense, Get It Done', 'Premium / High-End', 'Family-Owned Feel', 'Tech-Forward / Modern'].map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleInputChange('brandStyle', option)}
                      className={`px-4 py-3 rounded-lg border text-left transition ${
                        formData.brandStyle === option
                          ? 'bg-emerald-600 border-emerald-500 text-white'
                          : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">What kind of experience do you want customers to have?</label>
                <textarea
                  value={formData.customerExperience}
                  onChange={(e) => handleInputChange('customerExperience', e.target.value)}
                  placeholder="They should feel taken care of, know exactly what's happening with their job, never have to chase us down..."
                  rows={4}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>
            </>
          )}

          {/* Step 5 */}
          {currentStep === 5 && (
            <>
              <h2 className="text-2xl font-bold text-white mb-2">Timeline & Investment</h2>
              <p className="text-slate-400 mb-8">Let&apos;s talk about when and what you&apos;re comfortable with.</p>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-3">How soon do you need this?</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {['Yesterday (ASAP)', 'Within a month', 'Next few months', 'Just exploring for now'].map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleInputChange('urgency', option)}
                      className={`px-4 py-3 rounded-lg border text-left transition ${
                        formData.urgency === option
                          ? 'bg-emerald-600 border-emerald-500 text-white'
                          : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-3">What&apos;s your comfort range for getting this set up?</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {['Under $1,000', '$1,000 - $2,000', '$2,000 - $3,500', '$3,500 - $5,000', 'Over $5,000 for the right solution'].map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleInputChange('budgetRange', option)}
                      className={`px-4 py-3 rounded-lg border text-left transition ${
                        formData.budgetRange === option
                          ? 'bg-emerald-600 border-emerald-500 text-white'
                          : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">Any hard deadlines we should know about?</label>
                <textarea
                  value={formData.deadlines}
                  onChange={(e) => handleInputChange('deadlines', e.target.value)}
                  placeholder="Busy season starts in March, new location opening in 60 days, need it before the holidays..."
                  rows={3}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>
            </>
          )}

          {/* Step 6 */}
          {currentStep === 6 && (
            <>
              <h2 className="text-2xl font-bold text-white mb-2">How we&apos;ll work together</h2>
              <p className="text-slate-400 mb-8">Everyone works differently. Let&apos;s figure out what suits you.</p>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-3">How do you prefer to get updates?</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {['Quick text messages', 'Email updates', 'Weekly phone call', "Just tell me when it's done"].map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleInputChange('updatePreference', option)}
                      className={`px-4 py-3 rounded-lg border text-left transition ${
                        formData.updatePreference === option
                          ? 'bg-emerald-600 border-emerald-500 text-white'
                          : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-3">What hours work best for you?</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {['Early morning (before 9am)', 'Business hours (9-5)', 'After hours (5-8pm)', 'Weekends'].map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleInputChange('availableHours', option)}
                      className={`px-4 py-3 rounded-lg border text-left transition ${
                        formData.availableHours === option
                          ? 'bg-emerald-600 border-emerald-500 text-white'
                          : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">Any concerns or things you&apos;ve been burned on before?</label>
                <textarea
                  value={formData.concerns}
                  onChange={(e) => handleInputChange('concerns', e.target.value)}
                  placeholder="Last tech company ghosted me, I'm not great with computers, worried about cost overruns..."
                  rows={4}
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none resize-none"
                />
              </div>
            </>
          )}

          {/* Step 7 */}
          {currentStep === 7 && (
            <>
              <h2 className="text-2xl font-bold text-white mb-2">How do we reach you?</h2>
              <p className="text-slate-400 mb-8">Last step. We&apos;ll be in touch soon.</p>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">
                  Email <span className="text-emerald-400">*</span>
                </label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => handleInputChange('email', e.target.value)}
                  placeholder="john@smithsauto.com"
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-2">
                  Phone <span className="text-emerald-400">*</span>
                </label>
                <input
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => handleInputChange('phone', e.target.value)}
                  placeholder="(763) 555-0123"
                  className="w-full bg-slate-800 border border-slate-700 rounded-lg px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none"
                />
              </div>

              <div className="mb-6">
                <label className="block text-slate-300 text-sm font-medium mb-3">Best time to reach you?</label>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {['Morning', 'Afternoon', 'Evening', 'Text anytime'].map((option) => (
                    <button
                      key={option}
                      type="button"
                      onClick={() => handleInputChange('bestTime', option)}
                      className={`px-4 py-3 rounded-lg border text-left transition ${
                        formData.bestTime === option
                          ? 'bg-emerald-600 border-emerald-500 text-white'
                          : 'bg-slate-800 border-slate-700 text-slate-300 hover:border-slate-600'
                      }`}
                    >
                      {option}
                    </button>
                  ))}
                </div>
              </div>
            </>
          )}

          {/* Navigation */}
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
            {currentStep === 7 ? (
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
        </div>

        {/* Trust Footer */}
        <div className="text-center mt-8 text-slate-500 text-sm">
          <p>Your information stays private. No spam, no selling your data.</p>
        </div>
      </div>
    </div>
  )
}
