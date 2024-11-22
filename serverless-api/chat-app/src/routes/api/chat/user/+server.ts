import type {UserData} from "@/types";

/**
 * server for testing purposes
 * @constructor
 */
export async function GET(): Promise<any> {

    const user: UserData = {
        id: "ABC123"
    }

    await delay(100)

    return new Response(JSON.stringify(user), {
        headers: {
            "Content-Type": "application/json"
        }
    });
}

function delay(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}