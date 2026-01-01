const API_BASE = 'http://localhost:8888/api/v1/diary';

// --- Global State ---
let clients = [];
let cases = [];

// --- Init ---
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
    loadDailyBoard();
    loadClients(); // Prefetch for selects
});

// --- Navigation ---
function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'));

    document.getElementById(tabId).classList.add('active');
    document.querySelector(`button[onclick="switchTab('${tabId}')"]`).classList.add('active');

    if (tabId === 'daily-board') loadDailyBoard();
    if (tabId === 'case-master') loadCaseMaster();
    if (tabId === 'clients') loadClientsTable();
    if (tabId === 'fee-ledger') loadFeeLedger();
}

// --- Modals ---
function openModal(id) { document.getElementById(id).classList.add('show'); }
function closeModal(id) { document.getElementById(id).classList.remove('show'); }
window.onclick = function (event) {
    if (event.target.classList.contains('modal')) event.target.classList.remove('show');
}

async function openCaseModal() {
    populateClientSelect(); // Sync
    openModal('modal-case');
}
function openClientModal() { openModal('modal-client'); }

// --- API Calls & Renders ---

// 1. Dashboard
// 1. Dashboard
async function loadDashboard() {
    try {
        const res = await fetch(`${API_BASE}/dashboard`);
        if (!res.ok) throw new Error("Dashboard API failed");

        const data = await res.json();

        // Safety checks and formatting
        document.getElementById('stat-hearings').innerText = data.hearings_today !== undefined ? data.hearings_today : 0;
        document.getElementById('stat-cases').innerText = data.cases_pending !== undefined ? data.cases_pending : 0;
        document.getElementById('stat-tasks').innerText = data.tasks_due_today !== undefined ? data.tasks_due_today : 0;

        const feesVal = data.fees_outstanding !== undefined ? data.fees_outstanding : 0;
        document.getElementById('stat-fees').innerText = feesVal.toLocaleString('en-IN', { style: 'currency', currency: 'INR' });

    } catch (e) {
        console.error("Error loading dashboard", e);
        document.getElementById('stat-hearings').innerText = "-";
        document.getElementById('stat-cases').innerText = "-";
        document.getElementById('stat-tasks').innerText = "-";
        document.getElementById('stat-fees').innerText = "₹-";
    }
}

// Global Log Hearing Modal
async function openHearingModal() {
    // Ensure cases are loaded for the dropdown
    if (cases.length === 0) {
        // Fetch specific for dropdown if not already loaded
        const res = await fetch(`${API_BASE}/cases`);
        cases = await res.json();
    }

    const sel = document.getElementById('hearing-case-select');
    sel.innerHTML = '<option value="">Select Case...</option>';
    cases.forEach(c => {
        sel.innerHTML += `<option value="${c.id}">${c.case_number} - ${c.court}</option>`;
    });

    openModal('modal-hearing');
}

async function handleLogHearingGlobal(e) {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = Object.fromEntries(fd);
    body.case_id = parseInt(body.case_id);

    try {
        const res = await fetch(`${API_BASE}/hearings`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });
        if (res.ok) {
            closeModal('modal-hearing');
            e.target.reset();
            loadDashboard(); // Refresh stats
            if (document.getElementById('daily-board').classList.contains('active')) loadDailyBoard();
        }
    } catch (err) { console.error(err); }
}

// 2. Clients
async function loadClients() {
    const res = await fetch(`${API_BASE}/clients`);
    clients = await res.json();
}

function populateClientSelect() {
    const sel = document.getElementById('case-client-select');
    sel.innerHTML = '<option value="">Select Client...</option>';
    clients.forEach(c => {
        sel.innerHTML += `<option value="${c.id}">${c.full_name}</option>`;
    });
}

async function handleCreateClient(e) {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = Object.fromEntries(fd);

    await fetch(`${API_BASE}/clients`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });

    closeModal('modal-client');
    e.target.reset();
    loadClients(); // Reload global list
    if (document.getElementById('clients').classList.contains('active')) loadClientsTable();
}

async function loadClientsTable() {
    await loadClients();
    const tbody = document.getElementById('clients-list');
    tbody.innerHTML = clients.map(c => `
        <tr>
            <td>${c.full_name}</td>
            <td>${c.mobile || '-'}</td>
            <td>${c.email || '-'}</td>
            <td><button class="btn btn-secondary" onclick="viewClient(${c.id})">Details</button></td>
        </tr>
    `).join('');
}


function viewClient(id) {
    alert("Client Details: Implementation Pending\\nID: " + id);
}

// 3. Cases
async function loadCaseMaster() {
    const res = await fetch(`${API_BASE}/cases`);
    cases = await res.json();

    const tbody = document.getElementById('cases-list');
    tbody.innerHTML = cases.map(c => {
        const clientName = clients.find(cl => cl.id === c.client_id)?.full_name || 'Unknown';
        return `
        <tr>
            <td><b>${c.case_number}</b></td>
            <td>${clientName}</td>
            <td>${c.court}</td>
            <td>${c.case_type}</td>
            <td>${c.next_hearing || '-'}</td>
            <td><span class="status-badge status-${c.status === 'Active' ? 'active' : 'disposed'}">${c.status}</span></td>
            <td><button class="btn" onclick="openCaseDetail(${c.id})">View</button></td>
        </tr>
        `;
    }).join('');
}

