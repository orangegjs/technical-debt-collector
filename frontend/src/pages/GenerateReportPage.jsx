// BCE Boundary: :GenerateReportPage
// US#38: displayReport(Report result) — daily
// US#39: displayReport(Report result) — weekly
// US#40: displayReport(Report result) — monthly

import React, { useState } from 'react'
import Sidebar from '../components/Sidebar'
import { generateReport } from '../api/reportApi'

export default function GenerateReportPage() {
  const [reportType, setReportType] = useState('daily')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function handleReportTypeChange(e) {
    const type = e.target.value
    setReportType(type)
    setReport(null)
    setError('')
    // reset dates when switching type
    setStartDate('')
    setEndDate('')
  }

  function handleStartDateChange(e) {
    const val = e.target.value
    setStartDate(val)
    setError('')
    // for daily, end date is always locked to start date
    if (reportType === 'daily') {
      setEndDate(val)
    }
  }

  function handleEndDateChange(e) {
    setEndDate(e.target.value)
    setError('')
  }

  function validate() {
    if (!startDate || !endDate) {
      setError('Please select both start date and end date.')
      return false
    }
    if (new Date(endDate) < new Date(startDate)) {
      setError('End date cannot be before start date.')
      return false
    }
    if (reportType === 'daily' && startDate !== endDate) {
      setError('Daily report: start date and end date must be the same.')
      return false
    }
    return true
  }

  async function handleGenerate() {
    if (!validate()) return
    setLoading(true)
    setError('')
    setReport(null)
    try {
      const result = await generateReport(reportType, startDate, endDate)
      setReport(result)
    } catch (e) {
      setError(e.detail || 'Failed to generate report.')
    } finally {
      setLoading(false)
    }
  }

  const isDaily = reportType === 'daily'

  return (
    <div className="flex min-h-screen bg-lightbg">
      <Sidebar />
      <main className="flex-1 p-8 flex flex-col gap-5">
        <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col gap-4 max-w-2xl">
          <h2 className="text-lg font-bold text-gray-900">Generate Report</h2>

          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium text-gray-500">Report Type</label>
            <select
              value={reportType}
              onChange={handleReportTypeChange}
              className="border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-primary"
            >
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>

          <div className="flex gap-3 flex-wrap">
            <div className="flex flex-col gap-1 flex-1 min-w-[140px]">
              <label className="text-xs font-medium text-gray-500">Start Date</label>
              <input
                type="date"
                value={startDate}
                onChange={handleStartDateChange}
                className="border border-gray-200 rounded-lg px-3 py-2 text-sm outline-none focus:border-primary"
              />
            </div>
            <div className="flex flex-col gap-1 flex-1 min-w-[140px]">
              <label className="text-xs font-medium text-gray-500">
                End Date
                {isDaily && <span className="ml-1 text-gray-400">(same as start for daily)</span>}
              </label>
              <input
                type="date"
                value={endDate}
                onChange={handleEndDateChange}
                disabled={isDaily}
                min={startDate || undefined}
                className={`border rounded-lg px-3 py-2 text-sm outline-none transition-colors ${
                  isDaily
                    ? 'border-gray-100 bg-gray-50 text-gray-400 cursor-not-allowed'
                    : 'border-gray-200 focus:border-primary'
                }`}
              />
            </div>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="self-start bg-primary text-white px-6 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            {loading ? 'Generating...' : 'Generate'}
          </button>

          {error && <p className="text-deletered text-sm">{error}</p>}
        </div>

        {report && (
          // displayReport(Report result)
          <div className="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col gap-4 max-w-2xl">
            <h3 className="text-base font-bold text-gray-900">
              {report.reportType.charAt(0).toUpperCase() + report.reportType.slice(1)} Report
            </h3>
            <p className="text-xs text-gray-500">
              Period: {report.startDate} — {report.endDate}
            </p>
            <table className="w-full text-sm">
              <tbody className="divide-y divide-gray-100">
                <DetailRow label="Total FRAs Created"     value={report.totalFRA} />
                <DetailRow label="Total Donations Made"   value={report.totalDonation} />
                <DetailRow label="Total Users Registered" value={report.totalAccount} />
                <DetailRow label="Report ID"              value={report.reportID} />
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  )
}

function DetailRow({ label, value }) {
  return (
    <tr>
      <td className="py-2.5 pr-4 font-medium text-gray-600 w-2/5 align-top">{label}</td>
      <td className="py-2.5 text-gray-800 align-top">{value}</td>
    </tr>
  )
}
