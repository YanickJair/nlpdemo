<template>
    <v-container grid-list-xs>     
        <v-row>
            <v-col cols="12">
                 <v-alert
                    v-if="defaultData && !error"
                    dark
                    dense
                    icon="mdi-school"
                    class="transparent text-center"
                    prominent
                >
                    <a
                        href="https://www.yelp.com/dataset"
                        target="_blank"
                        style="text-decoration: none;"
                    >
                        Reviews from YELP Dataset
                    </a>
                </v-alert>

                <Status
                    v-if="error"
                    :message="error.message"
                    :type_="error.type_"
                    :dismissible="error.dismissible"
                />
            </v-col>

            <!-- Configurations -->
            <v-col cols="4">
                <v-row>
                    <v-col cols="12">
                        <Configs 
                            :countries="countries"
                            v-on:countries_="val => countries = val"
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
                            :word_analogy="word_analogy"
                            v-on:word_analogy_="val => word_analogy = val"
                        />
                    </v-col>

                    <v-col>
                        <Stats
                            :size="dataset_size * 10"
                            :analyzed="analyzed.length"
                        />
                    </v-col>
                </v-row>
            </v-col>

            <!-- Form and text Displayer -->
            <v-col cols="8" class="mt-5" v-if="avaiable">
                <v-progress-linear
                    v-if="loading"
                    indeterminate
                    color="cyan"
                    class="mt-4"
                ></v-progress-linear>

                <v-row>
                    <!-- Displayer Component -->
                    <div v-if="!quiz && !summarizer && !word_analogy">
                        <v-col cols="12" v-for="review in dataset" :key="review.review_id" >
                            <v-card outlined>
                                <!-- Loader -->
                                <v-progress-linear
                                    v-if="review[review.review_id + '_' + review.business_id]"
                                    indeterminate
                                    color="cyan"
                                    class="mt-4"
                                ></v-progress-linear>

                                <!-- Reviews Displayer -->
                                <component
                                    :is="cc"
                                    v-bind="{
                                        text: review.text,
                                        search: text,
                                        className: 'context_' + review.review_id,
                                    }"
                                ></component>

                                <v-card-actions>
                                    <v-btn
                                        outlined
                                        color="success"
                                        small
                                        @click="analyze(review)"
                                    >Analyze Review</v-btn>
                                </v-card-actions>

                                <!-- Analysis Result -->
                                <v-card-text>
                                    <ExResult
                                        v-if="beenAnalyzed(review.review_id) != null"
                                        :result="beenAnalyzed(review.review_id)[0].analysi"
                                        :text="text"
                                    />
                                </v-card-text>
                            </v-card>
                        </v-col>

                        <v-col cols="12">
                            <Pagination
                                :page="page"
                                :length="dataset_size"
                                v-on:page_="val => page = val"
                            />
                        </v-col>
                    </div>

                    <!-- Question Answering or Summarize large Text-->
                    <v-col cols="12" v-if="(quiz || summarizer) && !word_analogy">
                        <QuizAndSummarization
                            :componentType="quiz ? 'QUIZ' : 'SUMMARY'"
                        />
                    </v-col>

                    <v-col cols="12" v-if="word_analogy">
                        <WordAnalogy
                            :loading="loading"
                            v-on:loading_="val => loading = val"
                        />
                    </v-col>
                </v-row>
            </v-col>

            <v-col v-else cols="8" class="mt-8">
                <WoringOn />
            </v-col>
        </v-row>

        <!-- Footer -->
    </v-container>
</template>

<script>
import axios from 'axios';
import _ from 'lodash';

import Configs from '@/components/Configs';
import Form from '@/components/Form';
import Displayer from '@/components/Displayer';
import Stats from '@/components/Stats';
import QuizAndSummarization from '@/components/QuizAndSummarization';
import Summarize from '@/components/Summarize';
import Status from '@/components/utils/Status';
import Pagination from '@/components/utils/Pagination';
import ExResult from '@/components/Result';
import WordAnalogy from '@/components/WordAnalogy';
import WoringOn from '@/components/utils/WorkinOn';

