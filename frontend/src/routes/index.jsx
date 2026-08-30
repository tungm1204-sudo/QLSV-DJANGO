import { lazy } from 'react';

export const routes = {
  public: [
    {
      path: '/login',
      component: lazy(() => import('../features/auth/LoginPage')),
    }
  ],
  protected: [
    {
      path: '/dashboard',
      component: lazy(() => import('../features/dashboard/DashboardPage')),
    },
    {
      path: '/master-data',
      component: lazy(() => import('../features/master_data/MasterDataPage')),
    },
    {
      path: '/users',
      component: lazy(() => import('../features/users/UsersPage')),
    },
    {
      path: '/roles',
      component: lazy(() => import('../features/roles/RolesPage')),
    },

    {
      path: '/audit-logs',
      component: lazy(() => import('../features/audit_logs/AuditLogsPage')),
    },
    {
      path: '/system-config',
      component: lazy(() => import('../features/configs/SystemConfigsPage')),
    },
    {
      path: '/hr/*',
      component: lazy(() => import('../features/hr/HrPage')),
    },
    {
      path: '/curriculum/courses',
      component: lazy(() => import('../features/curriculum/pages/CoursesPage')),
    },
    {
      path: '/curriculum/training-programs',
      component: lazy(() => import('../features/curriculum/pages/TrainingProgramsPage')),
    },
    {
      path: '/curriculum/training-programs/:id',
      component: lazy(() => import('../features/curriculum/pages/TrainingProgramDetailPage')),
    },
    {
      path: '/curriculum/training-plans',
      component: lazy(() => import('../features/curriculum/pages/TrainingPlansPage')),
    },
    {
      path: '/curriculum/training-plans/:id',
      component: lazy(() => import('../features/curriculum/pages/TrainingPlanManagementPage')),
    }
  ]
};
