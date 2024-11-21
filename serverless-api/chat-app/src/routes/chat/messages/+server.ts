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
            id: "1"
        },
        {
            user: "user2",
            date: new Date().toISOString(),
            text: "Hi, this is another message.",
            id: "2"
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