import { useState } from 'react'
import './SearchBar.css'

function SearchBar({ onSearch, disabled }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    onSearch(query)
  }

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <div className="search-input-container">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search for properties... (e.g., 'apartments in Zagreb under 200k euros')"
          className="search-input"
          disabled={disabled}
        />
        <button 
          type="submit" 
          className="search-button"
          disabled={disabled || !query.trim()}
        >
          <svg 
            width="20" 
            height="20" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2"
          >
            <circle cx="11" cy="11" r="8"/>
            <path d="m21 21-4.35-4.35"/>
          </svg>
        </button>
      </div>
    </form>
  )
}

export default SearchBar