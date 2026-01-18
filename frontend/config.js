// Frontend Configuration
// This file allows you to easily change the API URL if the backend port changes

const CONFIG = {
    // Backend API base URL
    // Change this if you modify the PORT in backend/.env
    API_BASE_URL: 'http://localhost:8888/api/v1',
    
    // API endpoints
    ENDPOINTS: {
        LEGAL_RESEARCH: '/legal-research',
        DRAFT_DOCUMENT: '/draft-document',
        SEARCH_CASES: '/search-cases',
        SEARCH_STATUTE: '/search-statute',
        TEMPLATES: '/templates',
        COST_TRACKING: '/cost-tracking'
    }
};

// Make it available globally
if (typeof window !== 'undefined') {
    window.CONFIG = CONFIG;
}










