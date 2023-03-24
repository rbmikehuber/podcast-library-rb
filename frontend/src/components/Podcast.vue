<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import axios from 'axios'
import fileDownload from 'js-file-download'
import moment from 'moment'
import { BASE_URL } from '../../api'

type Word = {
    word: string
    start_time: number
    end_time: number
}

const podcastId = ref(0)
const podcasts = ref([{
    "name": "",
    "id": 0
}])

const words = ref<Word[]>([])
const selectedWords = ref<Word[]>([])

const transcriptText = computed(() => {
    return words.value.map(w => w.word).join(" ")
})

const getSelectedWords = (selectionEvent: any) => {
    if (!selectionEvent.anchorNode) {
        return []
    } else {
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
}

const summary = ref("")

const summaryLoading = ref(true)
const tagsLoading = ref(true)
const transcriptLoading = ref(true)

const fetchDataFromApi = () => {
    tags.value = []
    summary.value = ""
    summaryLoading.value = true
    tagsLoading.value = true
    transcriptLoading.value = true

    axios
        .get(`${BASE_URL}/podcasts/${podcastId.value}/words`)
        .then(r => {
            words.value = r.data
            transcriptLoading.value = false
        })

    axios
        .get(`${BASE_URL}/podcasts/${podcastId.value}/summary`)
        .then(r => {
            summary.value = r.data
            summaryLoading.value = false
        })

    axios
        .get(`${BASE_URL}/podcasts/${podcastId.value}/keywords`)
        .then(r => {
            tags.value = r.data
            tagsLoading.value = false
        })

        axios
        .get(`${BASE_URL}/podcasts`)
        .then(r => {
            podcasts.value = r.data
        })        
}

onMounted(fetchDataFromApi)

const getSoundBite = (e: any) => {
    console.log(selectedWords.value)

    const req = {
        words: selectedWords.value
    }

    axios
        .post(`${BASE_URL}/podcasts/${podcastId.value}/excerpt`, req,
        {
            responseType: 'arraybuffer'
        })
        .then(r => fileDownload(r.data, "excerpt.mp3"))
}

const possibleSelectionChange = (e: any) => {
    const s = window.getSelection()
    selectedWords.value = getSelectedWords(s)
}

const formatSeconds = (seconds: number) => moment.utc(seconds*1000).format('HH:mm:ss')

const wordsInTranscriptSelected = computed(() => selectedWords.value.length !== 0)

const selectedWordsTimeText = computed(() => {
    if (!wordsInTranscriptSelected.value) {
        return ""
    } else {
        const startTime = selectedWords.value[0].start_time
        const endTime = selectedWords.value[selectedWords.value.length-1].end_time
        return `${formatSeconds(startTime)} - ${formatSeconds(endTime)}`
    }
})

document.body.addEventListener('mouseup', possibleSelectionChange)
document.body.addEventListener('click', possibleSelectionChange)

const tags=ref<string[]>([])
</script>

<template>
    <h1>Podcast Insights</h1>
    <select @change="fetchDataFromApi" v-model="podcastId">
        <option v-for="p in podcasts" :value="p.id">{{ p.name }}</option>
    </select>
    <div class="tag-container">
        <span v-if="tagsLoading"><i>Loading...</i></span>
        <div v-for="tag in tags" class="tag">{{ tag }}</div>
    </div>
    <div class="container">
        <div class="child container-left">
            <div class="summary content-container">
                <h3>Summary</h3>
                <span v-if="summaryLoading"><i>Loading...</i></span>
                <span v-if="!summaryLoading">{{  summary }}</span>
            </div>
            <div class="additionals content-container">
                <h3>Additionals</h3>
                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
            </div>
            <p>{{ selectedWordsTimeText }}</p>
            <button :disabled="!wordsInTranscriptSelected" @click="getSoundBite">Sound Bite</button>
        </div>
        <div class="child transcript content-container">
            <h3>Transcript</h3>
            <span v-if="transcriptLoading"><i>Loading...</i></span>
            <span v-if="!transcriptLoading">{{  transcriptText }}</span>
        </div>
    </div>
</template>
<style scoped>
.container-left {
    margin-right: 20px;
}
.additionals {
    height: 300px;
    overflow: auto;    
}
.summary {
    margin-bottom: 10px;
    height: 300px;
    overflow: auto;
}
.tag-container {
    display: flex;
}
.tag {
    border: 1px solid lightblue;
    border-radius: 5px;
    flex: 1;
    margin: 5px;
}
.container {
    display: flex;
}

.child {
    flex: 1;
}

.transcript {
    height: 610px;
    overflow: auto;
}

.content-container {
    border: 1px solid lightyellow;
    border-radius: 5px;
    padding: 10px;
}
</style>
