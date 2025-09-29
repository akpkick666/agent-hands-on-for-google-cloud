"use client";

import { useMemo } from "react";
import { useChat } from "@ai-sdk/react";
import {
  ChatLayout,
  ChatHeader,
  ChatTitle,
  ChatDescription,
  ChatMessages,
  ChatMessageList,
  ChatMessage,
  ChatBubble,
  ChatBubbleAvatar,
  ChatBubbleMessage,
  ChatComposer,
  ChatInput,
  ChatSendButton,
  ChatToolbar,
  ChatToolbarItem,
  ChatEmptyState,
  ChatScrollAnchor
} from "ai-elements/shadcn";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Paperclip, RefreshCcw, Square } from "lucide-react";

const roleLabel: Record<string, string> = {
  assistant: "AI",
  user: "You",
  system: "System"
};

export default function Page() {
  const {
    messages,
    input,
    handleInputChange,
    handleSubmit,
    isLoading,
    stop,
    reload,
    error
  } = useChat({
    api: "/api/chat"
  });

  const hasMessages = messages.length > 0;
  const hasAssistantResponse = useMemo(
    () => messages.some((message) => message.role === "assistant"),
    [messages]
  );

  return (
    <ChatLayout className="mx-auto flex min-h-screen max-w-4xl flex-col px-4 py-10">
      <ChatHeader>
        <ChatTitle>ADK Assistant</ChatTitle>
        <ChatDescription>
          Chat with the ADK backend using the AI SDK chat primitives and streamed
          responses.
        </ChatDescription>
      </ChatHeader>

      <ChatMessages className="mt-6 flex-1">
        <ChatMessageList>
          {!hasMessages ? (
            <ChatEmptyState
              title="Start a conversation"
              description="Ask the assistant anything about your ADK deployment."
            />
          ) : null}

          {messages.map((message) => (
            <ChatMessage key={message.id} role={message.role}>
              <ChatBubble
                variant={message.role === "user" ? "sent" : "received"}
              >
                <ChatBubbleAvatar>
                  <Avatar className="h-8 w-8">
                    <AvatarFallback>
                      {roleLabel[message.role] ?? String(message.role).charAt(0).toUpperCase()}
                    </AvatarFallback>
                  </Avatar>
                </ChatBubbleAvatar>
                <ChatBubbleMessage>{message.content}</ChatBubbleMessage>
              </ChatBubble>
            </ChatMessage>
          ))}

          {error ? (
            <ChatMessage role="system">
              <ChatBubble variant="received">
                <ChatBubbleMessage>
                  {error.message || "Something went wrong while contacting the assistant."}
                </ChatBubbleMessage>
              </ChatBubble>
            </ChatMessage>
          ) : null}

          <ChatScrollAnchor trackVisibility={isLoading} />
        </ChatMessageList>
      </ChatMessages>

      <ChatComposer onSubmit={handleSubmit} className="mt-6">
        <ChatToolbar>
          <ChatToolbarItem>
            <Button
              type="button"
              size="icon"
              variant="ghost"
              className="border border-dashed border-input text-muted-foreground"
              disabled
            >
              <Paperclip className="h-4 w-4" aria-hidden="true" />
              <span className="sr-only">Attach file</span>
            </Button>
          </ChatToolbarItem>
          <ChatToolbarItem>
            <Button
              type="button"
              variant="ghost"
              onClick={() => reload()}
              disabled={!hasAssistantResponse || isLoading}
              className="gap-1 text-muted-foreground hover:text-foreground"
            >
              <RefreshCcw className="h-4 w-4" aria-hidden="true" />
              Reset
            </Button>
          </ChatToolbarItem>
          {isLoading ? (
            <ChatToolbarItem className="ml-auto">
              <Button
                type="button"
                variant="ghost"
                onClick={() => stop()}
                className="gap-1 text-muted-foreground hover:text-foreground"
              >
                <Square className="h-4 w-4" aria-hidden="true" />
                Stop
              </Button>
            </ChatToolbarItem>
          ) : null}
        </ChatToolbar>

        <ChatInput
          value={input}
          onChange={handleInputChange}
          placeholder="Ask the ADK assistant…"
          disabled={isLoading}
          autoFocus
          aria-label="Message the ADK assistant"
        />
        <ChatSendButton disabled={isLoading || input.trim().length === 0} />
      </ChatComposer>
    </ChatLayout>
  );
}
