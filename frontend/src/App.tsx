import { useState } from 'react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { Upload, AlertCircle, CheckCircle, Info, Loader2, X } from 'lucide-react'

interface Issue {
  id: string
  severity: 'critical' | 'high' | 'medium' | 'low' | 'info'
  title: string
  description: string
  file_path?: string | null
  line_start?: number | null
  line_end?: number | null
  suggestion?: string | null
  source: string
}

interface ReviewResponse {
  review_id: string
  total_issues: number
  summary: {
    critical: number
    high: number
    medium: number
    low: number
    info: number
  }
  issues: Issue[]
}
const severityColors = {
  critical: 'bg-red-600',
  high: 'bg-orange-600',
  medium: 'bg-yellow-600',
  low: 'bg-blue-600',
  info: 'bg-gray-600'
}

const severityIcons = {
  critical: AlertCircle,
  high: AlertCircle,
  medium: AlertCircle,
  low: Info,
  info: Info
}

export default function App() {
  const [file, setFile] = useState<File | null>(null)
  const [review, setReview] = useState<ReviewResponse | null>(null)
  const [loading, setLoading] = useState(false)

  const onDrop = (acceptedFiles: File[]) => {
    const f = acceptedFiles[0]
    if (f && f.name.endsWith('.py')) {
      setFile(f)
      setReview(null)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/x-python': ['.py'] },
    maxFiles: 1
  })

  const analyze = async () => {
    if (!file) return
    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await axios.post('http://localhost:8000/api/v1/review/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setReview(res.data)
    } catch (err) {
      alert('Error analyzing file')
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <div className="min-h-screen bg-gray-900 text-gray-100">
        <div className="container mx-auto p-8 max-w-6xl">
          <h1 className="text-4xl font-bold text-center mb-8 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
            AI Code Review System
          </h1>

          {!review && (
            <div {...getRootProps()} className={`border-4 border-dashed rounded-xl p-16 text-center cursor-pointer transition-all ${isDragActive ? 'border-blue-500 bg-blue-900/20' : 'border-gray-700 hover:border-gray-500'}`}>
              <input {...getInputProps()} />
              <Upload className="w-20 h-20 mx-auto mb-6 text-gray-500" />
              <p className="text-2xl mb-4">
                {isDragActive ? "Drop your Python file here" : "Drag & drop a .py file here"}
              </p>
              <p className="text-gray-500">or click to browse</p>
              {file && <p className="mt-6 text-green-400 font-semibold">{file.name}</p>}
            </div>
          )}

          {file && !review && (
            <div className="text-center mt-8">
              <button
                onClick={analyze}
                disabled={loading}
                className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg font-bold text-xl hover:scale-105 transition-transform disabled:opacity-50"
              >
                {loading ? <>Analyzing...<Loader2 className="inline ml-3 animate-spin" /></> : 'Start AI Review'}
              </button>
            </div>
          )}

          {review && (
            <div className="mt-12">
              <div className="flex justify-between items-center mb-8">
                <h2 className="text-3xl font-bold">Review Results • {review.total_issues} issues</h2>
                <button onClick={() => { setFile(null); setReview(null) }} className="text-gray-400 hover:text-white">
                  <X className="w-8 h-8" />
                </button>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
                {Object.entries(review.summary).map(([sev, count]) => {
                  if (count === 0) return null
                  const Icon = severityIcons[sev as keyof typeof severityIcons] || Info
                  return (
                    <div key={sev} className={`p-4 rounded-lg ${severityColors[sev as keyof typeof severityColors]} text-white text-center`}>
                      <Icon className="w-10 h-10 mx-auto mb-2" />
                      <div className="text-3xl font-bold">{count}</div>
                      <div className="capitalize">{sev}</div>
                    </div>
                  )
                })}
              </div>

              <div className="space-y-6">
                {review.issues.map((issue) => (
                  <div key={issue.id} className="bg-gray-800 rounded-lg p-6 border border-gray-700">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <div className={`w-4 h-4 rounded-full ${severityColors[issue.severity]}`} />
                        <span className="text-sm text-gray-400 uppercase">{issue.source}</span>
                        <h3 className="text-xl font-semibold">{issue.title}</h3>
                      </div>
                      {issue.line_start && <span className="text-gray-500">Line {issue.line_start}</span>}
                    </div>
                    <p className="text-gray-300 mb-4">{issue.description}</p>
                    {issue.source === 'codet5' && (
                      <div className="bg-gray-900/50 p-4 rounded border border-purple-700">
                        <strong className="text-purple-400">AI Suggestion:</strong> {issue.description}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  )
}