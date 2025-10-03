/*!
 * Particles.js - v2.0.0
 * https://github.com/VincentGarreau/particles.js
 * 请在生产环境中使用压缩版
 */
var pJS = function(tag_id, params) {
  var canvas_el = document.querySelector('#' + tag_id + ' > canvas');
  
  // 确保canvas元素存在
  if (!canvas_el) {
    var particlesContainer = document.getElementById(tag_id);
    if (particlesContainer) {
      canvas_el = document.createElement('canvas');
      particlesContainer.appendChild(canvas_el);
    } else {
      console.error('Particles.js: container element #' + tag_id + ' not found');
      return;
    }
  }

  /* particles.js variables with default values */
  this.pJS = {
    canvas: {
      el: canvas_el,
      w: canvas_el.offsetWidth || 0,
      h: canvas_el.offsetHeight || 0
    },
    particles: {
      number: {
        value: 80,
        density: {
          enable: true,
          value_area: 800
        }
      },
      color: {
        value: '#000000'
      },
      shape: {
        type: 'circle',
        stroke: {
          width: 0,
          color: '#000000'
        },
        polygon: {
          nb_sides: 5
        }
      },
      opacity: {
        value: 1,
        random: false,
        anim: {
          enable: false,
          speed: 2,
          opacity_min: 0,
          sync: false
        }
      },
      size: {
        value: 20,
        random: false,
        anim: {
          enable: false,
          speed: 20,
          size_min: 0,
          sync: false
        }
      },
      line_linked: {
        enable: true,
        distance: 100,
        color: '#000000',
        opacity: 1,
        width: 1
      },
      move: {
        enable: true,
        speed: 2,
        direction: 'none',
        random: false,
        straight: false,
        out_mode: 'out',
        bounce: false,
        attract: {
          enable: false,
          rotateX: 3000,
          rotateY: 3000
        }
      },
      array: []
    },
    interactivity: {
      detect_on: 'canvas',
      events: {
        onhover: {
          enable: true,
          mode: 'grab'
        },
        onclick: {
          enable: true,
          mode: 'push'
        },
        resize: true
      },
      modes: {
        grab: {
          distance: 100,
          line_linked: {
            opacity: 1
          }
        },
        bubble: {
          distance: 200,
          size: 80,
          duration: 0.4
        },
        repulse: {
          distance: 200,
          duration: 0.4
        },
        push: {
          particles_nb: 4
        },
        remove: {
          particles_nb: 2
        }
      },
      mouse: {}
    },
    retina_detect: false,
    fn: {
      interact: {},
      modes: {},
      vendors: {}
    },
    tmp: {}
  };

  var pJS = this.pJS;

  /* params settings */
  if (params) {
    Object.deepExtend(pJS, params);
  }

  pJS.tmp.obj = {}
  pJS.tmp.array = {}

  /* ---------- CANVAS ------------ */
  pJS.fn.canvasInit = function() {
    pJS.canvas.ctx = pJS.canvas.el.getContext('2d');
  };

  pJS.fn.canvasSize = function() {
    pJS.canvas.w = pJS.canvas.el.offsetWidth;
    pJS.canvas.h = pJS.canvas.el.offsetHeight;

    if (pJS.retina_detect && window.devicePixelRatio > 1) {
      pJS.canvas.el.width = pJS.canvas.w * 2;
      pJS.canvas.el.height = pJS.canvas.h * 2;
      pJS.canvas.ctx.scale(2, 2);
    } else {
      pJS.canvas.el.width = pJS.canvas.w;
      pJS.canvas.el.height = pJS.canvas.h;
    }
  };

  /* --------- PARTICLES ------------ */
  pJS.fn.particle = function(color, opacity, position) {
    this.x = position ? position.x : Math.random() * pJS.canvas.w;
    this.y = position ? position.y : Math.random() * pJS.canvas.h;

    this.vx = 0;
    this.vy = 0;

    this.radius = (pJS.particles.size.random ? Math.random() : 1) * pJS.particles.size.value;

    if (pJS.particles.opacity.random) {
      this.opacity = Math.random();
    } else {
      this.opacity = pJS.particles.opacity.value;
    }

    this.color = color;

    this.line_linked = {
      opacity: pJS.particles.line_linked.opacity
    };

    this.move = {
      enable: pJS.particles.move.enable,
      speed: (pJS.particles.move.random ? Math.random() : 1) * pJS.particles.move.speed,
      direction: pJS.particles.move.direction,
      random: pJS.particles.move.random,
      straight: pJS.particles.move.straight,
      out_mode: pJS.particles.move.out_mode,
      bounce: pJS.particles.move.bounce
    };

    this.shape = pJS.particles.shape.type;
    this.shapeData = {
      type: this.shape,
      stroke: pJS.particles.shape.stroke,
      polygon: pJS.particles.shape.polygon
    };

    this.anim = {
      opacity: {
        enable: pJS.particles.opacity.anim.enable,
        speed: pJS.particles.opacity.anim.speed,
        opacity_min: pJS.particles.opacity.anim.opacity_min,
        sync: pJS.particles.opacity.anim.sync,
        status: false,
        count: 0
      },
      size: {
        enable: pJS.particles.size.anim.enable,
        speed: pJS.particles.size.anim.speed,
        size_min: pJS.particles.size.anim.size_min,
        sync: pJS.particles.size.anim.sync,
        status: false,
        count: 0
      }
    };

    if (this.anim.opacity.enable) {
      this.anim.opacity.status = true;
      if (!this.anim.opacity.sync) {
        this.anim.opacity.speed = Math.random() * this.anim.opacity.speed;
      }
    }

    if (this.anim.size.enable) {
      this.anim.size.status = true;
      if (!this.anim.size.sync) {
        this.anim.size.speed = Math.random() * this.anim.size.speed;
      }
    }

    this.update = function() {
      this.x += this.vx;
      this.y += this.vy;

      if (this.anim.opacity.status) {
        this.opacityUpdate();
      }

      if (this.anim.size.status) {
        this.sizeUpdate();
      }

      this.moveParticle();
      this.draw();
    };

    this.opacityUpdate = function() {
      if (this.opacity >= 1) {
        this.anim.opacity.count = -1;
      } else if (this.opacity <= this.anim.opacity.opacity_min) {
        this.anim.opacity.count = 1;
      }

      this.opacity += this.anim.opacity.count * this.anim.opacity.speed / 100;

      if (this.opacity < 0) {
        this.opacity = 0;
      }
    };

    this.sizeUpdate = function() {
      if (this.radius >= pJS.particles.size.value) {
        this.anim.size.count = -1;
      } else if (this.radius <= this.anim.size.size_min) {
        this.anim.size.count = 1;
      }

      this.radius += this.anim.size.count * this.anim.size.speed / 100;

      if (this.radius < 0) {
        this.radius = 0;
      }
    };

    this.moveParticle = function() {
      if (!this.move.enable) return;

      var vel = pJS.fn.vendors.velocity(this);
      this.vx = vel.x;
      this.vy = vel.y;

      this.checkOverlap();
    };

    this.checkOverlap = function() {
      if (this.x - this.radius > pJS.canvas.w) {
        this.x = 0 - this.radius;
      } else if (this.x + this.radius < 0) {
        this.x = pJS.canvas.w + this.radius;
      }

      if (this.y - this.radius > pJS.canvas.h) {
        this.y = 0 - this.radius;
      } else if (this.y + this.radius < 0) {
        this.y = pJS.canvas.h + this.radius;
      }
    };

    this.draw = function() {
      pJS.canvas.ctx.fillStyle = this.color;
      pJS.canvas.ctx.globalAlpha = this.opacity;

      switch (this.shape) {
        case 'circle':
          pJS.canvas.ctx.beginPath();
          pJS.canvas.ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
          pJS.canvas.ctx.fill();
          break;
        case 'square':
          pJS.canvas.ctx.beginPath();
          pJS.canvas.ctx.rect(
            this.x - this.radius,
            this.y - this.radius,
            this.radius * 2,
            this.radius * 2
          );
          pJS.canvas.ctx.fill();
          break;
        case 'polygon':
          if (this.shapeData.polygon.nb_sides > 2) {
            pJS.canvas.ctx.beginPath();
            pJS.fn.vendors.drawPolygon(
              this.x,
              this.y,
              this.radius,
              this.shapeData.polygon.nb_sides
            );
            pJS.canvas.ctx.fill();
          }
          break;
      }
    };
  };

  pJS.fn.particlesCreate = function() {
    pJS.particles.array = [];
    for (var i = 0; i < pJS.particles.number.value; i++) {
      var color = pJS.fn.vendors.color();
      pJS.particles.array.push(new pJS.fn.particle(color));
    }
  };

  pJS.fn.particlesDraw = function() {
    pJS.canvas.ctx.clearRect(0, 0, pJS.canvas.w, pJS.canvas.h);

    for (var i = 0; i < pJS.particles.array.length; i++) {
      var p = pJS.particles.array[i];
      p.update();
    }

    if (pJS.particles.line_linked.enable) {
      pJS.fn.vendors.linkParticles();
    }
  };

  /* --------- INTERACTIVITY ----------- */
  pJS.fn.interactivity.eventsInit = function() {
    if (pJS.interactivity.events.resize) {
      window.addEventListener('resize', function() {
        pJS.fn.canvasSize();
        pJS.fn.particlesReset();
      });
    }
  };

  /* --------- VENDORS ----------- */
  pJS.fn.vendors.color = function() {
    var color = pJS.particles.color.value;
    return color;
  };

  pJS.fn.vendors.velocity = function(p) {
    var speed = p.move.speed;
    var direction = p.move.direction;

    switch (direction) {
      case 'top':
        return { x: 0, y: -speed };
      case 'top-right':
        return { x: speed * 0.7, y: -speed * 0.7 };
      case 'right':
        return { x: speed, y: 0 };
      case 'bottom-right':
        return { x: speed * 0.7, y: speed * 0.7 };
      case 'bottom':
        return { x: 0, y: speed };
      case 'bottom-left':
        return { x: -speed * 0.7, y: speed * 0.7 };
      case 'left':
        return { x: -speed, y: 0 };
      case 'top-left':
        return { x: -speed * 0.7, y: -speed * 0.7 };
      default:
        var angle = Math.random() * Math.PI * 2;
        return { x: Math.cos(angle) * speed, y: Math.sin(angle) * speed };
    }
  };

  pJS.fn.vendors.linkParticles = function() {
    for (var i = 0; i < pJS.particles.array.length; i++) {
      for (var j = i + 1; j < pJS.particles.array.length; j++) {
        var dx = pJS.particles.array[i].x - pJS.particles.array[j].x;
        var dy = pJS.particles.array[i].y - pJS.particles.array[j].y;
        var dist = Math.sqrt(dx * dx + dy * dy);

        if (dist <= pJS.particles.line_linked.distance) {
          var opacity_line = pJS.particles.line_linked.opacity * (1 - dist / pJS.particles.line_linked.distance);

          pJS.canvas.ctx.beginPath();
          pJS.canvas.ctx.strokeStyle = pJS.particles.line_linked.color;
          pJS.canvas.ctx.lineWidth = pJS.particles.line_linked.width;
          pJS.canvas.ctx.globalAlpha = opacity_line;
          pJS.canvas.ctx.moveTo(pJS.particles.array[i].x, pJS.particles.array[i].y);
          pJS.canvas.ctx.lineTo(pJS.particles.array[j].x, pJS.particles.array[j].y);
          pJS.canvas.ctx.stroke();
        }
      }
    }
  };

  pJS.fn.vendors.drawPolygon = function(x, y, radius, sides) {
    var angle = (2 * Math.PI) / sides;
    pJS.canvas.ctx.moveTo(x + radius, y);
    for (var i = 1; i < sides; i++) {
      pJS.canvas.ctx.lineTo(
        x + radius * Math.cos(i * angle),
        y + radius * Math.sin(i * angle)
      );
    }
    pJS.canvas.ctx.closePath();
  };

  /* --------- INIT ----------- */
  pJS.fn.init = function() {
    pJS.fn.canvasInit();
    pJS.fn.canvasSize();
    pJS.fn.particlesCreate();
    pJS.fn.particlesDraw();
    pJS.fn.interactivity.eventsInit();

    requestAnimationFrame(update);

    function update() {
      pJS.fn.particlesDraw();
      requestAnimationFrame(update);
    }
  };

  pJS.fn.particlesReset = function() {
    if (pJS.particles.array) {
      pJS.particles.array.length = 0;
    }
    pJS.fn.particlesCreate();
  };

  /* --------- START ----------- */
  pJS.fn.init();

  return this.pJS;
};

/* ------ GLOBAL FUNCTION ------ */
window.particlesJS = function(tag_id, params) {
  return new pJS(tag_id, params);
};

/* ------ DEEP EXTEND ------ */
Object.deepExtend = function(destination, source) {
  for (var property in source) {
    if (source[property] && source[property].constructor && source[property].constructor === Object) {
      destination[property] = destination[property] || {};
      arguments.callee(destination[property], source[property]);
    } else {
      destination[property] = source[property];
    }
  }
  return destination;
};