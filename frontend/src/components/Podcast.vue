<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import fileDownload from 'js-file-download'

type Word = {
    word: string
    start_time: string
    end_time: string
}

const podcastId = ref(0)
const words = ref<Word[]>([])
const selectedWords = ref<Word[]>([])

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
    console.log(selectedWords.value)

    const req = {
        words: selectedWords.value
    }

    axios
        .post(`http://localhost:8000/podcasts/${podcastId.value}/excerpt`, req,
        {
            responseType: 'arraybuffer'
        })
        .then(r => fileDownload(r.data, "excerpt.mp3"))
}

const onMouseUpTranscript = (e: any) => {
    const s = window.getSelection()
    selectedWords.value = getSelectedWords(s)
}

const selectedWordsTimeText = computed(() => {
    if (selectedWords.value.length === 0) {
        return ""
    } else {
        const startTime = selectedWords.value[0].start_time
        const endTime = selectedWords.value[selectedWords.value.length-1].end_time
        return `${startTime}s - ${endTime}s`
    }
})

</script>

<template>
    <div class="container"></div>
        <div class="child">
            <p>{{ selectedWordsTimeText }}</p>
            <button @click="buttonClicked">Sound Bite</button>
        </div>
        <div class="child transcript" @mouseup="onMouseUpTranscript">{{ transcriptText }}</div>
</template>
<style scoped>
.container {
    display: flex;
}

.child {
    flex: 1;
}

.child.transcript {
    margin-left: 20px;
    border: 2px solid yellow;
}
</style>
