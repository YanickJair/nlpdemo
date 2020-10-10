<template>
    <v-card
        class="mx-auto"
        outlined
    >
        <v-list-item two-line>
            <v-list-item-content>
                <div class="overline mb-4 text-center">Dataset Size</div>
                <v-list-item-title class="headline mb-1 text-center">{{ size }}</v-list-item-title>
            </v-list-item-content>
        </v-list-item>

        <v-list-item two-line>
            <v-list-item-content>
                <div class="overline mb-4 text-center">Analyzed</div>
                <v-list-item-title class="headline mb-1 text-center">{{ analyzed }}</v-list-item-title>
            </v-list-item-content>
        </v-list-item>
    </v-card>
</template>

<script>
export default {
    props: ["size", "analyzed"]
}
</script>