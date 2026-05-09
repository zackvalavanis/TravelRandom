import { useState } from "react"
import type { LoginPage } from "../types/types"
import { useNavigate } from "react-router"
import toast from 'react-hot-toast'
import { UseAuth } from "../Auth/UseAuth"


export function LoginPage() {
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login } = UseAuth()
  const [formData, setFormData] = useState<LoginPage>({
    email: "",
    password: ""
  })
  const [showPassword, setShowPassword] = useState(false)


  const HandleLogin = async (formData: LoginPage) => {
    setLoading(true)

    try {
      const res = await fetch('http://localhost:8000/auth/login', {
        "method": 'POST',
        "headers": {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password
        })
      })
      const data = await res.json()

      if (!res.ok) {
        toast.error(data.detail || "Login Failed")
        return
      }

      if (!data?.access_token) {
        toast.error("No token returned from the server")
        return
      }

      console.log("LOGIN SUCCESS", data)

      login(data.access_token)

      toast.success("Logged in successfully")
      navigate('/')
    } catch (error) {
      console.error(error)
      toast.error("Server error. Try Again.")
    } finally {
      setLoading(false)
    }
  }

  const submit = (e: React.FormEvent) => {
    e.preventDefault()
    HandleLogin(formData)
  }

  return (
    <div className='login-page'>
      <h1>Login</h1>
      <form className='form' onSubmit={submit}>
        <input
          name="email"
          type='email'
          placeholder="email"
          onChange={(e) =>
            setFormData({ ...formData, email: e.target.value })}
        >
        </input>
        <input
          name="password"
          id="passwordField"
          type={showPassword ? 'text' : 'password'}
          placeholder='password'
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        >
        </input>
        <button type='button' onClick={() => setShowPassword(!showPassword)}>{showPassword ? "Hide" : "Show Password"}</button>

        <button type='submit' disabled={loading}>{loading ? "Logging in.." : "Login"}</button>
      </form>
    </div>
  )
}