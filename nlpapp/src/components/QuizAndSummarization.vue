<template>
    <v-card class="elevation-0 pa-3">
        <v-alert
            outlined
            type="info"
            prominent
            border="left"
        >
            {{ componentType == 'QUIZ' ? alert_q : alert_sa }}
        </v-alert>

        <div>
            <v-alert
                class="ma-5"
                v-if="error"
                dense
                :type="error.success ? 'info' : 'error'"
            >
                {{ error.message }}
            </v-alert>

            <v-form
                ref="form"
                v-model="valid"
                :lazy-validation="lazy"
            >
                <v-textarea
                    outlined
                    v-model="text"
                    name="input-7-4"
                    required
                    :rules="textRules"
                    label="text"
                ></v-textarea>

                <v-btn color="success" class="elevation-0" small @click="addText">
                    {{ componentType == 'QUIZ' ? 'Add Text' : 'Summarize Text' }}
                </v-btn>
            </v-form>

            <v-progress-linear
                v-if="loading"
                indeterminate
                color="cyan"
                class="mt-4"
            ></v-progress-linear>

            <v-card-text
                class="mt-4"
                v-if="$data._text"
                style="border-width: 1px; border-style:solid; border-color:black"
            >
                {{ $data._text }}
            </v-card-text>

            <v-card-text v-if="$data._text && this.componentType == 'QUIZ'">
                <v-form
                    ref="form_quiz"
                >
                    <v-text-field
                        v-model="quiz"
                        :counter="80"
                        :rules="quizRules"
                        label="question"
                        width="200"
                        outlined
                        required
                    ></v-text-field>
                    
                    <v-btn color="success" text small @click="quizz">Submit</v-btn>
                </v-form>

                <v-list v-if="quiz_and_answers.length > 0">
                    <v-list-item>
                        <v-list-item-content>
                            <v-list-item-title class="body-3">Question Answering</v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>

                    <v-list-item two-line v-for="(answer, i) in quiz_and_answers" :key="i">
                        <v-list-item-content>
                            <v-list-item-title>{{ answer.quiz }}</v-list-item-title>
                            <v-list-item-subtitle v-text="answer.anwser"></v-list-item-subtitle>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
            </v-card-text>
        </div>
    </v-card>
</template>

<script>
import axios from 'axios';

export default {
    props: ["componentType"],
    data() {
        return {
            loading: false,
            valid: true,
            lazy: false,
            alert_q: `Extract Question Answering from large Text. Enter a text and try to extract answer from questions you type in.`,
            alert_sa: `Summarize large text and see if it makes sense to you.`,
            text: null,
            _text: null,
            textRules: [
                v => !!v || 'text is required',
                v => (v && v.length >= 200) || 'Name must be more than 200 characters',
            ],
            quizRules: [
                v => !!v || 'Question is required',
                v => (v && v.length <= 80) || 'Question must be less than 80 characters',
            ],
            quiz: null,
            quiz_and_answers: [],
            summary_text: null,
            error: null
        }
    },

    methods: {
        async quizz() {
            if (this.$refs.form_quiz.validate()) {
                try {
                    this.loading = true;
    
                    const res = await axios.post(`${this.$hostname}/answer-question`, {
                        question: this.quiz,
                        text: this.$data._text
                    });

                    const anwser = res.data.answer;
                    this.quiz_and_answers.push({
                        quiz: this.quiz,
                        anwser: anwser
                    });
                    this.quiz = null;
                } catch (error) {
                    this.loading = false;
                    this.error = {
                        success: false,
                        message: "Internal Server Error"
                    };
                }
                this.loading = false;
            }
        },

        async summarize_text() {
            try {
                this.loading = true;
                const res = await axios.post(`${this.$hostname}/summarizer`, {
                    text: this.text
                });

                this.$data._text = res.data.summary_text;
            } catch (error) {
                this.loading = false;
                this.error = {
                    success: false,
                    message: "Internal Server Error"
                };
            }
            this.loading = false;
        },

        addText() {
            if (this.$refs.form.validate()) {
                if (this.componentType == 'SUMMARY') {
                    this.summarize_text();
                } else {
                    this.$data._text = this.text;
                    this.text = null;
                }
            }
        }
    }
}
</script>