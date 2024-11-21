<script lang="ts">

    interface Tab {
        id: number;
        name: string;
    }

    let tabs: Tab[] = [
        {id: 1, name: "#software"},
        {id: 2, name: "#random"},
        {id: 3, name: "#svelte"}
    ]

    let selected: number = $state(1)

    function select(id: number) {
        selected = id
    }
</script>

<div role="tablist" class="pt-2 tabs tabs-lifted">
    {#each tabs as tab}
        <a role="tab"
           class="tab"
           tabindex="{tab.id}"
           class:tab-active={tab.id === selected}
           onclick="{() => select(tab.id)}"
        >
            {tab.name}
        </a>
    {/each}
</div>