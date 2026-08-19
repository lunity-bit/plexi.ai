export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // =========================
    // API TEST
    // =========================

    if (url.pathname === "/api/test") {
      return Response.json({
        status: "online",
        message: "Plexi Worker çalışıyor!"
      });
    }

    // =========================
    // CHAT
    // =========================

    if (url.pathname === "/chat" && request.method === "POST") {
      try {
        const data = await request.json();

        const question = String(
          data.message || ""
        ).trim();

        if (!question) {
          return Response.json(
            { error: "Bir şey yazmalısın." },
            { status: 400 }
          );
        }

        if (!env.NVIDIA_API_KEY) {
          return Response.json(
            {
              error:
                "NVIDIA_API_KEY Worker'a bağlı değil."
            },
            { status: 500 }
          );
        }

        const response = await fetch(
          "https://integrate.api.nvidia.com/v1/chat/completions",
          {
            method: "POST",

            headers: {
              "Authorization":
                `Bearer ${env.NVIDIA_API_KEY}`,
              "Content-Type":
                "application/json"
            },

            body: JSON.stringify({
              model:
                "nvidia/nemotron-3-ultra-550b-a55b",

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

        const resultText =
          await response.text();

        if (!response.ok) {
          console.error(
            "NVIDIA ERROR:",
            response.status,
            resultText
          );

          return Response.json(
            {
              error:
                "NVIDIA API hata verdi.",
              status:
                response.status,
              details:
                resultText
            },
            { status: 500 }
          );
        }

        const result =
          JSON.parse(resultText);

        const answer =
          result?.choices?.[0]?.message?.content;

        if (!answer) {
          return Response.json(
            {
              error:
                "NVIDIA cevap üretmedi."
            },
            { status: 500 }
          );
        }

        return Response.json({
          response: answer
        });

      } catch (error) {

        console.error(
          "WORKER ERROR:",
          error
        );

        return Response.json(
          {
            error:
              "Worker hatası.",
            details:
              error instanceof Error
                ? error.message
                : String(error)
          },
          { status: 500 }
        );
      }
    }

    // =========================
    // FRONTEND
    // =========================

    return env.ASSETS.fetch(request);
  }
};
