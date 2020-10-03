<template>
    <v-row justify="center">
        <v-dialog v-model="_dialog" max-width="600px">
            <v-card>
                <v-card-title>
                    Connect to a Database
                </v-card-title>
                <v-row
                    class="pa-4"
                    justify="space-between"
                >
                    <v-col cols="5">
                        <v-autocomplete
                            v-model="connector"
                            :items="DATABASES"
                            outlined
                            color="blue-grey lighten-2"
                            label="Select"
                            item-text="name"
                            item-value="name"
                        >
                            <template v-slot:selection="data">
                                <v-chip
                                    v-bind="data.attrs"
                                    :input-value="data.selected"
                                    close
                                    @click="data.select"
                                    @click:close="connector = null"
                                >
                                <v-avatar left>
                                    <v-img :src="data.item.avatar"></v-img>
                                </v-avatar>
                                {{ data.item.name }}
                                </v-chip>
                            </template>
                        </v-autocomplete>
                    </v-col>

                    <v-divider vertical></v-divider>

                    <v-col cols="6">
                        <v-form
                            ref="form"
                            v-model="valid"
                            lazy-validation
                        >
                            <v-text-field
                                v-model="host"
                                :counter="40"
                                :rules="hostRules"
                                label="host"
                                required
                            ></v-text-field>
                            <v-text-field
                                v-model="port"
                                :counter="40"
                                :rules="hostRules"
                                label="port"
                                required
                            ></v-text-field>
                            <v-text-field
                                v-model="username"
                                :counter="40"
                                :rules="hostRules"
                                label="username"
                                required
                            ></v-text-field>
                            <v-text-field
                                v-model="password"
                                type="password"
                                :rules="hostRules"
                                label="password"
                                required
                            ></v-text-field>
                            <v-text-field
                                v-model="table"
                                :rules="hostRules"
                                label="table"
                                required
                            ></v-text-field>
                            <v-text-field
                                v-model="field"
                                :rules="hostRules"
                                label="field to review"
                                required
                            ></v-text-field>
                        </v-form>
                    </v-col>
                </v-row>
            </v-card>
        </v-dialog>
    </v-row>
</template>

<script>
export default {
    props: ["dialog"],
    data() {
        return {
            valid: true,
            connector: null,
            host: null,
            hostRules: [
                v => !!v || 'Name is required',
                v => (v && v.length <= 10) || 'Name must be less than 10 characters',
            ],
            port: null,
            username: null,
            password: null,
            database: null,
            table: null,
            field: null,
            DATABASES: [
                { id: 1, name: "PostgresSQL", avatar: "270e21a9.png" },
                { id: 2, name: "MongoDB", avatar: "mongo.png" }
            ]
        }
    },
    computed: {
        _dialog: {
            get() {
                return this.dialog;
            },
            set(val) {
                this.$emit("dialog_", val);
            }
        }
    },
}
</script>