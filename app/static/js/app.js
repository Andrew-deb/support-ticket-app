// ==========================================
// Support Ticket App — Frontend JavaScript
// ==========================================
// This file handles all communication between the browser UI (index.html)
// and the FastAPI backend (/api/tickets, /api/tickets/{id}/messages).
//
// PATTERN: Every user action triggers a fetch() call to the API,
// then updates the DOM with the response.

const API_BASE = "/api/tickets";

// ==========================================
// STATE — tracks current UI state
// ==========================================
let allTickets = [];           // Full list of tickets from the API
let currentFilter = "all";     // Active filter tab
let selectedTicketId = null;   // Currently selected ticket

// ==========================================
// INITIALIZATION — runs when page loads
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
    loadTickets();
});

// ==========================================
// TICKET LIST — Fetch and display all tickets
// ==========================================

async function loadTickets() {
    showLoading(true);
    try {
        const res = await fetch(API_BASE + "/");
        if (!res.ok) throw new Error("Failed to load tickets");
        allTickets = await res.json();
        renderTickets();
        updateStats();
    } catch (err) {
        showToast("Error loading tickets: " + err.message, "error");
    } finally {
        showLoading(false);
    }
}

function renderTickets() {
    const list = document.getElementById("ticket-list");

    // Apply filter
    const filtered = currentFilter === "all"
        ? allTickets
        : allTickets.filter(t => t.status === currentFilter);

    if (filtered.length === 0) {
        list.innerHTML = `
            <div class="empty-state">
                <p>${currentFilter === "all" ? "No tickets yet." : `No ${currentFilter.replace("_", " ")} tickets.`}</p>
                <button class="btn btn-primary" onclick="openCreateModal()">Create First Ticket</button>
            </div>`;
        return;
    }

    list.innerHTML = filtered.map((ticket, i) => `
        <div class="ticket-card ${ticket.ticket_id === selectedTicketId ? 'active' : ''}"
             onclick="selectTicket('${ticket.ticket_id}')"
             style="animation-delay: ${i * 0.05}s">
            <div class="ticket-card-header">
                <span class="ticket-card-title">${escapeHtml(ticket.title)}</span>
                <span class="status-badge ${ticket.status}">${formatStatus(ticket.status)}</span>
            </div>
            <div class="ticket-card-meta">
                <span>${escapeHtml(ticket.created_by)}</span>
                <span>${formatDate(ticket.created_at)}</span>
            </div>
        </div>
    `).join("");
}

function updateStats() {
    document.getElementById("stat-total").textContent = allTickets.length;
    document.getElementById("stat-open").textContent = allTickets.filter(t => t.status === "open").length;
    document.getElementById("stat-progress").textContent = allTickets.filter(t => t.status === "in_progress").length;
    document.getElementById("stat-resolved").textContent = allTickets.filter(t => t.status === "resolved").length;
}

// ==========================================
// FILTER — Switch between status tabs
// ==========================================

function setFilter(filter, btn) {
    currentFilter = filter;

    // Update active tab styling
    document.querySelectorAll(".filter-tab").forEach(t => t.classList.remove("active"));
    btn.classList.add("active");

    renderTickets();
}

// ==========================================
// TICKET DETAIL — View a single ticket
// ==========================================

async function selectTicket(ticketId) {
    selectedTicketId = ticketId;
    const ticket = allTickets.find(t => t.ticket_id === ticketId);
    if (!ticket) return;

    // Update the detail panel
    document.getElementById("detail-title").textContent = ticket.title;
    document.getElementById("detail-created-by").textContent = "Created by: " + ticket.created_by;
    document.getElementById("detail-created-at").textContent = "Created: " + formatDate(ticket.created_at);
    document.getElementById("detail-status-select").value = ticket.status;

    // Show the detail panel
    document.getElementById("ticket-detail").style.display = "block";

    // Highlight the active card
    renderTickets();

    // Load messages for this ticket
    await loadMessages(ticketId);
}

function closeDetail() {
    selectedTicketId = null;
    document.getElementById("ticket-detail").style.display = "none";
    renderTickets();
}

// ==========================================
// STATUS UPDATE — Change ticket status
// ==========================================

async function updateTicketStatus() {
    if (!selectedTicketId) return;

    const newStatus = document.getElementById("detail-status-select").value;

    try {
        const res = await fetch(`${API_BASE}/${selectedTicketId}/status`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: newStatus }),
        });

        if (!res.ok) throw new Error("Failed to update status");

        showToast(`Status updated to "${formatStatus(newStatus)}"`, "success");
        await loadTickets();

        // Re-select the ticket to refresh the detail view
        await selectTicket(selectedTicketId);
    } catch (err) {
        showToast("Error updating status: " + err.message, "error");
    }
}

