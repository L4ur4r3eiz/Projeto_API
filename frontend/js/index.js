document.addEventListener('DOMContentLoaded', () => {
  const preloader = document.getElementById('app-preloader');
  
  if (preloader) {
    // Aguarda a animação da barra de progresso (1.8s) para esconder o preloader suavemente
    setTimeout(() => {
      preloader.classList.add('fade-out');
    }, 1800);
  }
});