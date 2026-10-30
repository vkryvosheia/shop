import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { StoreLayout } from './components/StoreLayout'
import { NotFound } from './pages/NotFound'

const router = createBrowserRouter([
  {
    path: '/',
    element: <StoreLayout />,
    children: [
      {
        index: true,
        element: <div>Store Catalog Page</div>,
      },
      {
        path: '*',
        element: <NotFound />,
      },
    ],
  },
])

export function App() {
  return <RouterProvider router={router} />
}

export default App
