// Frontend Configuration
// This file allows you to easily change the API URL if the backend port changes

const CONFIG = {
    // Backend API base URL
    // Automatically determine if we are in dev (localhost) or prod
    API_BASE_URL: (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
        ? 'http://localhost:8888/api/v1'
        : '/api/v1', // In prod, we assume api is served from same origin or via proxy

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










