<script lang="ts">
    import Icon from '@iconify/svelte';

    interface NavButton {
        id: number;
        icon: string;
    }

    let navButtons: NavButton[] = [
        {id: 1, icon: "mdi:home"},
        {id: 2, icon: "duo-icons:message-3"},
        {id: 3, icon: "ic:sharp-settings-suggest"}
    ]

    let selected: number = $state(2)

    function select(id: number) {
        selected = id
    }

</script>

<div class="btm-nav">

    {#each navButtons as navButton}
        <button onclick="{() => select(navButton.id)}" class:active={navButton.id === selected}>
            <Icon icon={navButton.icon} height="auto"/>
        </button>
    {/each}

</div>

