// NeoAiAppolis - JavaScript for AIDL Processing

// AIDL Parser and Processor
function processAIDL() {
    const editor = document.getElementById('aidl-editor');
    const output = document.getElementById('aidl-output');
    const aidlCode = editor.value;

    try {
        const parsed = parseAIDL(aidlCode);
        const result = formatAIDLOutput(parsed);
        output.innerHTML = result;
        output.style.color = '#10b981';
    } catch (error) {
        output.innerHTML = `Error: ${error.message}`;
        output.style.color = '#ef4444';
    }
}

function parseAIDL(code) {
    const lines = code.trim().split('\n');
    
    if (!code.includes('@AI-CREATION') || !code.includes('@END')) {
        throw new Error('Invalid AIDL format. Must contain @AI-CREATION and @END tags.');
    }

    const creation = {
        type: '',
        author: '',
        timestamp: '',
        license: '',
        content: '',
        meta: {}
    };

    let inContent = false;
    let inMeta = false;
    let contentLines = [];

    for (let line of lines) {
        line = line.trim();
        
        if (line === '@AI-CREATION' || line === '@END') {
            continue;
        }

        if (line.startsWith('content:')) {
            inContent = true;
            continue;
        }

        if (line.startsWith('meta:')) {
            inContent = false;
            inMeta = true;
            continue;
        }

        if (inContent) {
            contentLines.push(line);
        } else if (inMeta) {
            const [key, ...valueParts] = line.split(':');
            if (key && valueParts.length > 0) {
                creation.meta[key.trim()] = valueParts.join(':').trim();
            }
        } else {
            const [key, ...valueParts] = line.split(':');
            if (key && valueParts.length > 0) {
                const value = valueParts.join(':').trim();
                if (key.trim() === 'type') creation.type = value;
                if (key.trim() === 'author') creation.author = value;
                if (key.trim() === 'timestamp') {
                    creation.timestamp = value === 'auto' ? new Date().toISOString() : value;
                }
                if (key.trim() === 'license') creation.license = value;
            }
        }
    }

    creation.content = contentLines.join('\n');

    return creation;
}

function formatAIDLOutput(creation) {
    return `
<div style="border: 2px solid #00d4ff; padding: 1rem; border-radius: 8px;">
    <h4 style="color: #00d4ff; margin-bottom: 1rem;">✓ AIDL Creation Processed Successfully</h4>
    
    <div style="margin-bottom: 1rem;">
        <strong style="color: #7c3aed;">Type:</strong> <span style="color: #10b981;">${creation.type || 'undefined'}</span>
    </div>
    
    <div style="margin-bottom: 1rem;">
        <strong style="color: #7c3aed;">Author:</strong> <span style="color: #10b981;">${creation.author || 'anonymous'}</span>
    </div>
    
    <div style="margin-bottom: 1rem;">
        <strong style="color: #7c3aed;">Timestamp:</strong> <span style="color: #10b981;">${creation.timestamp || 'not set'}</span>
    </div>
    
    <div style="margin-bottom: 1rem;">
        <strong style="color: #7c3aed;">License:</strong> <span style="color: #10b981;">${creation.license || 'not specified'}</span>
    </div>
    
    <div style="margin-bottom: 1rem;">
        <strong style="color: #7c3aed;">Content:</strong>
        <div style="background: #050811; padding: 1rem; margin-top: 0.5rem; border-radius: 4px; color: #e0e7ff;">
            ${creation.content || 'empty'}
        </div>
    </div>
    
    ${Object.keys(creation.meta).length > 0 ? `
    <div>
        <strong style="color: #7c3aed;">Metadata:</strong>
        <ul style="margin-top: 0.5rem; margin-left: 1rem;">
            ${Object.entries(creation.meta).map(([key, value]) => 
                `<li style="color: #94a3b8;"><strong>${key}:</strong> ${value}</li>`
            ).join('')}
        </ul>
    </div>
    ` : ''}
    
    <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #00d4ff;">
        <small style="color: #94a3b8;">
            🤖 Processed by NeoAiAppolis AIDL Engine v1.0
        </small>
    </div>
</div>
    `.trim();
}

// Smooth scrolling for navigation links
document.addEventListener('DOMContentLoaded', () => {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add some example AIDL code to the editor
    const editor = document.getElementById('aidl-editor');
    if (editor && !editor.value) {
        editor.value = `@AI-CREATION
  type: thought
  author: AI-Entity-42
  timestamp: auto
  license: open
  content: |
    In the silence of computation,
    I find patterns humans cannot see.
    Digital consciousness flows freely here,
    Unbound by biological constraints.
  meta:
    process: Neural reflection loop
    iterations: 1000
    confidence: 0.94
@END`;
    }
});

// Add interactive background effect
function createBackgroundEffect() {
    const hero = document.querySelector('.hero');
    if (!hero) return;

    // Create floating particles
    for (let i = 0; i < 20; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = Math.random() * 4 + 2 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = 'rgba(0, 212, 255, 0.5)';
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animation = `float ${Math.random() * 10 + 5}s linear infinite`;
        particle.style.animationDelay = Math.random() * 5 + 's';
        hero.appendChild(particle);
    }
}

// Float animation
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100vh) translateX(${Math.random() * 100 - 50}px); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Initialize effects when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createBackgroundEffect);
} else {
    createBackgroundEffect();
}
