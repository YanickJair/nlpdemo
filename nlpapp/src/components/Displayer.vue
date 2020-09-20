<template>
    <v-card-text :class="className" outlined>
        <p>{{ text }}</p>
    </v-card-text>
</template>

<script>
import Mark from 'mark.js';

export default {
    props: {
        text: {
            type: String,
            default() {
                return ""
            }
        },
        search: {
            type: String,
            default() {
                return ""
            }
        },
        className: {
            type: String
        },
        pos: {
            type: Number,
            default() {
                return 0
            }
        }
    },

    watch: {
        search(val) {
            var markInstance = new Mark(document.querySelector('.' + this.className));
            
            const options = {
                separateWordSearch: true,
                diacritics: false,
                debug: false,
                element: 'mark',
                className: "marked",
                "synonyms": {"one": "1"}
            };
            markInstance.unmark({
                done: function(){
                    markInstance.mark(val, options);
                },
            });
        },
    }
}
</script>

<style scoped>
span.markYellow {
  background: yellow;
  color: blue;
}

span.markBlue {
  background: blue;
  color: white;
}
</style>