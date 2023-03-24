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
const podcastIds = ref([0])
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

const fetchDataFromApi = () => {
    tags.value = []
    summary.value = ""

    axios
        .get(`${BASE_URL}/podcasts/${podcastId.value}/words`)
        .then(r => {
            words.value = r.data
        })

    axios
        .get(`${BASE_URL}/podcasts/${podcastId.value}/summary`)
        .then(r => {
            summary.value = r.data
        })

    axios
        .get(`${BASE_URL}/podcasts/${podcastId.value}/keywords`)
        .then(r => {
            console.log(r.data)
            tags.value = r.data
        })

        axios
        .get(`${BASE_URL}/podcasts`)
        .then(r => {
            console.log(r.data)
            podcastIds.value = r.data
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
        <option v-for="id in podcastIds" :value="id">{{ id }}</option>
    </select>
    <div class="tag-container">
        <div v-for="tag in tags" class="tag">{{ tag }}</div>
    </div>
    <div class="container">
        <div class="child container-left">
            <div class="summary">
                <h3>Summary</h3>
                <p>{{  summary }}</p>
            </div>
            <div class="additionals">
                <h3>Additionals</h3>
                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
            </div>
            <p>{{ selectedWordsTimeText }}</p>
            <button :disabled="!wordsInTranscriptSelected" @click="getSoundBite">Sound Bite</button>
        </div>
        <div class="child transcript">
            <h3>Transcript</h3>
            <div>{{ transcriptText }}</div>
        </div>
    </div>
</template>
<style scoped>
.container-left {
    margin-right: 20px;
}
.additionals {
    border: 2px solid yellow;
    height: 300px;
    overflow: auto;    
}
.summary {
    border: 2px solid yellow;
    margin-bottom: 10px;
    height: 300px;
    overflow: auto;
}
.tag-container {
    display: flex;
}
.tag {
    border: 1px solid lightblue;
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
    border: 2px solid yellow;
    height: 610px;
    overflow: auto;
}
</style>
