export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/api/test") {
      return Response.json({
        status: "online",
        message: "Plexi Worker çalışıyor!"
      });
    }

    return new Response("Plexi");
  }
};
