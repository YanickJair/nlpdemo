<template>
    <v-row justify="center">
        <v-dialog
            v-model="_loading"
            width="100"
        >
            <v-row justify="center">
                <v-card height="200" width="200" flat class="transparent elevation-0">
                    <v-progress-circular
                    :size="70"
                    :width="7"
                    color="purple"
                    :indeterminate="true"
                ></v-progress-circular>
            </v-card>
            </v-row>
        </v-dialog>
    </v-row>
</template>

<script>
export default {
    props: ["loading"],
    computed: {
        _loading: {
            get() {
                return this.loading;
            },
            set(val) {
                this.$emit("loading", val);
            }
        }
    }
}
</script>