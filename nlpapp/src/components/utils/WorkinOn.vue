<template>
    <v-alert
      border="top"
      colored-border
      type="info"
      elevation="2"
    >
        <span v-html="msg"></span>
    </v-alert>
</template>

<script>
export default {
    data() {
        return {
            msg: `
            Por questões €, o Demo de momento não está disponivel.<br>
            For € reasons, this Demo is not available. Come back later! 
            `
        }
    }
}
</script>