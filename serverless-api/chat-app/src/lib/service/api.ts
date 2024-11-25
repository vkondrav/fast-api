import type {ChatBubbleModel, MessageData, UserData, UserModel} from "@/types";
import * as Ably from 'ably';

export async function fetchMessages(currentUser: UserModel): Promise<ChatBubbleModel[]> {

    const response = await fetch("/api/chat/messages");

    const data: MessageData[] = await response.json();

    return data.map((item: MessageData) => (
        {
            userName: item.user,
            time: localeDateTime(item.date),
            message: item.text,
            avatarUrl: robohash(item.user),
            isCurrentUser: currentUser.name === item.user,
            moderation_pass: item.moderation_pass
        }
    ));
}

function localeDateTime(date: string): string {
    return new Date(date).toLocaleString()
}

function robohash(user: string): string {
    return `https://robohash.org/${encodeURIComponent(user)}.svg?size=60x60`
}

export async function fetchCurrentUser(): Promise<UserModel> {

    const response = await fetch("/api/chat/user");

    const data: UserData = await response.json();
    let avatarUrl = robohash(data.id)

    return {
        name: data.id,
        avatarUrl: avatarUrl
    }
}

export async function sendMessage(message: string): Promise<ChatBubbleModel> {
    const response = await fetch(`/api/chat/messages?text=${encodeURIComponent(message)}`, {
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
        isCurrentUser: true,
        moderation_pass: newMessage.moderation_pass
    }
}

export async function subscribe(currentUser: UserModel, onMessageReceived: (data: ChatBubbleModel) => void) {

    const ablySubscriptionApiKey = "6NlX7w.Tz0Ysw:uX3jPm2Pxk6WrQeSxt5QcXqEKSmOB8OCDTlCstw3usg"

    let ably = new Ably.Realtime(ablySubscriptionApiKey)

    ably.connection.once("connected", () => {
        console.log("Connected to Ably!")
    })

    const channel = ably.channels.get("messages")
    await channel.subscribe("message", (message) => {

        let newMessage: MessageData = JSON.parse(message.data)

        console.log("Message received: " + newMessage)

        let newChatBubble: ChatBubbleModel = {
            userName: newMessage.user,
            time: localeDateTime(newMessage.date),
            message: newMessage.text,
            avatarUrl: robohash(newMessage.user),
            isCurrentUser: currentUser.name === newMessage.user,
            moderation_pass: newMessage.moderation_pass
        }

        onMessageReceived(newChatBubble)
    });
}
