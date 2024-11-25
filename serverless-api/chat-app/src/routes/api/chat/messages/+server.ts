import type {MessageData} from "@/types";

/**
 * server for testing purposes
 * @constructor
 */
export async function GET(): Promise<any> {

    const messages: MessageData[] = [
        {
            user: "user1",
            date: new Date().toISOString(),
            text: "Hello, this is a message.",
            id: "1",
            moderation_pass: true
        },
        {
            user: "user2",
            date: new Date().toISOString(),
            text: "Hi, this is another message.",
            id: "2",
            moderation_pass: true
        },
        {
            user: "user3",
            date: new Date().toISOString(),
            text: "Message 3",
            id: "3",
            moderation_pass: true
        },
        {
            user: "user4",
            date: new Date().toISOString(),
            text: "Message 4",
            id: "4",
            moderation_pass: true
        },
        {
            user: "user5",
            date: new Date().toISOString(),
            text: "Message 5",
            id: "5",
            moderation_pass: true
        },
        {
            user: "user6",
            date: new Date().toISOString(),
            text: "Message 6",
            id: "6",
            moderation_pass: false,
        },
        {
            user: "user7",
            date: new Date().toISOString(),
            text: "Message 7",
            id: "7",
            moderation_pass: false
        },
        {
            user: "user8",
            date: new Date().toISOString(),
            text: "Message 8",
            id: "8",
            moderation_pass: true
        },
        {
            user: "user9",
            date: new Date().toISOString(),
            text: "Message 9",
            id: "9",
            moderation_pass: true
        },
        {
            user: "user10",
            date: new Date().toISOString(),
            text: "Message 10",
            id: "10"
        },
        {
            user: "user11",
            date: new Date().toISOString(),
            text: "Message 11",
            id: "11",
            moderation_pass: true
        },
        {
            user: "user12",
            date: new Date().toISOString(),
            text: "Message 12",
            id: "12",
            moderation_pass: false
        }
    ];

    await delay(3_000)

    return new Response(JSON.stringify(messages), {
        headers: {
            "Content-Type": "application/json"
        }
    });
}

function delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}