<script lang="ts">

    export let sendMessage: (message: string) => void;

    let input = "";

    function send() {
        sendMessage(input);
        input = "";
    }

    function onkeydown(event: KeyboardEvent): void {
        if (event.key === "Enter") {
            send();
        }
    }

</script>

<div class="flex pt-2">
    <input
            type="text"
            placeholder="Type here"
            class="input input-bordered flex-grow"
            bind:value={input}
            {onkeydown}
    />
    <div class="pr-2"></div>
    <button class="btn btn-accent" onclick={ () => send() }>Send</button>
</div>