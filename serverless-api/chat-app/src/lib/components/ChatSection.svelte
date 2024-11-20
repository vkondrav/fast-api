<script lang="ts">
    import type {ChatBubbleData} from "@/types";
    import {ChatBubble} from "@/components";

    let {messages}: { messages: ChatBubbleData[] } = $props()
    let chatSection: HTMLDivElement;

    $effect(() => {
        messages.values()
        chatSection.scrollTop = chatSection.scrollHeight;
    });

</script>

<div
        id="chat-section"
        class="flex-grow overflow-y-auto"
        bind:this={chatSection}
>
    {#each messages as message}
        <ChatBubble data={message}/>
    {/each}
</div>