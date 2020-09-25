<template>
    <v-container grid-list-xs>     
        <v-row>
            <v-col cols="12">
                <Header
                    :default="defaultData"
                    v-on:setDefaultData="val => defaultData = val"
                    v-on:addData="val => dataset.push(val)"
                />
            </v-col>

            <v-col cols="12">
                 <v-alert
                    v-if="defaultData"
                    dark
                    dense
                    icon="mdi-school"
                    class="transparent text-center"
                    prominent
                >
                    YELP Reviews
                </v-alert>
            </v-col>

            <!-- Configurations -->
            <v-col cols="4">
                <v-row>
                    <v-col cols="12">
                        <Configs 
                            :countries="countries"
                            v-on:countries="val => countries = val"
                            :entities="entities"
                            v-on:entities_="val => entities = val"
                            :verbs="verbs"
                            v-on:verbs_="val => verbs = val"
                            :numbers="numbers"
                            v-on:numbers_="val => numbers = val"
                            :persons="persons"
                            v-on:persons_="val => persons = val"
                            :summarizer="summarizer"
                            v-on:summarizer_="val => summarizer = val"
                            :sentiment="sentiment"
                            v-on:sentiment_="val => sentiment = val"
                            :quiz="quiz"
                            v-on:quiz_="val => quiz = val"
                        />
                    </v-col>

                    <v-col>
                        <Stats
                            :size="dataset.length"
                            :analyzed="analyzed.length"
                        />
                    </v-col>
                </v-row>
            </v-col>

            <!-- Form and text Displayer -->
            <v-col cols="8" class="mt-5">
                <v-row v-if="!loading">
                    <!--v-col v-if="!quiz">
                        <Form
                            :text="text"
                            v-on:searchText="val => text = val"
                        />
                    </v-col-->

                    <!-- Displayer Component -->
                    <div v-if="!quiz && !summarizer">
                        <v-col cols="12" v-for="review in dataset" :key="review.review_id" >
                            <v-card outlined>
                                <component
                                    :is="cc"
                                    v-bind="{
                                        text: review.text,
                                        search: text,
                                        className: 'context_' + review.review_id,
                                    }"
                                ></component>
                                <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn
                                        outlined
                                        color="indigo"
                                        small
                                        @click="analyze(review.review_id, review.text)"
                                    >Analyze</v-btn>
                                </v-card-actions>
                            </v-card>
                        </v-col>
                    </div>

                    <!-- Question Answering or Summarize large Text-->
                    <v-col cols="12" v-if="quiz || summarizer">
                        <Quiz
                            :componentType="quiz ? 'QUIZ' : 'SUMMARY'"
                        />
                    </v-col>
                </v-row>

                <v-container class="fill-height" fluid v-else>
                    <v-row align="center" justify="center">
                        <v-col cols="12" sm="8" md="4">
                            <v-progress-circular
                                indeterminate
                                color="primary"
                            ></v-progress-circular>
                        </v-col>
                    </v-row>
                </v-container>
            </v-col>
        </v-row>

        <!-- Result -->
        <Result
            :result="items"
            :dialog="resultDialog"
            :SENTIMENT_ANALYSIS="SENTIMENT_ANALYSIS"
            :text="text"
            v-on:closeResult="val => resultDialog = val"
            :summarized="summarized"
            :chartdata="chartdata"
        />

        <!-- Loader -->
        <!--Loader
            :loading="loading"
            v-on:loading="val => loading = val"
        /-->
    </v-container>
</template>

<script>
import axios from 'axios';
import _ from 'lodash';

import Configs from '@/components/Configs.vue';
import Form from '@/components/Form.vue';
import Result from '@/components/Result.vue';
import Displayer from '@/components/Displayer.vue';
import Header from '@/components/Header.vue';
import Loader from '@/components/Loader.vue';
import Stats from '@/components/Stats.vue';
import Quiz from '@/components/Quiz.vue';
import Summarize from '@/components/Summarize.vue';

export default {
    name: 'Home',

    components: {
        Configs,
        Form,
        Result,
        Displayer,
        Header,
        Loader,
        Stats,
        Quiz,
        Summarize
    },

    data() {
        return {
            cc: Displayer,
            defaultData: true,
            analyzed: [],
            valid: true,
            text: null,
            optionInputs: [],
            countries: true,
            entities: true,
            verbs: true,
            numbers: true,
            persons: true,
            summarizer: false,
            summarized: null,
            sentiment: false,
            quiz: false,
            analysis_res: [],
            items: [],
            resultDialog: false,
            dataset: [],
            loading: false,
            SENTIMENT_ANALYSIS: null,
            chartdata: null
        }
    },
  
    watch:{
        analysis_res(val) {
            this.getIitems(val)
        },

        defaultData(val) {
            if (val) this.getDataset();
            else this.dataset = [];
            this.analyzed = [];
        },

        quiz(val) {
            if (val) {
                this.sentiment = false;
                this.summarizer = false;
            }
        },

        summarizer(val) {
            if (val) {
                this.sentiment = false;
                this.quiz = false;
            }
        },

        sentiment(val) {
            if (val) {
                this.summarizer = false;
                this.quiz = false;
            }
        }
    },

    methods: {
        async analyze(pos, post) {
            try {
                this.loading = true;
    
                const res = await axios.post("http://127.0.0.1:5000/analysis", {
                    text: post,
                    configs: this.getConfig(post)
                });

                this.analysis_res = res.data;
                if (!_.includes(this.analyzed, pos)) this.analyzed.push(pos);
                this.loading = false;
                this.resultDialog = true;
            } catch (error) {
                this.loading = false;
                this.resultDialog = false;
                console.log(error)
            }
        },
        getConfig(post) {
            const config = []

            if (this.persons) config.push("persons");
            if (this.countries) config.push("countries");
            if (this.entities) config.push("entities");
            if (this.numbers) config.push("numbers");
            if (this.verbs) config.push("verbs");
            if (this.sentiment /* && post.length > 200 */) config.push("sentiment");
            return config;
        },

        async getDataset() {
            try {
                let rating = 1;
                const res = await axios.get(`http://127.0.0.1:5000/yelp-dataset/${rating}`);
                this.dataset = res.data.slice(0, 10);
            } catch (error) {
                console.log(error)
            }
        },

        getIitems(val) {
            if (!_.isNil(val.SENTIMENT_ANALYSIS)) this.SENTIMENT_ANALYSIS = val.SENTIMENT_ANALYSIS;
            this.chartdata = {
                labels: val.time_spent.labels,
                data: val.time_spent.data
            };
            console.log(this.chartdata);
            this.items = [
                {
                    name: "PERSONS",
                    children: val.PERSONS ? val.PERSONS.map(p => {
                        return {
                            name: p[0]
                        }
                    }) : []
                },
                {
                    name: "ENTITIES",
                    children: val.ENTITIES ? val.ENTITIES.map(p => {
                        return {
                            name: `${ p[0] + ' : ' + p[1] }`
                        }
                    }) : []
                },
                {
                    name: "COUNTRIES",
                    children: val.COUNTRIES ? val.COUNTRIES.map(p => {
                        return {
                            name:  p[0]
                        }
                    }) : []
                },
                {
                    name: "VERBS/AUX",
                    children: val.VERBS ? val.VERBS.map(p => {
                        return {
                            name:  p[0]
                        }
                    }) : []
                }
            ]
        }
    },

    mounted() {
        this.loading = true;
        this.getDataset();
        this.loading = false;
    }
}
</script>