<template>
    <div class="container align-items-senter">
    </div>
    <h2>Movies</h2>
    <div class="row justify-content-between gap-3">
      <div class="row w-50 border border-opacity-10 rounded p-0"
            v-for="movie in movies" key="movie.id">
        <div class="col p-0">
            <img class="img-fluid rounded-start" v-bind:src="movie.poster"  v-if="test"/>
        </div>
        <div class="col pr-0">
          <h3 class="mt-3">{{ movie.title }}</h3>
          <p>{{ movie.description }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  let movies = ref([]);
  let test =[];
  
  onMounted(() => {
    fetchMovies();
  });
  
  let fetchMovies = () => {
    fetch("/api/v1/movies", {
        method: 'GET'
    })
      .then(response => response.json())
      .then(data => {
        movies.value = data;
      })
      .catch(error => {
        console.error("Error fetching movies:", error);
      });
  };
  </script>