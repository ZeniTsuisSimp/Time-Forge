import * as THREE from 'three';

// Setup
const canvas = document.querySelector('#bg-canvas');
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ canvas, alpha: true });

renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
camera.position.setZ(30);

// Create particles
const particlesGeometry = new THREE.BufferGeometry();
const particlesCount = 8000;
const posArray = new Float32Array(particlesCount * 3);
const velocityArray = new Float32Array(particlesCount * 3);

for(let i = 0; i < particlesCount * 3; i++) {
    posArray[i] = (Math.random() - 0.5) * 100;
    velocityArray[i] = (Math.random() - 0.5) * 0.02;
}

particlesGeometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

// Create multiple particle systems with different colors
const createParticleSystem = (color, size, count) => {
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(count * 3);
    
    for(let i = 0; i < count * 3; i++) {
        positions[i] = (Math.random() - 0.5) * 100;
    }
    
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    
    const material = new THREE.PointsMaterial({
        size: size,
        color: color,
        transparent: true,
        opacity: 0.6,
        blending: THREE.AdditiveBlending
    });
    
    return new THREE.Points(geometry, material);
};

const particleSystem1 = createParticleSystem('#646cff', 0.05, 2000);
const particleSystem2 = createParticleSystem('#ff64c8', 0.03, 3000);
const particleSystem3 = createParticleSystem('#64ffb4', 0.02, 4000);

scene.add(particleSystem1);
scene.add(particleSystem2);
scene.add(particleSystem3);

// Create floating timeline elements
const timelineGeometry = new THREE.TorusGeometry(10, 0.5, 16, 100);
const timelineMaterial = new THREE.MeshBasicMaterial({ 
    color: '#646cff',
    transparent: true,
    opacity: 0.3,
    wireframe: true
});
const timeline = new THREE.Mesh(timelineGeometry, timelineMaterial);
scene.add(timeline);

// Wave effect
let waveTime = 0;
const waveSpeed = 0.001;
const waveAmplitude = 0.2;

// Animation
function animate() {
    requestAnimationFrame(animate);
    
    waveTime += waveSpeed;
    
    // Rotate particle systems
    particleSystem1.rotation.x += 0.0001;
    particleSystem1.rotation.y += 0.0002;
    
    particleSystem2.rotation.x -= 0.0002;
    particleSystem2.rotation.z += 0.0001;
    
    particleSystem3.rotation.y += 0.0001;
    particleSystem3.rotation.z -= 0.0001;
    
    // Animate timeline
    timeline.rotation.x += 0.001;
    timeline.rotation.y += 0.002;
    timeline.scale.x = 1 + Math.sin(waveTime) * waveAmplitude;
    timeline.scale.y = 1 + Math.cos(waveTime) * waveAmplitude;
    
    // Update particle positions with wave effect
    const positions = particleSystem1.geometry.attributes.position.array;
    for(let i = 0; i < positions.length; i += 3) {
        positions[i + 1] += Math.sin(waveTime + positions[i] * 0.1) * 0.02;
    }
    particleSystem1.geometry.attributes.position.needsUpdate = true;
    
    renderer.render(scene, camera);
}

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

// Mouse movement effect with parallax
let mouseX = 0;
let mouseY = 0;
let targetX = 0;
let targetY = 0;

document.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX - window.innerWidth / 2) * 0.001;
    mouseY = (event.clientY - window.innerHeight / 2) * 0.001;
});

// Smooth camera movement
function updateCamera() {
    targetX += (mouseX - targetX) * 0.05;
    targetY += (mouseY - targetY) * 0.05;
    
    camera.position.x += (targetX - camera.position.x) * 0.1;
    camera.position.y += (-targetY - camera.position.y) * 0.1;
    camera.lookAt(scene.position);
    
    requestAnimationFrame(updateCamera);
}

animate();
updateCamera();

// Button hover effects
const buttons = document.querySelectorAll('.btn');
buttons.forEach(button => {
    button.addEventListener('mouseover', () => {
        button.style.transform = 'scale(1.05)';
    });
    
    button.addEventListener('mouseout', () => {
        button.style.transform = 'scale(1)';
    });
});

// Smooth scroll for navigation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});