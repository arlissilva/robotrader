import React, { useEffect, useState } from 'react'
import axios from 'axios'

const Ordens = () => {
  const [ordens, setOrdens] = useState([])

  useEffect(() => {
    const fetchOrdens = async () => {
      const res = await axios.get('http://localhost:8000/ordens')
      setOrdens(res.data)
    }

    fetchOrdens()
    const interval = setInterval(fetchOrdens, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div>
      <h2>📄 Ordens Executadas</h2>
      <ul>
        {ordens.slice().reverse().map((o, i) => (
          <li key={i}>{o.timestamp} - {o.ativo} - {o.tipo} @ {o.preco}</li>
        ))}
      </ul>
    </div>
  )
}

export default Ordens