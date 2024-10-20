<script setup lang="ts">
import { post } from '@/utils/request'

async function debug() {
  const response = await post('/apps/1a95b17a-7cc8-4c6e-9c31-1dc2534ca869/debug/', {
    body: { query: '你好，你是谁' },
  })
  console.log(response)
}
</script>
<template>
  <a-button @click="debug">发起请求</a-button>
</template>

<style scoped></style>