// ==========================================
// DELETE TICKET — Remove a ticket permanently
// ==========================================

async function deleteTicket() {
    if (!selectedTicketId) return;

    // Confirmation dialog to prevent accidental deletion
    const confirmed = confirm("Are you sure you want to delete this ticket? All messages will be deleted too.");
    if (!confirmed) return;

    try {
        const res = await fetch(`${API_BASE}/${selectedTicketId}`, {
            method: "DELETE",
        });

        if (!res.ok && res.status !== 204) throw new Error("Failed to delete ticket");

        showToast("Ticket deleted", "success");
        closeDetail();
        await loadTickets();
    } catch (err) {
        showToast("Error deleting ticket: " + err.message, "error");
    }
}

// ==========================================
// MESSAGES — Load and display messages
// ==========================================

async function loadMessages(ticketId) {
    const messagesList = document.getElementById("messages-list");
    messagesList.innerHTML = '<div class="loading-spinner"><div class="spinner"></div></div>';

    try {
        const res = await fetch(`${API_BASE}/${ticketId}/messages`);
        if (!res.ok) throw new Error("Failed to load messages");

        const messages = await res.json();

        if (messages.length === 0) {
            messagesList.innerHTML = '<p class="no-messages">No messages yet. Start the conversation below.</p>';
            return;
        }

        messagesList.innerHTML = messages.map(msg => `
            <div class="message-bubble">
                <div class="message-author">${escapeHtml(msg.author)}</div>
                <div class="message-text">${escapeHtml(msg.message_text)}</div>
                <div class="message-time">${formatDate(msg.created_at)}</div>
            </div>
        `).join("");

        // Auto-scroll to the latest message
        messagesList.scrollTop = messagesList.scrollHeight;
    } catch (err) {
        messagesList.innerHTML = '<p class="no-messages">Error loading messages.</p>';
    }
}

async function submitMessage(event) {
    event.preventDefault();

    if (!selectedTicketId) return;

    const author = document.getElementById("msg-author").value.trim();
    const text = document.getElementById("msg-text").value.trim();

    if (!author || !text) {
        showToast("Please fill in all fields", "error");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/${selectedTicketId}/messages`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message_text: text, author: author }),
        });

        if (!res.ok) throw new Error("Failed to send message");

        // Clear the form and reload messages
        document.getElementById("msg-text").value = "";
        showToast("Message sent!", "success");
        await loadMessages(selectedTicketId);
    } catch (err) {
        showToast("Error sending message: " + err.message, "error");
    }
}

// ==========================================
// CREATE TICKET — Modal form
// ==========================================

function openCreateModal() {
    document.getElementById("create-modal").style.display = "flex";
    document.getElementById("create-title").focus();
}

function closeCreateModal(event) {
    // If called from overlay click, only close if clicking the overlay itself
    if (event && event.target !== event.currentTarget) return;
    document.getElementById("create-modal").style.display = "none";
    document.getElementById("create-ticket-form").reset();
}

async function submitNewTicket(event) {
    event.preventDefault();

    const title = document.getElementById("create-title").value.trim();
    const createdBy = document.getElementById("create-author").value.trim();

    if (!title || !createdBy) {
        showToast("Please fill in all fields", "error");
        return;
    }

    const submitBtn = document.getElementById("btn-submit-ticket");
    submitBtn.disabled = true;
    submitBtn.textContent = "Creating...";

    try {
        const res = await fetch(API_BASE + "/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ title: title, created_by: createdBy, status: "open" }),
        });

        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.detail || "Failed to create ticket");
        }

        closeCreateModal();
        showToast("Ticket created successfully!", "success");
        await loadTickets();
    } catch (err) {
        showToast("Error: " + err.message, "error");
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = "Create Ticket";
    }
}

// ==========================================
// UTILITY FUNCTIONS
// ==========================================

function formatStatus(status) {
    const map = { open: "Open", in_progress: "In Progress", resolved: "Resolved" };
    return map[status] || status;
}

function formatDate(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

function showLoading(show) {
    const loader = document.getElementById("loading");
    if (loader) loader.style.display = show ? "flex" : "none";
}

function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);

    // Auto-remove after 4 seconds
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateX(40px)";
        toast.style.transition = "all 0.3s ease";
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}
