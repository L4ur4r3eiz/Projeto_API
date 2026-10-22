// Funções do Modal de Saída
function abrirModalSair() {
  document.getElementById('modal-sair').classList.add('active');
}

function fecharModalSair() {
  document.getElementById('modal-sair').classList.remove('active');
}

function confirmarSaida() {
  fecharModalSair();
  // Executa a função original do seu backend JS sem alterar sua lógica
  if (typeof sair === 'function') {
    sair();
  }
}

// Funções do Modal de Sucesso de Cadastro
function abrirModalSucesso() {
  document.getElementById('modal-sucesso').classList.add('active');
}

function fecharModalSucesso() {
  document.getElementById('modal-sucesso').classList.remove('active');
}

// Exemplo de integração com o submit do formulário:
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form-agendamento');
  if (form) {
    form.addEventListener('submit', (e) => {
      // Abre o modal visual de sucesso
      abrirModalSucesso();
    });
  }
});

function togglePasswordVisibility(inputId, button) {
  const passwordInput = document.getElementById(inputId);
  if (!passwordInput) return;

  const iconEye = button.querySelector('.icon-eye');
  const iconEyeOff = button.querySelector('.icon-eye-off');

  if (passwordInput.type === 'password') {
    passwordInput.type = 'text';
    if (iconEye) iconEye.style.display = 'none';
    if (iconEyeOff) iconEyeOff.style.display = 'block';
  } else {
    passwordInput.type = 'password';
    if (iconEye) iconEye.style.display = 'block';
    if (iconEyeOff) iconEyeOff.style.display = 'none';
  }
}