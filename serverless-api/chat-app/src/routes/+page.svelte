<script lang="ts">
    import type {ChatBubbleData, UserData} from "@/types";
    import {ChatSection, Input, NavBar} from "@/components";
    import {fetchMessages, fetchCurrentUser, sendMessage, subscribe} from "@/service";
    import {onMount} from "svelte";

    let messages: ChatBubbleData[] = $state([]);

    let currentUser: UserData = $state({name: "", avatarUrl: ""});

    onMount(async () => {
        currentUser = fetchCurrentUser();
        messages = await fetchMessages(currentUser)
        await subscribe(currentUser, (message: ChatBubbleData) => {
            messages = [...messages, message]
        })
    });
</script>

<div class="mx-auto flex flex-col h-screen pb-4 px-4">
    <NavBar user={currentUser}/>
    <ChatSection {messages}/>
    <Input sendMessage={sendMessage}/>
</div>