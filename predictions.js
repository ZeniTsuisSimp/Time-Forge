import * as THREE from 'three';

// Setup
const canvas = document.querySelector('#bg-canvas');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true });

renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
camera.position.setZ(30);

// Create colorful nebula effect
const createNebula = () => {
    const geometry = new THREE.BufferGeometry();
    const count = 10000;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    
    for(let i = 0; i < count * 3; i += 3) {
        positions[i] = (Math.random() - 0.5) * 100;
        positions[i + 1] = (Math.random() - 0.5) * 100;
        positions[i + 2] = (Math.random() - 0.5) * 100;
        
        // Create rainbow colors
        colors[i] = Math.random();
        colors[i + 1] = Math.random();
        colors[i + 2] = Math.random();
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    
    const material = new THREE.PointsMaterial({
        size: 0.1,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        blending: THREE.AdditiveBlending
    });
    
    return new THREE.Points(geometry, material);
};

const nebula = createNebula();
scene.add(nebula);

// Create floating symbols for each prediction type
const createSymbol = (emoji, position) => {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    canvas.width = 128;
    canvas.height = 128;
    context.font = '80px Arial';
    context.fillText(emoji, 24, 96);
    
    const texture = new THREE.CanvasTexture(canvas);
    const material = new THREE.SpriteMaterial({ map: texture });
    const sprite = new THREE.Sprite(material);
    sprite.position.set(...position);
    sprite.scale.set(5, 5, 5);
    return sprite;
};

const symbols = [
    createSymbol('📈', [-15, 10, -5]),
    createSymbol('🏠', [0, -10, -5]),
    createSymbol('💰', [15, 10, -5])
];

symbols.forEach(symbol => scene.add(symbol));

// Animation
let time = 0;
function animate() {
    requestAnimationFrame(animate);
    time += 0.001;
    
    nebula.rotation.x += 0.0005;
    nebula.rotation.y += 0.0003;
    
    symbols.forEach((symbol, index) => {
        symbol.position.y += Math.sin(time + index) * 0.02;
    });
    
    renderer.render(scene, camera);
}

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Mouse interaction
let mouseX = 0;
let mouseY = 0;
document.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX - window.innerWidth / 2) * 0.001;
    mouseY = (event.clientY - window.innerHeight / 2) * 0.001;
    
    camera.position.x += (mouseX - camera.position.x) * 0.05;
    camera.position.y += (-mouseY - camera.position.y) * 0.05;
    camera.lookAt(scene.position);
});

animate();

// Handle prediction card clicks
document.querySelectorAll('.predict-btn').forEach(button => {
    button.addEventListener('click', (e) => {
        const card = e.target.closest('.prediction-card');
        const type = card.dataset.type;
        
        // Add cool click effect
        card.style.transform = 'scale(0.95)';
        setTimeout(() => {
            card.style.transform = 'scale(1)';
            // Redirect to specific prediction page
            window.location.href = `${type}-prediction.html`;
        }, 200);
    });
}); 