import { useParams } from "react-router-dom";
import users from "./users.json";

const User = () => {
  const { id } = useParams(); // Get dynamic user ID from URL
  const user = users.find((u) => u.id === parseInt(id));

  if (!user) {
    return <h2>User not found</h2>;
  }

  return (
    <div>
      <h2>User Details</h2>
      <p><strong>Name:</strong> {user.name}</p>
      <p><strong>Age:</strong> {user.age}</p>
    </div>
  );
};

export default User;
