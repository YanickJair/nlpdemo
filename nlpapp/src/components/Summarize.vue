<template>
    <v-card class="elevation-0 pa-3">
        <v-alert
            outlined
            type="info"
            prominent
            border="left"
        >
            {{ alert }}
        </v-alert>

        <div>
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

                <v-btn color="success" class="elevation-0" small @click="addText">Add Text</v-btn>
            </v-form>

            <v-card-text
                class="mt-4"
                v-if="$data._text"
                style="border-width: 1px; border-style:solid; border-color:black"
            >
                {{ $data._text }}
            </v-card-text>
        </div>
    </v-card>
</template>

<script>
export default {
    data() {
        return {
            alert: `
            Summarize large text and see if it makes sense to you.
            `,
            text: null,
            _text: null
        }
    },

    methods: {
        
    }
}
</script>