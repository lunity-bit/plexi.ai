export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Sağlık testi
    if (url.pathname === "/api/test") {
      return Response.json({
        status: "online",
        message: "Plexi Worker çalışıyor!"
      });
    }

    // Frontend
    return env.ASSETS.fetch(request);
  }
};
