import PropertyCard from './PropertyCard'
import './ResultsGrid.css'

function ResultsGrid({ results }) {
  if (!results || results.length === 0) {
    return null
  }

  return (
    <div className="results-grid">
      {results.map((property, index) => (
        <PropertyCard key={property.id || index} property={property} />
      ))}
    </div>
  )
}

export default ResultsGrid