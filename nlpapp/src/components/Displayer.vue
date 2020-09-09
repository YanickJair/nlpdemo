<template>
    <v-card-text class="context" outlined>
        {{ text }}
    </v-card-text>
</template>

<script>
export default {
    props: ["text"]
}
</script>