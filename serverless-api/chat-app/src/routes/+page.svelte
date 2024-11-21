<script lang="ts">
    import type {ChatBubbleData, UIState, UserData} from "@/types";
    import { initialState } from "@/types";
    import {ChatSection, Input, NavBar} from "@/components";
    import {fetchMessages, fetchCurrentUser, sendMessage, subscribe} from "@/service";
    import {onMount} from "svelte";

    let uiState: UIState = $state(initialState)

    let currentUser: UserData = $state({name: "", avatarUrl: ""});

    onMount(async () => {
        currentUser = fetchCurrentUser();

        uiState = {
            isLoading: false,
            messages: await fetchMessages(currentUser)
        }

        await subscribe(currentUser, (message: ChatBubbleData) => {
            uiState.messages = [...uiState.messages, message]
        })
    });
</script>

<div class="mx-auto flex flex-col h-screen pb-4 px-4">
    <NavBar user={currentUser}/>
    <ChatSection {uiState} />
    <Input sendMessage={sendMessage}/>
</div>