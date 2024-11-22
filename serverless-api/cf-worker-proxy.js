/**
 * worker code to be deployed to Cloudflare Workers
 * proxies all calls to AWS Lambda
 * caches all app files for 1 hour
 */
export default {
    async fetch(request, env) {

        const targetURL = env.AWS_LAMBDA_URL;

        if (!targetURL) {
            return new Response("AWS_LAMBDA_URL environment variable is not defined", { status: 500 });
        }

        const cache = caches.default;

        const requestURL = new URL(request.url);
        const proxyURL = new URL(targetURL);
        proxyURL.pathname = requestURL.pathname;
        proxyURL.search = requestURL.search;

        const cacheKey = new Request(proxyURL.toString(), request);

        let response = await cache.match(cacheKey);
        if (response) {
            console.log("Serving from cache");
            return response;
        }

        response = await fetch(proxyURL, request);

        const responseClone = response.clone();

        const contentType = response.headers.get("Content-Type") || "";
        if (
            response.status === 200 &&
            (
                contentType.includes("text/html") ||
                contentType.includes("text/css") ||
                contentType.includes("application/javascript") ||
                contentType.startsWith("image/")
            )
        ) {
            const headers = new Headers(response.headers);
            headers.set("Cache-Control", "public, max-age=3600");

            const cachedResponse = new Response(responseClone.body, {
                status: responseClone.status,
                statusText: responseClone.statusText,
                headers: headers,
            });

            await cache.put(cacheKey, cachedResponse);
        }

        return response;
    }
};
