<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="6">
                <v-container class="max-width">
                    <v-pagination
                        v-model="_page"
                        class="my-4"
                        :length="length"
                    ></v-pagination>
                </v-container>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
export default {
    props: ["page", "length"],

    computed: {
        _page: {
            get() { return this.page; },
            set(val) { this.$emit("page_", val); }
        }
    }
}
</script>