<script lang="ts">
    import type { ChatBubbleModel } from "@/types";
    import { Avatar } from "@/components";

    export let data: ChatBubbleModel;
</script>

<div
    class="chat"
    class:chat-start={!data.isCurrentUser}
    class:chat-end={data.isCurrentUser}
>
    <div class="chat-image avatar px-2">
        <Avatar avatarUrl={data.avatarUrl} />
    </div>
    <div class="chat-header pb-1">
        {data.userName}
        <time class="text-xs opacity-50">{data.time}</time>
    </div>
    <div
        class="chat-bubble"
        class:chat-bubble-secondary={!data.isCurrentUser}
        class:chat-bubble-info={data.isCurrentUser}
        class:chat-bubble-error={!data.moderation_pass}
        class:italic={!data.moderation_pass}
    >
        {data.message}
    </div>
</div>
