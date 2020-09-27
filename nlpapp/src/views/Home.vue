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
                    v-if="defaultData && !error"
                    dark
                    dense
                    icon="mdi-school"
                    class="transparent text-center"
                    prominent
                >
                    YELP Reviews
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
                            :size="dataset_size * 10"
                            :analyzed="analyzed.length"
                        />
                    </v-col>
                </v-row>
            </v-col>

            <!-- Form and text Displayer -->
            <v-col cols="8" class="mt-5">
                <v-progress-linear
                    v-if="loading"
                    indeterminate
                    color="cyan"
                    class="mt-4"
                ></v-progress-linear>

                <v-row>
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
                    <v-col cols="12" v-if="quiz || summarizer">
                        <Quiz
                            :componentType="quiz ? 'QUIZ' : 'SUMMARY'"
                        />
                    </v-col>
                </v-row>
            </v-col>
        </v-row>

        <!-- Result -->
    </v-container>
</template>

<script>
import axios from 'axios';
import _ from 'lodash';

import Configs from '@/components/Configs.vue';
import Form from '@/components/Form.vue';
import Displayer from '@/components/Displayer.vue';
import Header from '@/components/Header.vue';
import Stats from '@/components/Stats.vue';
import Quiz from '@/components/Quiz.vue';
import Summarize from '@/components/Summarize.vue';
import Status from '@/components/utils/Status.vue';
import Pagination from '@/components/utils/Pagination.vue';
import ExResult from '@/components/utils/Result.vue';

export default {
    name: 'Home',

    components: {
        Configs,
        Form,
        Displayer,
        Header,
        Stats,
        Quiz,
        Summarize,
        Status,
        Pagination,
        ExResult
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
            chartdata: null,
            error: null,
            page: 1,
            dataset_size: 0,
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
        },

        page(val) {
            this.getDataset();
        }
    },

    methods: {
        async analyze(review_id, post) {
            try {

                if (this.getConfig().length > 0) {
                    this.loading = true;

                    console.log(post)
    
                    const res = await axios.post("http://127.0.0.1:5000/analysis", {
                        text: post,
                        configs: this.getConfig(post)
                    });

                    this.analysis_res = res.data;
                    console.log(res.data)
                    if (_.filter(this.analyzed, ['review_id', review_id]).length == 0)
                        this.analyzed.push({
                            review_id: review_id,
                            analysi: this.getIitems(res.data)
                        });

                    this.loading = false;
                    this.resultDialog = true;
                }
            } catch (error) {
                this.loading = false;
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
            if (this.sentiment /* && post.length > 200 */) config.push("sentiment");
            return config;
        },

        async getDataset() {
            try {
                this.loading = true;

                let start = 0;
                if (this.page == 1)
                    start = 0;
                else
                    start = 10 * this.page;
                let end = start + 10;
                
                const res = await axios.get(`http://127.0.0.1:5000/yelp-dataset/${start}/${end}`);
                this.dataset = res.data.dataset;
                this.dataset_size = res.data.pages;
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
        this.getDataset();
    }
}
</script>