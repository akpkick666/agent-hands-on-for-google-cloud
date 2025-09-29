import { NextRequest } from "next/server";

const ADK_CHAT_PATH = "/api/chat";

export async function POST(req: NextRequest) {
  const baseUrl = process.env.NEXT_PUBLIC_ADK_BASE_URL;

  if (!baseUrl) {
    return new Response("ADK base URL is not configured.", {
      status: 500
    });
  }

  const url = new URL(ADK_CHAT_PATH, baseUrl);

  const forwardHeaders = new Headers(req.headers);
  forwardHeaders.delete("host");
  forwardHeaders.delete("content-length");

  try {
    const upstreamResponse = await fetch(url, {
      method: "POST",
      headers: forwardHeaders,
      body: req.body,
      cache: "no-store",
      duplex: "half"
    });

    const responseHeaders = new Headers(upstreamResponse.headers);
    responseHeaders.delete("content-length");

    return new Response(upstreamResponse.body, {
      status: upstreamResponse.status,
      statusText: upstreamResponse.statusText,
      headers: responseHeaders
    });
  } catch (error) {
    console.error("Failed to reach ADK chat endpoint", error);
    return new Response("Failed to reach ADK chat endpoint", { status: 502 });
  }
}
