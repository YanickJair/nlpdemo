<template>
  <v-app>
    <v-main>
      <Header />
        <Home />
      <Footer />
    </v-main>
  </v-app>
</template>

<script>
import Home from './views/Home';
import Footer from '@/components/Footer';
import Header from '@/components/Header';

export default {
  name: 'App',

  components: { Home, Header, Footer }
};
</script>
