<template>
  <div>
    <h1>Upload Movie</h1>
    <form @submit.prevent="saveMovie" id="movieForm">
      <div class="form-group mb-3">
        <label for="title" class="form-label">Movie Title</label>
        <input type="text" name="title" class="form-control" v-model="title" />
      </div>
      <div class="form-group mb-3">
        <label for="poster" class="form-label">Movie Poster</label>
        <input type="file" name="poster" class="form-control" @change="handleFileChange" />
      </div>
      <div class="form-group mb-3">
        <label for="description" class="form-label">Movie Description</label>
        <textarea name="description" class="form-control" v-model="description"></textarea>
      </div>
        <button @click="saveMovie" class="btn btn-primary">Submit</button>
      </form>
    </div>
</template>
  
<script setup>
  const emit = defineEmits(['submit'])
  
  function saveMovie(){
    emit('submit')
    let movieForm = document.getElementById('movieForm');
    let form_data = new FormData(movieForm);

    fetch("/api/v1/movies", {
        method: 'POST',
        body: form_data,
        headers: {
        'X-CSRFToken': csrf_token.value
      }
})

    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        // display a success message
        console.log(data);
    })
    .catch(function (error) {
        console.log(error);
    });

    };

  import { ref, onMounted} from "vue";

  onMounted(() => {
    getCsrfToken();
    });
   let csrf_token = ref("");
   function getCsrfToken() {
    fetch('/api/v1/csrf-token')
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
      })
}


  </script>  