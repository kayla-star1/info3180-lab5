<template>
  <div>
    <form id="movieForm" @submit.prevent="saveMovie">
      <div v-if="success || errors.length > 0">
        <ul v-if="success">
          <li>Successfully added movie</li>
        </ul>
        <ul v-else>
          <li v-for="error in errors">{{ error }}</li>
        </ul>
      </div>
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" class="form-control"/>
      </div>
      <div class="form-group mb-3">
        <label for="poster" class="form-label">Movie Poster</label>
        <input type="file" name="poster" class="form-control"/>
      </div>
      <div class="form-group mb-3">
        <label for="description" class="form-label">Movie Description</label>
        <textarea name="description" class="form-control"></textarea>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

let csrf_token = ref('');
let errors = ref([]);
let success = ref(false);

onMounted(() => {
  getCsrfToken();
});

const getCsrfToken = () => {
  fetch('/api/v1/csrf-token', {
    headers: {
      'Content-Type': 'application/json',
    },
  })
    .then((response) => response.json())
    .then((data) => {
      csrf_token.value = data.csrf_token;
    });
};

const saveMovie = async () => {
  const movieForm = document.getElementById('movieForm');
  const form_data = new FormData(movieForm);

  try {
    const response = await fetch("/api/v1/movies", {
  method: 'POST',
  body: form_data,
  headers: { 'X-CSRFToken': csrf_token.value },
});
console.log(response);
const data = await response.json();

    if (data.errors) {
      errors.value = [data.errors];
    } else {
      success.value = true;
    }
  } catch (error) {
    console.error("FAILED", error);
  }
  errors.value = [];
  success.value = false;
};
</script>