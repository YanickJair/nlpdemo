<template>
    <v-alert
      dense
      outlined
      :type="type_"
      :dismissible="dismissible"
    >
        {{ message }}
    </v-alert>
</template>

<script>
export default {
    props: {
        message: {
            type: String,
            rquired: true
        },
        dismissible: {
            type: Boolean,
            default: false
        },
        type_: {
            type: String,
            required: true
        }
    }
}
</script>