const testimonials = [
    { name: "Sarah J.", content: "OMG this top is everything! The sparkle is unreal ✨", rating: 5 },
    { name: "Emily R.", content: "Wore this to my birthday dinner and got so many compliments.", rating: 5 },
    { name: "Jessica M.", content: "Beautiful quality, heavy fabric. Shipping was fast too.", rating: 4 }
];

// Inject Testimonials
const testimonialGrid = document.querySelector('.testimonial-grid');
testimonials.forEach(t => {
    const div = document.createElement('div');
    div.className = 'testimonial-card';
    div.innerHTML = `
        <div class="stars">${'★'.repeat(t.rating)}</div>
        <p>"${t.content}"</p>
        <p class="author">- ${t.name}</p>
    `;
    testimonialGrid.appendChild(div);
});

// Accordion Logic
document.querySelectorAll('.accordion-header').forEach(btn => {
    btn.addEventListener('click', () => {
        const content = btn.nextElementSibling;
        content.classList.toggle('active');
        btn.querySelector('.icon').textContent = content.classList.contains('active') ? '-' : '+';
    });
});

// Cart Logic
function handleAddToCart(type) {
    if (type === 'primary') {
        processOrder(59);
    } else {
        showOrderBumpPopup();
    }
}

function showOrderBumpPopup() {
    document.getElementById('order-bump-popup').classList.remove('hidden');
}

function processOrder(amount) {
    const poolUrl = 'https://simpleswap-automation-1.onrender.com';
    const btn = event.target;
    const originalText = btn.innerText;
    btn.innerText = 'Processing...';
    btn.disabled = true;

    fetch(`${poolUrl}/buy-now`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ amountUSD: amount })
    })
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                window.location.href = data.url;
            } else {
                alert('Error processing order. Please try again.');
                btn.innerText = originalText;
                btn.disabled = false;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error processing order. Please try again.');
            btn.innerText = originalText;
            btn.disabled = false;
        });
}
