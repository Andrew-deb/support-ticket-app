-- =============================================
-- Sample Data for Support Ticket App
-- =============================================
-- Inserts 3 tickets (with different statuses) and 2 messages per ticket.
-- Run this AFTER create_tables.sql.

-- -----------------------------------------------
-- Ticket 1: Open ticket about Wi-Fi issues
-- -----------------------------------------------
INSERT INTO tickets (title, status, created_by)
VALUES ('Wi-Fi not working in Building 3', 'open', 'john@company.com');

-- Messages for Ticket 1 (we'll use a subquery to get the ticket_id)
INSERT INTO ticket_messages (ticket_id, message_text, author)
VALUES (
    (SELECT ticket_id FROM tickets WHERE title = 'Wi-Fi not working in Building 3'),
    'The Wi-Fi has been down since this morning. Multiple employees are affected.',
    'john@company.com'
);

INSERT INTO ticket_messages (ticket_id, message_text, author)
VALUES (
    (SELECT ticket_id FROM tickets WHERE title = 'Wi-Fi not working in Building 3'),
    'We are looking into this. Can you confirm which floor you are on?',
    'support@company.com'
);

-- -----------------------------------------------
-- Ticket 2: In-progress ticket about HR portal
-- -----------------------------------------------
INSERT INTO tickets (title, status, created_by)
VALUES ('Cannot access HR portal - login error', 'in_progress', 'jane@company.com');

INSERT INTO ticket_messages (ticket_id, message_text, author)
VALUES (
    (SELECT ticket_id FROM tickets WHERE title = 'Cannot access HR portal - login error'),
    'I keep getting a 403 Forbidden error when trying to access the HR portal.',
    'jane@company.com'
);

INSERT INTO ticket_messages (ticket_id, message_text, author)
VALUES (
    (SELECT ticket_id FROM tickets WHERE title = 'Cannot access HR portal - login error'),
    'Your permissions have been updated. Please try clearing your browser cache and logging in again.',
    'admin@company.com'
);

-- -----------------------------------------------
-- Ticket 3: Resolved ticket about software install
-- -----------------------------------------------
INSERT INTO tickets (title, status, created_by)
VALUES ('Request for Adobe Creative Suite installation', 'resolved', 'mike@company.com');

INSERT INTO ticket_messages (ticket_id, message_text, author)
VALUES (
    (SELECT ticket_id FROM tickets WHERE title = 'Request for Adobe Creative Suite installation'),
    'I need Adobe Creative Suite installed on my workstation for the upcoming design project.',
    'mike@company.com'
);

INSERT INTO ticket_messages (ticket_id, message_text, author)
VALUES (
    (SELECT ticket_id FROM tickets WHERE title = 'Request for Adobe Creative Suite installation'),
    'Adobe Creative Suite has been installed on your machine. Please restart and confirm it is working.',
    'support@company.com'
);
