import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import MainLayout from './components/MainLayout';
import LoginPage from './pages/Login';
import Dashboard from './pages/Dashboard';
import StudentList from './pages/StudentList';
import TeacherList from './pages/TeacherList';
import ClassroomList from './pages/ClassroomList';
import CourseList from './pages/CourseList';
import AssignmentList from './pages/AssignmentList';
import AttendancePage from './pages/AttendancePage';
import ExamResultPage from './pages/ExamResultPage';
import StudentGradesPage from './pages/StudentGradesPage';
import StudentSchedulePage from './pages/StudentSchedulePage';
import AcademicsConfigPage from './pages/AcademicsConfigPage';
import EnrollmentPage from './pages/EnrollmentPage';
import TuitionPage from './pages/TuitionPage';

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
      {
        path: 'assignments',
        element: <AssignmentList />,
      },
      {
        path: 'attendance',
        element: <AttendancePage />,
      },
      {
        path: 'enter-grades',
        element: <ExamResultPage />,
      },
      {
        path: 'grades',
        element: <StudentGradesPage />,
      },
      {
        path: 'schedule',
        element: <StudentSchedulePage />,
      },
      {
        path: 'config',
        element: <AcademicsConfigPage />,
      },
      {
        path: 'enrollments',
        element: <EnrollmentPage />,
      },
      {
        path: 'tuition',
        element: <TuitionPage />,
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
