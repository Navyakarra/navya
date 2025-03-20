export async function getServerSideProps() {
    const res = await fetch('https://jsonplaceholder.typicode.com/posts/1');
    const data = await res.json();
  
    return {
      props: { post: data },
    };
  }
  
  export default function News({ post }) {
    return (
      <div>
        <h1>{post.title}</h1>
        <p>{post.body}</p>
      </div>
    );
  }
  