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
    // Redirect to SimpleSwap or Pool Logic
    // For this protocol, we simulate the redirect or use the pool URL
    const poolUrl = 'https://simpleswap-automation-1.onrender.com'; // Or from config
    console.log(`Processing order for $${amount}`);
    
    // In a real scenario, this would POST to the pool or redirect to SimpleSwap with params
    // For now, we'll redirect to a "success" page or the pool
    window.location.href = `${poolUrl}/buy-now?amount=${amount}`;
}
