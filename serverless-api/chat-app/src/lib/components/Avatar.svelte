<script lang="ts">
    export let avatarUrl: string;
</script>

<div role="button" class="btn btn-ghost btn-circle avatar ring ring-offset-2 bg-zinc-300">
    <div class="ring-primary ring-offset-base-100 w-12 rounded-full">
        <img src={avatarUrl} alt=""/>
    </div>
</div>