export default {
    name: 'Home',

    components: {
        Configs,
        Form,
        Displayer,
        Stats,
        QuizAndSummarization,
        Summarize,
        Status,
        Pagination,
        ExResult,
        WordAnalogy,
        WoringOn
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
            word_analogy: false,
            sentiment: false,
            quiz: false,
            analysis_res: [],
            items: [],
            resultDialog: false,
            dataset: [],
            loading: false,
            SENTIMENT_ANALYSIS: null,
            chartdata: null,
            error: null,
            page: 1,
            dataset_size: 0,
            avaiable: true
        }
    },
  
    watch:{
        /* analysis_res(val) {
            this.getIitems(val)
        }, */

        defaultData(val) {
            if (val) this.getDataset();
            else this.dataset = [];
            this.analyzed = [];
        },

        quiz(val) {
            if (val) {
                this.summarizer = false;
                this.word_analogy = false;
                this.disableConfigFields();
            }
        },

        summarizer(val) {
            if (val) {
                this.quiz = false;
                this.word_analogy = false;
                this.disableConfigFields();
            }
        },

        word_analogy(val) {
            if (val) {
                this.summarizer = false;
                this.quiz = false;
                this.disableConfigFields();
            }
        },

        page(val) { this.getDataset(); },

        sentiment(val) { if (val) this.disableDownConfigFields(); },
        countries(val) { if (val) this.disableDownConfigFields(); },
        entities(val) { if (val) this.disableDownConfigFields(); },
        numbers(val) { if (val) this.disableDownConfigFields(); },
        persons(val) { if (val) this.disableDownConfigFields(); },
        verbs(val) { if (val) this.disableDownConfigFields(); }
    },

    methods: {
        disableConfigFields() {
            this.sentiment = false;
            this.countries = false;
            this.entities = false;
            this.verbs = false;
            this.numbers = false;
            this.persons = false;
        },

        disableDownConfigFields() {
            this.quiz = false;
            this.word_analogy = false;
            this.summarizer = false;
        },
        
        async analyze(review) {
            try {
                if (this.getConfig().length > 0) {
                    review[review.review_id + '_' + review.business_id] = true;
    
                    const res = await axios.post( `${this.$hostname}/analysis`, {
                        text: review.text,
                        configs: this.getConfig(review.text)
                    });

                    this.analysis_res = res.data;
                    const is_index = _.findIndex(this.analyzed, ['review_id', review.review_id]);
                    const item = {
                        review_id: review.review_id,
                        analysi: this.getIitems(res.data)
                    };
                    if (is_index == -1) {
                        this.analyzed.push(item);
                    }
                    else {
                        this.analyzed[is_index] = { ...item };
                    }
                    
                    review[review.review_id + '_' + review.business_id] = false;
                    this.resultDialog = true;
                }
            } catch (error) {
                this.error = {
                    message: "Server Connection Error. Please try again later.",
                    dismissible: false,
                    type_: "error"
                };
                review[review.review_id + '_' + review.business_id] = false;
                this.resultDialog = false;
            }
        },
        getConfig(post) {
            const config = []

            if (this.persons) config.push("persons");
            if (this.countries) config.push("countries");
            if (this.entities) config.push("entities");
            if (this.numbers) config.push("numbers");
            if (this.verbs) config.push("verbs");
            if (this.sentiment) config.push("sentiment");
            return config;
        },

        getDataset() {
            try {
                this.loading = true;

                let start = 0;
                if (this.page == 1)
                    start = 0;
                else
                    start = 10 * this.page;
                let end = start + 10;
                
                const res = axios.get(`${this.$hostname}/yelp-dataset/${start}/${end}`)
                    .then(
                        res => {
                            this.dataset = res.data.dataset;
                            this.dataset_size = res.data.pages;
                        }
                    ).catch(
                        error => {
                            this.loading = false;
                            this.error = {
                                message: "Server Connection Error. Please try again later.",
                                dismissible: false,
                                type_: "error"
                            };
                        }
                    );
                
            } catch (error) {
                this.loading = false;
                this.error = {
                    message: "Server Connection Error. Please try again later.",
                    dismissible: false,
                    type_: "error"
                };
            }
            this.loading = false;
        },

        getIitems(val) {
            if (!_.isNil(val.SENTIMENT_ANALYSIS)) this.SENTIMENT_ANALYSIS = val.SENTIMENT_ANALYSIS;
            this.chartdata = {
                labels: val.time_spent.labels,
                data: val.time_spent.data
            };
            return {
                result: [
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
                ],
                SENTIMENT_ANALYSIS: this.SENTIMENT_ANALYSIS,
                chartdata: this.chartdata
            }
        },

        beenAnalyzed(review_id) {
            return _.filter(this.analyzed, ['review_id', review_id]).length > 0
                ? _.filter(this.analyzed, ['review_id', review_id])
                : null;
        }
    },

    mounted() {
        if (this.avaiable)
            this.getDataset();
    }
}
</script>