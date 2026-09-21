# Feature inventory — source-derived starting checklist

Derived from `README.md`, `DEVELOPER.md` §3, §4, §9, §10, §16 and
`Feature-Testing-Manual/` at the revision you resolve. **Every row is a
hypothesis until a real run confirms it.** Reconcile, then copy the confirmed
set into `coverage.json` with measured evidence. Do not carry a row you did
not see.

## Public / unauthenticated
| id | Where | What to show |
|---|---|---|
| landing | `/` | Marketing page; signed-in visitor bounces to `/dashboard`. |
| sign-in-wall | `/sign-in` | Clerk form appears. **Human signs in; agent never types here.** |
| join-signed-out | `/join/CLS-…` | Redirects to sign-in with `redirect_url` preserved. |

## Student
| id | Where | What to show |
|---|---|---|
| onboarding | `/onboarding` | Role / institution / course intake; routes on submit. |
| library | `/dashboard` | Textbook cards; public books open immediately. |
| empty-state | `/dashboard` | New student with no access sees the empty state. |
| request-access | card → Request | Private textbook → Pending; admin sees it. |
| hidden-invisible | `/dashboard` | Hidden textbook absent from student library. |
| join-by-code | `/join/[code]` or dashboard field | Invite preview → join → class appears, access granted. |
| join-limits | `/join/[code]` | Wrong domain / full / expired code is refused with a message. |
| open-textbook | card → Open | Token minted, redirect with `?access_token`, protected page loads (or stop at hub, stated). |
| settings | `/settings` | Name edit + Clerk profile; role-aware back-link. |
| logout | Logout button | Hub session ends; an open textbook tab loses access (§4.4). |

## Instructor
| id | Where | What to show |
|---|---|---|
| instructor-request | onboarding → pending screen | Holding screen until admin approves. |
| class-create | dashboard | Create class, assign textbooks. |
| invite-create | class panel | `CLS-XXXXXX` code with domain / capacity / expiry. |
| roster | class panel | Enrolled students listed after a join. |
| concept-map-permission | admin grants → `/concept-map/[id]` | Instructor can open the editor only after the grant. |

## Admin (`/admin` tabs)
| id | Tab | What to show |
|---|---|---|
| textbook-register | textbooks | Create with image upload, status `public`/`private`/`hidden`. |
| textbook-status-change | textbooks | Flip status; effect on a student library. |
| textbook-delete | textbooks | Delete with confirmation. |
| textbook-view-all | view-textbooks | Admin sees hidden books too. |
| users-list | users | First 100 Clerk users. |
| set-role | users / admins | Promote to admin; approve instructor request (email fires only if Resend configured — say so). |
| requests-approve-deny | requests | Approve one, deny one; student side updates. |
| classes-overview | classes | All classes and rosters. |
| concept-map-import | concept-maps | Import a pipeline run from S3 (or local sample if AWS unset — label it). |
| concept-map-review | `/concept-map/[id]` | Keyboard-driven accept / edit / remove; progress header. |
| concept-map-export | editor | Export blocked while pending; succeeds when clean. |
| analytics-dashboard | `/admin/analytics` | Overview / users / user-detail (PostHog key required; otherwise a labeled blocker). |

## Service / api-only (no screen — transcript or `api-only`)
| id | Endpoint |
|---|---|
| access-verify | `POST /api/access/verify` from a textbook site |
| cors-auto-whitelist | registering a URL whitelists its origin (source fact, §5.1) |
| memory-api | `/api/memory/*` with `MEMORY_API_SECRET` — **never show the secret** |
| articles-api | `GET /api/articles/*` public glossary |
| first-party-analytics | session start/end beacons |

## Planned / dormant (Verdict material, not beats)
Password-change invalidation (§4.5), `medhavy-ui` chassis (§17), tutor
persona registry (`docs/tutor-persona-proposal.md`), `status='verified'`
concept-map state, non-atomic analytics summaries (§11.1), the two
1,000-line dashboards as refactor debt (§9).
