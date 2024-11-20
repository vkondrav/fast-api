<script lang="ts">

    import {Avatar} from "@/components";
    import type {UserData} from "@/types";

    export let user: UserData
</script>

<div class="navbar bg-base-300">
    <div class="flex-1">
        <p class="btn btn-ghost text-xl">Serverless Chat App</p>
    </div>
    <div class="flex-none gap-2">
        <p class="font-bold">{user.name}</p>
        <Avatar avatarUrl={user.avatarUrl}/>
    </div>
</div>