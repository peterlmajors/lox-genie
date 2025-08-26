# API Documentation

This directory contains the FastAPI routers for the Lox API, providing endpoints for fantasy football data integration with Sleeper and FantasyCalc APIs.

## Overview

The API is organized into five main modules, each handling specific aspects of fantasy football data:

- **FantasyCalc Integration** - Crowdsourced player values via optimization algorithim
- **Sleeper User Management** - User profiles and league participation
- **Sleeper Team Management** - Roster management and team data
- **Sleeper League Management** - League-wide data and user teams
- **Sleeper Draft Management** - Draft picks and auction data

## API Endpoints

### FantasyCalc (`/fantasycalc`)

#### `GET /fantasycalc/rankings`

Retrieves player rankings from FantasyCalc API with customizable parameters.

**Query Parameters:**

- `dynasty` (bool, default: false) - Whether to get dynasty rankings
- `superflex` (bool, default: true) - Whether league is superflex (2 QB)
- `teams` (int, default: 10) - Number of teams in league
- `ppr` (float, default: 1) - Points per reception setting
- `top_n` (int, default: 10) - Number of top players to return

**Response:** List of player rankings with fantasy values

**Example:**

```bash
GET /fantasycalc/rankings?dynasty=true&superflex=true&teams=12&ppr=1&top_n=50
```

### Sleeper User (`/sleeper_user`)

#### `GET /sleeper_user/users/{user_id}/leagues`

Get all NFL leagues for a user with metadata including scoring settings and league configuration.

**Path Parameters:**

- `user_id` (int) - Sleeper user ID

**Query Parameters:**

- `season` (int, default: current NFL year) - Season to query

**Response:** List of leagues with metadata, scoring settings, and league type flags (PPR, superflex, etc.)

#### `GET /sleeper_user/users/{user_id}/leagues/{league_id}/waiver_budget`

Get waiver budget information for a specific user or all users in a league.

**Path Parameters:**

- `user_id` (int) - Sleeper user ID
- `league_id` (str) - League ID

**Response:** Waiver budget used (int) for specific user or dict of all users' budgets

#### `GET /sleeper_user/users/{user_id}/leagues/{league_id}/record`

Get win/loss record for a user in a specific league.

**Response:** `{"wins": int, "losses": int}`

#### `GET /sleeper_user/users/{user_id}/leagues/current/record`

Get records for all current leagues for a user.

**Response:** List of records with league names and IDs

#### `GET /sleeper_user/users/{user_id}/leagues/previous/record`

Get records for all previous leagues for a user.

**Response:** List of records with league names and IDs

#### `GET /sleeper_user/users/{user_id}/leagues/{league_id}/win_percentage`

Calculate win percentage for a user in a league.

**Response:** Win percentage as float (0.0-1.0)

#### `GET /sleeper_user/users/{user_id}/leagues/season/{year}/record`

Get user records for a specific season across all leagues.

**Response:** List of records for the specified season

### Sleeper Team (`/sleeper_team`)

#### `GET /sleeper_team/leagues/{league_id}/users/{user_id}/roster`

Get detailed roster information for a user including starters, bench players, and taxi squad.

**Path Parameters:**

- `league_id` (str) - League ID
- `user_id` (str) - User ID

**Response:** Roster data with player IDs, starters, non-starters, taxi squad, and nicknames

#### `GET /sleeper_team/leagues/{league_id}/users/{user_id}/waiver_budget`

Get waiver budget information (duplicate of user endpoint for team context).

### Sleeper Leagues (`/sleeper_leagues`)

#### `GET /sleeper_leagues/leagues/{league_id}/rosters`

Get all rosters in a league with optional user exclusion.

**Path Parameters:**

- `league_id` (str) - League ID

**Query Parameters:**

- `exclude_names` (str or list[str], optional) - User display names to exclude

**Response:** DataFrame with all league rosters

#### `GET /sleeper_leagues/leagues/{league_id}/users`

Get all users and their team names in a league.

**Response:** List of users with user_id, display_name, and team_name

### Sleeper Draft (`/sleeper_draft`)

#### `GET /sleeper_draft/leagues/{league_id}/drafts/{draft_id}/picks`

Get detailed draft picks for a specific draft with player and team information.

**Path Parameters:**

- `league_id` (int) - League ID
- `draft_id` (int) - Draft ID

**Response:** List of draft picks with player details, team info, and auction prices (if applicable)

#### `GET /sleeper_draft/leagues/{league_id}/picks`

Get all draft picks for a league across all drafts (rookie and auction).

**Response:** Polars DataFrame with comprehensive pick history

## Data Models

### League Metadata

```json
{
  "league_id": "string",
  "draft_id": "string",
  "name": "string",
  "status": "string",
  "season_type": "string",
  "total_rosters": "integer",
  "roster_positions": "object",
  "offense_scoring": "object",
  "defense_scoring": "object",
  "kicker_scoring": "object",
  "ppr": "boolean",
  "tight_end_premium": "boolean",
  "superflex": "boolean"
}
```

### Roster Data

```json
{
  "user_id": "string",
  "starters": ["string"],
  "non_starters": ["string"],
  "taxi": ["string"],
  "nicknames": "object"
}
```

### Draft Pick

```json
{
  "player_id": "string",
  "player_name": "string",
  "round": "integer",
  "pick": "integer",
  "user_id": "string",
  "team_name": "string",
  "display_name": "string",
  "price": "integer" // for auction drafts
}
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found (user/league not found)
- `502` - Bad Gateway (external API errors)

## Configuration

The API uses settings from `config.py` including:

- NFL year and data ranges
- Scoring stat categories (offense, defense, kicker)
- API keys and endpoints
- League-specific settings

## Dependencies

- FastAPI
- httpx (for external API calls)
- pandas/polars (for data processing)
- Pydantic (for data validation)

## Usage Examples

### Get User's Current League Records

```bash
curl "http://localhost:8000/sleeper_user/users/12345/leagues/current/record"
```

### Get League Rosters

```bash
curl "http://localhost:8000/sleeper_leagues/leagues/league123/rosters"
```

### Get Dynasty Rankings

```bash
curl "http://localhost:8000/fantasycalc/rankings?dynasty=true&superflex=true&teams=12&top_n=100"
```

### Get Draft History

```bash
curl "http://localhost:8000/sleeper_draft/leagues/league123/picks"
```
