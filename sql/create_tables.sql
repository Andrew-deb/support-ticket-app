-- =============================================
-- Lakebase Schema Setup for Support Ticket App
-- =============================================
-- Run this SQL against your Lakebase instance to create the required tables.
-- You can run it via DBeaver, pgAdmin, a Python script, or the Databricks SQL Editor.

-- Table 1: tickets
-- Stores each support ticket
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('open', 'in_progress', 'resolved')),
    created_by TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Table 2: ticket_messages
-- Stores messages/conversations on each ticket
-- ticket_id is a foreign key linking each message to its parent ticket
CREATE TABLE IF NOT EXISTS ticket_messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID NOT NULL REFERENCES tickets(ticket_id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    author TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
