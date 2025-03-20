import { useRouter } from 'next/router';

export default function BlogPost() {
  const router = useRouter();
  const { id } = router.query; // Extracts dynamic `id` from URL

  return (
    <div>
      <h1>Blog Post: {id}</h1>
      <p>This is a dynamically generated blog post page.</p>
    </div>
  );
}
