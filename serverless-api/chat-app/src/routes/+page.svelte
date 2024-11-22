<script lang="ts">
    import type {ChatBubbleModel, UIState, UserModel} from "@/types";
    import { initialState } from "@/types";
    import {BottomNav, ChatSection, Input, NavBar, TabBar} from "@/components";
    import {fetchMessages, fetchCurrentUser, sendMessage, subscribe} from "@/service";
    import {onMount} from "svelte";

    let uiState: UIState = $state(initialState)

    onMount(async () => {

        let currentUser: UserModel = await fetchCurrentUser()

        uiState.user = await fetchCurrentUser()

        uiState = {
            ...uiState,
            messages: await fetchMessages(currentUser),
            isLoading: false
        }

        await subscribe(currentUser, (message: ChatBubbleModel) => {
            uiState.messages = [...uiState.messages, message]
        })
    });
</script>

<div class="mx-auto flex flex-col h-screen pb-4 px-4">
    <NavBar user={uiState.user}/>
    <TabBar/>
    <ChatSection {uiState} />
    <Input sendMessage={sendMessage}/>
    <BottomNav/>
</div>