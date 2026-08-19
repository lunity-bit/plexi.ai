export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // ==============================
    // API TEST
    // ==============================

    if (url.pathname === "/api/test") {
      return Response.json({
        status: "online",
        message: "Plexi Worker çalışıyor!"
      });
    }

    // ==============================
    // CHAT
    // ==============================

    if (url.pathname === "/chat" && request.method === "POST") {
      try {
        const data = await request.json();

        const question = String(data.message || "").trim();

        if (!question) {
          return Response.json(
            { error: "Bir şey yazmalısın." },
            { status: 400 }
          );
        }

        const response = await fetch(
          "https://integrate.api.nvidia.com/v1/chat/completions",
          {
            method: "POST",

            headers: {
              "Authorization": `Bearer ${env.NVIDIA_API_KEY}`,
              "Content-Type": "application/json"
            },

            body: JSON.stringify({
              model: "nvidia/nemotron-3-ultra-550b-a55b",

              messages: [
                {
                  role: "user",
                  content: question
                }
              ],

              temperature: 0.7,
              max_tokens: 1000
            })
          }
        );

        if (!response.ok) {
          const errorText = await response.text();

          return Response.json(
            {
              error: "NVIDIA API hatası.",
              details: errorText
            },
            { status: 500 }
          );
        }

        const result = await response.json();

        const answer =
          result?.choices?.[0]?.message?.content;

        if (!answer) {
          return Response.json(
            { error: "NVIDIA cevap üretmedi." },
            { status: 500 }
          );
        }

        return Response.json({
          response: answer
        });

      } catch (error) {

        return Response.json(
          {
            error: error.message
          },
          { status: 500 }
        );
      }
    }

    // ==============================
    // FRONTEND
    // ==============================

    return env.ASSETS.fetch(request);
  }
};
