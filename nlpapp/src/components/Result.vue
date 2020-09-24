<template>
    <div class="mt-5">
        <v-dialog
            v-model="_dialog"
            width="100%"
            height="100%"
            max-width="800"
            max-height="800"
        >
            <v-card
            >
                <v-row>
                    <v-col cols="6">
                        <v-list-item two-line v-if="SENTIMENT_ANALYSIS">
                            <v-list-item-content>
                                <div class="overline mb-4 text-center">Sentiment Analyze</div>
                                <v-list-item-title class="headline mb-1 text-center">
                                    {{ SENTIMENT_ANALYSIS[0].label }}
                                </v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-col>
                    <v-col :cols="SENTIMENT_ANALYSIS ? 6 : 12">
                        <v-card-text class="context">
                            <v-treeview
                                hoverable
                                :items="result"
                            ></v-treeview>
                        </v-card-text>
                    </v-col>

                    <v-col cols="12">
                        <v-list-item two-line v-if="summarized">
                            <v-list-item-content>
                                <div class="overline mb-4 text-center">Summarized Text</div>
                                <v-card-text>
                                    {{summarized}}
                                </v-card-text>
                            </v-list-item-content>
                        </v-list-item>
                    </v-col>
                    <v-col cols="12">
                        <ChartTimer
                            max-height="200"
                            :height="200"
                            :chartdata="_chartdata"
                            :options="options"
                        />
                    </v-col>
                </v-row>
            </v-card>
        </v-dialog>
    </div>
</template>

<script>

import ChartTimer from './charts/Timer';

export default {
    props: ["result", "dialog", "text", "SENTIMENT_ANALYSIS", "summarized", "chartdata"],
    components: { ChartTimer },
    data() {
        return {
            options: {
                responsive: true,
                maintainAspectRatio: false,
            }
        }
    },
    computed: {
        _dialog: {
            get() { return this.dialog; },
            set(val) {
                this.$emit("closeResult", val);
            }
        },
        _chartdata() {
            return this.chartdata ? {
                labels: this.chartdata.labels,
                datasets: [
                    {
                        label: 'Time Spent in Fraction of Seconds',
                        fill: '-1',
                        backgroundColor: '#36a2eb',
                        borderColor: '#36a2eb',
                        data: this.chartdata.data
                    }
                ]
            } : null
        }
    }
}
</script>