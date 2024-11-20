<script lang="ts">
    import type { ChatBubbleData } from "@/types";
    import { Avatar } from "@/components";

    export let data: ChatBubbleData;
</script>

<div
    class="chat"
    class:chat-start={!data.isCurrentUser}
    class:chat-end={data.isCurrentUser}
>
    <div class="chat-image avatar px-2">
        <Avatar avatarUrl={data.avatarUrl} />
    </div>
    <div class="chat-header">
        {data.userName}
        <time class="text-xs opacity-50">{data.time}</time>
    </div>
    <div
        class="chat-bubble"
        class:chat-bubble-secondary={!data.isCurrentUser}
        class:chat-bubble-info={data.isCurrentUser}
    >
        {data.message}
    </div>
    <div class="chat-footer opacity-50">Delivered</div>
</div>
