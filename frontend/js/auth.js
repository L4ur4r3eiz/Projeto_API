// ============================================================
// js/auth.js — Funções compartilhadas de autenticação
// Descrição: Usadas por toda tela protegida, pra checar login
//            e mandar o token em toda requisição pra API.
// ============================================================

// ─── Bloqueia a página se não tiver um token guardado ───
function protegerPagina() {
  const token = localStorage.getItem('token')
  if (!token) {
    window.location.href = 'login.html'
  }
}

// ─── Faz um fetch normal, mas já anexando o token no cabeçalho ───
async function fetchAutenticado(url, opcoes = {}) {
  const token = localStorage.getItem('token')
  const headers = { ...opcoes.headers }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  const resposta = await fetch(url, { ...opcoes, headers })

  if (resposta.status === 401) {
    localStorage.removeItem('token')
    window.location.href = 'login.html'
  }

  return resposta
}

// ─── Desloga: apaga o token e volta pra tela de login ───
function sair() {
  localStorage.removeItem('token')
  window.location.href = 'login.html'
}
