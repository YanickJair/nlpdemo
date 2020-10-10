<template>
    <v-footer
        dark
        padless
    >
        <v-card
            class="flex"
            flat
            tile
        >
            <v-card-title class="dark">
                <strong class="subheading">
                    {{ new Date().getFullYear() }} — <strong>&copy;</strong>
                </strong>

                <v-spacer></v-spacer>
                <v-btn
                    color="success"
                    text
                    @click="dialog = true"
                    small
                    disabled
                >Get in touch <v-icon small class="ml-2">mdi-email</v-icon></v-btn>
                <a
                    v-for="site in sites"
                    :href="site.url"
                    :key="site.url"
                    class="mx-4"
                    dark
                    icon
                    :to="site.url"
                    target="_blank"
                >
                    <v-icon size="24px">
                        {{ site.icon }}
                    </v-icon>
                </a>
            </v-card-title>
        </v-card>

        <v-dialog
            v-model="dialog"
            width="500"
        >
            <v-card>
                <v-card-title class="body-2 grey lighten-1">
                    Wanna get in touch? Send me an email.
                </v-card-title>

                <v-card-text class="mt-5">
                    <v-form
                        ref="form"
                        v-model="valid"
                        lazy-validation
                    >
                        <v-text-field
                            v-model="fullname"
                            :counter="50"
                            :rules="nameRules"
                            label="Full name"
                            required
                            outlined
                        ></v-text-field>

                        <v-text-field
                            v-model="email"
                            :rules="emailRules"
                            label="E-mail"
                            required
                            outlined
                        ></v-text-field>

                        <v-textarea
                            outlined
                            name="input-7-4"
                            v-model="message"
                            :rules="messageRules"
                            label="write your message here please"
                        ></v-textarea>
                    </v-form>
                </v-card-text>

                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="primary"
                        text
                        @click="sendMail"
                    >
                        Send
                    </v-btn>
                    <v-btn
                        color="error"
                        text
                        @click="dialog = false"
                    >
                        Cancel
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-footer>
</template>

<script>
export default {
    data: () => ({
        dialog: false,
        valid: true,
        fullname: '',
        nameRules: [
            v => !!v || 'Name is required',
            v => (v && v.length <= 50) || 'Name must be less than 50 characters',
        ],
        email: '',
        emailRules: [
            v => !!v || 'E-mail is required',
            v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
        ],
        message: null,
        messageRules: [
            v => !!v || 'Message is required',
        ],
        sites: [
            {
                url: 'https://github.com/YanickJair',
                icon: 'mdi-github'
            },
            {
                url: 'https://www.linkedin.com/in/yanick-jair-t-61a88a16a/',
                icon: 'mdi-linkedin',
            },
            {
                url: 'https://www.youtube.com/channel/UCnjsn6JoCuAKHy8Z4z8x4FQ',
                icon: 'mdi-youtube',
            }
        ],
    }),

    methods: {
        sendMail() {
            if (this.$refs.form.validate()) {
                console.log("OK");
            }
        }
    }
}
</script>