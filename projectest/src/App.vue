<template>
  <div class="flex flex-col h-screen">
    <h1 class="color-yellow-200">Welcome to Merchant Locator</h1>
    <div class="flex flex-grow bg-gray-700 text-white">
      <!-- Left half with search bar and categories -->
      <div class="w-1/2">
        <header class="bg-gray-200 p-4 flex justify-between items-center">
          <input
            type="text"
            placeholder="Search..."
            v-model="searchTerm"
            @input="searchMerchants"
            class="w-4/5 px-4 py-2 rounded-lg border-gray-300 focus:outline-none focus:border-indigo-500 text-black"
          />
          <button
            @click="searchMerchants"
            class="w-1/5 px-4 py-2 bg-gray-600 text-white rounded-lg ml-2"
          >
            Search
          </button>
        </header>

        <!-- Categories buttons -->
        <div class="flex mt-4">
          <button
            @click="filterCategory('gym')"
            class="flex-1 px-4 py-2 bg-gray-600 text-white rounded-lg mr-2"
          >
            Gym
          </button>
          <button
            @click="filterCategory('coffeeshop')"
            class="flex-1 px-4 py-2 bg-gray-600 text-white rounded-lg mr-2"
          >
            Coffee Shop
          </button>
          <button
            @click="filterCategory('restaurant')"
            class="flex-1 px-4 py-2 bg-gray-600 text-white rounded-lg"
          >
            Restaurant
          </button>
        </div>

        <!-- Display images -->
        <main class="container mx-auto px-4 py-8">
          <div class="grid grid-cols-3 gap-4">
            <img
              v-for="(image, index) in filteredImages"
              :key="index"
              :src="`./assets/${image.src}`"
              :alt="'Image ' + (index + 1)"
              class="w-full h-auto"
            />
          </div>
        </main>
      </div>

      <!-- Right half with map -->
      <div class="w-1/2 bg-gray-200 p-4">
        <h2 class="text-xl font-bold">Map</h2>
        <div class="map-container">
          <div id="map" class="w-full h-full"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import merchantsData from '@/assets/merchants.json'; // Import the JSON file

const searchTerm = ref('');
const map = ref(null);

const searchMerchants = () => {
  const term = searchTerm.value.toLowerCase();
  const merchant = merchantsData.results.find(merchant => merchant.name.toLowerCase().includes(term));
  
  if (merchant) {
    const latitude = parseFloat(merchant.location.latitude);
    const longitude = parseFloat(merchant.location.longitude);

    if (!isNaN(latitude) && !isNaN(longitude)) {
      map.value.setView([latitude, longitude], 13);
    }
  }
};

// Initialize Leaflet map
onMounted(() => {
  map.value = L.map('map').setView([11.210323390068652, 125.00943694990097], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map.value);

  // Add markers for all merchants
  merchantsData.results.forEach(merchant => {
    const latitude = parseFloat(merchant.location.latitude);
    const longitude = parseFloat(merchant.location.longitude);

    if (!isNaN(latitude) && !isNaN(longitude)) {
      L.marker([latitude, longitude]).addTo(map.value)
        .bindPopup(merchant.name);
    }
  });
});
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 100%;
}
#map {
  width: 100%;
  height: 100%;
}
</style>
