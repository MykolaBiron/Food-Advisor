# FoodAdvisor API Documentation Template

Use this document as the human-readable API contract for frontend integration.
Keep it versioned in git and update it in every backend PR that changes API behavior.

## 1) API Overview

- API Name: FoodAdvisor API
- Version: v1
- Base URLs:
  - Local: http://127.0.0.1:8000/api/v1
  - Staging: <staging-url>
  - Production: <production-url>
- Response format: application/json
- Time format: ISO 8601 in UTC

## 2) Authentication

- Auth type: Session or JWT (pick one and keep this section updated)
- Protected routes: Require authenticated user
- Header (JWT):
  - Authorization: Bearer <access_token>

### Login Example

Request:
```http
POST /api/v1/auth/login/
Content-Type: application/json

{
  "username": "demo_user",
  "password": "demo_password"
}
```

Success response (example):
```json
{
  "access": "<jwt-access-token>",
  "refresh": "<jwt-refresh-token>"
}
```

## 3) Global Error Format

Use a consistent error shape across endpoints.

```json
{
  "detail": "Human readable error",
  "code": "optional_machine_code",
  "fields": {
    "field_name": ["Validation message"]
  }
}
```

## 4) Common HTTP Status Codes

- 200 OK: Successful read or update
- 201 Created: Resource created
- 400 Bad Request: Validation or malformed payload
- 401 Unauthorized: Missing/invalid auth
- 403 Forbidden: Authenticated but not allowed
- 404 Not Found: Resource not found or not owned by user
- 500 Internal Server Error: Unexpected backend error

## 5) Endpoint Contract Template

Copy this block for each endpoint.

---

### <Endpoint Name>

- Method: <GET|POST|PATCH|PUT|DELETE>
- Path: `<path>`
- Auth required: <Yes|No>
- Purpose: <one sentence>

Request headers:
- Content-Type: application/json
- Authorization: Bearer <access_token> (if required)

Path params:
- `<param>`: <type> - <description>

Query params:
- `<param>`: <type> - <description>

Request body:
```json
{
  "field": "value"
}
```

Success response (status <code>):
```json
{
  "field": "value"
}
```

Error responses:
- 400: <when>
- 401: <when>
- 403: <when>
- 404: <when>

Notes:
- <business rule 1>
- <business rule 2>

---

## 6) FoodAdvisor Initial Endpoint Specs

Fill these first so frontend can begin implementation.

### Register

- Method: POST
- Path: `/api/v1/auth/register/`
- Auth required: No
- Purpose: Create a new user account.

Request body:
```json
{
  "username": "new_user",
  "password": "strong_password"
}
```

Success response (201):
```json
{
  "id": 12,
  "username": "new_user"
}
```

### Create or Update Profile

- Method: POST (or PATCH if updating existing)
- Path: `/api/v1/profile/create/`
- Auth required: Yes
- Purpose: Save profile details and calculate daily nutrition targets.

Request body:
```json
{
  "age": 25,
  "sex": "male",
  "height": 180,
  "weight": 78,
  "goal": "maintain_weight",
  "activity": "moderate",
  "num_workouts": "2-3"
}
```

Success response (201 or 200):
```json
{
  "user": 12,
  "age": 25,
  "sex": "male",
  "height": 180,
  "weight": 78.0,
  "goal": "maintain_weight",
  "activity": "moderate",
  "num_workouts": "2-3",
  "calories": 2460,
  "proteins": 148,
  "carbs": 307,
  "fats": 71
}
```

### Save Meal

- Method: PATCH
- Path: `/api/v1/meals/{meal_id}/save/`
- Auth required: Yes
- Purpose: Mark a meal as saved for the current user.

Path params:
- meal_id: integer - Meal primary key.

Success response (200):
```json
{
  "detail": "Meal saved successfully",
  "meal_id": 55,
  "saved": true
}
```

### Search Food

- Method: GET
- Path: `/api/v1/foods/search/`
- Auth required: Yes (or No, if you decide it is public)
- Purpose: Search food options from USDA.

Query params:
- q: string - Search term.

Success response (200):
```json
{
  "foods": [
    {
      "description": "Chicken breast",
      "fdcId": 12345
    }
  ]
}
```

## 7) Pagination Contract (if used)

```json
{
  "count": 120,
  "next": "http://127.0.0.1:8000/api/v1/meals/?page=2",
  "previous": null,
  "results": [
    { "id": 1, "name": "Pasta" }
  ]
}
```

## 8) Frontend Integration Checklist

- Base URL configured by environment (local/staging/prod)
- Auth token storage implemented (SecureStore for Expo)
- Authorization header attached to protected requests
- 401 handling with login redirect or token refresh
- Consistent error parser for `detail` and `fields`

## 9) API Changelog

Add one entry per backend PR that changes API behavior.

### 2026-04-13

- Added: initial endpoint documentation template.
- Changed: <fill when endpoints are finalized>
- Deprecated: <fill if anything is being replaced>

## 10) Team Rules

- Every new endpoint must be documented before merge.
- Every API change must include one example request and response.
- Breaking changes require:
  - changelog entry
  - frontend notification
  - migration window or version bump
