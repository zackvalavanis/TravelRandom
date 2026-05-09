import { Outlet, RouterProvider, createBrowserRouter } from "react-router"
import { Header } from "./Screens/Header"
import { HomeScreen } from "./Screens/HomeScreen"
import { Footer } from "./Screens/Footer"
import { LoginPage } from "./Screens/LoginPage"


function App() {

  const router = createBrowserRouter([
    {
      element: (
        <div>
          < Header />
          <Outlet />
          <Footer />
        </div>
      ),
      children: [
        { path: '/', element: <HomeScreen /> },
        { path: '/loginpage', element: <LoginPage /> }
      ]
    },
  ])

  return (
    <>
      <RouterProvider router={router} />
    </>
  )
}

export default App
