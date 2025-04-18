 import { useRouter } from 'next/router'
 import { useEffect, useState } from 'react'
 import axios from 'axios'
 import Layout from '../../components/Layout'
 import Link from 'next/link'

 export default function ProjectPage() {
   const router = useRouter()
   const { id } = router.query
   const [sessions, setSessions] = useState([])
   useEffect(() => {
     if (id) {
       axios.get(`http://localhost:8000/sessions/${id}`)
         .then(res => setSessions(res.data))
         .catch(console.error)
     }
   }, [id])
   return (
     <Layout>
       <h1>Sessions</h1>
       <ul>
        {sessions.map(s => (
          <li key={s.id}>
            <Link href={`/session/${s.id}`}>{s.title}</Link>
          </li>
        ))}
       </ul>
     </Layout>
   )
 }