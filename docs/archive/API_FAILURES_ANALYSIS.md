# API Failures Analysis from HAR Logs

## Summary
- **Total Requests**: 29
- **Successful (200)**: 15 ✅
- **Failed/Error**: 14 ❌
- **Fonts/Resources**: 3 (not counted as API failures)

## Success Rate by Category
- **Working APIs**: 10 agencies ✅
- **Failing APIs**: 4 agencies ❌
- **Partial Issues**: 3 agencies (timeouts, rate limits, etc.) ⚠️

---

## Detailed Failure Analysis

### 1. TIMEOUTS (0) - 2 Requests
These APIs didn't respond within the timeout window.

#### BLS API Timeout ⏱️
- **Request**: `POST api.bls.gov/publicAPI/v2/timeseries/data/`
- **Status**: 0 (Timeout)
- **Root Cause**: CORS - POST-based API, browser doesn't support CORS
- **Solution**: ✅ Use Flask backend proxy (already implemented)
- **Action**: No change needed - working as designed

#### FTC ReportPortal Timeout ⏱️
- **Request**: `GET reportportal.ftc.gov/api/widget/data`
- **Status**: 0 (Timeout)
- **Root Cause**: API endpoint unreachable or extremely slow
- **Solution**: Fix endpoint or disable for now
- **Action**: **NEEDS FIX** - Check if API endpoint is correct

---

### 2. 404 NOT FOUND - 3 Requests
API endpoints don't exist at the specified URLs.

