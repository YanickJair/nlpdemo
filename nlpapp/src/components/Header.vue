<template>
    <div>
        <v-app-bar
            dark
        >
            <v-toolbar-title>NLP DEMO - Python + Spacy</v-toolbar-title>

            <v-spacer></v-spacer>
            <v-switch
                class="ma-3 mt-8"
                v-model="_default"
                label="Default Data"
            ></v-switch>

            <v-tooltip bottom v-if="!_default">
                <template v-slot:activator="{ on, attrs }">
                    <v-btn
                        icon
                        v-bind="attrs"
                        v-on="on"
                        @click="dialog = true"
                    >
                        <v-icon>mdi-plus</v-icon>
                    </v-btn>
                </template>
                <span>Add My Text</span>
            </v-tooltip>
        </v-app-bar>

        <v-row justify="center">
            <v-dialog v-model="dialog" max-width="600px">
                <v-card>
                    <v-card-title>
                        <span class="headline">Add your own Text.</span>
                    </v-card-title>

                    <v-card-text>
                        <v-container>
                            <v-row>
                                <v-col cols="12" sm="12" md="12">
                                    <v-textarea
                                        outlined
                                        label="*"
                                        required
                                        v-model="text"
                                    ></v-textarea>
                                </v-col>
                            </v-row>
                        </v-container>
                    </v-card-text>

                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="dialog = false">Close</v-btn>
                        <v-btn color="blue darken-1" text @click="addData">Save</v-btn>
                    </v-card-actions>
                </v-card>
            </v-dialog>
        </v-row>
    </div>
</template>

<script>
export default {
    props: ["default"],
    data() {
        return {
            dialog: false,
            text: null
        }
    },

    computed: {
        _default: {
            get() {
                return this.default;
            },
            set(val) {
                this.$emit("setDefaultData", val);
            }
        }
    },

    methods: {
        addData() {
            if (this.text != null) {
                this.$emit("addData", this.text);
                this.text = null;
                this.dialog = false;
            }
        }
    }
}
</script>