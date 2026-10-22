const API = 'http://127.0.0.1:8000'
const formCadastro = document.getElementById('form-cadastro')

formCadastro.addEventListener('submit', async (e) => {
  e.preventDefault()

  const usuario = {
    nome: document.getElementById('nome').value,
    email: document.getElementById('email').value,
    senha: document.getElementById('senha').value
  }

  try {
    const resposta = await fetch(`${API}/usuarios`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(usuario)
    })

    const resultado = await resposta.json()

    if (resposta.ok) {
      alert('Cadastro feito com sucesso! Entre com seu e-mail e senha.')
      window.location.href = 'login.html'
    } else {
      alert('Erro ao cadastrar: ' + (resultado.detail || resultado.erro || JSON.stringify(resultado)))
    }
  } catch (erro) {
    console.error('Falha ao conectar à API:', erro)
    alert('Não foi possível conectar à API. Verifique se o servidor está ligado.')
  }
})