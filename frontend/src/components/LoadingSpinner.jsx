import './LoadingSpinner.css'

function LoadingSpinner() {
  return (
    <div className="loading-container">
      <div className="spinner">
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
        <div className="spinner-ring"></div>
      </div>
      <p className="loading-text">🤖 Searching properties with AI...</p>
    </div>
  )
}

export default LoadingSpinner