<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import fileDownload from 'js-file-download'

type Word = {
    word: string
    startTime: string
    endTime: string
}

const podcastId = ref(0)
const words = ref<Word[]>([
    {
        word: "this",
        startTime: "0.800s",
        endTime: "1.200s"        
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
                endCharIx: selectionEvent.anchorOffset + selectionEvent.extentOffset - 1
            } :
            {
                startCharIx: selectionEvent.extentOffset,
                endCharIx: selectionEvent.extentOffset + selectionEvent.anchorOffset - 1
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
        .post(`http://localhost:8000/podcasts/${podcastId.value}/excerpt`, req)
        .then(r => fileDownload(r.data, "excerpt.mp3"))
}

</script>

<template>
  <div>{{ transcriptText }}</div>
  <button @click="buttonClicked">Do it</button>
</template>
