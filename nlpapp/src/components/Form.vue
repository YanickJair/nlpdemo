<template>
    <v-text-field
        class="ma-4"
        v-model="_text"
        :counter="90"
        label="search word"
        outlined
        required
    ></v-text-field>
</template>

<script>
export default {
    props: ["text"],
    data() {
        return {
            valid: true,
        }
    },

    computed: {
        _text: {
            get() { return this.text; },
            set(val) { this.$emit("searchText", val); }
        }
    }
}
</script>