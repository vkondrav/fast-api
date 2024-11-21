<script lang="ts">
    import type {UIState} from "@/types";
    import {ChatBubble, ProgressBar} from "@/components";

    let {uiState}: { uiState: UIState } = $props()

    let chatSection: HTMLDivElement;

    $effect(() => {
        uiState.messages

        chatSection.scrollTop = chatSection.scrollHeight;
    });

</script>

<div
        id="chat-section"
        class="flex-grow overflow-y-auto"
        bind:this={chatSection}
>

    {#if uiState.isLoading}

        <ProgressBar/>

    {:else}

        {#each uiState.messages as message}
            <ChatBubble data={message}/>
        {/each}

    {/if}


</div>