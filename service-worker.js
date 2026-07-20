const CACHE_NAME = "solar-roi-v1";

const files = [
"/",
"/style.css",
"/icon.png"
];


self.addEventListener("install", e=>{

e.waitUntil(

caches.open(CACHE_NAME)
.then(cache=>{

return cache.addAll(files);

})

);

});


self.addEventListener("fetch", e=>{

e.respondWith(

caches.match(e.request)
.then(response=>{

return response || fetch(e.request);

})

);

});
