<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import fileDownload from 'js-file-download'
//import { } from '@cosmos/web'

type Word = {
    word: string
    start_time: string
    end_time: string
}

const podcastId = ref(0)
const words = ref<Word[]>([
    {
        word: "this",
        start_time: "0.800s",
        end_time: "1.200s"        
    }
])

const transcriptText = computed(() => {
    return words.value.map(w => w.word).join(" ")
})

const getSelectedWords = (selectionEvent: any) => {
    const { startCharIx, endCharIx } = 
        selectionEvent.anchorOffset < selectionEvent.extentOffset ? 
            {
                startCharIx: selectionEvent.anchorOffset,
                endCharIx: selectionEvent.extentOffset
            } :
            {
                startCharIx: selectionEvent.extentOffset,
                endCharIx: selectionEvent.anchorOffset
            }

    const selectedWords : Word[] = []
    let currentCharIx = 0

    for (let i = 0; i < words.value.length; i++) {
        if (startCharIx <= currentCharIx && currentCharIx <= endCharIx) {
            selectedWords.push(words.value[i])
        }

        currentCharIx += words.value[i].word.length + 1
    }

    return selectedWords
}

onMounted(() => {
    axios
        .get(`http://localhost:8000/podcasts/${podcastId.value}/words`)
        .then(r => {
            words.value = r.data
        })

})

const buttonClicked = (e: any) => {
    const s = window.getSelection()
    const selectedWords = getSelectedWords(s)
    console.log(s)
    console.log(selectedWords)

    const req = {
        words: selectedWords
    }

    axios
        .post(`http://localhost:8000/podcasts/${podcastId.value}/excerpt`, req,
        {
            responseType: 'arraybuffer'
        })
        .then(r => fileDownload(r.data, "excerpt.mp3"))
}

</script>

<template>
  <div>{{ transcriptText }}</div>
  <button @click="buttonClicked">Do it</button>
</template>
