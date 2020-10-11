<template>
    <v-card class="pa-4 elevation-0">
        <v-alert
            border="top"
            colored-border
            type="info"
            elevation="0"
        >
            Given a sequence of words or a word, predict the next word/words. This is also called the language modeling task.
            This is done by using GloVe. "GloVe is an unsupervised learning algorithm for obtaining vector representations for words.
            Training is performed on aggregated global word-word co-occurrence statistics from a corpus, and the resulting representations showcase interesting linear substructures of the word vector space."
            <br>More about GloVe can be found <a :href="glove" target="_blank">here</a>
        </v-alert>
        <v-form>
            <v-alert
                border="top"
                colored-border
                type="error"
                elevation="0"
                v-if="error"
            >
                {{ error }}
            </v-alert>
            <v-row>
                <v-col cols="12">
                    <v-switch
                        v-model="words_n"
                        inset
                        :label="!words_n ? 'One Word Analogy' : 'Sequence of Words Analogy'"
                    ></v-switch>
                </v-col>
                <v-col :cols="!words_n ? 12 : 4">
                    <v-text-field
                        name="name"
                        v-model="word_1"
                        placeholder="i.e. young"
                        :label="!words_n ? 'word' : 'word 1'"
                        id="id"
                    ></v-text-field>
                </v-col>

                <v-col cols="4" v-if="words_n">
                    <v-text-field
                        name="name"
                        label="word 2"
                        v-model="word_2"
                        placeholder="i.e. youngest"
                        id="id"
                    ></v-text-field>
                </v-col>

                <v-col cols="4" v-if="words_n">
                    <v-text-field
                        name="name"
                        placeholder="i.e. fast"
                        label="word 3"
                        v-model="word_3"
                        id="id"
                    ></v-text-field>
                </v-col>
            </v-row>
            <v-btn small color="success" @click="submitAnalogy">Submit</v-btn>
        </v-form>

        <v-expansion-panels v-if="analogies.length > 0" class="mt-5 elevation-0">
            <v-expansion-panel v-for="(analogie, i) in analogies" :key="i">
                <v-expansion-panel-header>
                    <v-row no-gutters>
                        <v-col cols="4" v-for="(header, j) in analogie.header" :key="j">
                            {{ header }}
                        </v-col>
                    </v-row>
                </v-expansion-panel-header>

                <v-expansion-panel-content>
                    <v-simple-table>
                        <template v-slot:default>
                            <tbody>
                                <tr
                                    v-for="(result, k) in analogie.result"
                                    :key="k"
                                >
                                    <td>{{ analogie.header.length == 1 ? analogie.header[0] : analogie.header[2]  }}</td>
                                    <td>{{ result }}</td>
                                </tr>
                            </tbody>
                        </template>
                    </v-simple-table>
                </v-expansion-panel-content>
            </v-expansion-panel>
        </v-expansion-panels>
    </v-card>
</template>

<script>
import axios from 'axios';
import _ from 'lodash';

export default {
    props: ["loading"],

    data() {
        return {
            words_n: false,
            word_1: null,
            word_2: null,
            word_3: null,
            analogies: [],
            error: null,
            glove: 'https://nlp.stanford.edu/projects/glove/'
        }
    },

    computed: {
        _loading: {
            get() {
                return this.loading
            },
            set(val) {
                this.$emit("loading_", val);
            }
        },
    },

    methods: {
        async submitAnalogy() {
            this._loading = true;
            this.error = null;
            try {
                if (!this.words_n) {
                    if (this.word_1) {
                        const res = await this.submit({
                            word1: this.word_1
                        });

                        const analogies = res.analogies;
                        if (analogies != null) {
                            this.analogies.push({
                                header: [this.word_1],
                                result: analogies
                            });
                            this.clearFieldsAndReverse();
                        }
                        else
                            this.error = 'Sorry, word not found in Corpus(dataset). Try another one';
                    } else
                        this.error = 'please enter a word so we can try to make an analogy based on it.';
                } else {
                    if (this.word_2 && this.word_2 && this.word_3) {
                        const res = await this.submit({
                            word1: this.word_1,
                            word2: this.word_2,
                            word3: this.word_3
                        });

                        const analogies = res.analogies;
                        this.analogies.push({
                            header: [this.word_1, this.word_2, this.word_3],
                            result: analogies
                        });
                        this.clearFieldsAndReverse();
                    } else
                        this.error = 'please enter the words so we can try to make an analogy based on them.';
                }           
            } catch(error) {
                console.log(error)
                this.error = 'Internal Server Error. Please try again later.';
            }
            this._loading = false;
        },

        clearFieldsAndReverse() {
            this.word_1 = null;
            this.word_2 = null;
            this.word_3 = null;
            this.error = null;
            _.reverse(this.analogies);
        },

        async submit(inputs) {
            const res = await axios.post(`${this.$hostname}/word-analogy`, {
                ...inputs
            });
            return res.data;
        }
    },

    watch: {
        words_n(val) {
            this.error = null;
        }
    }
}
</script>