async function handleCreateCase(e) {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = Object.fromEntries(fd);

    await fetch(`${API_BASE}/cases`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });

    closeModal('modal-case');
    e.target.reset();
    loadCaseMaster();
}

async function openCaseDetail(id) {
    // Ideally fetch details properly
    const res = await fetch(`${API_BASE}/cases/${id}`);
    const caseData = await res.json();
    openModal('modal-case-detail');

    const clientName = clients.find(cl => cl.id === caseData.client_id)?.full_name || 'Unknown';

    document.getElementById('case-detail-content').innerHTML = `
        <div class="case-detail-header">
            <div>
                <h3>${caseData.case_number}</h3>
                <p>Court: ${caseData.court}</p>
            </div>
            <div>
                <p>Client: <b>${clientName}</b></p>
                <p>Status: ${caseData.status}</p>
            </div>
        </div>
        
        <!-- Tabs inside Modal -->
        <div style="margin-bottom: 20px;">
           <button class="btn" onclick="loadCaseHearings(${id})">Hearings</button>
           <button class="btn btn-secondary">Tasks</button>
           <button class="btn btn-secondary">Fees</button>
        </div>
        
        <div id="case-inner-content">
            <p>Select a tab to view details.</p>
        </div>
    `;
    loadCaseHearings(id); // Default load hearings
}


// 4. Hearings / Daily Board
async function loadDailyBoard() {
    const res = await fetch(`${API_BASE}/dashboard`); // Contains upcoming hearings
    const data = await res.json();

    const tbody = document.getElementById('hearings-list');
    tbody.innerHTML = data.upcoming_hearings.map(h => `
        <tr>
            <td>${h.hearing_date}</td>
            <td>Case #${h.case_id}</td>
            <td>-</td>
            <td>${h.purpose || 'Hearing'}</td>
            <td><button class="btn btn-secondary">Update</button></td>
        </tr>
    `).join('');
}

async function loadCaseHearings(caseId) {
    const res = await fetch(`${API_BASE}/hearings?case_id=${caseId}`);
    const hearings = await res.json();

    document.getElementById('case-inner-content').innerHTML = `
        <h4>Hearing History</h4>
        <table style="font-size: 0.9em;">
            <thead><tr><th>Date</th><th>Purpose</th><th>Order</th><th>Next Date</th></tr></thead>
            <tbody>
                ${hearings.map(h => `
                    <tr>
                        <td>${h.hearing_date}</td>
                        <td>${h.purpose || '-'}</td>
                        <td>${h.order_passed || '-'}</td>
                        <td>${h.next_date || '-'}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
        
        <div style="margin-top: 20px; border-top: 1px solid #eee; padding-top: 15px;">
            <h4>Log New Hearing</h4>
            <form onsubmit="handleLogHearing(event, ${caseId})">
                <input type="hidden" name="case_id" value="${caseId}">
                <div class="form-grid">
                    <div class="form-group">
                        <label>Date</label>
                        <input type="date" name="hearing_date" required>
                    </div>
                    <div class="form-group">
                        <label>Next Hearing Date</label>
                        <input type="date" name="next_date">
                    </div>
                </div>
                 <div class="form-group">
                    <label>Order / Summary</label>
                    <textarea name="remarks" placeholder="What happened inside the court?"></textarea>
                </div>
                <button type="submit" class="btn">Update Diary</button>
            </form>
        </div>
    `;
}

async function handleLogHearing(e, caseId) {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = Object.fromEntries(fd);
    body.case_id = parseInt(caseId); // Ensure int

    await fetch(`${API_BASE}/hearings`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
    });

    loadCaseHearings(caseId); // Reload inner list
    loadCaseHearings(caseId); // Reload inner list
}

// 5. Fee Ledger
// 5. Fee Ledger
async function loadFeeLedger() {
    try {
        const tbody = document.getElementById('fees-list');
        // Placeholder for now as per user instruction, but allowing new entries
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center">Select a Case to view Fees or Log a new Fee. Global Ledger coming soon.</td></tr>';
    } catch (e) { console.error(e); }
}

async function openFeeModal() {
    // Ensure cases loaded
    if (cases.length === 0) {
        try {
            const res = await fetch(`${API_BASE}/cases`);
            cases = await res.json();
        } catch (e) { console.error("Error loading cases", e); }
    }

    const sel = document.getElementById('fee-case-select');
    sel.innerHTML = '<option value="">Select Case...</option>';
    cases.forEach(c => {
        sel.innerHTML += `<option value="${c.id}">${c.case_number} - ${c.court}</option>`;
    });

    openModal('modal-fee');
}

async function handleLogFee(e) {
    e.preventDefault();
    const fd = new FormData(e.target);
    const body = Object.fromEntries(fd);
    body.case_id = parseInt(body.case_id);
    body.amount_billed = parseFloat(body.amount_billed || 0);
    body.amount_received = parseFloat(body.amount_received || 0);

    try {
        await fetch(`${API_BASE}/fees`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        closeModal('modal-fee');
        e.target.reset();
        loadDashboard();
        loadFeeLedger();
    } catch (err) { console.error(err); }
}

