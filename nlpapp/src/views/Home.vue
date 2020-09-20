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
                    Comments from Facebook
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
                <v-row >
                    <v-col>
                        <Form
                            :text="text"
                            v-on:searchText="val => text = val"
                        />
                    </v-col>
                    <v-col cols="12" v-for="(post, i) in dataset" :key="i">
                        <v-card outlined>
                            <component
                                :is="cc"
                                v-bind="{
                                    text: post,
                                    search: text,
                                    className: 'context_' + i,
                                }"
                            ></component>
                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn
                                    outlined
                                    color="indigo"
                                    small
                                    @click="analyze(i, post)"
                                >Analyze</v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>
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
        <Loader
            :loading="loading"
            v-on:loading="val => loading = val"
        />
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

export default {
    name: 'Home',

    components: {
        Configs,
        Form,
        Result,
        Displayer,
        Header,
        Loader,
        Stats
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
            if (this.summarizer) config.push("summarize");
            if (this.sentiment && post.length > 200 && !this.summarizer) config.push("sentiment");
            return config;
        },

        async getDataset() {
            const res = await axios.get("http://127.0.0.1:5000/dataset/5");
            this.dataset = res.data;
        },

        getIitems(val) {
            if (!_.isNil(val.SENTIMENT_ANALYSIS)) this.SENTIMENT_ANALYSIS = val.SENTIMENT_ANALYSIS;
            if (!_.isNil(val.summarized)) this.summarized = val.summarized;
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
        this.getDataset();
    }
}
</script>