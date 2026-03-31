function toggleMenu() {
    const navMenu = document.querySelector('.nav-menu');
    const menuToggle = document.querySelector('.menu-toggle');

    navMenu.classList.toggle('active');

    const spans = menuToggle.querySelectorAll('span');
    if (navMenu.classList.contains('active')) {
        spans[0].style.transform = 'rotate(45deg) translate(6px, 6px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(6px, -6px)';
    } else {
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    }
}

window.addEventListener('scroll', function () {
    const header = document.querySelector('.header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(255, 255, 255, 0.15)';
    } else {
        header.style.background = 'rgba(255, 255, 255, 0.1)';
    }
});

document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', function (e) {
        document.querySelectorAll('.nav-menu a').forEach(a => a.classList.remove('active'));
        this.classList.add('active');

        if (window.innerWidth <= 768) {
            const navMenu = document.querySelector('.nav-menu');
            const menuToggle = document.querySelector('.menu-toggle');
            navMenu.classList.remove('active');

            const spans = menuToggle.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });
});

function toggleChat() {
    document.getElementById("chatModal")
        .classList.toggle("active");
}

document.addEventListener("DOMContentLoaded", () => {

    const cards = document.querySelectorAll(".hack-card");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }
        });
    }, {
        threshold: 0.2
    });

    cards.forEach(card => observer.observe(card));

});

// Page load bo'lganda loaderni o'chirish
window.addEventListener("load", () => {
    const loader = document.getElementById("page-loader");

    setTimeout(() => {
        loader.classList.add("hide");
    }, 500);
});


// Sahifa almashganda loader chiqishi
document.querySelectorAll("a").forEach(link => {

    link.addEventListener("click", function (e) {

        const href = this.getAttribute("href");

        if (!href || href.startsWith("#") || href.startsWith("javascript")) return;

        e.preventDefault();

        const loader = document.getElementById("page-loader");

        loader.classList.remove("hide");

        setTimeout(() => {
            window.location.href = href;
        }, 300);

    });

});

const text = "Sartupers ATT school";
const speed = 70; // ms per char
let i = 0;

function typeWriter() {
  if (i < text.length) {
    document.getElementById("type-text").innerHTML += text.charAt(i);
    i++;
    setTimeout(typeWriter, speed);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("type-text");
  el.classList.add("typing");
  typeWriter();
});

const texts = [
  "Startupers ATT school "
];

let textIndex = 0;
let charIndex = 0;
let isDeleting = false;

const typingSpeed = 50;
const deletingSpeed = 40;
const delayBetweenTexts = 1500;

document.addEventListener("DOMContentLoaded", () => {

  const el = document.getElementById("type-text");
  if (!el) return; // 🔴 crashni to‘xtatadi

  function typeLoop() {
    const currentText = texts[textIndex];

    if (isDeleting) {
      el.innerHTML = currentText.substring(0, charIndex--);
    } else {
      el.innerHTML = currentText.substring(0, charIndex++);
    }

    let speed = isDeleting ? deletingSpeed : typingSpeed;

    if (!isDeleting && charIndex === currentText.length) {
      speed = delayBetweenTexts;
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      textIndex = (textIndex + 1) % texts.length;
      speed = 500;
    }

    setTimeout(typeLoop, speed);
  }

  typeLoop();
});