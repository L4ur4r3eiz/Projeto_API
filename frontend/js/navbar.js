window.addEventListener('scroll', () => {
  const navbar = document.querySelector('.navbar');
  if (navbar) {
    if (window.scrollY > 40) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }
});

document.querySelectorAll('[data-nav-toggle]').forEach((button) => {
  const navLinks = document.getElementById(button.getAttribute('aria-controls'));
  if (!navLinks) return;

  const fecharMenu = () => {
    navLinks.classList.remove('show');
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-label', 'Abrir menu');
  };

  button.addEventListener('click', () => {
    const aberto = navLinks.classList.toggle('show');
    button.setAttribute('aria-expanded', String(aberto));
    button.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
  });

  navLinks.querySelectorAll('a, button').forEach((item) => {
    item.addEventListener('click', fecharMenu);
  });

  document.addEventListener('click', (event) => {
    if (!button.closest('.navbar').contains(event.target)) {
      fecharMenu();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') fecharMenu();
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 768) fecharMenu();
  });
});