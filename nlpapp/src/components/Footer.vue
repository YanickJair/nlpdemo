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

                <v-alert
                    class="ma-5"
                    v-if="error"
                    dense
                    :type="error.success ? 'info' : 'error'"
                >
                    {{ error.message }}
                </v-alert>

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
                        :loading="loading"
                        :disabled="loading"
                        text
                        @click="sendMail"
                    >
                        Send
                        <template v-slot:loader>
                            <span class="custom-loader">
                                <v-icon light>mdi-cached</v-icon>
                            </span>
                        </template>
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
import axios from 'axios';

export default {
    data: () => ({
        avaiable: false,
        dialog: false,
        loading: false,
        error: null,
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
        async sendMail() {
            if (this.$refs.form.validate()) {
                try {
                    this.loading = true;
                    const res = await axios.post(`${this.$hostname}/get-in-touch`, {
                        sender: this.email,
                        fullname: this.fullname,
                        message: this.message
                    });

                    this.email = null;
                    this.fullname = null;
                    this.message = null;
                    if (res.data.success)
                        this.error = {
                            success: true,
                            message: "Thank you for getting in touch! I'll make sure to respond as soon as possible."
                        };
                    else
                        this.error = {
                            success: false,
                            message: "Sorry! It was no possible to send your email."
                        };
                } catch (error) {
                    this.loading = false;
                    this.error = {
                        success: false,
                        message: "Internal Server Error"
                    };
                }
                this.loading = false;
            }
        }
    }
}
</script>

<style>
  .custom-loader {
    animation: loader 1s infinite;
    display: flex;
  }
  @-moz-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-webkit-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @-o-keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
  @keyframes loader {
    from {
      transform: rotate(0);
    }
    to {
      transform: rotate(360deg);
    }
  }
</style>
