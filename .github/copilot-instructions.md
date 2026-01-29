# AI Copilot Instructions — IMS2 (Inventory Management System)

## Architecture Overview

**IMS2** is a hybrid **Document/Inventory Monitoring System** with dual-stack components:

### Frontend Stack
- **Primary App**: [index.html](index.html) + [app.js](app.js) — localStorage-based document management
- **Specialized Views**: Separate HTML pages for admin inbox ([admin_inbox.html](admin_inbox.html)), cycle counting ([cycle_count.html](cycle_count.html)), user dashboards, etc.
- **Styling**: Centralized [styles.css](styles.css) with dark theme support (`body.dark-mode` class)
- **Storage**: Browser `localStorage` with keys prefixed `dms_*` (docs, users, auth, recycle bin)

### Backend Stack
- **Node.js/Express Server**: [server.js](server.js) — optional sync layer for multi-device scenarios
- **Database**: [db.json](db.json) — persistent file-based store (users, documents, sessions)
- **Real-time**: WebSocket support (`/ws` endpoint) for push updates to connected clients
- **Python Monitoring**: [monitoring_system_v3.py](monitoring_system_v3.py) — separate metrics collection service

### Data Flow
1. **Client-First**: App loads and renders from localStorage immediately
2. **Optional Sync**: If server is reachable (`/api/ping`), establishes WebSocket + 5-second polling
3. **Server Updates**: Changes broadcast via WebSocket to all connected clients
4. **Fallback**: If server unavailable, app continues offline using localStorage only

## Key Components & Patterns

### Authentication (app.js)
- **Demo credentials**: `admin` / `password` or `user` / `password`
- **Tokens**: Session tokens stored in localStorage (`dms_auth_token_v1`) and server sessions (`db.json`)
- **Role-based**: `admin` and `user` roles control UI visibility (recycle bin, user dashboard hidden for non-admins)
- **Inactivity**: Auto-logout after 1 hour (`INACTIVITY_MS = 60*60*1000`)

### Document Model
```javascript
{
  controlNumber: string,
  title: string,
  owner: string,
  status: enum,  // e.g., 'Approved', 'Revision', 'Pending for Approve'
  winsStatus: enum,  // 'Approved', 'Pending for Approve', 'Rejected'
  createdAt: timestamp,
  updatedAt: timestamp,
  notes: string,
  forwarded: boolean,  // Admin workflow state
  adminStatus: enum  // 'Received', 'Returned', 'Need User Attention'
}
```

### Admin Inbox Workflow
- Docs marked with `forwarded: true` appear in admin view
- Statuses: `Received` → `Returned` (with optional `returnReason`) → `Need User Attention`
- Sidebar shows count badges; admin page filters by status and search query

### CSV Import/Export
- Headers: `controlNumber,title,owner,status,winsStatus,createdAt,updatedAt`
- Duplicate handling: prompt user to overwrite or skip
- Template available via "Download Template" button

## Critical Developer Workflows

### Local Development
```bash
npm install && npm start  # Starts Express on :3000, serves static files
```

### Running Without Server
- Open [index.html](index.html) directly in browser (e.g., live-server, double-click)
- App detects server unavailability and continues offline with localStorage

### Testing
- `test_storage.py` — Python test suite for monitoring system
- Manual smoke test: import sample CSV with `TEST-*` control numbers

### Debugging Multi-Device Sync
- WebSocket connection status logged in browser console
- Server sync polls every 5 seconds if WebSocket unavailable
- Check browser DevTools → Application → Local Storage → `dms_*` keys

## Project-Specific Conventions

### Naming & Storage Keys
- **Storage prefix**: `dms_*` (e.g., `dms_docs_v1`, `dms_auth_v1`)
- **API routes**: `/api/docs`, `/api/auth/login`, `/api/auth/forgot`
- **WebSocket event type**: `msg.type === 'docs_updated'` triggers full fetch

### HTML Page Structure
- **Header/Navbar**: Consistent across pages (edit via [navbar.html](navbar.html) snippet)
- **Sidebar**: Navigation toggles on mobile
- **Modals**: Form overlays use `.hidden` class for visibility toggle
- **Dark Mode**: Applied via `body.dark-mode` CSS class

### Error & Status Communication
- `announceStatus(msg)` — temporary screen-reader announcements (`#sr-status`)
- Toast notifications for user feedback
- Graceful fallback if server/WebSocket unavailable

## Integration Points & External Dependencies

### Server Endpoints
| Method | Route | Purpose |
|--------|-------|---------|
| POST | `/api/auth/login` | Authenticate user, return token |
| GET | `/api/docs` | Fetch all docs (syncs to client) |
| POST/PUT | `/api/docs` | Create/update docs (broadcast via WS) |
| GET | `/api/ping` | Health check (triggers `USE_SERVER = true`) |
| WS | `/ws` | Real-time push updates |

### Dependencies
- **Frontend**: Chart.js (CDN) for dashboard visualizations
- **Backend**: bcryptjs (password hashing), express, cors, ws (WebSocket), uuid
- **Python**: sqlite3, urllib, logging (monitoring system)

## Common Modification Patterns

### Adding a New Document Field
1. Update Model schema in code comments
2. Add input to form in [index.html](index.html) (form ID: `doc-form`)
3. Update CSV headers in export/import functions
4. Add rendering to `renderDocs()` in [app.js](app.js)
5. Sync to server: POST `/api/docs` will persist

### Adding Admin Workflow Status
1. Define enum value in document model
2. Update `adminStatus` labels in `renderDocs()` 
3. Add filter button in [admin_inbox.html](admin_inbox.html)
4. Update backend to validate status transitions

### Connecting a New HTML Page
- Import shared styles: `<link rel="stylesheet" href="styles.css" />`
- Load auth state from localStorage or fetch via `/api/docs`
- Use consistent navbar markup from [navbar.html](navbar.html)
- Implement inactivity timer same as [app.js](app.js) pattern

## Notes for AI Agents

- **Backward compatibility**: Storage versioning (`dms_*_v1`) allows safe schema evolution
- **Offline-first design**: Always prioritize localStorage as source of truth; server is optional enhancement
- **Minimal state management**: No frameworks—vanilla JS with localStorage and fetch; keep it simple
- **Browser APIs only**: No Node-specific code in client; use fetch, WebSocket, localStorage
