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
    </v-footer>
</template>

<script>
  export default {
    data: () => ({
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
  }
</script>