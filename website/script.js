// 简单的粒子效果实现
window.addEventListener('DOMContentLoaded', function() {
  // 创建简单的粒子效果
  const createSimpleParticles = () => {
    const particlesContainer = document.getElementById('particles-js');
    if (!particlesContainer) return;
    
    // 移除之前可能存在的canvas
    const existingCanvas = particlesContainer.querySelector('canvas');
    if (existingCanvas) particlesContainer.removeChild(existingCanvas);
    
    // 创建canvas
    const canvas = document.createElement('canvas');
    particlesContainer.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    
    // 设置canvas尺寸
    const resizeCanvas = () => {
      canvas.width = particlesContainer.offsetWidth;
      canvas.height = particlesContainer.offsetHeight;
    };
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // 粒子配置
    const particlesConfig = {
      particles: {
        number: 50,
        size: 2,
        color: '#00bcd4'
      },
      links: {
        distance: 150,
        width: 1,
        color: '#00bcd4'
      }
    };
    
    // 创建粒子
    let particles = [];
    
    const createParticles = () => {
      particles = [];
      for (let i = 0; i < particlesConfig.particles.number; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * particlesConfig.particles.size + 1,
          speedX: (Math.random() - 0.5) * 0.5,
          speedY: (Math.random() - 0.5) * 0.5,
          color: particlesConfig.particles.color
        });
      }
    };
    
    createParticles();
    
    // 绘制和更新粒子
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // 绘制连接线
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < particlesConfig.links.distance) {
            const opacity = 1 - distance / particlesConfig.links.distance;
            ctx.beginPath();
            ctx.strokeStyle = particlesConfig.links.color + Math.floor(opacity * 255).toString(16).padStart(2, '0');
            ctx.lineWidth = particlesConfig.links.width * opacity;
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }
      
      // 绘制粒子
      particles.forEach(particle => {
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
        ctx.fillStyle = particle.color;
        ctx.fill();
        
        // 更新粒子位置
        particle.x += particle.speedX;
        particle.y += particle.speedY;
        
        // 边界检查
        if (particle.x < 0 || particle.x > canvas.width) particle.speedX *= -1;
        if (particle.y < 0 || particle.y > canvas.height) particle.speedY *= -1;
      });
      
      requestAnimationFrame(animate);
    };
    
    animate();
  };
  
  // 初始化简单粒子效果
  createSimpleParticles();

  // 平滑滚动功能
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        window.scrollTo({
          top: targetElement.offsetTop - 80, // 减去头部高度
          behavior: 'smooth'
        });
      }
    });
  });

  // 导航栏滚动高亮
  const highlightNavOnScroll = () => {
    const sections = ['home', 'services', 'products', 'about', 'contact'];
    const navLinks = document.querySelectorAll('nav a');
    
    let currentSection = '';
    
    sections.forEach(section => {
      const sectionElement = document.getElementById(section);
      if (sectionElement) {
        const sectionTop = sectionElement.offsetTop;
        if (window.scrollY >= sectionTop - 100) {
          currentSection = section;
        }
      }
    });
    
    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentSection}`) {
        link.classList.add('active');
      }
    });
  };
  
  window.addEventListener('scroll', highlightNavOnScroll);

  // 服务卡片悬停效果
  const serviceCards = document.querySelectorAll('.service-card');
  serviceCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-10px)';
      card.style.boxShadow = '0 15px 30px rgba(0, 188, 212, 0.15)';
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0)';
      card.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.1)';
    });
  });

  // 产品卡片悬停效果
  const productCards = document.querySelectorAll('.product-card');
  productCards.forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'scale(1.03)';
      card.style.boxShadow = '0 15px 30px rgba(0, 188, 212, 0.2)';
    });
    
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'scale(1)';
      card.style.boxShadow = '0 10px 20px rgba(0, 0, 0, 0.1)';
    });
  });

  // 移动端菜单切换
  const menuToggle = document.createElement('div');
  menuToggle.className = 'menu-toggle';
  menuToggle.innerHTML = '☰';
  menuToggle.style.cssText = `
    display: none;
    font-size: 24px;
    cursor: pointer;
    color: #fff;
  `;
  
  const headerContent = document.querySelector('.header-content');
  if (headerContent) {
    headerContent.appendChild(menuToggle);
  }
  
  const nav = document.querySelector('nav');
  
  menuToggle.addEventListener('click', () => {
    if (nav) {
      nav.style.display = nav.style.display === 'block' ? 'none' : 'block';
    }
  });
  
  // 响应式处理
  const handleResponsive = () => {
    if (window.innerWidth < 768) {
      if (nav) nav.style.display = 'none';
      if (menuToggle) menuToggle.style.display = 'block';
    } else {
      if (nav) nav.style.display = 'block';
      if (menuToggle) menuToggle.style.display = 'none';
    }
  };
  
  handleResponsive();
  window.addEventListener('resize', handleResponsive);

  // 返回顶部按钮
  const backToTopButton = document.createElement('button');
  backToTopButton.className = 'back-to-top';
  backToTopButton.innerHTML = '↑';
  backToTopButton.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: rgba(0, 188, 212, 0.8);
    color: white;
    border: none;
    cursor: pointer;
    font-size: 20px;
    display: none;
    justify-content: center;
    align-items: center;
    transition: all 0.3s ease;
    z-index: 1000;
  `;
  
  document.body.appendChild(backToTopButton);
  
  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      backToTopButton.style.display = 'flex';
    } else {
      backToTopButton.style.display = 'none';
    }
  });
  
  backToTopButton.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
  
  // 表单提交处理
  const contactForm = document.querySelector('#contact form');
  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      
      // 简单的表单验证
      const name = contactForm.querySelector('input[name="name"]').value;
      const email = contactForm.querySelector('input[name="email"]').value;
      const message = contactForm.querySelector('textarea[name="message"]').value;
      
      if (name && email && message) {
        alert('感谢您的留言！我们会尽快与您联系。');
        contactForm.reset();
      } else {
        alert('请填写所有必填字段。');
      }
    });
  }

  // 滚动动画效果
  const animateOnScroll = () => {
    const elements = document.querySelectorAll('.service-card, .product-card, .about-content');
    
    elements.forEach(element => {
      const elementTop = element.getBoundingClientRect().top;
      const elementVisible = 150;
      
      if (elementTop < window.innerHeight - elementVisible) {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
      }
    });
  };
  
  // 初始化动画状态
  const initAnimationStates = () => {
    const elements = document.querySelectorAll('.service-card, .product-card, .about-content');
    
    elements.forEach(element => {
      element.style.opacity = '0';
      element.style.transform = 'translateY(30px)';
      element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    });
  };
  
  initAnimationStates();
  window.addEventListener('scroll', animateOnScroll);
  
  // 触发一次动画检查
  setTimeout(animateOnScroll, 100);
});