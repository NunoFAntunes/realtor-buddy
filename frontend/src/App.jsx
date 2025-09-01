import { useState } from 'react'
import SearchBar from './components/SearchBar'
import ResultsGrid from './components/ResultsGrid'
import LoadingSpinner from './components/LoadingSpinner'
import './App.css'

function App() {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [totalResults, setTotalResults] = useState(0)

  const handleSearch = async (query) => {
    if (!query.trim()) return

    setLoading(true)
    setError(null)
    setResults([])

    try {
      const response = await fetch('/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      })

      const data = await response.json()

      if (data.success) {
        setResults(data.results || [])
        setTotalResults(data.total_results || 0)
      } else {
        setError(data.error || 'Search failed')
      }
    } catch (err) {
      setError('Failed to connect to server')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1 className="title">Realtor Buddy</h1>
          <p className="subtitle">Find your perfect Croatian property</p>
        </header>

        <div className="search-section">
          <SearchBar onSearch={handleSearch} disabled={loading} />
        </div>

        <div className="content">
          {loading && <LoadingSpinner />}
          
          {error && (
            <div className="error">
              <p>❌ {error}</p>
            </div>
          )}
          
          {!loading && !error && results.length > 0 && (
            <>
              <div className="results-header">
                <p>{totalResults} properties found</p>
              </div>
              <ResultsGrid results={results} />
            </>
          )}
          
          {!loading && !error && results.length === 0 && totalResults === 0 && (
            <div className="empty-state">
              <p>Start by typing your property search above</p>
              <div className="examples">
                <p>Try searches like:</p>
                <ul>
                  <li>"apartments in Zagreb under 200,000 euros"</li>
                  <li>"houses with sea view in Split"</li>
                  <li>"3 bedroom properties with elevator"</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App