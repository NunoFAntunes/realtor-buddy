import './PropertyCard.css'

function PropertyCard({ property }) {
  const formatPrice = (price) => {
    if (!price) return 'Price on request'
    return `€${price.toLocaleString()}`
  }

  const formatArea = (area) => {
    if (!area) return 'N/A'
    return `${area} m²`
  }

  const getPropertyImage = (imageUrls) => {
    if (imageUrls && imageUrls.length > 0) {
      return imageUrls[0]
    }
    return null
  }

  return (
    <div className="property-card">
      <div className="card-image">
        {getPropertyImage(property.image_urls) ? (
          <img 
            src={getPropertyImage(property.image_urls)} 
            alt={property.title || 'Property'} 
            onError={(e) => {
              e.target.style.display = 'none'
              e.target.nextSibling.style.display = 'flex'
            }}
          />
        ) : null}
        <div className="image-placeholder" style={{ display: getPropertyImage(property.image_urls) ? 'none' : 'flex' }}>
          <svg width="48" height="48" viewBox="0 0 24 24" fill="#ccc">
            <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
          </svg>
        </div>
      </div>
      
      <div className="card-content">
        <div className="card-header">
          <div className="price">{formatPrice(property.price)}</div>
          {property.lokacija && (
            <div className="location">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="#666">
                <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
              </svg>
              {property.lokacija}
            </div>
          )}
        </div>
        
        {property.title && (
          <h3 className="card-title">{property.title}</h3>
        )}
        
        <div className="card-details">
          <div className="detail-item">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="#666">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            <span>{property.broj_soba || 'N/A'} rooms</span>
          </div>
          
          <div className="detail-item">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="#666">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
              <rect x="7" y="7" width="10" height="10"/>
            </svg>
            <span>{formatArea(property.povrsina)}</span>
          </div>
          
          {property.kat && (
            <div className="detail-item">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="#666">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
              <span>Floor: {property.kat}</span>
            </div>
          )}
        </div>
        
        <div className="card-features">
          {property.lift === 'da' && (
            <span className="feature-tag">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-5 14H7v-2h2v-2H7v-2h7v6zm2-6v2h2v2h-2v2h-2V9h2v2z"/>
              </svg>
              Elevator
            </span>
          )}
          
          {property.pogled_na_more === 'da' && (
            <span className="feature-tag">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <path d="M3.5 18.49l6-6.01 4 4L22 6.92l-1.41-1.41-7.09 7.97-4-4L2 16.99l1.5 1.5z"/>
              </svg>
              Sea View
            </span>
          )}
          
          {property.energetski_razred && (
            <span className="feature-tag">
              Energy: {property.energetski_razred}
            </span>
          )}
        </div>
        
        {property.agency_name && (
          <div className="agency">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="#888">
              <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
            </svg>
            {property.agency_name}
          </div>
        )}
      </div>
    </div>
  )
}

export default PropertyCard