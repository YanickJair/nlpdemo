<template>
    <div>
        <v-app-bar
            dark
        >
            <v-avatar size="40">
                <img src="Website Yanick-08.png" alt="alt">
            </v-avatar>
            <v-toolbar-title class="ml-4">Natural Language Processing - Demo</v-toolbar-title>

            <v-spacer></v-spacer>
            
            <v-btn
                class="primary"
                @click="dialog = true"
            >Hook Database</v-btn>
        </v-app-bar> 

        <HookDB
            :dialog="dialog"
            v-on:dialog_="val => dialog = val"
        />
    </div>
</template>

<script>
import HookDB from './HookDB'

export default {
    components: { HookDB },
    data() {
        return {
            dialog: false,
            text: null
        }
    },
}
</script>