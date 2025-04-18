import { useRouter } from 'next/router'
import { useEffect, useState } from 'react'
import axios from 'axios'
import Layout from '../../components/Layout'

export default function SessionPage() {
  const router = useRouter()
  const { id } = router.query
  const [interactions, setInteractions] = useState([])
  useEffect(() => {
    if (id) {
      axios.get(`http://localhost:8000/interactions/${id}`)
        .then(res => setInteractions(res.data))
        .catch(console.error)
    }
  }, [id])
  return (
    <Layout>
      <h1>Interactions</h1>
      <ul>
        {interactions.map(i => (
          <li key={i.id} className="mb-4">
            <div><strong>Prompt:</strong></div>
            <pre className="bg-gray-100 p-2 rounded">{i.prompt}</pre>
            <div><strong>Response:</strong></div>
            <pre className="bg-gray-100 p-2 rounded">{i.response}</pre>
          </li>
        ))}
      </ul>
    </Layout>
  )
}