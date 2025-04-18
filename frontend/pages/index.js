 import { useEffect, useState } from 'react'
 import axios from 'axios'
 import Link from 'next/link'
 import Layout from '../components/Layout'

 export default function Home() {
   const [projects, setProjects] = useState([])
   useEffect(() => {
     axios.get('http://localhost:8000/projects')
       .then(res => setProjects(res.data))
       .catch(console.error)
   }, [])
   return (
     <Layout>
       <h1>Projects</h1>
       <ul>
        {projects.map(p => (
          <li key={p.id}>
            <Link href={`/project/${p.id}`}>{p.name}</Link>
          </li>
        ))}
       </ul>
     </Layout>
   )
 }