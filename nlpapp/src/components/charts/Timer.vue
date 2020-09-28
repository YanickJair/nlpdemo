<script>
import { Line } from 'vue-chartjs';

export default {
    extends: Line,
    props: {
        chartdata: {
            type: Object,
            default() { return null }
        }
    },
    options: {
        type: Object,
        default() { return null }
    },
    mounted() {
        this.renderChart(this.chartdata, this.options)
    }
};
</script>