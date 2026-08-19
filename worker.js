export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Test
    if (url.pathname === "/api/test") {
      return Response.json({
        status: "online",
        message: "Plexi gerçek Worker üzerinde çalışıyor."
      });
    }

    // Chat
    if (url.pathname === "/chat" && request.method === "POST") {
      try {
        const body = await request.json();

        const message = body.message;

        if (!message) {
          return Response.json(
            { error: "Mesaj boş." },
            { status: 400 }
          );
        }

        return Response.json({
          response: "Plexi backend bağlantısı hazır. 🧠"
        });

      } catch {
        return Response.json(
          { error: "Geçersiz istek." },
          { status: 400 }
        );
      }
    }

    return new Response("Plexi");
  }
};
