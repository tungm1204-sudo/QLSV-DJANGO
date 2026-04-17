import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import MainLayout from './components/MainLayout';
import LoginPage from './pages/Login';
import Dashboard from './pages/Dashboard';
import StudentList from './pages/StudentList';
import TeacherList from './pages/TeacherList';
import ClassroomList from './pages/ClassroomList';
import CourseList from './pages/CourseList';

const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        path: '',
        element: <Dashboard />,
      },
      {
        path: 'students',
        element: <StudentList />,
      },
      {
        path: 'teachers',
        element: <TeacherList />,
      },
      {
        path: 'classrooms',
        element: <ClassroomList />,
      },
      {
        path: 'courses',
        element: <CourseList />,
      },
    ],
  },
]);

function App() {
  return (
    <RouterProvider router={router} />
  );
}

export default App;
