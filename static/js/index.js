const counters = document.querySelectorAll('.counter');
const statsSection = document.querySelector('.stats-section');

function startCounters() {
    counters.forEach(counter => {
        const updateCounter = () => {
            const target = +counter.getAttribute('data-target');
            const suffix = counter.getAttribute('data-suffix') || '';
            const current = parseInt(counter.innerText) || 0;

            const increment = target / 100;

            if (current < target) {
                counter.innerText = Math.ceil(current + increment);
                setTimeout(updateCounter, 20);
            } else {
                counter.innerText = target + suffix;
            }
        };

        updateCounter();
    });
}

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            startCounters();
            observer.unobserve(statsSection); // run only once
        }
    });
}, {
    threshold: 0.5
});

observer.observe(statsSection);



document.addEventListener("DOMContentLoaded", function () {
    var myCarousel = document.querySelector('#testimonialCarousel');

    new bootstrap.Carousel(myCarousel, {
        interval: 3000,
        ride: 'carousel'
    });
});


// RESUME

document.addEventListener("DOMContentLoaded", function () {

pdfjsLib.GlobalWorkerOptions.workerSrc =
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

document.querySelectorAll(".pdf-viewer").forEach(container => {

    const url = container.getAttribute("data-url");

    const loadingTask = pdfjsLib.getDocument(url);

    loadingTask.promise.then(function(pdf) {

        pdf.getPage(1).then(function(page) {

            const baseViewport = page.getViewport({ scale: 1 });

            const scale = container.clientWidth / baseViewport.width;

            const viewport = page.getViewport({ scale });

            const canvas = document.createElement("canvas");
            const context = canvas.getContext("2d");

            canvas.height = viewport.height;
            canvas.width = viewport.width;

            container.innerHTML = "";
            container.appendChild(canvas);

            page.render({
                canvasContext: context,
                viewport: viewport
            });
        });

    });

});

});