<template>
    <v-card class="mt-5" outlined>
        <v-card-title primary-title>
            Configurations<v-icon class="ml-2" color="primary">mdi-cog-outline</v-icon>
        </v-card-title>
        <v-card-actions>
            <v-container class="px-0 ml-10" fluid>
                <v-switch
                    v-model="countries_"
                    label="Countries"
                ></v-switch>

                <v-switch
                    v-model="entities_"
                    label="Entities"
                ></v-switch>

                <v-switch
                    v-model="numbers_"
                    label="Numbers"
                ></v-switch>

                <v-switch
                    v-model="persons_"
                    label="Persons"
                ></v-switch>

                <v-switch
                    v-model="verbs_"
                    label="Verbs"
                ></v-switch>

                <v-divider></v-divider>
                <v-switch
                    v-model="_sentiment"
                    label="Sentiment Analysis"
                ></v-switch>
                <v-switch
                    v-model="_summarizer"
                    label="Summarize"
                ></v-switch>
            </v-container>
        </v-card-actions>
    </v-card>
</template>

<script>
export default {
    props: [
        "countries",
        "entities",
        "numbers",
        "persons",
        "verbs",
        "summarizer",
        "sentiment"
    ],

    computed: {
        countries_: {
            get() {
                return this.countries;
            },
            set(val) {
                this.$emit("countries_", val);
            }
        },

        entities_: {
            get() {
                return this.countries;
            },
            set(val) {
                this.$emit("entities_", val);
            }
        },

        numbers_: {
            get() {
                return this.countries;
            },
            set(val) {
                this.$emit("numbers_", val);
            }
        },

        persons_: {
            get() {
                return this.countries;
            },
            set(val) {
                this.$emit("persons_", val);
            }
        },

        verbs_: {
            get() {
                return this.countries;
            },
            set(val) {
                this.$emit("verbs_", val);
            }
        },

        _summarizer: {
            get() {
                return this.summarizer;
            },
            set(val) {
                this.$emit("summarizer_", val);
            }
        },

        _sentiment: {
            get() {
                return this.sentiment;
            },
            set(val) {
                this.$emit("sentiment_", val);
            }
        }
    },
}
</script>