async function handleApiRequest(url, request, env) {
  const cache = caches.default;
  const targetURL = env.AWS_LAMBDA_URL;

  if (request.method === 'GET') {
      let response = await cache.match(request);

      if (!response) {

          response = await fetch(targetURL + url.pathname + url.search, {
              method: request.method,
              headers: request.headers,
          });

          response = new Response(response.body, response);
          response.headers.append('Cache-Control', 's-maxage=3');
          await cache.put(request, response.clone());

          return response;

      } else {

          return response;
      }

  } else {

      return fetch(targetURL + url.pathname + url.search, {
          method: request.method,
          headers: request.headers,
          body: await request.text(),
      });
  }
}

async function handlePageRequest(url, request, env) {
  const targetURL = env.PAGES_URL;

  return fetch(targetURL + url.pathname + url.search, {
      method: request.method,
      headers: request.headers,
      body: request.method !== 'GET' ? await request.text() : null,
  });
}

export default {
  async fetch(request, env) {
      const url = new URL(request.url);

      if (url.pathname.startsWith('/api')) {
          return handleApiRequest(url, request, env);
      } else {
          return handlePageRequest(url, request, env);
      }
  },
};