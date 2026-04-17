import { useAuthStore } from '../stores/authStore';

export default function Dashboard() {
  const user = useAuthStore(state => state.user);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
          Dashboard
        </h1>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {/* Placeholder Stat Cards */}
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
          <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Vai trò của bạn</p>
          <p className="mt-2 text-3xl font-bold text-gray-900 dark:text-white capitalize">
            {user?.role.replace('_', ' ')}
          </p>
        </div>
      </div>
    </div>
  );
}
