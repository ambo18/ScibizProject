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
            v-model="search"
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
import { ref, computed, onMounted } from 'vue';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import merchantsData from '@/assets/merchants.json'; // Import the JSON file

const search = ref('');
const filteredMerchants = ref([]);
const map = ref(null);

const filterCategory = (category) => {
  search.value = category;
};

const searchMerchants = () => {
  const searchTerm = search.value.toLowerCase();
  filteredMerchants.value = merchantsData.results.filter(merchant => merchant.name.toLowerCase().includes(searchTerm));
  
  // Clear existing markers from the map
  map.value.eachLayer(layer => {
    if (layer instanceof L.Marker) {
      map.value.removeLayer(layer);
    }
  });

  // Add markers for filtered merchants
  filteredMerchants.value.forEach(merchant => {
    const latitude = parseFloat(merchant.location.latitude);
    const longitude = parseFloat(merchant.location.longitude);
    const logoUrl = merchant.logos['30x30']; // Get the URL of the 30x30 logo

    if (!isNaN(latitude) && !isNaN(longitude) && logoUrl) {
      const icon = L.divIcon({
        html: `<div><img src="${logoUrl}" style="width: 30px; height: 30px;"><br>${merchant.name}</div>`,
        iconSize: [30, 40], // Adjust the size if needed
        iconAnchor: [15, 40] // Position the anchor point of the icon
      });

      L.marker([latitude, longitude], { icon }).addTo(map.value)
        .bindPopup(merchant.name);
    }
  });
};

// Initialize Leaflet map
onMounted(() => {
  map.value = L.map('map').setView([11.210323390068652, 125.00943694990097], 13);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map.value);

  // Add markers for all merchants initially
  merchantsData.results.forEach(merchant => {
    const latitude = parseFloat(merchant.location.latitude);
    const longitude = parseFloat(merchant.location.longitude);
    const logoUrl = merchant.logos['30x30']; // Get the URL of the 30x30 logo

    if (!isNaN(latitude) && !isNaN(longitude) && logoUrl) {
      const icon = L.divIcon({
        html: `<div><img src="${logoUrl}" style="width: 30px; height: 30px;"><br>${merchant.name}</div>`,
        iconSize: [30, 40], // Adjust the size if needed
        iconAnchor: [15, 40] // Position the anchor point of the icon
      });

      L.marker([latitude, longitude], { icon }).addTo(map.value)
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