#### DOJ Press Releases 404 ❌
- **Request**: `GET www.justice.gov/api/v1/press-releases`
- **Status**: 404
- **Root Cause**: Wrong endpoint URL
- **Current Code**:
  ```javascript
  doj: { fetch: async (sub, query, opts = {}) => {
    const url = `https://www.justice.gov/api/v1/press-releases?pagesize=${opts.limit || 20}`;
    // ... fetch
  }}
  ```
- **Solution**: Check DOJ API documentation for correct endpoint
- **Likely Fix**: May need different base URL or endpoint structure
- **Action**: **NEEDS FIX** - Update endpoint URL

#### FCC Equipment 404 ❌
- **Request**: `GET opendata.fcc.gov/resource/i5ic-sdri.json`
- **Status**: 404
- **Note**: The log shows `3b3k-34jp.json` **succeeded** with 200!
- **Root Cause**: Using wrong Socrata dataset ID
- **Solution**: Use dataset `3b3k-34jp` instead of `i5ic-sdri`
- **Action**: **NEEDS FIX** - Update dataset ID in code

#### EPA TRI 404 ❌
- **Request**: `GET www.epa.gov/enviro/api/tri/search.json`
- **Status**: 404
- **Root Cause**: Wrong endpoint URL
- **Solution**: Check EPA environmental data API documentation
- **Likely Fix**: May need different structure or parameters
- **Action**: **NEEDS FIX** - Update endpoint URL

---

### 3. 422 UNPROCESSABLE ENTITY - 2 Requests
Request was malformed or missing required parameters.

#### USAspending 422 ❌
- **Request**: `POST api.usaspending.gov/api/v2/search/spending_by_award/`
- **Status**: 422
- **Root Cause**: Missing required request body field
- **Current Code**: Likely missing `filters` field in POST body
- **Solution**: Add required fields to POST payload
- **Likely Fix**:
  ```javascript
  {
    filters: {},  // Required field
    limit: 20,
    offset: 0
  }
  ```
- **Action**: **NEEDS FIX** - Update POST body structure

#### FEC Candidates 422 ❌
- **Request**: `GET api.open.fec.gov/v1/candidates/?api_key=DEMO_KEY&...`
- **Status**: 422
- **Root Cause**: Invalid query parameters
- **Current Code**: Likely using wrong parameter names or values
- **Solution**: Check FEC API documentation
- **Likely Fix**: Parameter names may be different
- **Action**: **NEEDS FIX** - Update query parameters

---

### 4. 429 RATE LIMITED - 1 Request ⚠️
API received too many requests from this client.

#### NASA APOD 429 ⚠️
- **Request**: `GET api.nasa.gov/planetary/apod?api_key=DEMO_KEY&...`
- **Status**: 429 (Too Many Requests)
- **Root Cause**: Using `DEMO_KEY` which has strict rate limits
- **Solution**: User needs to provide their own NASA API key
- **Current Behavior**: Gracefully degrades (shows error message)
- **Action**: ✅ Working as designed - users can add their own key

---

### 5. 403 FORBIDDEN - 1 Request
Access denied to this resource.

#### NHTSA Recalls 403 ❌
- **Request**: `GET api.nhtsa.gov/recalls/recallsearch?...`
- **Status**: 403
- **Root Cause**: API rejecting requests (possibly missing User-Agent or from unauthorized source)
- **Solution**: May need to add specific headers or use different endpoint
- **Action**: **NEEDS FIX** - Investigate headers or endpoint

---

### 6. 301 REDIRECT - 1 Request ⚠️
Server redirecting to different URL.

#### FDIC Banks 301 ⚠️
- **Request**: `GET banks.data.fdic.gov/api/institutions?...`
- **Status**: 301 (Moved Permanently)
- **Root Cause**: URL has changed, redirecting to new location
- **Solution**: Follow the redirect or use new URL
- **Current Behavior**: Browser may follow, but worth updating
- **Action**: Update to use final URL instead of redirect

---

### 7. 405 METHOD NOT ALLOWED - 1 Request
API doesn't support CORS preflight requests.

#### BLS OPTIONS 405 ❌
- **Request**: `OPTIONS api.bls.gov/publicAPI/v2/timeseries/data/`
- **Status**: 405
- **Root Cause**: API doesn't support CORS (doesn't respond to OPTIONS)
- **Solution**: ✅ Use Flask backend proxy (already implemented)
- **Action**: No change needed - working as designed

---

### 8. 522 CLOUDFLARE ERROR - 1 Request
CORS proxy service failed.

#### allorigins CORS Proxy 522 ⚠️
- **Request**: `GET api.allorigins.win/raw?url=...`
- **Status**: 522 (Connection Timed Out)
- **Root Cause**: Using external CORS proxy that timed out
- **Solution**: Remove dependency on external CORS proxy
- **Action**: Don't use this fallback - rely on Flask backend instead

---

## Summary of Required Fixes

### Critical (Broken Endpoints) - Need to Fix:
1. **DOJ** - Wrong API endpoint
2. **FCC Equipment** - Using wrong dataset ID (i5ic-sdri → 3b3k-34jp)
3. **EPA** - Wrong API endpoint
4. **USAspending** - Missing required POST body fields
5. **FEC** - Invalid query parameters
6. **NHTSA Recalls** - Access denied, may need headers
7. **FTC** - Endpoint unreachable

### Working as Designed ✅:
- **BLS** - Correctly using Flask backend (CORS issue)
- **NASA** - Rate limited with DEMO_KEY (user can add their own)
- **FDIC** - 301 redirect (browser handles, but could update URL)

### Already Fixed/Working ✅:
- SEC, FDA, Treasury, Weather, USGS, Census, NIST, LOC, NARA, FCC (ECFS)

---

## Action Items

| Agency | Issue | Priority | Action |
|--------|-------|----------|--------|
| DOJ | 404 - Wrong endpoint | HIGH | Find correct Press Releases API endpoint |
| EPA | 404 - Wrong endpoint | HIGH | Find correct Environmental Data API endpoint |
| FCC Equipment | 404 - Wrong dataset | HIGH | Change `i5ic-sdri` to `3b3k-34jp` |
| USAspending | 422 - Missing body | HIGH | Add `filters` field to POST payload |
| FEC | 422 - Bad params | HIGH | Fix query parameter names |
| NHTSA Recalls | 403 - Access denied | HIGH | Add headers or find alternative endpoint |
| FTC | Timeout | MEDIUM | Investigate endpoint or replace |
| FDIC | 301 - Redirect | LOW | Update URL (browser handles redirects) |
| NASA | 429 - Rate limit | LOW | Document that user needs API key (current behavior OK) |
| BLS | CORS/Timeout | RESOLVED | Working with Flask backend ✅ |

---

## Next Steps

1. **Fix high-priority 404 endpoints** - These need correct URLs
2. **Fix POST body issues** - USAspending needs `filters` field
3. **Fix query parameters** - FEC needs correct parameter names
4. **Investigate access issues** - NHTSA and FTC may need special handling
5. **Update FDIC URL** - Move to permanent URL
6. **Test all fixes** with real browser requests
7. **Document API requirements** in code comments

---

## Reference: Working APIs (No Changes Needed)
✅ SEC EDGAR
✅ FDA Drug Events
✅ Treasury Fiscal Data
✅ NOAA Weather Alerts
✅ USGS Earthquakes
✅ Census ACS Data
✅ NIST CVEs
✅ Library of Congress
✅ NARA Archives
✅ FCC ECFS (Socrata)
