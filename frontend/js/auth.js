// ============================================================
// js/auth.js — Funções compartilhadas de autenticação
// ============================================================

function obterTipoUsuario() {
  return localStorage.getItem('tipo')
}

function protegerPagina(perfisPermitidos) {
  const token = localStorage.getItem('token')
  const tipo = obterTipoUsuario()

  if (!token || !tipo) {
    window.location.href = 'login.html'
    return false
  }

  const perfis = perfisPermitidos || (document.body.dataset.perfisPermitidos || 'admin,funcionario')
    .split(',')
    .map((perfil) => perfil.trim())

  if (!['admin', 'funcionario'].includes(tipo) || !perfis.includes(tipo)) {
    window.location.href = 'login.html'
    return false
  }

  return true
}

function aplicarControleDeAcesso() {
  const tipo = obterTipoUsuario()

  document.querySelectorAll('[data-perfis]').forEach((elemento) => {
    const perfis = elemento.dataset.perfis.split(',').map((perfil) => perfil.trim())
    elemento.style.display = perfis.includes(tipo) ? '' : 'none'
  })

  if (tipo !== 'admin') {
    document.querySelectorAll('#card-cadastrar-equipe').forEach((elemento) => {
      elemento.style.display = 'none'
    })
  }
}

async function fetchAutenticado(url, opcoes = {}) {
  const token = localStorage.getItem('token')
  const headers = { ...opcoes.headers }

  if (!token) {
    window.location.href = 'login.html'
    throw new Error('Sessão não autenticada')
  }

  headers.Authorization = `Bearer ${token}`
  const resposta = await fetch(url, { ...opcoes, headers })

  if (resposta.status === 401) {
    localStorage.removeItem('token')
    localStorage.removeItem('tipo')
    window.location.href = 'login.html'
  } else if (resposta.status === 403) {
    window.location.href = 'dashboard.html'
  }

  return resposta
}

function sair() {
  localStorage.removeItem('token')
  localStorage.removeItem('tipo')
  window.location.href = 'login.html'
}

document.addEventListener('DOMContentLoaded', () => {
  protegerPagina()
  aplicarControleDeAcesso()
})
