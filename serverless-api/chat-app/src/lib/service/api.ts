import type {ChatBubbleData, MessageData, UserData} from "@/types";
import * as Ably from 'ably';

export async function fetchMessages(currentUser: UserData): Promise<ChatBubbleData[]> {

    const response = await fetch("/chat/messages");

    const data: MessageData[] = await response.json();

    return data.map((item: MessageData) => (
        {
            userName: item.user,
            time: localeDateTime(item.date),
            message: item.text,
            avatarUrl: robohash(item.user),
            isCurrentUser: currentUser.name === item.user
        }
    ));
}

function localeDateTime(date: string): string {
    return new Date(date).toLocaleString()
}

function robohash(user: string): string {
    return `https://robohash.org/${encodeURIComponent(user)}.svg?size=60x60`
}

export function fetchCurrentUser(): UserData {
    let userName = getCookie("user_id") || "undefined"
    let avatarUrl = robohash(userName)

    return {
        name: userName,
        avatarUrl: avatarUrl
    }
}

function getCookie(name: string): string | undefined {

    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop()?.split(';').shift();
    }
    return undefined;
}

export async function sendMessage(message: string): Promise<ChatBubbleData> {
    const response = await fetch(`/chat/messages?text=${encodeURIComponent(message)}`, {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to send message");
    }

    let newMessage: MessageData = await response.json()

    return {
        userName: newMessage.user,
        time: localeDateTime(newMessage.date),
        message: newMessage.text,
        avatarUrl: robohash(newMessage.user),
        isCurrentUser: true
    }
}

export async function subscribe(currentUser: UserData, onMessageReceived: (data: ChatBubbleData) => void) {

    const ablySubscriptionApiKey = "6NlX7w.Tz0Ysw:uX3jPm2Pxk6WrQeSxt5QcXqEKSmOB8OCDTlCstw3usg"

    let ably = new Ably.Realtime(ablySubscriptionApiKey)

    ably.connection.once("connected", () => {
        console.log("Connected to Ably!")
    })

    const channel = ably.channels.get("messages")
    await channel.subscribe("message", (message) => {

        let newMessage: MessageData = JSON.parse(message.data)

        console.log("Message received: " + newMessage)

        let newChatBubble: ChatBubbleData = {
            userName: newMessage.user,
            time: localeDateTime(newMessage.date),
            message: newMessage.text,
            avatarUrl: robohash(newMessage.user),
            isCurrentUser: currentUser.name === newMessage.user
        }

        onMessageReceived(newChatBubble)
    });
}
