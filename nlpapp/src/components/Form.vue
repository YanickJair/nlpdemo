<template>
    <v-form
        class="ma-10 mt-5"
        ref="form"
        v-model="valid"
        lazy-validation
    >
        <v-text-field
            v-model="text"
            :counter="90"
            label="Name"
            required
        ></v-text-field>
    </v-form>
</template>

<script>
export default {
    props: ["valid", "text"]
}
</script>