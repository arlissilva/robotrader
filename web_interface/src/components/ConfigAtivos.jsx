import React, { useState, useEffect } from 'react'
import axios from 'axios'

const ConfigAtivos = () => {
  const [ativos, setAtivos] = useState("")
  const [atual, setAtual] = useState([])

  useEffect(() => {
    axios.get("http://localhost:8000/ativos").then(res => setAtual(res.data))
  }, [])

  const salvar = async () => {
    const lista = ativos.split(',').map(s => s.trim().toUpperCase())
    await axios.post("http://localhost:8000/ativos", { simbolos: lista })
    setAtual(lista)
    setAtivos("")
  }

  return (
    <div>
      <h2>⚙️ Configurar Ativos</h2>
      <p>Ativos atuais: {atual.join(", ") || "Nenhum"}</p>
      <input
        type="text"
        value={ativos}
        onChange={e => setAtivos(e.target.value)}
        placeholder="Ex: WINQ25,WDOQ25"
      />
      <button onClick={salvar}>Salvar</button>
    </div>
  )
}

export default ConfigAtivos