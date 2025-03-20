export async function getStaticProps() {
    const res = await fetch('https://jsonplaceholder.typicode.com/posts/2');
    const data = await res.json();
  
    return {
      props: { post: data },
      revalidate: 10, // Incremental Static Regeneration (ISR)
    };
  }
  
  export default function StaticBlog({ post }) {
    return (
      <div>
        <h1>{post.title}</h1>
        <p>{post.body}</p>
      </div>
    );
  }
  