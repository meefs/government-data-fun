// OpenGovDash CORS proxy — Cloudflare Worker.
// Forwards browser requests to government APIs that don't send CORS headers.
// Strips client auth/cookie headers; pins Access-Control-Allow-Origin to our known hosts.

const UPSTREAMS = {
  bls:         'https://api.bls.gov',
  nih_pubmed:  'https://eutils.ncbi.nlm.nih.gov',
  loc:         'https://www.loc.gov',
  usaspending: 'https://api.usaspending.gov',
  doj:         'https://www.justice.gov',
  dot:         'https://api.nhtsa.gov',
  epa:         'https://data.epa.gov',
  sam:         'https://api.sam.gov',
  ftc:         'https://reportportal.ftc.gov',
  nara:        'https://catalog.archives.gov',
  fcc_ecfs:    'https://publicapi.fcc.gov',
};

const ALLOWED_ORIGIN_PATTERNS = [
  /^https:\/\/selvidge\.tech$/,
  /^https:\/\/[a-z0-9-]+\.github\.io$/,
  /^http:\/\/localhost(:\d+)?$/,
  /^http:\/\/127\.0\.0\.1(:\d+)?$/,
];

const DEFAULT_ORIGIN = 'https://selvidge.tech';

function pickAllowOrigin(origin) {
  if (origin && ALLOWED_ORIGIN_PATTERNS.some(re => re.test(origin))) return origin;
  return DEFAULT_ORIGIN;
}

function corsHeaders(origin) {
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Accept, X-Requested-With',
    'Access-Control-Max-Age': '86400',
    'Vary': 'Origin',
  };
}

function json(body, status, origin) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...corsHeaders(origin) },
  });
}

export default {
  async fetch(request) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';
    const allowOrigin = pickAllowOrigin(origin);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(allowOrigin) });
    }

    if (url.pathname === '/' || url.pathname === '/health') {
      return json({ ok: true, upstreams: Object.keys(UPSTREAMS) }, 200, allowOrigin);
    }

    const match = url.pathname.match(/^\/p\/([a-z_]+)(\/.*)?$/);
    if (!match || !UPSTREAMS[match[1]]) {
      return json({ error: 'unknown upstream', path: url.pathname }, 404, allowOrigin);
    }

    const upstreamBase = UPSTREAMS[match[1]];
    const upstreamPath = match[2] || '/';
    const upstreamUrl = upstreamBase + upstreamPath + url.search;

    const outHeaders = new Headers();
    for (const [k, v] of request.headers) {
      const lower = k.toLowerCase();
      if (lower === 'authorization' || lower === 'cookie' || lower === 'host'
          || lower === 'x-forwarded-for' || lower === 'x-real-ip'
          || lower.startsWith('cf-')) continue;
      outHeaders.set(k, v);
    }
    outHeaders.set('User-Agent', 'OpenGovDash/1.0 (+https://github.com/HBT89/government-data-fun)');

    let upstreamResp;
    try {
      upstreamResp = await fetch(upstreamUrl, {
        method: request.method,
        headers: outHeaders,
        body: ['GET', 'HEAD'].includes(request.method) ? undefined : request.body,
        redirect: 'follow',
      });
    } catch (err) {
      return json({ error: 'upstream fetch failed', message: err.message, upstream: upstreamUrl }, 502, allowOrigin);
    }

    const respHeaders = new Headers(upstreamResp.headers);
    respHeaders.delete('set-cookie');
    respHeaders.delete('set-cookie2');
    for (const [k, v] of Object.entries(corsHeaders(allowOrigin))) respHeaders.set(k, v);

    return new Response(upstreamResp.body, {
      status: upstreamResp.status,
      headers: respHeaders,
    });
  },
};
