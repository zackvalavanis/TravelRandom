import { Link } from "react-router";
import { UseAuth } from "../Auth/UseAuth";

export function Header() {
  const { user } = UseAuth()

  return (
    <div>
      <Link to='/'>Home</Link>
      {user ? (
        <Link to='/something'>Something</Link>
      ) : (
        <Link to='login-page'>Login</Link>
      )}
    </div>
  )
}