import { createBrowserRouter } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import HomePage from '../pages/HomePage';
import UploadPage from '../pages/UploadPage';
import AnalyzePage from '../pages/AnalyzePage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <Layout />,
    children: [
      {
        index: true,
        element: <HomePage />,
      },
      {
        path: 'upload',
        element: <UploadPage />,
      },
      {
        path: 'analyze',
        element: <AnalyzePage />,
      },
    ],
  },
]);

export default router;