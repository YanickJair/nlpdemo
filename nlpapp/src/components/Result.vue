<template>
    <v-expansion-panels inset flat>
        <v-expansion-panel>
            <v-expansion-panel-header class="success--text" outlined>
                Analysis Result
            </v-expansion-panel-header>
                <v-expansion-panel-content>
                    <v-row>
                        <v-col cols="6">
                            <v-list-item two-line v-if="result.SENTIMENT_ANALYSIS">
                                <v-list-item-content>
                                    <div class="overline mb-4 text-center">Sentiment Analyze</div>
                                    <v-list-item-title class="headline mb-4 text-center">
                                        {{ result.SENTIMENT_ANALYSIS[0].label }}
                                    </v-list-item-title>

                                    <v-list-item-subtitle class="text-center">
                                        {{ parseFloat(result.SENTIMENT_ANALYSIS[0].score.toFixed(6)) }}
                                    </v-list-item-subtitle>
                                </v-list-item-content>
                            </v-list-item>
                        </v-col>
                        <v-col :cols="result.SENTIMENT_ANALYSIS ? 6 : 12">
                            <v-card-text class="context">
                                <v-treeview
                                    hoverable
                                    :items="result.result"
                                ></v-treeview>
                            </v-card-text>
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
                </v-expansion-panel-content>
        </v-expansion-panel>
    </v-expansion-panels>
</template>

<script>
import ChartTimer from './charts/Timer';

export default {
    props: ["result"],
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
        _chartdata() {
            return this.result.chartdata ? {
                labels: this.result.chartdata.labels,
                datasets: [
                    {
                        label: 'Time Spent in Fraction of Seconds',
                        fill: '-1',
                        backgroundColor: '#36a2eb',
                        borderColor: '#36a2eb',
                        data: this.result.chartdata.data
                    }
                ]
            } : null
        }
    }
}
</script>