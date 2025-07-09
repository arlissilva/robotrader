import React, { useState, useEffect } from 'react'
import axios from 'axios'

const App = () => {
  const [usuario, setUsuario] = useState('')
  const [senha, setSenha] = useState('')
  const [token, setToken] = useState(localStorage.getItem("token") || "")
  const [mensagem, setMensagem] = useState("")

  const logar = async () => {
    try {
      const res = await axios.post('/login', new URLSearchParams({
        username: usuario,
        password: senha
      }))
      localStorage.setItem("token", res.data.access_token)
      setToken(res.data.access_token)
      setMensagem("✅ Login bem-sucedido!")
    } catch (err) {
      setMensagem("❌ Login falhou: " + err.response?.data?.detail)
    }
  }

  const buscarDados = async () => {
    try {
      const res = await axios.get('/dados', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setMensagem("🔐 " + res.data.mensagem)
    } catch (err) {
      setMensagem("⚠️ Acesso negado.")
    }
  }

  const logout = () => {
    localStorage.removeItem("token")
    setToken("")
    setMensagem("🔒 Deslogado.")
  }

  useEffect(() => {
    if (token) buscarDados()
  }, [token])

  if (!token) {
    return (
      <div style={{ padding: 20 }}>
        <h2>🔐 Login</h2>
        <input placeholder="Usuário" value={usuario} onChange={e => setUsuario(e.target.value)} />
        <br />
        <input type="password" placeholder="Senha" value={senha} onChange={e => setSenha(e.target.value)} />
        <br />
        <button onClick={logar}>Entrar</button>
        <p>{mensagem}</p>
      </div>
    )
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>🎉 Área Protegida</h2>
      <button onClick={logout}>Logout</button>
      <p>{mensagem}</p>
    </div>
  )
}

export default App
